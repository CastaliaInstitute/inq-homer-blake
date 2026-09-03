# Casewrap cover design proofs

The cover proof builder creates one-page, left-to-right back/spine/front
design studies using the current art direction and embedded licensed fonts:

```sh
python3 scripts/build_cover_proof.py \
  --volume iliad --pages 350 \
  --output output/pdf/inq-homer-iliad-cover-design-proof.pdf
python3 scripts/build_cover_proof.py \
  --volume odyssey --pages 150 \
  --output output/pdf/inq-homer-odyssey-cover-design-proof.pdf
```

These are design proofs, not uploadable Lulu covers. They use a clearly marked
placeholder spine solely to test art direction, hierarchy, panel relationships,
and casewrap safety. The spine title is intentionally omitted. Once the
interior is final, download Lulu's custom template for the exact page count,
paper, binding, and trim, then replace the proof geometry and record the
template filename, dimensions, download date, and spine width in
`design/release-manifest.yaml`.

The proof pairs each volume's original CastaliaInstitute concept plate with a
historical Flaxman/engraver scan on the reverse panel. The distinction is
documented in [the provenance audit](provenance-audit.md); the cover treatment
does not present either original concept as a William Blake work.
