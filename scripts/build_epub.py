#!/usr/bin/env python3
"""Build deterministic, private editorial-proof EPUBs for Homer's epics."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import tempfile
import uuid
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output" / "epub"
FIXED_TIME = (2026, 9, 3, 0, 0, 0)

VOLUMES = {
    "iliad": {"title": "The Iliad", "cover": ROOT / "assets/covers/epic/iliad/front-cover.jpg"},
    "odyssey": {"title": "The Odyssey", "cover": ROOT / "assets/covers/epic/odyssey/front-cover.jpg"},
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def document(title: str, body: str, body_class: str = "") -> str:
    return f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head><title>{esc(title)}</title><meta charset="utf-8"/><link rel="stylesheet" type="text/css" href="../css/book.css"/></head>
<body class="{body_class}">{body}</body></html>'''


def parse_export(path: Path) -> list[tuple[int, list[str]]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    books: list[tuple[int, list[str]]] = []
    current: list[str] | None = None
    number = 0
    for line in lines[2:]:
        match = re.fullmatch(r"BOOK (\d+)", line)
        if match:
            if current is not None:
                books.append((number, current))
            number = int(match.group(1))
            current = []
        elif current is not None and line.strip():
            current.append(line.strip())
    if current is not None:
        books.append((number, current))
    if [number for number, _ in books] != list(range(1, 25)):
        raise ValueError(f"{path} must contain Books 1–24 exactly once and in order")
    if any(not lines for _, lines in books):
        raise ValueError(f"{path} contains an empty book")
    return books


def package(title: str, identifier: str) -> str:
    items = "\n".join(
        f'<item id="book-{number:02}" href="text/book-{number:02}.xhtml" media-type="application/xhtml+xml"/>'
        for number in range(1, 25)
    )
    spine = "\n".join(f'<itemref idref="book-{number:02}"/>' for number in range(1, 25))
    return f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="pub-id">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="pub-id">urn:uuid:{identifier}</dc:identifier>
<dc:title>{esc(title)}</dc:title><dc:creator>Homer</dc:creator><dc:language>en</dc:language>
<dc:publisher>Castalia Institute</dc:publisher><dc:contributor>Translated by a.Longfellow</dc:contributor>
<dc:contributor>Illustrated by a.Blake</dc:contributor>
<dc:rights>Private editorial proof. Not approved for sale or public distribution.</dc:rights>
<meta property="dcterms:modified">2026-09-03T00:00:00Z</meta>
</metadata>
<manifest>
<item id="nav" href="text/nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
<item id="cover-page" href="text/cover.xhtml" media-type="application/xhtml+xml"/>
<item id="title-page" href="text/title.xhtml" media-type="application/xhtml+xml"/>
<item id="notice" href="text/notice.xhtml" media-type="application/xhtml+xml"/>
<item id="css" href="css/book.css" media-type="text/css"/>
<item id="font" href="fonts/CormorantGaramond-Regular.ttf" media-type="font/ttf"/>
<item id="cover-image" href="images/cover.jpg" media-type="image/jpeg" properties="cover-image"/>
{items}
</manifest>
<spine><itemref idref="cover-page"/><itemref idref="title-page"/><itemref idref="nav"/><itemref idref="notice"/>{spine}</spine>
</package>'''


def build(volume: str) -> dict:
    spec = VOLUMES[volume]
    source = ROOT / "output" / "text" / f"inq-homer-{volume}.txt"
    books = parse_export(source)
    source_bytes = source.read_bytes()
    cover_bytes = spec["cover"].read_bytes()
    font = ROOT / "assets/fonts/CormorantGaramond-Regular.ttf"
    identifier = str(uuid.uuid5(uuid.NAMESPACE_URL, sha256(source_bytes) + sha256(cover_bytes)))
    output = OUTPUT_DIR / f"inq-homer-{volume}-editorial-proof.epub"

    with tempfile.TemporaryDirectory(prefix=f"inq-homer-{volume}-epub-") as tmp:
        root = Path(tmp)
        oebps = root / "OEBPS"
        for directory in (root / "META-INF", oebps / "text", oebps / "css", oebps / "fonts", oebps / "images"):
            directory.mkdir(parents=True, exist_ok=True)
        (root / "mimetype").write_text("application/epub+zip", encoding="ascii")
        (root / "META-INF/container.xml").write_text('<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/package.opf" media-type="application/oebps-package+xml"/></rootfiles></container>', encoding="utf-8")
        shutil.copyfile(spec["cover"], oebps / "images/cover.jpg")
        shutil.copyfile(font, oebps / "fonts/CormorantGaramond-Regular.ttf")
        (oebps / "css/book.css").write_text("""@font-face{font-family:Cormorant;src:url('../fonts/CormorantGaramond-Regular.ttf')}body{font-family:Cormorant,Georgia,serif;line-height:1.42;margin:6%;color:#211713}p{margin:0 0 .34em}.verse{orphans:2;widows:2}.cover{margin:0;text-align:center}.cover img{display:block;width:100%;height:auto;max-height:100vh;object-fit:contain}.title{text-align:center;padding-top:18%}.title h1{font-size:2.8em;margin-bottom:.5em}.credit{letter-spacing:.06em}.notice{border:.08em solid #7d2d25;padding:1em;margin-top:18%;font-family:Georgia,serif}nav ol{list-style:none;padding:0}nav li{margin:.35em 0}h1{break-before:page;text-align:center}""", encoding="utf-8")
        (oebps / "text/cover.xhtml").write_text(document("Cover", '<img epub:type="cover" src="../images/cover.jpg" alt="Cover of ' + esc(spec["title"]) + '"/>', "cover"), encoding="utf-8")
        title_body = f'<p>iNQ EPIC</p><h1>{esc(spec["title"])}</h1><p class="credit">Homer</p><p class="credit">Translated by a.Longfellow</p><p class="credit">Illustrated by a.Blake</p><p>Editorial proof</p>'
        (oebps / "text/title.xhtml").write_text(document(spec["title"], title_body, "title"), encoding="utf-8")
        notice = '<h1>Editorial proof notice</h1><div class="notice"><p>This edition is a private working proof. It is not approved for sale or public distribution.</p><p>All twenty-four books remain under review. Independent Greek-fidelity, literary, meter, notes, art-direction, production, and physical-proof approvals remain open. Illustration plates are intentionally omitted until final art and rights are locked.</p></div>'
        (oebps / "text/notice.xhtml").write_text(document("Editorial proof notice", notice), encoding="utf-8")
        links = "".join(f'<li><a href="book-{number:02}.xhtml">Book {number}</a></li>' for number, _ in books)
        nav = f'<nav epub:type="toc" id="toc"><h1>Contents</h1><ol>{links}</ol></nav>'
        (oebps / "text/nav.xhtml").write_text(document("Contents", nav), encoding="utf-8")
        for number, lines in books:
            paragraphs = "".join(f'<p class="verse">{esc(line)}</p>' for line in lines)
            (oebps / f"text/book-{number:02}.xhtml").write_text(document(f"Book {number}", f'<h1>Book {number}</h1>{paragraphs}'), encoding="utf-8")
        (oebps / "package.opf").write_text(package(spec["title"], identifier), encoding="utf-8")

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output, "w") as archive:
            info = zipfile.ZipInfo("mimetype", FIXED_TIME)
            info.compress_type = zipfile.ZIP_STORED
            archive.writestr(info, b"application/epub+zip")
            for path in sorted(root.rglob("*")):
                if path.is_file() and path.name != "mimetype":
                    info = zipfile.ZipInfo(path.relative_to(root).as_posix(), FIXED_TIME)
                    info.compress_type = zipfile.ZIP_DEFLATED
                    archive.writestr(info, path.read_bytes(), compresslevel=9)

    epub_bytes = output.read_bytes()
    manifest = {
        "schemaVersion": 1,
        "title": spec["title"],
        "author": "Homer",
        "translator": "a.Longfellow",
        "illustrator": "a.Blake",
        "releaseClass": "private_editorial_proof",
        "saleApproved": False,
        "publicDistributionApproved": False,
        "books": 24,
        "illustrationPlates": 0,
        "illustrationStatus": "omitted_pending_final_art_and_rights",
        "source": source.relative_to(ROOT).as_posix(),
        "sourceSha256": sha256(source_bytes),
        "wordCount": sum(len(line.split()) for _, lines in books for line in lines),
        "identifier": identifier,
        "epub": output.name,
        "epubSha256": sha256(epub_bytes),
        "bytes": len(epub_bytes),
        "openEditorialGates": ["greek_fidelity", "literary", "meter", "notes_glossary", "art_direction", "production", "physical_proof"],
    }
    manifest_path = OUTPUT_DIR / f"inq-homer-{volume}-editorial-proof.manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--volume", choices=[*VOLUMES, "all"], default="all")
    args = parser.parse_args()
    selected = VOLUMES if args.volume == "all" else [args.volume]
    print(json.dumps([build(volume) for volume in selected], indent=2))


if __name__ == "__main__":
    main()
