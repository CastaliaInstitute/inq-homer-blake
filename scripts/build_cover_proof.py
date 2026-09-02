#!/usr/bin/env python3
"""Build clearly marked, template-independent casewrap cover design proofs."""

from __future__ import annotations

import argparse
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = ROOT / "assets" / "fonts"
for name, filename in {
    "Cormorant": "CormorantGaramond-Regular.ttf",
    "CormorantI": "CormorantGaramond-Italic.ttf",
    "CormorantB": "CormorantGaramond-SemiBold.ttf",
}.items():
    pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / filename)))

TRIM_W, TRIM_H = 7 * inch, 10 * inch
BLEED = 0.125 * inch
WRAP = 0.75 * inch
DEFAULT_SPINE = 0.5 * inch


def fit_image(canvas: Canvas, path: Path, x: float, y: float, w: float, h: float) -> None:
    with Image.open(path) as image:
        iw, ih = image.size
    scale = max(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    canvas.drawImage(str(path), x + (w - dw) / 2, y + (h - dh) / 2, dw, dh,
                    preserveAspectRatio=True, mask="auto")


def label(canvas: Canvas, text: str, x: float, y: float, size: float = 9,
          color=white, font="Cormorant") -> None:
    canvas.setFillColor(color)
    canvas.setFont(font, size)
    canvas.drawString(x, y, text)


def build(volume: str, title: str, pages: int, art: Path, back_art: Path, output: Path) -> None:
    # The placeholder spine is deliberately not a printer estimate. The exact
    # Lulu template must replace this geometry before any release export.
    spine = DEFAULT_SPINE
    doc_w = 2 * (TRIM_W + WRAP) + spine
    doc_h = TRIM_H + 2 * WRAP
    canvas = Canvas(str(output), pagesize=(doc_w, doc_h), pageCompression=1,
                    title=f"{title} cover design proof", author="CastaliaInstitute")

    # Back, spine, and front panels in the conventional left-to-right spread.
    back_x = 0
    spine_x = TRIM_W + WRAP
    front_x = spine_x + spine
    canvas.setFillColor(HexColor("#181815"))
    canvas.rect(0, 0, doc_w, doc_h, fill=1, stroke=0)
    fit_image(canvas, back_art, back_x, 0, TRIM_W + WRAP, doc_h)
    canvas.setFillColor(HexColor("#12120f"))
    canvas.rect(spine_x, 0, spine, doc_h, fill=1, stroke=0)
    fit_image(canvas, art, front_x, 0, TRIM_W + WRAP, doc_h)

    # Dark veils preserve contrast without altering the source art master.
    canvas.setFillColor(HexColor("#000000"))
    canvas.setFillAlpha(0.45)
    canvas.rect(front_x, 0, TRIM_W + WRAP, doc_h, fill=1, stroke=0)
    canvas.setFillAlpha(0.60)
    canvas.rect(0, 0, TRIM_W + WRAP, doc_h, fill=1, stroke=0)
    canvas.setFillAlpha(1)

    label(canvas, "CASTALIA INSTITUTE", WRAP, doc_h - WRAP - 28, 10, HexColor("#e6d8bd"), "CormorantB")
    canvas.setFillColor(HexColor("#f1e8d6"))
    canvas.setFont("CormorantB", 31)
    canvas.drawString(front_x + WRAP + 22, doc_h - WRAP - 90, title.upper())
    label(canvas, "HOMER", front_x + WRAP + 24, doc_h - WRAP - 120, 13, HexColor("#e6d8bd"), "CormorantI")
    label(canvas, "A new Longfellow-inspired translation", front_x + WRAP + 24, WRAP + 56, 11, white, "CormorantI")
    label(canvas, "PROVISIONAL COVER DESIGN PROOF", WRAP, WRAP + 28, 8, HexColor("#e6d8bd"), "CormorantB")
    label(canvas, f"Current architecture proof: {pages} pages", WRAP, WRAP + 14, 7.5, white)
    label(canvas, "Historical and original image credits remain in the provenance dossier.", WRAP, 18, 7, HexColor("#ded6c8"))

    # Spine title is intentionally omitted: the printer template controls its
    # final width and safe area.
    canvas.setFillColor(HexColor("#d7c7a9"))
    canvas.setStrokeColor(HexColor("#c3b18f"))
    canvas.setLineWidth(0.4)
    canvas.rect(WRAP, WRAP, doc_w - 2 * WRAP, TRIM_H, fill=0, stroke=1)
    canvas.setFillColor(HexColor("#e3d5bd"))
    canvas.setFont("CormorantB", 7)
    canvas.drawCentredString(spine_x + spine / 2, doc_h - WRAP - 16, "TEMPLATE PENDING")
    canvas.showPage()
    canvas.save()
    print(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--volume", choices=("iliad", "odyssey"), required=True)
    parser.add_argument("--pages", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.pages < 24:
        raise SystemExit("cover proofs require at least 24 pages")
    if args.volume == "iliad":
        title = "The Iliad"
        art = ROOT / "assets/generated/iliad/book-01-apollo-v2.png"
        back_art = ROOT / "assets/source/iliad/met-337355-dp-14470-001.jpg"
    else:
        title = "The Odyssey"
        art = ROOT / "assets/generated/odyssey/book-01-athena-v2.png"
        back_art = ROOT / "assets/source/iliad/met-337355-dp-15151-001.jpg"
    for path in (art, back_art):
        if not path.is_file():
            raise SystemExit(f"missing cover art: {path}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    build(args.volume, title, args.pages, art, back_art, args.output)


if __name__ == "__main__":
    main()
