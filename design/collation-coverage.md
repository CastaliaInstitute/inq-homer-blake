# Source-collation coverage audit

**Audit date:** 2026-09-02  
**Source authority:** pinned Perseus Greek editions recorded in
[`text/source-lock.md`](../text/source-lock.md)  
**Scope:** Iliad Books 1–24 and Odyssey Books 1–24

The repository contains source-collated authority files whose filename
intervals cover every canonical line range in `text/source-coverage.csv`:

| Volume | Books | Coverage result | Review state |
|---|---:|---|---|
| *Iliad* | 24 | 1.1 through 24.804 covered; interval audit passed | Books 1–2 and 19–24 are `review`; Books 3–18 are `draft`; gates pending |
| *Odyssey* | 24 | 1.1 through 24.548 covered; interval audit passed | Books 1–2 and 19–24 are `review`; Books 3–18 are `draft`; gates pending |

The audit checks filename intervals for gaps against the canonical final-line
field. It does not certify that every English sentence is final, metrical, or
approved. Reviewers must still record Greek-fidelity, narrative, verse, diction,
notes, and production decisions in `text/translation-status.csv` before any
book can advance beyond `draft`.

## Reproduce the interval audit

```sh
python3 - <<'PY'
from pathlib import Path
import csv, re

for row in csv.DictReader(open("text/source-coverage.csv")):
    volume, book = row["volume"], int(row["book"])
    end, cursor = int(row["canonical_greek_last_line"]), 1
    intervals = []
    for path in Path(f"text/{volume}").glob(f"book-{book:02d}-collation-*.md"):
        match = re.search(r"collation-(\d+)-(\d+)\.md$", path.name)
        if match:
            intervals.append((int(match.group(1)), int(match.group(2))))
    for start, stop in sorted(intervals):
        assert start <= cursor, (volume, book, cursor, start)
        cursor = max(cursor, stop + 1)
    assert cursor == end + 1, (volume, book, cursor, end)
print("full-range gaps: none")
PY
```
