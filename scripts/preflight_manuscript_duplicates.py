#!/usr/bin/env python3

"""Reject repeated multi-line blocks in the assembled Homer manuscripts."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from translation_extract import book_translation  # noqa: E402

BLOCK_LINES = 4
MIN_BLOCK_CHARACTERS = 160


def normalized(line: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", line.lower())


failures: list[str] = []
checked = 0
for volume in ("iliad", "odyssey"):
    for path in sorted((ROOT / "text" / volume).glob("book-??-opening.md")):
        lines = [normalized(line) for line in book_translation(path)]
        seen: dict[tuple[str, ...], int] = {}
        for index in range(len(lines) - BLOCK_LINES + 1):
            block = tuple(lines[index : index + BLOCK_LINES])
            if sum(len(line) for line in block) < MIN_BLOCK_CHARACTERS:
                continue
            previous = seen.get(block)
            if previous is not None and index - previous >= BLOCK_LINES:
                failures.append(
                    f"{path.relative_to(ROOT)}: repeated {BLOCK_LINES}-line block "
                    f"at extracted lines {previous + 1} and {index + 1}"
                )
            else:
                seen[block] = index
        checked += 1

if failures:
    for failure in failures:
        print(f"FAIL manuscript duplication: {failure}", file=sys.stderr)
    raise SystemExit(1)

print(f"Manuscript duplication preflight passed: {checked} books checked.")
