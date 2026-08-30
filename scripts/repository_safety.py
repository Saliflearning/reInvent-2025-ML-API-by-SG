"""Scan the tracked tree and all reachable Git blobs for public-safety risks."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

MAX_BLOB_BYTES = 2_000_000
SCANNER_PATH = "scripts/repository_safety.py"
INTERNAL_PATH = re.compile(
    r"(^|/)(?:AGENTS|CLAUDE)\.md$|(^|/)(?:\.agents|\.claude|\.specify|specs|graphify-out)(/|$)",
    re.IGNORECASE,
)
CHECKS = (
    ("private-path", re.compile(r"(?:[A-Z]:\\Users\\|/Users/|/home/)", re.IGNORECASE)),
    ("legal-name", re.compile(r"\bSalif\s+Guingani\b", re.IGNORECASE)),
    (
        "email",
        re.compile(
            r"\b[A-Z0-9._%+-]+@(?!users\.noreply\.github\.com\b)[A-Z0-9.-]+\.[A-Z]{2,}\b",
            re.IGNORECASE,
        ),
    ),
    (
        "phone",
        re.compile(r"(?<!\d)(?:\+?1[ .-]?)?\(?[2-9]\d{2}\)?[ .-]?\d{3}[ .-]?\d{4}(?!\d)"),
    ),
    ("aws-access-key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("private-key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
)


def git(*args: str, text: bool = True) -> str | bytes:
    return subprocess.check_output(
        ["git", *args],
        text=text,
        encoding="utf-8" if text else None,
        errors="replace" if text else None,
    )


def scan_text(text: str, path: str, include_path_policy: bool) -> list[str]:
    if path == SCANNER_PATH:
        return []

    findings: list[str] = []
    normalized = path.replace("\\", "/")
    if include_path_policy and INTERNAL_PATH.search(normalized):
        findings.append(f"internal-artifact:{normalized}")
    for category, pattern in CHECKS:
        if normalized.endswith(".terraform.lock.hcl") and category in {"email", "phone"}:
            # Provider checksums are random and can resemble phone-number shapes.
            continue
        if pattern.search(text):
            findings.append(f"{category}:{normalized}")
    return findings


def scan_current() -> list[str]:
    findings: list[str] = []
    for raw_path in git("ls-files", "-z").split("\0"):
        if not raw_path:
            continue
        path = Path(raw_path)
        try:
            with path.open("rb") as handle:
                if os.fstat(handle.fileno()).st_size > MAX_BLOB_BYTES:
                    continue
                data = handle.read(MAX_BLOB_BYTES + 1)
        except FileNotFoundError:
            continue
        if b"\0" in data:
            continue
        findings.extend(scan_text(data.decode("utf-8", errors="replace"), raw_path, True))
    return findings


def scan_history() -> list[str]:
    findings: list[str] = []
    seen: set[str] = set()
    for line in git("rev-list", "--objects", "--all").splitlines():
        oid, _, path = line.partition(" ")
        if not path or oid in seen:
            continue
        seen.add(oid)
        try:
            size = int(git("cat-file", "-s", oid).strip())
        except (subprocess.CalledProcessError, ValueError):
            continue
        if size > MAX_BLOB_BYTES:
            continue
        data = git("cat-file", "-p", oid, text=False)
        if b"\0" in data:
            continue
        findings.extend(scan_text(data.decode("utf-8", errors="replace"), path, False))
    return findings


def self_test() -> list[str]:
    failures: list[str] = []
    fixtures = {
        "legal-name": "Salif Guingani",
        "email": "owner@example.com",
        "phone": "317-555-0123",
        "aws-access-key": "AKIAABCDEFGHIJKLMNOP",
        "github-token": "ghp_abcdefghijklmnopqrstuvwxyz123456",
        "private-key": "-----BEGIN PRIVATE KEY-----",
        "private-path": r"C:\Users\owner\project",
        "jwt": "eyJabcdefghijk.abcdefghijk.abcdefghijk",
    }
    for expected, fixture in fixtures.items():
        categories = {item.split(":", 1)[0] for item in scan_text(fixture, "fixture.txt", False)}
        if expected not in categories:
            failures.append(f"missing-self-test:{expected}")
    if scan_text("bot@users.noreply.github.com", "fixture.txt", False):
        failures.append("noreply-email-allowlist")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--current", action="store_true")
    group.add_argument("--history", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        findings = self_test()
        mode = "self-test"
    elif args.current:
        findings = scan_current()
        mode = "current"
    else:
        findings = scan_history()
        mode = "history"

    if findings:
        for finding in sorted(set(findings)):
            print(finding)
        print(f"Repository safety gate failed ({mode}).", file=sys.stderr)
        return 1

    print(f"Repository safety gate passed ({mode}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
