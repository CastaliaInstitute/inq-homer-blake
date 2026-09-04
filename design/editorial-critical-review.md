# A+ critical editorial audit

**Audit date:** 2026-09-04

**Scope:** *The Iliad* and *The Odyssey* manuscripts and publication artifacts

**A+ standard:** evidence-backed fidelity and completeness; intact 24-book
structure; musical, speakable Longfellow-inspired English without padding;
truthful credits and provenance; exact comic-size production; valid EPUB/PDF;
rights, accessibility, metadata, and reproducible-build evidence.

## Verdict

**HOLD — neither volume meets A+ release standard.** Both have complete
book-level source coverage, but source-range continuity is not proof of a
complete or faithful translation. All 288 human review gates are pending,
the narrow density passes require independent scrutiny, and neither cover is
printer-approved. No successful validator or PDF build overrides these holds.

## Criterion grades

| Criterion | Grade | Finding | Gate to A+ |
|---|:---:|---|---|
| Text completeness and fidelity | C+ | 48/48 books have contiguous pinned-Greek source authority. Forty-seven clear the conservative density screen; *Odyssey* Book 23 is an honest 4.78-word/source-line compression hold after removal of an unsupported duplicate bed passage. These are triage results, not proof of literary completeness. | Independent line-level omissions/additions and adopted-reading records for every book; expand or formally waive Book 23 before promotion, without padding. |
| Book/line structure | B | Books 1–24 occur once and in order in both manuscripts and exports; duplicate regression screen passes. | Human structural inventory against every Greek book and a renewed post-lock duplicate/omission pass. |
| Oral, musical English | D+ | Heuristic 8–12-syllable band: *Iliad* 58.7% (7,472/12,733); *Odyssey* 70.2% (6,052/8,626). 7,835 outliers are unreviewed; syllable count does not test stress or beauty. | Named stress/read-aloud review, revision of syntactic drag and prose lineation, documented intentional exceptions. |
| Credits | C- | The corrected provisional PDF cover proofs name Homer, Castalia Institute as translator, and Castalia Institute as cover-art creator; the legacy raster covers still falsely say “Translated by A.Longfellow” and “Illustrated by A.Blake.” | Retire legacy rasters, adapt corrected covers to exact printer templates, and verify title/author/translator/cover-artist/plate-role credits in every final format. |
| Plate provenance | C+ | Historical records distinguish Flaxman design from Blake/Piroli engraving; original candidates are now credited to CastaliaInstitute and explicitly not to Blake. | Final selection, exact passage/caption, creator/system, rights grant, native master, checksum, and printed credit for all 48 plates. |
| Comic-size production | C | Primary architecture proofs use exact 477 × 738 pt comic pages. Alternate BookVault candidates validate exact 168 × 260 mm trim, 24 full-page plates, and embedded fonts. | Lock vendor route, output intent, stock/binding, page counts, exact cover templates/spines, final exports, and physical proof. |
| EPUB/accessibility | B- | Private proofs are reflowable, semantically headed, navigable, illustration-free, and fail closed for sale/public distribution; builder records source/translator roles and accessibility metadata. | Clean authoritative EPUBCheck and assistive-technology spot check after final cover/text lock. |
| Rights accuracy | C | Historical scans record public-domain source status; “not by William Blake” protects attribution but is not a license for original work. | Rights/license evidence for every selected original plate, cover, font, and distribution territory. |
| Reproducible validation | B- | Source, structure, duplicate, density, art, EPUB-internal, and PDF geometry checks exist and fail closed on stale hashes. | Current-branch CI; EPUBCheck; final profile/overprint/trim checks; two clean deterministic builds after lock. |

**Overall grade: C / HOLD.** See
[`release-readiness.md`](release-readiness.md) for exact remaining gates and
artifact-level status.

## Safe corrections made in this audit

- Established standard US comic trim as the primary production target;
  relabeled 168 × 260 mm files as alternate BookVault prepress studies.
- Corrected print-manifest authorship from an ambiguous Blake shorthand to
  `CastaliaInstitute` and
  added a validator guard against future blanket Blake attribution.
- Removed unsafe raster cover studies from the EPUB build path and added
  explicit translator-role, source-edition, accessibility, and fail-closed
  cover-status metadata.
- Corrected future interior and cover builders to use truthful Castalia
  Institute translator/art credits and exact trim; the primary architecture
  builder preserves two-column source-line lineation. PDF and image assets were not
  altered by this audit.

The edition remains a private editorial prototype. Do not publish, sell, or
mark either volume release-approved.
