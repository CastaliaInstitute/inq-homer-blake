#!/usr/bin/env python3

from pathlib import Path

from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import inch
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/pdf/inq-homer-book-1-proof.pdf"
FONT_DIR = Path("/System/Library/Fonts/Supplemental")

pdfmetrics.registerFont(TTFont("TimesNR", str(FONT_DIR / "Times New Roman.ttf")))
pdfmetrics.registerFont(TTFont("TimesNRI", str(FONT_DIR / "Times New Roman Italic.ttf")))
pdfmetrics.registerFont(TTFont("TimesNRB", str(FONT_DIR / "Times New Roman Bold.ttf")))

PAGE_W, PAGE_H = 6.625 * inch, 10.25 * inch
MARGIN_X, MARGIN_Y = 0.72 * inch, 0.75 * inch
COLUMN_GUTTER = 0.24 * inch

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="ProofTitle", fontName="TimesNRB", fontSize=25, leading=30,
    alignment=TA_CENTER, textColor="#1f1c18", spaceAfter=18,
))
styles.add(ParagraphStyle(
    name="ProofSub", fontName="TimesNRI", fontSize=12, leading=16,
    alignment=TA_CENTER, textColor="#625b52", spaceAfter=12,
))
styles.add(ParagraphStyle(
    name="BookHead", fontName="TimesNRB", fontSize=18, leading=22,
    alignment=TA_LEFT, textColor="#1f1c18", spaceAfter=8,
))
styles.add(ParagraphStyle(
    name="Verse", fontName="TimesNR", fontSize=11.2, leading=16,
    alignment=TA_LEFT, textColor="#1f1c18", leftIndent=0.05 * inch,
    spaceAfter=0,
))
styles.add(ParagraphStyle(
    name="Caption", fontName="TimesNR", fontSize=7.5, leading=10,
    alignment=TA_LEFT, textColor="#625b52", spaceBefore=6,
))
styles.add(ParagraphStyle(
    name="Small", fontName="TimesNR", fontSize=8.5, leading=12,
    alignment=TA_LEFT, textColor="#3d3934",
))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColorRGB(0.72, 0.69, 0.64)
    canvas.setLineWidth(0.35)
    canvas.line(MARGIN_X, 0.48 * inch, PAGE_W - MARGIN_X, 0.48 * inch)
    canvas.setFont("TimesNR", 7.5)
    canvas.setFillColorRGB(0.39, 0.36, 0.32)
    canvas.drawString(MARGIN_X, 0.31 * inch, "HOMER / iNQ HOMER BLAKE / BOOK 1 PROOF")
    canvas.drawRightString(PAGE_W - MARGIN_X, 0.31 * inch, str(doc.page))
    canvas.restoreState()


def verse(lines):
    flow = []
    for line in lines:
        flow.extend([Paragraph(line, styles["Verse"]), Spacer(1, 2.2)])
    return flow


OUT.parent.mkdir(parents=True, exist_ok=True)
doc = BaseDocTemplate(
    str(OUT), pagesize=(PAGE_W, PAGE_H), leftMargin=MARGIN_X,
    rightMargin=MARGIN_X, topMargin=MARGIN_Y, bottomMargin=0.7 * inch,
    title="Homer: Iliad Book 1 Proof", author="CastaliaInstitute",
)
full_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="full")
column_width = (doc.width - COLUMN_GUTTER) / 2
left_frame = Frame(doc.leftMargin, doc.bottomMargin, column_width, doc.height, id="left-column")
right_frame = Frame(doc.leftMargin + column_width + COLUMN_GUTTER, doc.bottomMargin,
                    column_width, doc.height, id="right-column")
doc.addPageTemplates([
    PageTemplate(id="full", frames=full_frame, onPage=footer),
    PageTemplate(id="two-column", frames=[left_frame, right_frame], onPage=footer),
])

story = []
story += [Spacer(1, 1.3 * inch), Paragraph("HOMER", styles["ProofSub"]),
          Paragraph("THE ILIAD", styles["ProofTitle"]),
          Paragraph("Book 1 / Interior proof", styles["ProofSub"]),
          Spacer(1, 0.25 * inch),
          Paragraph("A new translation in the formal spirit of Longfellow's Divine Comedy,\n"
                    "with an original plate by CastaliaInstitute.", styles["ProofSub"]),
          Spacer(1, 1.8 * inch),
          Paragraph("6.625 x 10.25 inch comic-size hardcover edition / 80# coated paper target", styles["Small"]),
          NextPageTemplate("two-column"), PageBreak()]

story += [Paragraph("BOOK 1", styles["BookHead"]),
          Paragraph("The Anger of Achilles", styles["ProofSub"])]
story += verse([
    "Sing, goddess, of the anger of Peleus' son Achilles,",
    "that brought uncounted grief upon the Achaeans,",
    "and cast the steadfast lives of many heroes",
    "before their time into the house of Hades,",
    "leaving their bodies for the dogs and birds to tear -",
    "so the will of Zeus was brought toward its fulfillment -",
    "from that first hour when Agamemnon, king of men,",
    "and godlike Achilles broke apart in strife.",
    "Which of the deathless powers drove them together",
    "to quarrel? The son of Leto and Zeus:",
    "Apollo. For the king had angered him,",
    "and through the army a deadly sickness moved;",
    "the people fell, because Atreus' son had dishonored",
    "the priest Chryses, when he came before the ships.",
])
story += [Spacer(1, 0.22 * inch), Paragraph(
    "Working draft: Iliad 1.1-16. Greek base text: Monro and Allen, Homeri Opera. "
    "Not approved for final layout.", styles["Caption"]),
          NextPageTemplate("full"), PageBreak()]

image_path = ROOT / "assets/generated/iliad/book-01-apollo-v2.png"
story += [Image(str(image_path), width=5.55 * inch, height=7.92 * inch),
          Paragraph("Apollo descending upon the Achaean camp. Original concept plate by "
                    "CastaliaInstitute; informed by Blake's visionary line but not by "
                    "a specific Blake plate. Concept-review only; not final print resolution.",
                    styles["Caption"]), NextPageTemplate("full"), PageBreak()]

story += [Paragraph("PROOF NOTES", styles["BookHead"]),
          Paragraph("This four-page proof tests the shared page architecture: title page, "
                    "verse page, full-page plate, and caption treatment. The plate is "
                    "deliberately marked as original work and is not credited to William "
                    "Blake. Before production approval, lock the typeface licenses, expand "
                    "the page map, lock the print profile, and complete the "
                    "six translation review gates.", styles["Small"]),
          Spacer(1, 0.3 * inch),
          Paragraph("Preflight status", styles["BookHead"]),
          Paragraph("TEXT: draft / ART: concept-review / LAYOUT: sample proof / RELEASE: not ready",
                    styles["Small"])]

doc.build(story)
print(OUT)
