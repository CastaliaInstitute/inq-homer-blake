#!/usr/bin/env python3

"""Build deterministic, provisional whole-volume architecture proofs.

The source Markdown remains authoritative. This builder includes only each
book's Translation section; editorial decision logs remain outside the
interior proof until line-level review is complete.
"""

from pathlib import Path
import csv
import re
import sys
from xml.sax.saxutils import escape

from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import inch
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, Image, NextPageTemplate, PageBreak, PageTemplate, Paragraph, Spacer

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "output/pdf"
FONT_DIR = ROOT / "assets" / "fonts"
PLATE_MANIFEST = ROOT / "design/plate-manifest.csv"

for name, filename in {
    "Cormorant": "CormorantGaramond-Regular.ttf",
    "CormorantI": "CormorantGaramond-Italic.ttf",
    "CormorantB": "CormorantGaramond-SemiBold.ttf",
}.items():
    pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / filename)))

PAGE_W, PAGE_H = 7 * inch, 10 * inch
MARGIN_X, MARGIN_Y = 0.72 * inch, 0.75 * inch
COLUMN_GUTTER = 0.24 * inch

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="VolumeTitle", fontName="CormorantB", fontSize=27, leading=31,
                          alignment=TA_CENTER, textColor="#1f1c18", spaceAfter=18))
styles.add(ParagraphStyle(name="Sub", fontName="CormorantI", fontSize=11, leading=15,
                          alignment=TA_CENTER, textColor="#625b52", spaceAfter=12))
styles.add(ParagraphStyle(name="Book", fontName="CormorantB", fontSize=19, leading=23,
                          alignment=TA_LEFT, textColor="#1f1c18", spaceAfter=14))
styles.add(ParagraphStyle(name="Verse", fontName="Cormorant", fontSize=11.2, leading=14.6,
                          alignment=TA_LEFT, textColor="#1f1c18", leftIndent=0.05 * inch))
styles.add(ParagraphStyle(name="Small", fontName="Cormorant", fontSize=8.7, leading=11.8,
                          alignment=TA_LEFT, textColor="#3d3934"))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColorRGB(0.72, 0.69, 0.64)
    canvas.setLineWidth(0.35)
    canvas.line(MARGIN_X, 0.48 * inch, PAGE_W - MARGIN_X, 0.48 * inch)
    canvas.setFont("Cormorant", 7.5)
    canvas.setFillColorRGB(0.39, 0.36, 0.32)
    canvas.drawString(MARGIN_X, 0.31 * inch, "HOMER / iNQ HOMER BLAKE / PROVISIONAL VOLUME PROOF")
    canvas.drawRightString(PAGE_W - MARGIN_X, 0.31 * inch, str(doc.page))
    canvas.restoreState()


def book_translation(path):
    content = path.read_text()
    # Some volume-facing files intentionally retain a compact synopsis while
    # their complete, source-collated translation is kept in one or more
    # authority files. Use those authorities for the assembled proof, but only
    # when the opening explicitly identifies itself as compact and the
    # authority has the required revised-translation section.
    if "compact translation" in content.lower():
        authorities = []
        for candidate in sorted(path.parent.glob(f"{path.stem.replace('-opening', '')}-collation-*.md")):
            authority = candidate.read_text(encoding="utf-8")
            if "## Revised translation pass" in authority:
                range_match = re.search(r"collation-(\d+)-(\d+)\.md$", candidate.name)
                if range_match:
                    authorities.append((int(range_match.group(1)), int(range_match.group(2)), authority))
        source_range = re.search(r"Source passage:.*?Book \d+, lines\s+1\D+(\d+)", content, re.S)
        authorities.sort(key=lambda item: item[0])
        covers_book = bool(source_range and authorities and authorities[0][0] == 1)
        if covers_book:
            expected_end = int(source_range.group(1))
            cursor = 1
            for start, end, _ in authorities:
                if start != cursor:
                    covers_book = False
                    break
                cursor = end + 1
            covers_book = covers_book and cursor - 1 == expected_end
        if covers_book:
            bodies = []
            for _, _, authority in authorities:
                match = re.search(r"^## Revised translation pass\s*\n(.*?)(?=^## Decision|\Z)", authority, re.S | re.M)
                if match:
                    bodies.append(match.group(1).strip())
            if len(bodies) == len(authorities):
                content = "## Translation\n" + "\n\n".join(bodies)
    translation_lines = []
    active_section = False
    for raw_line in content.splitlines():
        heading = re.match(r"^##\s+(.+?)\s*$", raw_line)
        if heading:
            active_section = heading.group(1).startswith(("Translation", "Extension"))
            continue
        if active_section:
            translation_lines.append(raw_line)
    if not translation_lines:
        raise ValueError(f"{path} lacks a Translation section")
    lines = []
    skip_metadata_block = False
    for raw_line in translation_lines:
        line = raw_line.strip()
        if not line:
            skip_metadata_block = False
            continue
        # Extension headings and source-range labels are editorial metadata,
        # not interior verse. Keep the extraction safe if more sections are
        # added before the decision log.
        if line.startswith("#") or line.startswith(("**Source passage:", "**Continuation:", "**Book ")):
            skip_metadata_block = True
            continue
        if skip_metadata_block:
            continue
        line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
        lines.append(escape(line))
    return lines


def forward_block(path):
    paragraphs = []
    for block in path.read_text(encoding="utf-8").split("\n\n"):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines or lines[0].startswith("# ") or lines[0].startswith("*"):
            continue
        paragraphs.append(escape(" ".join(line.lstrip('# ').strip() for line in lines)))
    return paragraphs


def plate_for(epic, book_number):
    with PLATE_MANIFEST.open(newline="", encoding="utf-8") as handle:
        records = list(csv.DictReader(handle))
    candidates = [
        record for record in records
        if record["epic"].lower() == epic.lower()
        and int(record["book"]) == int(book_number)
        and record["curation_status"] in {"concept-review", "source-review"}
    ]
    # Prefer a new, manifest-listed concept over a historical reference when
    # both exist for a book; all inserted plates remain visibly provisional.
    candidates.sort(key=lambda record: (record["source_type"] != "generated", record["final_file"]))
    return candidates[0] if candidates else None


def plate_block(record):
    asset = ROOT / record["final_file"]
    if not asset.is_file():
        raise ValueError(f"plate manifest asset is missing: {record['final_file']}")
    width = float(record["width_px"])
    height = float(record["height_px"])
    max_width = PAGE_W - 2 * MARGIN_X
    max_height = PAGE_H - MARGIN_Y - 1.15 * inch
    scale = min(max_width / width, max_height / height)
    image = Image(str(asset), width=width * scale, height=height * scale)
    caption = escape(record["caption"])
    credit = escape(record["credit_line"])
    return [
        NextPageTemplate("full"),
        PageBreak(),
        image,
        Spacer(1, 0.12 * inch),
        Paragraph(f"PLATE — {caption}", styles["Small"]),
        Paragraph(f"{credit} Concept-review placement only.", styles["Small"]),
        NextPageTemplate("two-column"),
        PageBreak(),
    ]


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
             PageBreak(), Paragraph("FORWARD", styles["Book"])]
    for paragraph in forward_block(ROOT / "volumes" / epic / "forward.md"):
        story.extend([Paragraph(paragraph, styles["Verse"]), Spacer(1, 8)])
    story.append(PageBreak())
    for index, path in enumerate(paths, 1):
        book_number = path.stem.split("-")[1]
        story.append(Paragraph(f"BOOK {int(book_number)}", styles["Book"]))
        story.append(Paragraph("First-pass working translation", styles["Sub"]))
        for line in book_translation(path):
            story.extend([Paragraph(line, styles["Verse"]), Spacer(1, 1.4)])
        story.append(Paragraph(f"Source range: Book {int(book_number)}. Full-book provisional draft. Not approved for final layout.", styles["Small"]))
        record = plate_for(epic, int(book_number))
        if record:
            story.extend(plate_block(record))
        if index != len(paths):
            story.append(PageBreak())
    doc = BaseDocTemplate(str(out), pagesize=(PAGE_W, PAGE_H), leftMargin=MARGIN_X,
                          rightMargin=MARGIN_X, topMargin=MARGIN_Y, bottomMargin=0.7 * inch,
                          title=f"Homer: {title} provisional volume proof", author="CastaliaInstitute")
    full_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="full")
    column_width = (doc.width - COLUMN_GUTTER) / 2
    left_frame = Frame(doc.leftMargin, doc.bottomMargin, column_width, doc.height, id="left-column")
    right_frame = Frame(doc.leftMargin + column_width + COLUMN_GUTTER, doc.bottomMargin,
                        column_width, doc.height, id="right-column")
    doc.addPageTemplates([
        PageTemplate(id="full", frames=full_frame, onPage=footer),
        PageTemplate(id="two-column", frames=[left_frame, right_frame], onPage=footer),
    ])
    # Front matter remains full width; the translated books use the requested
    # two-column interior architecture.
    story.insert(0, NextPageTemplate("full"))
    # The final front-matter PageBreak is the first one after FORWARD.
    for position, flowable in enumerate(story):
        if isinstance(flowable, Paragraph) and getattr(flowable, "text", "") == "BOOK 1":
            story.insert(position, NextPageTemplate("two-column"))
            break
    doc.build(story)
    print(out)


if __name__ == "__main__":
    build("iliad", "The Iliad", "inq-homer-iliad-volume-proof.pdf")
    build("odyssey", "The Odyssey", "inq-homer-odyssey-volume-proof.pdf")
