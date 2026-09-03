#!/usr/bin/env python3

from pathlib import Path
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, Image, NextPageTemplate, PageBreak, PageTemplate, Paragraph, Spacer

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/pdf/inq-homer-odyssey-book-1-proof.pdf"
FONT_DIR = Path("/System/Library/Fonts/Supplemental")
for name, filename in (("TimesNR", "Times New Roman.ttf"), ("TimesNRI", "Times New Roman Italic.ttf"), ("TimesNRB", "Times New Roman Bold.ttf")):
    pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / filename)))

PAGE_W, PAGE_H = 6.625 * inch, 10.25 * inch
MARGIN_X, MARGIN_Y = 0.72 * inch, 0.75 * inch
COLUMN_GUTTER = 0.24 * inch
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="ODTitle", fontName="TimesNRB", fontSize=25, leading=30, alignment=TA_CENTER, textColor="#1f1c18", spaceAfter=18))
styles.add(ParagraphStyle(name="ODSub", fontName="TimesNRI", fontSize=12, leading=16, alignment=TA_CENTER, textColor="#625b52", spaceAfter=12))
styles.add(ParagraphStyle(name="ODHead", fontName="TimesNRB", fontSize=18, leading=22, alignment=TA_LEFT, textColor="#1f1c18", spaceAfter=8))
styles.add(ParagraphStyle(name="ODVerse", fontName="TimesNR", fontSize=11.2, leading=16, alignment=TA_LEFT, textColor="#1f1c18", leftIndent=0.05 * inch))
styles.add(ParagraphStyle(name="ODCaption", fontName="TimesNR", fontSize=7.5, leading=10, alignment=TA_LEFT, textColor="#625b52", spaceBefore=6))
styles.add(ParagraphStyle(name="ODSmall", fontName="TimesNR", fontSize=8.5, leading=12, alignment=TA_LEFT, textColor="#3d3934"))

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
        flow.extend([Paragraph(line, styles["ODVerse"]), Spacer(1, 2.2)])
    return flow

OUT.parent.mkdir(parents=True, exist_ok=True)
doc = BaseDocTemplate(str(OUT), pagesize=(PAGE_W, PAGE_H), leftMargin=MARGIN_X, rightMargin=MARGIN_X, topMargin=MARGIN_Y, bottomMargin=0.7 * inch, title="Homer: Odyssey Book 1 Proof", author="CastaliaInstitute")
full_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="full")
column_width = (doc.width - COLUMN_GUTTER) / 2
left_frame = Frame(doc.leftMargin, doc.bottomMargin, column_width, doc.height, id="left-column")
right_frame = Frame(doc.leftMargin + column_width + COLUMN_GUTTER, doc.bottomMargin,
                    column_width, doc.height, id="right-column")
doc.addPageTemplates([
    PageTemplate(id="full", frames=full_frame, onPage=footer),
    PageTemplate(id="two-column", frames=[left_frame, right_frame], onPage=footer),
])

story = [Spacer(1, 1.3 * inch), Paragraph("HOMER", styles["ODSub"]), Paragraph("THE ODYSSEY", styles["ODTitle"]), Paragraph("Book 1 / Interior proof", styles["ODSub"]), Spacer(1, 0.25 * inch), Paragraph("A new translation in the formal spirit of Longfellow's Divine Comedy,<br/>with an original plate by CastaliaInstitute.", styles["ODSub"]), Spacer(1, 1.8 * inch), Paragraph("6.625 x 10.25 inch comic-size hardcover edition / 80# coated paper target", styles["ODSmall"]), NextPageTemplate("two-column"), PageBreak()]
story += [Paragraph("BOOK 1", styles["ODHead"]), Paragraph("The Man of Many Turnings", styles["ODSub"])]
story += verse(["Tell me of the man of many turnings, Muse,", "who wandered far, after he had brought down Troy's", "sacred citadel. Many were the people whose cities", "and minds he saw, and many the griefs he carried", "across the sea within his heart, struggling to save", "his life and bring his companions home. Yet he could", "not rescue them, though he desired it deeply:", "their own blind recklessness destroyed them,", "for they consumed the cattle of the Sun,", "and the god took from them the day of returning.", "Begin wherever you will, goddess born of Zeus;", "give us this story also. All the others now,", "who had escaped the steep destruction of the war,", "were home, beyond the battle and the sea. He alone,", "still longing for his wife and for the day of return,", "was held in hollow caves by the lady nymph,", "Calypso, shining among the deathless ones.", "But when the circling years had brought the hour", "the gods had spun for him to reach his home,", "to Ithaca, nor even there escape from toil", "among his friends, the gods took pity on him all,", "save Poseidon; he, unrelenting, nursed his wrath", "against godlike Odysseus, till he touched", "the land he loved.", "But Poseidon had gone to the distant Ethiopians,", "to share their hecatomb, at the earth's far edge;", "there the gods were gathered, and he among them.", "The father of gods and men began to speak,", "remembering Aegisthus, whom famed Orestes killed.", "‘Look how mortals blame the gods,’ he said, ‘and say", "their evils come from us. Yet they themselves, by folly,", "make sorrow beyond what fate has given them.", "So Aegisthus, against fate, took Agamemnon's wife", "and murdered him when he came home from Troy.", "He knew the god's warning, for Hermes had told him:", "do not kill the king, do not pursue his wife;", "the son of Atreus will be avenged by Orestes,", "when he comes to manhood and longs for his country.", "But Aegisthus would not listen. Now he has paid", "for all of it at once.", "Then the grey-eyed Athena answered him:", "‘Father Zeus, son of Cronus, highest of rulers,", "that man deserved the death that came upon him.", "Would that every man who acts as he did might perish!", "But my heart is troubled for the wise Odysseus,", "who has so long been kept from his friends and home,"])
story += [Spacer(1, 0.22 * inch), Paragraph("Working draft: Odyssey 1.1-50. Greek base text: A. T. Murray, The Odyssey (1919), Perseus CTS grc1. Not approved for final layout.", styles["ODCaption"]), NextPageTemplate("full"), PageBreak()]
story += [Image(str(ROOT / "assets/generated/odyssey/book-01-athena-v2.png"), width=5.58 * inch, height=7.90 * inch), Paragraph("Athena at the threshold of Odysseus's household. Original concept plate by CastaliaInstitute; informed by Blake's visionary line, not a specific Blake plate. 300 dpi placement candidate; print profile and final approval pending.", styles["ODCaption"]), NextPageTemplate("full"), PageBreak()]
story += [Paragraph("PROOF NOTES", styles["ODHead"]), Paragraph("This five-page proof tests the shared page architecture for the Odyssey volume: title page, two-column verse pages, full-page plate, and caption treatment. The plate is original work and is not credited to William Blake. Before production approval, lock the typeface licenses and print profile, expand the page map, and complete the six translation review gates.", styles["ODSmall"]), Spacer(1, 0.3 * inch), Paragraph("Preflight status", styles["ODHead"]), Paragraph("TEXT: draft / ART: concept-review / LAYOUT: sample proof / RELEASE: not ready", styles["ODSmall"])]
doc.build(story)
print(OUT)
