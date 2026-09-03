#!/usr/bin/env python3

"""Build a page-by-page traceability map for the current volume proofs.

This is deliberately an architecture map, not a final production map. It uses
the rendered PDF text and current manifests to account for every page without
promoting provisional translation or concept art to release status.
"""

from pathlib import Path
import csv
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "design" / "architecture-page-map.csv"
BOOK_STARTS = ROOT / "design" / "volume-proof-book-starts.csv"


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def pages(pdf):
    result = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True,
                            text=True, check=True)
    return result.stdout.split("\f")[:-1]


def clean_page(text):
    return " ".join(line.strip() for line in text.splitlines()
                    if line.strip() and not line.strip().startswith("HOMER / iNQ"))


def candidate_key(record):
    filename = Path(record["final_file"]).stem.lower()
    version_rank = 0 if re.search(r"-v\d+$", filename) and not filename.endswith("-v1") else 1
    return (record["source_type"] != "generated", version_rank, record["final_file"])


def main():
    statuses = read_csv(ROOT / "text" / "translation-status.csv")
    ranges = {(row["volume"].lower(), int(row["book"])): row["source_range"] for row in statuses}
    plates = read_csv(ROOT / "design" / "plate-manifest.csv")
    rows = []
    for epic in ("iliad", "odyssey"):
        pdf = ROOT / "output" / "pdf" / f"inq-homer-{epic}-volume-proof.pdf"
        current_book = None
        for number, text in enumerate(pages(pdf), 1):
            compact = clean_page(text)
            book_match = re.search(r"\bBOOK\s+(\d+)\b", compact)
            if book_match:
                current_book = int(book_match.group(1))
            if number == 1:
                page_type, book, source_range, text_file = "title", "", "", ""
                image_file, caption_id = "", ""
            elif "FORWARD" in compact[:80]:
                page_type, book, source_range = "forward", "", ""
                text_file, image_file, caption_id = f"volumes/{epic}/forward.md", "", ""
            elif "PLATE —" in compact:
                page_type = "plate"
                book = current_book or ""
                caption = compact.split("PLATE —", 1)[1].split(" Concept-review", 1)[0].strip()
                candidates = [p for p in plates if p["epic"].lower() == epic and int(p["book"]) == book]
                candidates.sort(key=candidate_key)
                record = next((p for p in candidates if p["caption"] in caption or caption in p["caption"]), None)
                source_range = record["passage"] if record else ""
                text_file = ""
                image_file = record["final_file"] if record else ""
                caption_id = record["plate_id"] if record else ""
            elif current_book:
                page_type, book = "book-opener" if book_match else "verse", current_book
                source_range = ranges[(epic, current_book)]
                text_file = f"text/{epic}/book-{current_book:02d}-opening.md"
                image_file, caption_id = "", ""
            else:
                page_type, book, source_range = "unclassified", "", ""
                text_file, image_file, caption_id = "", "", ""
            rows.append({
                "volume": f"{epic}-volume-proof",
                "page_number": number,
                "page_type": page_type,
                "epic": epic.title(),
                "book": book,
                "source_range": source_range,
                "text_file": text_file,
                "image_file": image_file,
                "caption_id": caption_id,
                "proof_status": "verified-architecture",
                "notes": "Derived from current comic-size provisional volume proof; final pagination and art selection remain open.",
            })
    fields = ["volume", "page_number", "page_type", "epic", "book", "source_range", "text_file",
              "image_file", "caption_id", "proof_status", "notes"]
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    start_fields = ["volume", "page_number", "page_type", "epic", "book", "source_range",
                    "text_file", "proof_status", "notes"]
    with BOOK_STARTS.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=start_fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows({field: row[field] for field in start_fields}
                         for row in rows if row["page_type"] == "book-opener")
    print(f"Wrote {OUT} ({len(rows)} pages)")


if __name__ == "__main__":
    main()
