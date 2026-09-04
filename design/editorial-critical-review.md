# Critical editorial review

**Audit date:** 2026-09-03
**Scope:** *The Iliad* and *The Odyssey*: text, credits, provenance, rights,
and production controls
**A+ target:** evidence-backed publication approval at 6.625 × 10.25 inches
(comic size); musical,
speakable Longfellow-inspired English governed by the Greek, not by padding

The cross-domain release control sheet is
[`design/release-readiness.md`](release-readiness.md).

## Editorial verdict

**Release decision: HOLD. Neither volume is A+ or release-approved.** Both
epics have all twenty-four books and contiguous source-span authorities, but
all 288 book-level gate cells remain pending and no independent human sign-off
is recorded. Odyssey Books 21–24 remain below the repository's conservative
reader-facing density floor. A build or validator pass must not override those
facts.

Source-range continuity is separate from reader-facing completeness. A revised
collation file can reach a Greek endpoint while its English remains materially
compressed. The Iliad is materially more developed as continuous verse; the
late Odyssey remains the principal completeness risk. All books remain
provisional until independent review and the approval gates are complete.

## A+ criterion grades

Grades measure distance from the stated A+ release standard, not relative
promise or successful compilation.

| Criterion | Grade | Evidence | Remaining release gate |
|---|:---:|---|---|
| Source/text completeness and fidelity | **C** | Pinned, hashed Greek copy texts and contiguous collation intervals cover all 48 books. The audit removed a duplicated *Iliad* 21.498–504, a wrong-book *Odyssey* 20 omen imported into Book 21, and a doubled Book 21 scar reveal. The density screen now holds *Odyssey* 21–24 at 4.66, 3.40, 3.41, and 4.18 English words per Greek line. | Independent line-by-line Greek comparison, adopted-reading record, and omissions/additions report for every book; faithful expansion of held books without invented padding. |
| Line/chapter/book structure | **B** | Both volumes contain Books 1–24 exactly once; source intervals are contiguous through canonical endpoints, and exports enforce book order. | Named structural inventory for every book and renewed duplicate/omission review after revisions. |
| Longfellow-for-the-ear musical English | **D+** | The heuristic 8–12-syllable band contains 7,444 of 12,712 Iliad lines (58.6%) and 5,802 of 8,354 Odyssey lines (69.5%), against the project's 85% aspiration; 7,820 lines remain logged as unreviewed outliers. A syllable band does not establish stress or beauty. | Human stress-by-stress and read-aloud review, revision of syntactic drag and prose lineation, and documented intentional exceptions. |
| Title/translator/illustrator credits | **B-** | Canonical title, Homer authorship, and Castalia Institute translation credit are now stated consistently in both front-matter plans and the release manifest. Illustration-free EPUB proofs no longer claim historical or supplemental illustrations. | Lock final plate selection, then apply creator-role-specific plate credits and final title-page language; no blanket Blake illustrator credit. |
| Original Blake plate provenance | **B-** | Two local Met scans have checksums, public-domain status, and role-accurate Flaxman-designer/Blake-or-Piroli-engraver records. Original supplements are explicitly not by Blake. | Select final historical plates, verify each final master and caption, and retain object-level provenance through production. |
| Comic-size production readiness | **C+** | Architecture proofs use 6.625 × 10.25 in (477 × 738 pt). BookVault candidates are a separate provisional route with exact 168 × 260 mm TrimBoxes and 174 × 266 mm bleed boxes. | Lock the authoritative printer route, page counts, profile, stock, binding, cover templates, spine widths, final exports, and physical proofs. |
| Rights accuracy | **C+** | The two historical scans record public-domain source status; generated concepts preserve an attribution boundary. | Final rights/license statements for every selected original plate and font, plus printer/distribution review. “Not by William Blake” is not itself a rights grant. |
| Repository validators | **B-** | Structural, source, density, meter, EPUB, provenance, and geometry checks are executable; a new multi-line duplication preflight guards the defect found in *Iliad* 21. The BookVault source-hash validator now fails correctly because manuscript revisions were not propagated into the PDFs during this no-generated-PDF pass. | Rebuild BookVault PDFs after text lock, rerun current-branch CI and final-art/final-PDF checks, and close all human gates. Automated green status is necessary but not sufficient. |

**Overall: C / release hold.** The principal blockers are independent Greek
fidelity, late-*Odyssey* completeness, oral prosody, final creator/rights
credits, a single comic-size production route, and physical proof approval.

## Defects corrected in this pass

- Removed the repeated Hermes–Leto passage from *Iliad* 21 at the 497/498
  source boundary while retaining it once under its correct 498–504 authority.
- Added an assembled-manuscript regression preflight for repeated four-line
  blocks.
- Removed a Book 20 Theoclymenus prophecy imported into *Odyssey* 21 and
  reduced its duplicated scar reveal to the single source event. This
  correctly returned Book 21 to the density hold.
- Corrected stale dashboard/checklist counts to the current four density
  holds, *Odyssey* Books 21–24.
- Established truthful shared credit rules and removed the blanket visual
  credit from illustration-free EPUB proof metadata.
- Marked both BookVault interiors stale after the manuscript corrections;
  their exact trim geometry remains evidence, but their text is no longer the
  current source authority.

## Required editorial sequence

1. Expand *Odyssey* 21–24 only from the pinned Greek and record restored source
   units; word count is a hold signal, never a license to add ornamental text.
2. Perform independent Greek-fidelity and omissions/additions review for all
   48 books, followed by a separate literary and oral-prosody pass.
3. Re-run meter, glossary, names, notes, duplication, and read-aloud review
   after every substantive revision. Promote no ledger row until a named
   reviewer signs all six gates.
4. Choose and document one exact 6.625 × 10.25 inch comic-size printer route.
   BookVault’s 168 × 260 mm files remain provisional alternatives. Rebuild final
   interiors, page maps, covers, and manifests only after text and art lock.
5. Complete rights, physical-proof, and final-production review before any
   sale or public-distribution approval.

## Current recommendation

Keep both volumes as private editorial prototypes. Do not distribute them as
final translations and do not mark either release-approved until the named
editorial, art, rights, printer, and physical-proof gates above are closed.
