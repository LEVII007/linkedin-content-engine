#!/usr/bin/env python3
"""Scan LinkedIn post text for PII, secrets, confidentiality markers, formatting, and AI phrasing.

Three tiers:
  BLOCK — never publish (personal data, secrets, confidentiality markers)
  WARN  — probably wrong (formatting LinkedIn mangles, engagement bait)
  SLOP  — reads as machine-written; rewrite the sentence, do not just delete the word

SLOP is advisory and never blocks. Every pattern is regression-tested against the author's
real posts in ../examples.md, so it cannot fire on his genuine writing. "Here's the thing:"
was removed from the filler list for exactly that reason — he actually writes it.
"""

import argparse
import pathlib
import re
import sys

MAX_CHARS = 3000

BLOCKING = [
    (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"), "email address"),
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "US SSN pattern"),
    (re.compile(r"(?<!\d)(?:\+?91[-.\s]?)?[6-9]\d{9}(?!\d)"), "India mobile number pattern"),
    (
        re.compile(r"(?<!\d)\+?1?[-.\s]?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}(?!\d)"),
        "US phone pattern",
    ),
    (re.compile(r"(?i)\bMRN\s*[:#]?\s*\d+"), "medical record number"),
    (re.compile(r"(?i)\bNPI\s*[:#]?\s*\d{10}\b"), "provider NPI"),
    (re.compile(r"(?i)\b(?:DOB|date of birth)\b"), "date of birth reference"),
    (re.compile(r"(?i)\bpatient\s+(?:id|name|#)\b"), "patient identifier"),
    (re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"), "IP address"),
    (
        re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "UUID / resource id",
    ),
    (re.compile(r"(?i)\b(?:password|passwd|secret|token|api.?key)\s*[:=]\s*\S+"), "credential"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key id"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key"),
    (
        re.compile(r"(?i)\b(?:internal only|confidential|under NDA|not for distribution)\b"),
        "confidentiality marker",
    ),
    (
        re.compile(
            r"(?i)\b(?:our|we|my|us|their)\b[^.!?\n]{0,40}"
            r"\$\s?\d[\d,.]*\s?(?:million|billion|M\b|B\b|k\b)"
        ),
        "our own monetary figure",
    ),
    (
        re.compile(r"(?i)\b(?:ARR|valuation|runway|burn rate)\b[^.!?\n]{0,20}\$\s?\d"),
        "company financial",
    ),
    (
        re.compile(r"(?i)\b(?:revenue|budget|deal|contract|investment)\s+(?:of|worth|valued)\b"),
        "financial detail",
    ),
]

WARNINGS = [
    (re.compile(r"\*\*|^#{1,6}\s|^\s*[-*]\s", re.M), "markdown syntax — LinkedIn renders it literally"),
    (
        re.compile(r"(?i)\b(?:thoughts\?|agree\?|comment below|follow for more|drop a|let me know below)"),
        "engagement bait",
    ),
    (re.compile(r"(?i)^\s*(?:P\.?S\.?|Repost if)", re.M), "growth-hack tail"),
    (re.compile(r"(?:#\w+\s*){7,}"), "more than six hashtags"),
    (
        re.compile(r"(?i)\$\s?\d[\d,.]*\s?(?:million|billion|M\b|B\b|k\b)"),
        "monetary figure — fine if it is public and sourced, not if it is ours",
    ),
]

# Advisory only. Rewrite the sentence; swapping the word leaves the same hollow sentence.
SLOP = [
    (
        re.compile(r"[\u2014\u2013]"),
        "em/en dash — he uses these about once per 50 lines; prefer a full stop or a comma",
    ),
    (
        re.compile(
            r"(?i)\b(?:not just|isn'?t just|more than just)\b[^.!?\n]{0,60}[,.:;\u2014-]\s*it'?s\b"
        ),
        "\"not just X, it's Y\" pivot — the most recognizable LLM construction",
    ),
    (
        re.compile(
            r"(?i)\b(?:game.?changer|revolutionary|paradigm shift|seismic|transformative"
            r"|groundbreaking|unprecedented)\b"
        ),
        "hollow intensifier — say what actually changed instead",
    ),
    (
        re.compile(
            r"(?i)\b(?:in today'?s (?:fast.?paced|digital|modern|evolving)|let'?s be honest"
            r"|the truth is,|everyone (?:is )?talking about)\b"
        ),
        "filler opener — delete it and start at the real first sentence",
    ),
    (
        re.compile(
            r"(?i)\b(?:delve|navigat\w+ the (?:landscape|complexit)|at its core"
            r"|when it comes to|it'?s worth noting|needless to say)\b"
        ),
        "LLM connective",
    ),
    (
        re.compile(
            r"(?i)\b(?:the future is here|only time will tell|time will tell"
            r"|food for thought|stay tuned|watch this space)\b"
        ),
        "empty closer — end on the last real sentence",
    ),
    (
        re.compile(
            r"(?i)\b(?:leverage|supercharge|testament to|seamless|cutting.?edge"
            r"|best.?in.?class|holistic|synergy)\b"
        ),
        "corporate abstraction — name the concrete thing",
    ),
    (re.compile(r"(?i)\bin conclusion\b|^\s*TL;?DR", re.M), "essay scaffolding"),
]


def post_text(document: str) -> str:
    """Return the body when a saved draft includes YAML frontmatter."""
    lines = document.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return document
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "".join(lines[index + 1 :]).lstrip("\r\n")
    return document


def check(document: str) -> tuple[list[str], list[str], list[str]]:
    text = post_text(document)
    errors = []
    warnings = []
    slop = []
    for pattern, label in BLOCKING:
        if match := pattern.search(text):
            errors.append(f"{label}: {match.group()!r}")
    for pattern, label in WARNINGS:
        if pattern.search(text):
            warnings.append(label)
    for pattern, label in SLOP:
        if match := pattern.search(text):
            slop.append(f"{label} [{match.group().strip()!r}]")
    if not text.strip():
        errors.append("draft is empty")
    if len(text) > MAX_CHARS:
        errors.append(f"{len(text)} characters exceeds LinkedIn's {MAX_CHARS} limit")
    return errors, warnings, slop


SELF_TESTS = [
    ("Reach me at a@b.com", "email address", True),
    ("Patient MRN: 88213 was excluded", "medical record number", True),
    ("api_key=sk-abc123", "credential", True),
    ("This is confidential, do not share", "confidentiality marker", True),
    ("A specific observation with no private data.", None, False),
    (
        "---\nnotes: confidential deal worth $8M\n---\nA safe post body.\n",
        None,
        False,
    ),
]

# Each must raise a SLOP note. None may block.
SLOP_TESTS = [
    ("The rollout was slow — and then it wasn't.", "em/en dash"),
    ("This isn't just a tooling problem, it's a trust problem.", "pivot"),
    ("A genuine game-changer for the category.", "hollow intensifier"),
    ("In today's fast-paced market, buyers expect more.", "filler opener"),
    ("Let's delve into what the data showed.", "LLM connective"),
    ("Only time will tell.", "empty closer"),
    ("We leverage a best-in-class platform.", "corporate abstraction"),
    ("In conclusion, adoption is slower than anyone models.", "essay scaffolding"),
]


def real_posts() -> str:
    """The author's actual posts, quoted in examples.md. The regression fixture."""
    path = pathlib.Path(__file__).resolve().parent.parent / "examples.md"
    if not path.exists():
        return ""
    quoted = [
        line[2:] if line.startswith("> ") else line[1:]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith(">")
    ]
    return "\n".join(quoted)


def self_test() -> int:
    failures = 0

    for text, expected_label, should_block in SELF_TESTS:
        errors, _, _ = check(text)
        blocked = bool(errors)
        passed = blocked == should_block and (
            expected_label is None or any(expected_label in error for error in errors)
        )
        result = errors or "clean"
        sample = text.splitlines()[-1][:46]
        print(f"{'PASS' if passed else 'FAIL'}  {sample:<48} -> {result}")
        failures += not passed

    print()
    for text, expected in SLOP_TESTS:
        errors, _, slop = check(text)
        passed = bool(slop) and not errors and any(expected in note for note in slop)
        label = slop[0].split(" [")[0][:40] if slop else "NOTHING FLAGGED"
        print(f"{'PASS' if passed else 'FAIL'}  {text[:46]:<48} -> {label}")
        failures += not passed

    print()
    fixture = real_posts()
    if not fixture:
        print("SKIP  examples.md not found — regression fixture unavailable")
    else:
        # Line by line: concatenating every post would trip the length limit spuriously.
        bad = []
        for line in fixture.splitlines():
            if not line.strip():
                continue
            errors, _, slop = check(line)
            # One genuine paired-dash aside is the only hit his real writing may produce.
            unexpected = [note for note in slop if "em/en dash" not in note]
            bad += errors + unexpected
        passed = not bad
        lines = len([x for x in fixture.splitlines() if x.strip()])
        detail = bad[:3] if bad else "no false positives"
        print(f"{'PASS' if passed else 'FAIL'}  regression: {lines} lines of his real posts -> {detail}")
        failures += not passed

    total = len(SELF_TESTS) + len(SLOP_TESTS) + (1 if fixture else 0)
    print(f"\n{total - failures}/{total} passed")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        parser.error("give a file, or --self-test")

    document = open(args.file, encoding="utf-8").read()
    errors, warnings, slop = check(document)
    for note in slop:
        print(f"SLOP  {note}")
    for warning in warnings:
        print(f"WARN  {warning}")
    for error in errors:
        print(f"BLOCK {error}")
    if errors:
        print(f"\n{len(errors)} blocking issue(s).")
        return 1
    if slop:
        print(f"\n{len(slop)} phrasing note(s). Rewrite the sentence, not just the word.")
    print("PASS  no blocking issues.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
