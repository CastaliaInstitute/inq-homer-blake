# Translation workflow

The control ledger in `text/translation-status.csv` is the authoritative
status record for all forty-eight books.

## Book cycle

1. Map the Greek source range and scene outline; set status to `outline`.
2. Draft from the Greek copy text; record the working file and set `draft`.
   A source-collated authority may be recorded alongside the compact production
   opening, but this does not advance the review status.
3. Run the six review gates in `text/review-gates.md`; each column must be
   changed from `pending` only by a recorded reviewer.
4. Set `approved` only when all six gates pass and the decision log is current.
5. Set `laid-out`, `proofed`, and `final` only after the corresponding page-map,
   PDF, and physical-proof evidence exists.

The ledger intentionally reports the project honestly: all forty-eight books
have working translation files and source-collated authorities covering their
canonical ranges, but every book remains `draft` with the six review gates
pending. Source collation is evidence of coverage, not approval of the prose.
