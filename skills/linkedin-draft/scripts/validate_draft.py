#!/usr/bin/env python3
"""Scan LinkedIn post text for PII, secrets, confidentiality markers, and formatting."""

import argparse
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
    (re.compile(r"(?i)\$\s?\d[\d,.]*\s?(?:million|billion|M\b|B\b|k\b)"), "monetary amount"),
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


def check(document: str) -> tuple[list[str], list[str]]:
    text = post_text(document)
    errors = []
    warnings = []
    for pattern, label in BLOCKING:
        if match := pattern.search(text):
            errors.append(f"{label}: {match.group()!r}")
    for pattern, label in WARNINGS:
        if pattern.search(text):
            warnings.append(label)
    if not text.strip():
        errors.append("draft is empty")
    if len(text) > MAX_CHARS:
        errors.append(f"{len(text)} characters exceeds LinkedIn's {MAX_CHARS} limit")
    return errors, warnings


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


def self_test() -> int:
    failures = 0
    for text, expected_label, should_block in SELF_TESTS:
        errors, _ = check(text)
        blocked = bool(errors)
        passed = blocked == should_block and (
            expected_label is None or any(expected_label in error for error in errors)
        )
        result = errors or "clean"
        sample = text.splitlines()[-1][:48]
        print(f"{'PASS' if passed else 'FAIL'}  {sample:<48} -> {result}")
        failures += not passed
    print(f"\n{len(SELF_TESTS) - failures}/{len(SELF_TESTS)} passed")
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
    errors, warnings = check(document)
    for warning in warnings:
        print(f"WARN  {warning}")
    for error in errors:
        print(f"BLOCK {error}")
    if errors:
        print(f"\n{len(errors)} blocking issue(s).")
        return 1
    print("PASS  no blocking issues.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
