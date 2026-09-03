# Translation review dashboard

**Audit date:** 2026-09-02  
**Authoritative ledger:** [`text/translation-status.csv`](../text/translation-status.csv)  
**Review policy:** [`text/review-gates.md`](../text/review-gates.md)

## Current state

| Measure | Result |
|---|---:|
| Iliad books in review | 24 |
| Odyssey books in review | 24 |
| Books with all six gates passed | 0 |
| Books approved for layout | 0 |
| Pending gate records | 288 |
| Book-level review packets started | 48 |

All 48 books have complete working verse and contiguous source-collation
coverage. `review` means the verse is ready for line-level editorial review; it
does not mean that the translation has been approved or that it is ready for
layout or print.

## Evidence required before approval

The current repository does not yet contain complete approval records for any
book. Iliad Book 1 has a first review packet at
[`text/reviews/iliad-book-01.md`](../text/reviews/iliad-book-01.md), but its
gates remain pending. Odyssey Book 1 has the matching packet at
[`text/reviews/odyssey-book-01.md`](../text/reviews/odyssey-book-01.md); its
gates also remain pending.
Book 2 packets are now present for both epics, and their gates remain pending.
Book 3 packets are now present for both epics, and their gates remain pending.
Book 4 packets are now present for both epics, and their gates remain pending.
Book 5 packets are now present for both epics, and their gates remain pending.
Book 6 packets are now present for both epics, and their gates remain pending.
Book 7 packets are now present for both epics, and their gates remain pending.
Book 8 packets are now present for both epics, and their gates remain pending.
Book 9 packets are now present for both epics, and their gates remain pending.
Book 10 packets are now present for both epics, and their gates remain pending.
Book 11 packets are now present for both epics, and their gates remain pending.
Book 12 packets are now present for both epics, and their gates remain pending.
Book 13 packets are now present for both epics, and their gates remain pending.
Book 14 packets are now present for both epics, and their gates remain pending.
Book 15 packets are now present for both epics, and their gates remain pending.
Book 16 packets are now present for both epics, and their gates remain pending.
Book 17 packets are now present for both epics, and their gates remain pending.
Book 18 packets are now present for both epics, and their gates remain pending.
Book 19 packets are now present for both epics, and their gates remain pending.
Book 20 packets are now present for both epics, and their gates remain pending.
Book 21 packets are now present for both epics, and their gates remain pending.
Book 22 packets are now present for both epics, and their gates remain pending.
Book 23 packets are now present for both epics, and their gates remain pending.
Book 24 packets are now present for both epics, and their gates remain pending.

- Greek-fidelity source map and omissions/additions report;
- structural narrative inventory;
- meter report demonstrating the project threshold of naturally five-stress
  lines, with intentional outliers logged;
- read-aloud revision notes;

The current [meter screening report](../text/meter-report.md) is a
machine-assisted syllable screen only; it does not satisfy the Verse gate until
stress, outliers, and read-aloud revisions are reviewed by a named editor.
- glossary, epithet, and proper-name concordance check;
- named reviewer, date, and signed decision for each of the six gates.

The absence is intentional and is reflected in every ledger gate column. The
next editorial pass must create these records from the pinned Greek sources,
then change individual gate cells only when a named reviewer has recorded the
result. No book may move to `approved`, `laid-out`, `proofed`, or `final` on the
basis of source coverage alone.

## Automated safeguards

- `scripts/preflight_translation.rb` requires every `review` or later book to
  have contiguous source-collation intervals through its canonical final line;
  it also requires six passing gates and a named, dated, approved packet before
  any later status.
- `scripts/preflight_source_lock.rb` verifies the pinned Greek editions and
  hashes.
- `scripts/preflight_pdfs.py` verifies geometry, fonts, and documented proof
  page counts, but does not certify editorial approval.
