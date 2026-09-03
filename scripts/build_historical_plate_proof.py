#!/usr/bin/env python3

from pathlib import Path
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, Image, PageBreak, PageTemplate, Paragraph, Spacer

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/pdf/inq-homer-historical-plate-proof.pdf"
FONT_DIR = Path("/System/Library/Fonts/Supplemental")
for name, filename in (("TimesNR", "Times New Roman.ttf"), ("TimesNRI", "Times New Roman Italic.ttf"), ("TimesNRB", "Times New Roman Bold.ttf")):
    pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / filename)))

W, H = 6.625 * inch, 10.25 * inch
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="HTitle", fontName="TimesNRB", fontSize=23, leading=28, alignment=TA_CENTER, textColor="#1f1c18"))
styles.add(ParagraphStyle(name="HSub", fontName="TimesNRI", fontSize=11, leading=15, alignment=TA_CENTER, textColor="#625b52"))
styles.add(ParagraphStyle(name="HHead", fontName="TimesNRB", fontSize=16, leading=20, alignment=TA_LEFT, textColor="#1f1c18", spaceAfter=8))
styles.add(ParagraphStyle(name="HCaption", fontName="TimesNR", fontSize=8, leading=11, alignment=TA_LEFT, textColor="#3d3934"))

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColorRGB(0.72, 0.69, 0.64)
    canvas.line(0.72 * inch, 0.48 * inch, W - 0.72 * inch, 0.48 * inch)
    canvas.setFont("TimesNR", 7.5)
    canvas.setFillColorRGB(0.39, 0.36, 0.32)
    canvas.drawString(0.72 * inch, 0.31 * inch, "HOMER / HISTORICAL PLATE PROOF")
    canvas.drawRightString(W - 0.72 * inch, 0.31 * inch, str(doc.page))
    canvas.restoreState()

doc = BaseDocTemplate(str(OUT), pagesize=(W, H), leftMargin=0.72 * inch, rightMargin=0.72 * inch, topMargin=0.7 * inch, bottomMargin=0.7 * inch, title="Homer Historical Plate Proof", author="CastaliaInstitute")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="body")
doc.addPageTemplates([PageTemplate(id="proof", frames=frame, onPage=footer)])

story = [Spacer(1, 1.7 * inch), Paragraph("HISTORICAL PLATES", styles["HTitle"]), Spacer(1, 0.2 * inch), Paragraph("Homer / Flaxman / Blake and Piroli", styles["HSub"]), Spacer(1, 0.35 * inch), Paragraph("A source-treatment proof for the two-volume 6.625 x 10.25 inch comic-size hardcover edition. These are historical scans, not new illustrations and not compositions by William Blake.", styles["HSub"]), PageBreak()]

plates = [
    ("assets/source/iliad/met-337355-dp-14470-001.jpg", "Plate 2: Minerva Repressing the Fury of Achilles", "John Flaxman, designer; William Blake, engraver; 1805 historical plate. Metropolitan Museum of Art, object 1970.565.63; scan DP-14470-001.") ,
    ("assets/source/iliad/met-337355-dp-15151-001.jpg", "Plate 31: Thetis Bringing the Armour to Achilles", "John Flaxman, designer; Tommaso Piroli, engraver; 1805 historical plate. Metropolitan Museum of Art, object 1970.565.63; scan DP-15151-001. Blake is not credited for this plate."),
]
for i, (path, title, caption) in enumerate(plates):
    story += [Paragraph(title, styles["HHead"]), Image(str(ROOT / path), width=5.55 * inch, height=3.65 * inch), Spacer(1, 0.15 * inch), Paragraph(caption, styles["HCaption"]), Spacer(1, 0.25 * inch), Paragraph("Source type: blake-original connection / historical reference. Rights: public domain status recorded in the source manifest; retain the museum record and scan URL with any derivative.", styles["HCaption"])]
    if i < len(plates) - 1:
        story.append(PageBreak())

doc.build(story)
print(OUT)
