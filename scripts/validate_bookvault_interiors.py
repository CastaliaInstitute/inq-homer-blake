#!/usr/bin/env python3
"""Fail closed on Homer BookVault prepress candidate structure and content."""

from __future__ import annotations

from collections import Counter
from html import unescape
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unicodedata

from translation_extract import book_translation


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "output" / "pdf" / "inq-homer-bookvault-interiors.manifest.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tokens(text: str) -> list[str]:
    normalized = unicodedata.normalize("NFKD", unescape(text)).casefold()
    # Join lexical hyphens because Poppler can drop them at a line break, but
    # keep punctuation dashes as boundaries ("him - it" must not become
    # ``himit``).
    normalized = re.sub(r"(?<=[a-z0-9])[-‐‑]\s*(?=[a-z0-9])", "", normalized)
    normalized = re.sub(r"[‒–—]", " ", normalized)
    return re.findall(r"[a-z0-9]+", normalized)


def pdfinfo(path: Path, start: int | None = None, end: int | None = None) -> str:
    command = ["pdfinfo"]
    if start is not None:
        command.extend(["-f", str(start), "-l", str(end or start), "-box"])
    command.append(str(path))
    return subprocess.check_output(command, text=True)


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["trimMm"] == [168, 260]
    assert manifest["documentMm"] == [174, 266]
    assert manifest["bleedMm"] == 3
    assert manifest["historicalScansIncluded"] is False
    assert manifest["releaseEligible"] is False

    for slug, volume in manifest["volumes"].items():
        pdf = ROOT / volume["pdf"]
        assert digest(pdf) == volume["pdfSha256"]
        assert volume["pageCount"] % 2 == 0
        assert volume["plateCount"] == len(volume["books"]) == 24
        assert [book["book"] for book in volume["books"]] == list(range(1, 25))
        assert all(book["plateApproval"] == "pending" for book in volume["books"])

        info = pdfinfo(pdf)
        assert f"Pages:           {volume['pageCount']}" in info
        boxes = pdfinfo(pdf, 1, volume["pageCount"])
        media = re.findall(r"^Page\s+\d+ MediaBox:\s+0\.00\s+0\.00\s+([\d.]+)\s+([\d.]+)", boxes, re.MULTILINE)
        trim = re.findall(r"^Page\s+\d+ TrimBox:\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)", boxes, re.MULTILINE)
        assert len(media) == len(trim) == volume["pageCount"]
        expected_media = (174 * 72 / 25.4, 266 * 72 / 25.4)
        expected_trim = (3 * 72 / 25.4, 3 * 72 / 25.4, 171 * 72 / 25.4, 263 * 72 / 25.4)
        assert all(all(abs(float(actual) - expected) < .02 for actual, expected in zip(row, expected_media)) for row in media)
        assert all(all(abs(float(actual) - expected) < .02 for actual, expected in zip(row, expected_trim)) for row in trim)

        images = subprocess.check_output(["pdfimages", "-list", str(pdf)], text=True)
        image_rows = [line.split() for line in images.splitlines() if re.match(r"^\s*\d+\s+\d+\s+image\s+", line)]
        full_page = [row for row in image_rows if (int(row[3]), int(row[4])) == (2055, 3142)]
        assert len(full_page) == 24, f"{slug}: expected 24 full-page plates, found {len(full_page)}"
        assert [int(row[0]) for row in full_page] == volume["colourPages"]

        fonts = subprocess.check_output(["pdffonts", str(pdf)], text=True)
        font_rows = [line.split() for line in fonts.splitlines()[2:] if line.strip()]
        assert font_rows and all(row[4] == "yes" for row in font_rows), f"{slug}: all fonts must be embedded"

        title = subprocess.check_output(["pdftotext", "-f", "1", "-l", "1", str(pdf), "-"], text=True)
        assert volume["title"] in title
        assert "Translated by a.Longfellow" in title
        assert "Illustrated by a.Blake" in title
        assert "Edited by Castalia Institute" not in title

        for book in volume["books"]:
            source = ROOT / book["source"]
            plate = ROOT / book["productionAsset"]
            assert digest(source) == book["sourceSha256"]
            assert digest(plate) == book["productionSha256"]
            assert book["productionPixels"] == [2055, 3142]
            assert book["platePage"] + 1 == book["textStartPage"]
            rendered = subprocess.check_output([
                "pdftotext", "-f", str(book["textStartPage"]), "-l", str(book["textEndPage"]), str(pdf), "-",
            ], text=True)
            expected = Counter(tokens("\n".join(book_translation(source))))
            missing = expected - Counter(tokens(rendered))
            assert not missing, f"{slug} Book {book['book']} lost source tokens: {dict(missing.most_common(8))}"

        print(
            f"PASS {pdf.name}: {volume['pageCount']} pages, exact 168 x 260 mm trim, "
            "24 full-page plates, embedded fonts, complete source text"
        )


if __name__ == "__main__":
    main()
