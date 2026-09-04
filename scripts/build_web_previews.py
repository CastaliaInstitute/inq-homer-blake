#!/usr/bin/env python3
"""Build the Homer web samplers as cover + one plate + complete Book I text."""

from __future__ import annotations

import fcntl
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image as PILImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import BaseDocTemplate, Frame, NextPageTemplate, PageBreak, PageTemplate, Paragraph, Spacer

from translation_extract import book_translation


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output" / "pdf"
TMP_DIR = ROOT / "tmp" / "pdfs" / "homer-web-previews"
FONT_DIR = ROOT / "assets" / "fonts"
# BookVault's canonical comic trim is exactly 168 x 260 mm.
PAGE_W, PAGE_H = 6.625 * inch, 10.25 * inch
MARGIN_X, MARGIN_TOP, MARGIN_BOTTOM = 15 * mm, 16 * mm, 15 * mm
COLUMN_GUTTER = 6 * mm

for name, filename in {
    "Cormorant": "CormorantGaramond-Regular.ttf",
    "CormorantI": "CormorantGaramond-Italic.ttf",
    "CormorantB": "CormorantGaramond-SemiBold.ttf",
}.items():
    pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / filename)))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="PreviewBook", fontName="CormorantB", fontSize=20, leading=23,
    alignment=TA_CENTER, textColor="#211d18", spaceAfter=4,
))
styles.add(ParagraphStyle(
    name="PreviewSub", fontName="CormorantI", fontSize=9.2, leading=11,
    alignment=TA_CENTER, textColor="#61594f", spaceAfter=12,
))
styles.add(ParagraphStyle(
    name="PreviewVerse", fontName="Cormorant", fontSize=9.35, leading=11.25,
    alignment=TA_LEFT, textColor="#211d18", spaceAfter=0,
))


class DeterministicCanvas(Canvas):
    def __init__(self, *args, **kwargs):
        kwargs["invariant"] = 1
        super().__init__(*args, **kwargs)


def draw_full_page(canvas: Canvas, path: Path) -> None:
    with PILImage.open(path) as image:
        width, height = image.size
    scale = max(PAGE_W / width, PAGE_H / height)
    draw_w, draw_h = width * scale, height * scale
    canvas.drawImage(
        ImageReader(str(path)),
        (PAGE_W - draw_w) / 2,
        (PAGE_H - draw_h) / 2,
        width=draw_w,
        height=draw_h,
        mask="auto",
    )


def text_footer(title: str):
    def footer(canvas: Canvas, doc: BaseDocTemplate) -> None:
        canvas.saveState()
        canvas.setStrokeColorRGB(0.72, 0.69, 0.64)
        canvas.setLineWidth(0.3)
        canvas.line(MARGIN_X, 9.5 * mm, PAGE_W - MARGIN_X, 9.5 * mm)
        canvas.setFont("Cormorant", 7.1)
        canvas.setFillColorRGB(0.34, 0.31, 0.27)
        canvas.drawString(MARGIN_X, 6.3 * mm, f"{title.upper()} / BOOK I")
        canvas.drawCentredString(PAGE_W / 2, 6.3 * mm, "Longfellow-inspired translation / Castalia Institute")
        canvas.drawRightString(PAGE_W - MARGIN_X, 6.3 * mm, str(doc.page))
        canvas.restoreState()
    return footer


def build(slug: str, title: str, book_label: str) -> Path:
    cover = ROOT / "assets" / "covers" / "epic" / slug / "front-cover.jpg"
    plate = ROOT / "assets" / "print" / "illustrations" / slug / "book-01-full-bleed.jpg"
    text_path = ROOT / "text" / slug / "book-01-opening.md"
    for path in (cover, plate, text_path):
        if not path.is_file():
            raise FileNotFoundError(path)

    output = OUTPUT_DIR / f"inq-homer-{slug}-web-preview.pdf"
    working = TMP_DIR / f"{slug}-web-preview.building.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    working.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(working), pagesize=(PAGE_W, PAGE_H),
        leftMargin=MARGIN_X, rightMargin=MARGIN_X,
        topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOTTOM,
        title=f"{title} - Book I illustrated preview",
        author="Castalia Institute",
        subject="iNQ Epic sampler: cover, one original a.Blake plate, and complete Book I text",
    )

    blank = Frame(0, 0, PAGE_W, PAGE_H, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="blank")
    column_width = (doc.width - COLUMN_GUTTER) / 2
    left = Frame(doc.leftMargin, doc.bottomMargin, column_width, doc.height, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="left")
    right = Frame(doc.leftMargin + column_width + COLUMN_GUTTER, doc.bottomMargin, column_width, doc.height, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="right")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=blank, onPage=lambda canvas, _doc: draw_full_page(canvas, cover)),
        PageTemplate(id="plate", frames=blank, onPage=lambda canvas, _doc: draw_full_page(canvas, plate)),
        PageTemplate(id="text", frames=[left, right], onPage=text_footer(title)),
    ])

    story = [NextPageTemplate("plate"), PageBreak(), NextPageTemplate("text"), PageBreak()]
    story.extend([
        Paragraph("BOOK I", styles["PreviewBook"]),
        Paragraph(book_label, styles["PreviewSub"]),
    ])
    for line in book_translation(text_path):
        story.extend([Paragraph(escape(line), styles["PreviewVerse"]), Spacer(1, 1.1)])

    doc.build(story, canvasmaker=DeterministicCanvas)
    working.replace(output)
    print(output)
    return output


def main() -> None:
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    with (TMP_DIR / "build.lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        build("iliad", "The Iliad", "The Anger of Achilles")
        build("odyssey", "The Odyssey", "The Man of Many Turnings")


if __name__ == "__main__":
    main()
