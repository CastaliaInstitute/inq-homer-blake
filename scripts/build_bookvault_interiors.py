#!/usr/bin/env python3
"""Build checksum-bound Homer prepress candidates for BookVault.

The PDFs use BookVault's 3 mm bleed convention: a 174 x 266 mm MediaBox
with an exact 168 x 260 mm TrimBox. They remain release-ineligible until the
translation, illustration, typography, and physical-proof gates are signed.
"""

from __future__ import annotations

import csv
import fcntl
import hashlib
import json
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
)

from translation_extract import book_translation


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf"
TMP = ROOT / "tmp" / "pdfs" / "homer-bookvault"
TRIM_MM = (168, 260)
BLEED_MM = 3
PAGE = ((TRIM_MM[0] + 2 * BLEED_MM) * mm, (TRIM_MM[1] + 2 * BLEED_MM) * mm)
TRIM_BOX = (BLEED_MM * mm, BLEED_MM * mm, PAGE[0] - BLEED_MM * mm, PAGE[1] - BLEED_MM * mm)
FONT_DIR = ROOT / "assets" / "fonts"
MARGIN_X = (BLEED_MM + 15) * mm
MARGIN_TOP = (BLEED_MM + 16) * mm
MARGIN_BOTTOM = (BLEED_MM + 15) * mm
COLUMN_GUTTER = 6 * mm

for name, filename in {
    "Cormorant": "CormorantGaramond-Regular.ttf",
    "CormorantI": "CormorantGaramond-Italic.ttf",
    "CormorantB": "CormorantGaramond-SemiBold.ttf",
}.items():
    pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / filename)))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


class ProductionCanvas(Canvas):
    def __init__(self, *args, **kwargs):
        kwargs["invariant"] = 1
        if not kwargs.get("initialFontName"):
            kwargs["initialFontName"] = "Cormorant"
        super().__init__(*args, **kwargs)

    def showPage(self):
        self.setTrimBox(TRIM_BOX)
        self.setBleedBox((0, 0, PAGE[0], PAGE[1]))
        super().showPage()


class PageMarker(Flowable):
    def __init__(self):
        super().__init__()
        self.page = 0

    def wrap(self, _width, _height):
        return 0, 0

    def draw(self):
        self.page = self.canv.getPageNumber()


class FullPagePlate(Flowable):
    def __init__(self, path: Path):
        super().__init__()
        self.path = path
        self.page = 0

    def wrap(self, width, height):
        return width, height

    def drawOn(self, canvas, _x, _y, _sW=0):
        self.page = canvas.getPageNumber()
        canvas.drawImage(str(self.path), 0, 0, width=PAGE[0], height=PAGE[1])


STYLES = {
    "title": ParagraphStyle("title", fontName="CormorantB", fontSize=28, leading=32, alignment=TA_CENTER, textColor=colors.HexColor("#211d18"), spaceAfter=12),
    "subtitle": ParagraphStyle("subtitle", fontName="CormorantI", fontSize=12, leading=16, alignment=TA_CENTER, textColor=colors.HexColor("#4d463e"), spaceAfter=8),
    "credit": ParagraphStyle("credit", fontName="Cormorant", fontSize=9, leading=12, alignment=TA_CENTER, textColor=colors.HexColor("#4d463e"), spaceAfter=3),
    "book": ParagraphStyle("book", fontName="CormorantB", fontSize=19, leading=23, alignment=TA_CENTER, textColor=colors.HexColor("#211d18"), spaceAfter=4),
    "booksub": ParagraphStyle("booksub", fontName="CormorantI", fontSize=9.2, leading=11, alignment=TA_CENTER, textColor=colors.HexColor("#61594f"), spaceAfter=12),
    "front": ParagraphStyle("front", fontName="Cormorant", fontSize=10.2, leading=14, alignment=TA_LEFT, textColor=colors.HexColor("#211d18"), spaceAfter=8),
    "verse": ParagraphStyle("verse", fontName="Cormorant", fontSize=9.35, leading=11.25, alignment=TA_LEFT, textColor=colors.HexColor("#211d18"), spaceAfter=0),
}


def footer(title: str):
    def draw(canvas: Canvas, doc: BaseDocTemplate):
        canvas.saveState()
        canvas.setStrokeColorRGB(0.72, 0.69, 0.64)
        canvas.setLineWidth(0.3)
        canvas.line(MARGIN_X, (BLEED_MM + 9.5) * mm, PAGE[0] - MARGIN_X, (BLEED_MM + 9.5) * mm)
        canvas.setFont("Cormorant", 7.1)
        canvas.setFillColorRGB(0.34, 0.31, 0.27)
        canvas.drawString(MARGIN_X, (BLEED_MM + 6.3) * mm, title.upper())
        canvas.drawCentredString(PAGE[0] / 2, (BLEED_MM + 6.3) * mm, "Longfellow-inspired translation / Castalia Institute")
        canvas.drawRightString(PAGE[0] - MARGIN_X, (BLEED_MM + 6.3) * mm, str(doc.page))
        canvas.restoreState()

    return draw


def forward_blocks(path: Path) -> list[str]:
    blocks = []
    for block in path.read_text(encoding="utf-8").split("\n\n"):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if lines and not lines[0].startswith(("# ", "*")):
            blocks.append(" ".join(line.lstrip("# ").strip() for line in lines))
    return blocks


def build(slug: str, title: str, book_subtitle: str, pad_final_blank: bool = False) -> tuple[Path, dict]:
    selections = csv_rows(ROOT / "design" / f"{slug}-plate-selection.csv")
    if len(selections) != 24 or [int(row["book"]) for row in selections] != list(range(1, 25)):
        raise ValueError(f"{slug}: expected one ordered plate selection for Books 1-24")
    if any(row["approval_status"] != "pending" for row in selections):
        raise ValueError(f"{slug}: this candidate builder expects pending illustration approvals")

    paths = [ROOT / "text" / slug / f"book-{book:02d}-opening.md" for book in range(1, 25)]
    if not all(path.is_file() for path in paths):
        raise FileNotFoundError(f"{slug}: missing authoritative book translation")

    title_marker = PageMarker()
    story = [
        title_marker,
        Spacer(1, 58 * mm),
        Paragraph(title, STYLES["title"]),
        Paragraph("Homer", STYLES["subtitle"]),
        Spacer(1, 11 * mm),
        Paragraph("A Longfellow-inspired translation by Castalia Institute", STYLES["credit"]),
        Paragraph("Historical Blake material and original Castalia Institute supplements", STYLES["credit"]),
        Paragraph("iNQ Epic - 168 x 260 mm edition", STYLES["credit"]),
        PageBreak(),
        Paragraph("FORWARD", STYLES["book"]),
    ]
    for block in forward_blocks(ROOT / "volumes" / slug / "forward.md"):
        story.append(Paragraph(escape(block), STYLES["front"]))

    book_records = []
    for book, (path, selection) in enumerate(zip(paths, selections), 1):
        plate = ROOT / "assets" / "print" / "illustrations" / slug / f"book-{book:02d}-full-bleed.jpg"
        if not plate.is_file():
            raise FileNotFoundError(plate)
        plate_flowable = FullPagePlate(plate)
        text_marker = PageMarker()
        story.extend([
            NextPageTemplate("plate"),
            PageBreak(),
            plate_flowable,
            NextPageTemplate("text"),
            PageBreak(),
            text_marker,
            Paragraph(f"BOOK {book}", STYLES["book"]),
            Paragraph(book_subtitle if book == 1 else f"Book {book}", STYLES["booksub"]),
        ])
        for line in book_translation(path):
            story.extend([Paragraph(line, STYLES["verse"]), Spacer(1, 1.1)])
        book_records.append({
            "book": book,
            "source": path.relative_to(ROOT).as_posix(),
            "sourceSha256": digest(path),
            "plateId": selection["plate_id"],
            "plateApproval": selection["approval_status"],
            "productionAsset": plate.relative_to(ROOT).as_posix(),
            "productionSha256": digest(plate),
            "productionPixels": [2055, 3142],
            "productionPpi": 300,
            "plateFlowable": plate_flowable,
            "textMarker": text_marker,
        })

    if pad_final_blank:
        story.extend([NextPageTemplate("blank"), PageBreak(), Spacer(1, 1)])

    out = OUT / f"inq-homer-{slug}-bookvault-interior.pdf"
    working = TMP / f"{slug}-interior.building.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    working.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(working), pagesize=PAGE,
        leftMargin=MARGIN_X, rightMargin=MARGIN_X,
        topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOTTOM,
        title=title, author="Castalia Institute",
        subject="iNQ Epic BookVault prepress candidate; release approval pending",
    )
    safe_width = PAGE[0] - 2 * MARGIN_X
    column_width = (safe_width - COLUMN_GUTTER) / 2
    front = Frame(MARGIN_X, MARGIN_BOTTOM, safe_width, PAGE[1] - MARGIN_TOP - MARGIN_BOTTOM, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="front")
    plate = Frame(0, 0, PAGE[0], PAGE[1], leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="plate")
    left = Frame(MARGIN_X, MARGIN_BOTTOM, column_width, PAGE[1] - MARGIN_TOP - MARGIN_BOTTOM, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="left")
    right = Frame(MARGIN_X + column_width + COLUMN_GUTTER, MARGIN_BOTTOM, column_width, PAGE[1] - MARGIN_TOP - MARGIN_BOTTOM, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="right")
    doc.addPageTemplates([
        PageTemplate(id="front", frames=front),
        PageTemplate(id="plate", frames=plate),
        PageTemplate(id="text", frames=[left, right], onPage=footer(title)),
        PageTemplate(id="blank", frames=plate),
    ])
    doc.build(story, canvasmaker=ProductionCanvas)

    page_count = int(subprocess.check_output(["pdfinfo", str(working)], text=True).split("Pages:", 1)[1].splitlines()[0].strip())
    if page_count % 2:
        if pad_final_blank:
            raise ValueError(f"{slug}: final blank-page padding did not produce an even page count")
        return build(slug, title, book_subtitle, pad_final_blank=True)
    working.replace(out)
    for index, record in enumerate(book_records):
        record["platePage"] = record.pop("plateFlowable").page
        record["textStartPage"] = record.pop("textMarker").page
        next_plate = book_records[index + 1]["plateFlowable"].page if index + 1 < len(book_records) else page_count + 1
        record["textEndPage"] = next_plate - 1

    return out, {
        "title": title,
        "pdf": out.relative_to(ROOT).as_posix(),
        "pdfSha256": digest(out),
        "pageCount": page_count,
        "trimMm": list(TRIM_MM),
        "documentMm": [174, 266],
        "bleedMm": BLEED_MM,
        "plateCount": 24,
        "colourPages": [record["platePage"] for record in book_records],
        "books": book_records,
        "releaseEligible": False,
        "releaseBlockers": ["translation-signoff", "illustration-signoff", "font-license-lock", "physical-proof"],
    }


def main() -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    with (TMP / "build.lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        iliad_pdf, iliad = build("iliad", "The Iliad", "The Anger of Achilles")
        odyssey_pdf, odyssey = build("odyssey", "The Odyssey", "The Man of Many Turnings")
        manifest = {
            "schemaVersion": 1,
            "format": "BookVault prepress candidate",
            "trimMm": list(TRIM_MM),
            "documentMm": [174, 266],
            "bleedMm": BLEED_MM,
            "historicalScansIncluded": False,
            "releaseEligible": False,
            "volumes": {"iliad": iliad, "odyssey": odyssey},
        }
        manifest_path = OUT / "inq-homer-bookvault-interiors.manifest.json"
        manifest_tmp = TMP / "manifest.building.json"
        manifest_tmp.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        manifest_tmp.replace(manifest_path)
        print(iliad_pdf)
        print(odyssey_pdf)
        print(manifest_path)


if __name__ == "__main__":
    main()
