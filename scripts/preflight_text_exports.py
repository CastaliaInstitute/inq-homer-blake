#!/usr/bin/env python3

"""Verify the structure of provisional accessible volume text exports."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from translation_extract import book_translation  # noqa: E402


def fail(message):
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


for volume in ("iliad", "odyssey"):
    path = ROOT / "output" / "text" / f"inq-homer-{volume}.txt"
    if not path.is_file():
        fail(f"missing export {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    headings = [line for line in text.splitlines() if line.startswith("BOOK ")]
    expected = [f"BOOK {number}" for number in range(1, 25)]
    if headings != expected:
        fail(f"{path.name} does not contain BOOK 1 through BOOK 24 in order")
    if "Decision log" in text or "Working synopsis" in text:
        fail(f"{path.name} contains editorial metadata")
    if "Provisional accessible text export" not in text:
        fail(f"{path.name} lacks its provisional status header")
    exported_books = text.splitlines()
    for number in range(1, 25):
        start = exported_books.index(f"BOOK {number}") + 1
        end = exported_books.index(f"BOOK {number + 1}") if number < 24 else len(exported_books)
        actual = [line for line in exported_books[start:end] if line.strip()]
        source = ROOT / "text" / volume / f"book-{number:02d}-opening.md"
        expected_lines = [line.strip() for line in book_translation(source) if line.strip()]
        if actual != expected_lines:
            fail(f"{path.name} Book {number} differs from {source.relative_to(ROOT)}; rebuild the text export")
    print(f"OK {path.relative_to(ROOT)}: 24 books, reading text only")

print("Text-export preflight passed: 2 accessible volume exports.")
