# Human editorial review protocol

**Edition:** Castalia Institute / Homer two-volume comic-size hardcover
**Scope:** 48 books, six gates per book, 288 gate records
**Status:** control procedure; no gate is approved by this document

This protocol defines the evidence required to move a book from `review` to
`approved`. AI-assisted collation, read-aloud notes, and machine screens are
preparation evidence only. They may identify questions and proposed changes;
they do not satisfy independent approval.

## Independence rule

The Greek-fidelity reviewer must compare the English against the pinned Greek
copy text and record omissions, additions, speaker changes, disputed readings,
and unresolved questions. The literary reviewer may be the same person only if
the release record explicitly declares that dual role; the production reviewer
must remain a separate check of the final rendered pages. A reviewer must not
approve a gate from a summary alone: the source passage, working text, and
relevant derivative must be inspected.

## Required gate evidence

| Gate | Reviewer must inspect | Record must contain |
|---|---|---|
| Greek fidelity | pinned Greek span and English line by line | adopted readings, omissions/additions, names, objects, speaker boundaries, unresolved variants |
| Narrative | complete book and scene sequence | scene inventory, causal transitions, temporal order, point-of-view or divine-intervention changes |
| Verse | complete text aloud in the comic-size two-column measure | stress notes, breath/page-turn issues, intentional outliers, accepted revisions |
| Diction | book plus cross-book glossary/concordance | proper names, epithets, repeated formulas, register, anachronism checks |
| Notes | notes, glossary, citations, and source links | claim-level citations, scope, uncertainty labels, and removal of unsupported glosses |
| Production | locked text rendered in the target architecture | page count, line wrapping, folios, captions, plate placement, font/image checks, and dated proof result |

## Signoff record

Each gate entry in `text/translation-status.csv` must be backed by a dated
record containing:

```text
book: Iliad or Odyssey Book N
gate: greek_fidelity | narrative | verse | diction | notes | production
decision: pass | revise | hold
reviewer: full name or approved editorial identity
review_date: YYYY-MM-DD
source_authority: pinned source identifier and relevant line span
evidence_files: paths to the review packet, source comparison, and derivative
findings: concise list of adopted changes and remaining questions
independent_of_ai_assistance: true | false
```

`pass` is permitted only when `independent_of_ai_assistance: true` and the
evidence files are present. A `revise` or `hold` decision must remain visible;
it must not be converted into a pass by rebuilding derivatives. When a source
correction is made, rebuild all affected exports and record the new source
hashes before the reviewer repeats the gate.

## Release-level checks

Before either volume is labeled approved, the release editor must verify that:

1. all 288 gate entries pass and each has a named reviewer and date;
2. all meter outliers have a human decision or a documented intentionality;
3. every selected plate has a locked passage, caption, creator role, rights
   record, native master, checksum, and physical-proof result;
4. the final comic-size two-column PDFs and covers are regenerated from the
   approved text and printer template; and
5. the reproducibility, EPUBCheck, PDF, accessibility, and physical-proof
   records refer to those same locked inputs.

The procedure is deliberately fail-closed: a complete source map or a green
automated build cannot substitute for named independent editorial judgment.
