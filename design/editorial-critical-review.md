# Critical editorial review

**Audit date:** 2026-09-03  
**Scope:** translation beauty, Greek fidelity, source coverage, and proof assembly  
**Format under review:** two volumes, comic trim 6.625 × 10.25 in, two columns

## Editorial verdict

The project has a promising Longfellow-derived voice: five-stress lineation,
ceremonial syntax, recurrent epithet-work, and a readable public cadence. The
Iliad draft is substantially closer to a continuous poetic translation than the
Odyssey draft. Neither volume is publication-ready, because the six review gates
remain pending for all 48 books and no independent human sign-off is recorded.

The most important issue is not cosmetic. Several Odyssey books are explicitly
described as “compact translation” or “first-pass literary draft,” and their
source-collated authorities are compressed narrative prose rather than a
line-complete poetic translation. This is valid editorial scaffolding, but it
must not be presented as the finished Longfellow-style translation.

## Evidence and severity

| Area | Evidence | Assessment |
|---|---|---|
| Voice / beauty | Longfellow-like five-stress cadence and elevated diction are visible throughout the Iliad and early Odyssey books. | Promising; requires sustained line edit for monotony, abstraction, and occasional modern phrasing. |
| Greek fidelity | Book-level review logs identify and correct concrete errors, including duplicated passages, altered counts, agency, spatial sense, and omitted objects. | Improving; independent omissions/additions review remains open. |
| Odyssey completeness | `scripts/translation_extract.py` correctly assembles marked collation files, but Books 19–22 extract only 14, 18, 87, and 15 reading lines respectively. Books 13–24 are labeled compact or first-pass in their manuscript headers. | **Release blocker.** Replace compressed passes with complete verse before approval. |
| Review governance | `text/translation-status.csv` keeps all 288 gate cells pending; no book is approved for layout. | Correctly conservative; retain these holds. |
| Production | PDF and layout preflights pass at 477 × 738 pt with two columns; current proofs are structurally valid. | Production-ready as sample proofs only, not as final books. |

## Required editorial sequence

1. Expand the compressed Odyssey authorities into complete poetic translations
   against the pinned Greek source, preserving the source-range boundaries.
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
do not distribute them as a complete translation until the Odyssey compression
blocker and the remaining human review gates are cleared.
