#!/usr/bin/env python3

"""Verify line-ranged headings in collation authorities are contiguous."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
files = sorted((ROOT / "text").glob("*/book-*-collation-*.md"))
if not files:
    raise SystemExit("FAIL: no collation authorities found")

checked = 0
skipped = 0

for path in files:
    match = re.search(r"collation-(\d+)-(\d+)\.md$", path.name)
    if not match:
        raise SystemExit(f"FAIL: unparseable collation filename: {path}")
    expected_start, expected_end = map(int, match.groups())
    sections = [
        (int(start), int(end))
        for start, end in re.findall(
            r"^### Lines (\d+)[–-](\d+)",
            path.read_text(encoding="utf-8"),
            re.MULTILINE,
        )
    ]
    if not sections:
        skipped += 1
        continue
    cursor = expected_start
    for start, end in sections:
        if start != cursor:
            raise SystemExit(
                f"FAIL: {path} has a section gap/overlap at {start}; expected {cursor}"
            )
        cursor = end + 1
    if cursor - 1 != expected_end:
        raise SystemExit(
            f"FAIL: {path} sections end at {cursor - 1}; expected {expected_end}"
        )
    checked += 1

print(
    f"Collation-section preflight passed: {checked} heading-based authorities; "
    f"{skipped} file-range authorities skipped."
)
