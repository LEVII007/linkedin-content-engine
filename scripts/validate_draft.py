#!/usr/bin/env python3
"""Pre-review safety check for a draft post.

Runs in stage 3, before a draft reaches the human. Errors block; warnings are
advisory. This checks for things that must never be published — leaked secrets,
personal data, confidentiality markers — plus formatting that LinkedIn silently
mangles.

It deliberately does NOT police vocabulary. Banning "game-changer" on a shallow
post yields a shallow post with better word choice; slop is a topic-supply
problem, handled upstream by the scoring threshold.

PII patterns adapted from martinopedal/linkedin-auto-poster (MIT), retargeted
from Norwegian identifiers to the healthcare/India/provider-data context.

Usage:
    ./validate_draft.py draft.txt
    ./validate_draft.py --self-test
"""
import argparse
import re
import sys

MAX_CHARS = 3000

# Errors — never publish
BLOCKING = [
    (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"), "email address"),
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "US SSN pattern"),
    (re.compile(r"(?<!\d)(?:\+?91[-.\s]?)?[6-9]\d{9}(?!\d)"), "India mobile number pattern"),
    (re.compile(r"(?<!\d)\+?1?[-.\s]?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}(?!\d)"), "US phone pattern"),
    (re.compile(r"(?i)\bMRN\s*[:#]?\s*\d+"), "medical record number"),
    (re.compile(r"(?i)\bNPI\s*[:#]?\s*\d{10}\b"), "provider NPI"),
    (re.compile(r"(?i)\b(?:DOB|date of birth)\b"), "date of birth reference"),
    (re.compile(r"(?i)\bpatient\s+(?:id|name|#)\b"), "patient identifier"),
    (re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"), "IP address"),
    (re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I), "UUID / resource id"),
    (re.compile(r"(?i)\b(?:password|passwd|secret|token|api.?key)\s*[:=]\s*\S+"), "credential"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key id"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key"),
    (re.compile(r"(?i)\b(?:internal only|confidential|under NDA|not for distribution)\b"), "confidentiality marker"),
    (re.compile(r"(?i)\b(?:revenue|budget|deal|contract)\s+(?:of|worth|valued)\b"), "private financial detail"),
]

# Warnings — advisory
ADVISORY = [
    (re.compile(r"\*\*|^#{1,6}\s|^\s*[-*]\s", re.M), "markdown syntax — LinkedIn renders it literally"),
    (re.compile(r"(?i)\b(?:thoughts\?|agree\?|comment below|drop a|let me know below)"), "engagement bait"),
    (re.compile(r"(?i)^\s*(?:P\.?S\.?|Repost if)", re.M), "growth-hack tail"),
    (re.compile(r"(?:#\w+\s*){7,}"), "more than six hashtags"),
]


def check(text: str):
    errors, warnings = [], []
    for pat, label in BLOCKING:
        m = pat.search(text)
        if m:
            errors.append(f"{label}: {m.group()!r}")
    for pat, label in ADVISORY:
        if pat.search(text):
            warnings.append(label)
    if not text.strip():
        errors.append("draft is empty")
    if len(text) > MAX_CHARS:
        errors.append(f"{len(text)} chars exceeds LinkedIn's {MAX_CHARS} limit")
    return errors, warnings


SELF_TESTS = [
    ("Reach me at a@b.com", "email address", True),
    ("Patient MRN: 88213 was excluded", "medical record number", True),
    ("NPI 1234567890 had no Part D rows", "provider NPI", True),
    ("api_key=sk-abc123", "credential", True),
    ("Closed a contract worth mid-six figures", "financial detail", True),
    ("This is confidential, do not share", "confidentiality marker", True),
    ("Call +919876543210", "India mobile number pattern", True),
    ("data.cms.gov returned 403 from ap-south-1", None, False),
    ("Cut false matches 97.4% with an identity-gated query", None, False),
    ("We raised $5M. #AI #Pharma #LifeSciences #SynthioLabs", None, False),
]


def self_test() -> int:
    failures = 0
    for text, expect_label, should_block in SELF_TESTS:
        errors, _ = check(text)
        blocked = bool(errors)
        ok = blocked == should_block and (
            expect_label is None or any(expect_label in e for e in errors)
        )
        print(f"{'PASS' if ok else 'FAIL'}  {text[:46]:<48} -> {errors or 'clean'}")
        failures += not ok
    print(f"\n{len(SELF_TESTS) - failures}/{len(SELF_TESTS)} passed")
    return 1 if failures else 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("file", nargs="?")
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()

    if a.self_test:
        return self_test()
    if not a.file:
        p.error("give a file, or --self-test")

    errors, warnings = check(open(a.file, encoding="utf-8").read())
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"BLOCK {e}")
    if errors:
        print(f"\n{len(errors)} blocking issue(s). Do not send to review — fix the draft.")
        return 1
    print("\nClean." if not warnings else f"\nNo blockers, {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
