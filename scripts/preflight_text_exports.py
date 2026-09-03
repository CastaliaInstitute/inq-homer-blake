#!/usr/bin/env python3

"""Verify the structure of provisional accessible volume text exports."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


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
    print(f"OK {path.relative_to(ROOT)}: 24 books, reading text only")

print("Text-export preflight passed: 2 accessible volume exports.")
