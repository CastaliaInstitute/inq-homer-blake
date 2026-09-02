# Translation workflow

The control ledger in `text/translation-status.csv` is the authoritative
status record for all forty-eight books.

## Book cycle

1. Map the Greek source range and scene outline; set status to `outline`.
2. Draft from the Greek copy text; record the working file and set `draft`.
3. Run the six review gates in `text/review-gates.md`; each column must be
   changed from `pending` only by a recorded reviewer.
4. Set `approved` only when all six gates pass and the decision log is current.
5. Set `laid-out`, `proofed`, and `final` only after the corresponding page-map,
   PDF, and physical-proof evidence exists.

The ledger intentionally reports the project honestly: Book 1 of each epic is
in draft, while the remaining books are mapped but not yet translated.
