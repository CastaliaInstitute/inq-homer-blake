# Print preflight checklist

- [ ] Final trim, bleed, binding, and spine width confirmed against the
      current printer specification.
- [ ] Interior pages use the approved 6.625 × 10.25 inch comic-size grid and safe margins.
- [ ] Full-bleed pages extend 0.125 inch beyond every trimmed edge.
- [ ] Images are high resolution, embedded, and converted to the approved
      print color profile.
- [ ] Every historical and generated plate has a manifest record and caption.
- [x] All 48 illustration placeholder slots have unique source-ranged prompts,
      checked by `scripts/preflight_illustration_placeholders.rb`.
- [ ] Manifest records identify source type, provenance, rights, file, credit,
      and review status.
- [ ] `scripts/validate_manifests.sh` and `scripts/preflight_assets.rb` pass.
- [ ] Front matter, book divisions, page numbers, and contents are complete.
- [ ] The page map accounts for every text page, plate, caption, and blank page.
- [ ] Typefaces, licenses, color profile, margins, and folio rules are locked
      in the release manifest.
- [ ] Interior and cover PDFs open without missing fonts or transparency
  warnings.
- [x] Development PDFs are checked for comic-size geometry and encryption by
      `scripts/preflight_pdfs.py`; release PDFs additionally require embedded fonts.
- [x] Representative two-column pages are checked by
      `scripts/preflight_layout.py`.
- [x] All 48 book-level read-aloud review records are present and explicitly
      non-final, checked by `scripts/preflight_read_aloud.rb`.
- [x] Provisional accessible exports are checked by
      `scripts/preflight_text_exports.py`.
- [ ] A rendered proof has been reviewed at 100% and on paper.
- [ ] Literary, art-historical, attribution, and production sign-offs are
      recorded before release.

The current tracked proof in `output/pdf/` is an architecture sample only;
its status must remain separate from final volume deliverables.
