# Translation workflow

The control ledger in `text/translation-status.csv` is the authoritative
status record for all forty-eight books.

## Book cycle

1. Map the Greek source range and scene outline; set status to `outline`.
2. Draft from the Greek copy text; record the working file and set `draft`.
   When the working verse is complete and its source-collated authority covers
   the canonical range, set `review`. This is a review queue, not an approval.
3. Run the six review gates in `text/review-gates.md`; each column must be
   changed from `pending` only by a recorded reviewer.
4. Set `approved` only when all six gates pass and the decision log is current.
5. Set `laid-out`, `proofed`, and `final` only after the corresponding page-map,
   PDF, and physical-proof evidence exists.

Before changing a book's status, run both `ruby scripts/preflight_translation.rb`
and `ruby scripts/preflight_review_packets.rb`.

The ledger intentionally reports the project honestly: all forty-eight books
have working translation files and source-collated authorities covering their
canonical ranges, and all forty-eight are now in `review` with the six review
gates pending. Source collation is evidence of coverage, not approval of the
prose.
