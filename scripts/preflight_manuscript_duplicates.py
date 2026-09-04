#!/usr/bin/env python3

"""Reject accidental repeated verse in Homer manuscripts and authorities."""

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


def adjacent_duplicate_lines(lines: list[str], label: str) -> None:
    for index in range(1, len(lines)):
        if lines[index] and lines[index] == lines[index - 1]:
            failures.append(
                f"{label}: repeated verse line at extracted lines "
                f"{index} and {index + 1}: {lines[index]}"
            )


failures: list[str] = []
checked = 0
for volume in ("iliad", "odyssey"):
    for path in sorted((ROOT / "text" / volume).glob("book-??-opening.md")):
        lines = [normalized(line) for line in book_translation(path)]
        adjacent_duplicate_lines(lines, str(path.relative_to(ROOT)))
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

    for path in sorted((ROOT / "text" / volume).glob("book-??-collation-*.md")):
        section = path.read_text(encoding="utf-8").split("## Revised translation pass", 1)[-1]
        section = section.split("## Decision log", 1)[0]
        lines = []
        for raw in section.splitlines():
            value = normalized(raw)
            if value and not raw.lstrip().startswith("#"):
                lines.append(value)
        adjacent_duplicate_lines(lines, str(path.relative_to(ROOT)))

if failures:
    for failure in failures:
        print(f"FAIL manuscript duplication: {failure}", file=sys.stderr)
    raise SystemExit(1)

print(f"Manuscript duplication preflight passed: {checked} books checked.")
