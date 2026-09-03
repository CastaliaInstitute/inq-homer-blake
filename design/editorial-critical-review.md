# Critical editorial review

**Audit date:** 2026-09-03  
**Scope:** translation beauty, Greek fidelity, source coverage, and proof assembly  
**Format under review:** two volumes, comic trim 6.625 × 10.25 in, two columns

The cross-domain release control sheet is [`design/release-readiness.md`](release-readiness.md).

## Editorial verdict

The project has a promising Longfellow-derived voice: five-stress lineation,
ceremonial syntax, recurrent epithet-work, and a readable public cadence. The
Iliad draft is substantially closer to a continuous poetic translation than the
Odyssey draft. Neither volume is publication-ready, because the six review gates
remain pending for all 48 books and no independent human sign-off is recorded.

The most important issue is not cosmetic. Source-range continuity is now
separated from reader-facing completeness: the density screen records books
whose English remains materially compressed even when a revised collation file
reaches the Greek endpoint. All books remain provisional until expansion,
independent review, and the approval gates are complete. Complete collation
authority must not be mistaken for an approved or finished Longfellow-style
translation.

## Evidence and severity

| Area | Evidence | Assessment |
|---|---|---|
| Voice / beauty | Longfellow-like five-stress cadence and elevated diction are visible throughout the Iliad and early Odyssey books. | Promising; requires sustained line edit for monotony, abstraction, and occasional modern phrasing. |
| Greek fidelity | Book-level review logs identify and correct concrete errors, including duplicated passages, altered counts, agency, spatial sense, and omitted objects. | Improving; independent omissions/additions review remains open. |
| Translation completeness | `scripts/preflight_translation_completeness.rb` verifies source-endpoint coverage; `design/translation-density-report.md` separately identifies materially compressed reader-facing books. | **Provisional hold;** expansion and independent fidelity/literary review remain open. |
| Review governance | `text/translation-status.csv` keeps all 288 gate cells pending; no book is approved for layout. | Correctly conservative; retain these holds. |
| Production | PDF and layout preflights pass at 477 × 738 pt with two columns; current proofs are structurally valid. | Production-ready as sample proofs only, not as final books. |

## Required editorial sequence

1. Keep all 48 complete working translations under independent Greek-fidelity
   and literary review, preserving the pinned source-range boundaries.
2. Perform independent Greek-fidelity and omissions/additions review, then a
   separate Longfellow/beauty pass. The latter should test cadence aloud, image
   precision, syntactic dignity, and avoidance of accidental imitation.
3. Re-run meter, glossary, names, notes, and read-aloud review after every
   substantive expansion. Do not promote a book in the ledger until a named
   reviewer signs all six gates.
4. Rebuild both comic-size proofs and update the page map, cover spine widths,
   and release manifest only after the final text is stable.

## Current recommendation

Keep the repository and comic-size proof pipeline active as an editorial
prototype. Label the PDFs and any reader-facing description as working proofs;
do not distribute them as a final translation until independent review,
production locks, and the remaining human approval gates are cleared.
