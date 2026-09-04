#!/usr/bin/env python3
"""Build a labeled visual contact sheet for the 48 provisional plate slots.

The sheet is a human-review aid only. It uses the current 2055 x 3142 px
print-review derivatives and never changes their provisional approval state.
"""

from __future__ import annotations

import csv
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "design" / "plate-selection-audit.csv"
OUT = ROOT / "design" / "plate-review-contact-sheet.jpg"

COLS = 6
THUMB_W = 240
THUMB_H = 367
LABEL_H = 52
PAD = 18
HEADER_H = 64


def font(size: int):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def main() -> None:
    with AUDIT.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 48:
        raise SystemExit(f"expected 48 plate rows, found {len(rows)}")

    rows.sort(key=lambda row: (row["volume"], int(row["book"])))
    rows.sort(key=lambda row: (0 if row["volume"] == "Iliad" else 1, int(row["book"])))

    rows_per_page = (len(rows) + COLS - 1) // COLS
    width = COLS * THUMB_W + (COLS + 1) * PAD
    height = HEADER_H + rows_per_page * (THUMB_H + LABEL_H + PAD) + PAD
    sheet = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(sheet)
    title_font = font(28)
    label_font = font(18)
    small_font = font(14)
    draw.text((PAD, 16), "Homer / Blake-informed edition — provisional plate review", fill="black", font=title_font)

    for index, row in enumerate(rows):
        col = index % COLS
        line = index // COLS
        x = PAD + col * THUMB_W + col * PAD
        y = HEADER_H + PAD + line * (THUMB_H + LABEL_H + PAD)
        image_path = ROOT / row["print_derivative"]
        if not image_path.is_file():
            raise SystemExit(f"missing print-review derivative: {image_path}")
        with Image.open(image_path) as source:
            image = source.convert("RGB")
            image.thumbnail((THUMB_W, THUMB_H), Image.Resampling.LANCZOS)
            tile = Image.new("RGB", (THUMB_W, THUMB_H), "#eeeeee")
            tile.paste(image, ((THUMB_W - image.width) // 2, (THUMB_H - image.height) // 2))
        sheet.paste(tile, (x, y))
        draw.rectangle((x, y, x + THUMB_W - 1, y + THUMB_H - 1), outline="#777777")
        slot = row["placeholder_slot"]
        status = row["approval_status"]
        draw.text((x + 4, y + THUMB_H + 4), f"{slot}  {row['plate_id'][:24]}", fill="black", font=label_font)
        draw.text((x + 4, y + THUMB_H + 28), f"{row['selection_status']} / {status}", fill="#555555", font=small_font)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(OUT, quality=92, optimize=True, progressive=True)
    print(f"Wrote {OUT} ({width}x{height}, {len(rows)} slots)")


if __name__ == "__main__":
    main()
