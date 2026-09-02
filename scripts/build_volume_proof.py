#!/usr/bin/env python3

"""Build deterministic, provisional whole-volume architecture proofs.

The source Markdown remains authoritative. This builder includes only each
book's Translation section; editorial decision logs remain outside the
interior proof until line-level review is complete.
"""

from pathlib import Path
import re
import sys
from xml.sax.saxutils import escape

from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import inch
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph, Spacer

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "output/pdf"
FONT_DIR = Path("/System/Library/Fonts/Supplemental")

for name, filename in {
    "TimesNR": "Times New Roman.ttf",
    "TimesNRI": "Times New Roman Italic.ttf",
    "TimesNRB": "Times New Roman Bold.ttf",
}.items():
    pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / filename)))

PAGE_W, PAGE_H = 7 * inch, 10 * inch
MARGIN_X, MARGIN_Y = 0.72 * inch, 0.75 * inch

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="VolumeTitle", fontName="TimesNRB", fontSize=25, leading=30,
                          alignment=TA_CENTER, textColor="#1f1c18", spaceAfter=18))
styles.add(ParagraphStyle(name="Sub", fontName="TimesNRI", fontSize=11, leading=15,
                          alignment=TA_CENTER, textColor="#625b52", spaceAfter=12))
styles.add(ParagraphStyle(name="Book", fontName="TimesNRB", fontSize=18, leading=22,
                          alignment=TA_LEFT, textColor="#1f1c18", spaceAfter=14))
styles.add(ParagraphStyle(name="Verse", fontName="TimesNR", fontSize=10.7, leading=14.2,
                          alignment=TA_LEFT, textColor="#1f1c18", leftIndent=0.05 * inch))
styles.add(ParagraphStyle(name="Small", fontName="TimesNR", fontSize=8.3, leading=11.5,
                          alignment=TA_LEFT, textColor="#3d3934"))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColorRGB(0.72, 0.69, 0.64)
    canvas.setLineWidth(0.35)
    canvas.line(MARGIN_X, 0.48 * inch, PAGE_W - MARGIN_X, 0.48 * inch)
    canvas.setFont("TimesNR", 7.5)
    canvas.setFillColorRGB(0.39, 0.36, 0.32)
    canvas.drawString(MARGIN_X, 0.31 * inch, "HOMER / iNQ HOMER BLAKE / PROVISIONAL VOLUME PROOF")
    canvas.drawRightString(PAGE_W - MARGIN_X, 0.31 * inch, str(doc.page))
    canvas.restoreState()


def book_translation(path):
    content = path.read_text()
    match = re.search(r"## Translation\s*\n(.*?)(?=\n## Decision log|\Z)", content, re.S)
    if not match:
        raise ValueError(f"{path} lacks a Translation section")
    lines = []
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line:
            continue
        # Extension headings and source-range labels are editorial metadata,
        # not interior verse. Keep the extraction safe if more sections are
        # added before the decision log.
        if line.startswith("## ") or line.startswith("**Source passage:"):
            continue
        line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
        lines.append(escape(line))
    return lines


def build(epic, title, out_name):
    paths = sorted((ROOT / "text" / epic).glob("book-*-opening.md"))
    if len(paths) != 24:
        raise ValueError(f"{epic}: expected 24 book drafts, found {len(paths)}")
    out = OUT_DIR / out_name
    story = [Spacer(1, 1.2 * inch), Paragraph("HOMER", styles["Sub"]),
             Paragraph(title.upper(), styles["VolumeTitle"]),
             Paragraph("Complete provisional interior architecture proof", styles["Sub"]),
             Spacer(1, 0.25 * inch),
             Paragraph("7 x 10 inch hardcover / 80# coated paper target", styles["Small"]),
             Spacer(1, 2.2 * inch),
             Paragraph("Translation status: first-pass draft; Greek-fidelity and editorial gates remain open.", styles["Small"]),
             PageBreak()]
    for index, path in enumerate(paths, 1):
        book_number = path.stem.split("-")[1]
        story.append(Paragraph(f"BOOK {int(book_number)}", styles["Book"]))
        story.append(Paragraph("First-pass working translation", styles["Sub"]))
        for line in book_translation(path):
            story.extend([Paragraph(line, styles["Verse"]), Spacer(1, 1.4)])
        story.append(Paragraph(f"Source range: Book {int(book_number)}. Full-book provisional draft. Not approved for final layout.", styles["Small"]))
        if index != len(paths):
            story.append(PageBreak())
    doc = BaseDocTemplate(str(out), pagesize=(PAGE_W, PAGE_H), leftMargin=MARGIN_X,
                          rightMargin=MARGIN_X, topMargin=MARGIN_Y, bottomMargin=0.7 * inch,
                          title=f"Homer: {title} provisional volume proof", author="CastaliaInstitute")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="body")
    doc.addPageTemplates([PageTemplate(id="volume", frames=frame, onPage=footer)])
    doc.build(story)
    print(out)


if __name__ == "__main__":
    build("iliad", "The Iliad", "inq-homer-iliad-volume-proof.pdf")
    build("odyssey", "The Odyssey", "inq-homer-odyssey-volume-proof.pdf")
