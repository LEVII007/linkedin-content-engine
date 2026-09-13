#!/usr/bin/env python3
import argparse
import re
import sys

MAX_CHARS = 3000

BLOCKING = [
    (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"), "email address"),
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "US SSN pattern"),
    (re.compile(r"(?<!\d)(?:\+?91[-.\s]?)?[6-9]\d{9}(?!\d)"), "India mobile number"),
    (re.compile(r"(?i)\bMRN\s*[:#]?\s*\d+"), "medical record number"),
    (re.compile(r"(?i)\bNPI\s*[:#]?\s*\d{10}\b"), "provider NPI"),
    (re.compile(r"(?i)\b(?:DOB|date of birth|patient\s+(?:id|name|#))\b"), "patient identifier"),
    (re.compile(r"(?i)\b(?:password|passwd|secret|token|api.?key)\s*[:=]\s*\S+"), "credential"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key"),
    (re.compile(r"(?i)\b(?:internal only|confidential|under NDA|not for distribution)\b"), "confidentiality marker"),
    (re.compile(r"(?i)\b(?:revenue|budget|deal|contract)\s+(?:of|worth|valued)\b"), "private financial detail"),
]

WARNINGS = [
    (re.compile(r"\*\*|^#{1,6}\s", re.M), "markdown syntax"),
    (re.compile(r"(?i)\b(?:thoughts\?|agree\?|comment below|follow for more)"), "engagement bait"),
    (re.compile(r"(?:#\w+\s*){7,}"), "more than six hashtags"),
]


def check(text: str) -> tuple[list[str], list[str]]:
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()
    text = open(args.file, encoding="utf-8").read()
    errors, warnings = check(text)
    for warning in warnings:
        print(f"WARN  {warning}")
    for error in errors:
        print(f"BLOCK {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
