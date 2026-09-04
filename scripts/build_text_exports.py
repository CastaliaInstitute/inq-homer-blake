#!/usr/bin/env python3

"""Build plain-text, screen-reader-friendly provisional volume exports."""

from html import unescape
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from translation_extract import book_translation  # noqa: E402


for volume, title in (("iliad", "The Iliad"), ("odyssey", "The Odyssey")):
    output = ROOT / "output" / "text" / f"inq-homer-{volume}.txt"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        handle.write(f"HOMER — {title.upper()}\n")
        handle.write("Provisional accessible text export — not approved for final release.\n\n")
        for path in sorted((ROOT / "text" / volume).glob("book-*-opening.md")):
            book = int(path.stem.split("-")[1])
            handle.write(f"BOOK {book}\n\n")
            for line in book_translation(path):
                text = unescape(line).strip()
                if text:
                    handle.write(text + "\n")
            handle.write("\n")
    print(output)
