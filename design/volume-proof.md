# Two-volume architecture proofs

`scripts/build_volume_proof.py` assembles the current 24-book working drafts
into deterministic interior architecture proofs:

```sh
python3 scripts/build_volume_proof.py
```

The builder requires exactly twenty-four `book-*-opening.md` files per epic,
extracts only each file's `## Translation` section, and begins every book on a
new page with a consistent book opener. Decision logs and editorial notes are
excluded from the interior text. The resulting PDFs are trimmed to 7 × 10
inches (504 × 720 points) and carry a visible `PROVISIONAL VOLUME PROOF`
footer.

These files demonstrate pagination, hierarchy, margins, running folios, and
book-to-book continuity. They are not release interiors: the translation
drafts remain provisional, typography and printer profiles are not locked,
image placement is not yet integrated, and cover-spread dimensions depend on
the final page counts.

The current proof page counts are recorded in
`design/release-manifest.yaml`. After rebuilding, run
`python3 scripts/preflight_pdfs.py` and render the PDFs with `pdftoppm` for
visual inspection before treating the counts as current.
