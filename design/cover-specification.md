# Hardcover cover specification

## Current production target

- Product: hardcover casewrap (Lulu is the provisional working target; vendor not finally selected)
- Trim: 6.625 × 10.25 inches (168.275 × 260.35 mm), standard US comic size
- Interior: 80# White Coated, Premium Color
- Cover: casewrap; current Lulu stock documentation lists an 80# gloss
  laminated white cover stock
- Material boundary: the requested 80# coated specification applies to the
  interior pages; casewrap cover stock and endsheet construction remain the
  printer's separate product specifications.
- Release state: architecture counts are recorded, but final printer templates
  and release exports are still pending

## Template authority

The final cover must be a one-page integrated spread containing back cover,
spine, and front cover. The authoritative template is the selected printer’s
custom template generated after each final interior PDF is uploaded; it supplies
the actual spine width for that page count and paper/binding selection. Lulu is
the current working target only and is not a final production lock.

Do not calculate a release spine from an estimate. Store the downloaded
template beside the final cover source and record its filename, download date,
page count, and template dimensions in the release manifest.

## Casewrap geometry controls

- Extend artwork through the complete template wrap area; the hardcover wrap
  is approximately 0.75 inch beyond the cover board area.
- Keep critical art and all text inside the template's book-cover area.
- Keep spine typography at least 0.125 inch clear of each spine edge to allow
  for manufacturing variance.
- Keep cover text and essential marks at least 0.75 inch inside the casewrap
  edge unless the downloaded template specifies a larger safe area.
- Keep the barcode in the template's designated area after ISBN assignment.
- Export as a single-page PDF with no trim or bleed marks, no password
  protection, embedded fonts or outlined type, and flattened transparency.

## Release record required for each volume

Current architecture counts are 350 pages for the Iliad and 177 pages for the
Odyssey. These counts are suitable for regenerating design studies, but they do
not replace the custom printer templates required for final spine calculation.

```text
interior_page_count: <locked count>
template_filename: <downloaded printer template>
template_downloaded: <YYYY-MM-DD>
spine_width_in: <template value>
cover_document_size_in: [<width>, <height>]
isbn: <assigned ISBN or pending>
cover_pdf: <one-page release PDF>
cover_preflight: <pending/pass/revise>
```

## Authority

This specification was checked against the current Lulu working target’s [casewrap guidance](https://help.lulu.com/en/support/solutions/articles/64000308572-creating-your-hardcover-casewrap-cover),
[custom-cover upload requirements](https://help.lulu.com/en/support/solutions/articles/64000282777-upload-your-cover-file),
[print-book workflow](https://help.lulu.com/en/support/solutions/articles/64000255486-how-to-create-a-print-book),
and [paper-stock documentation](https://help.lulu.com/en/support/solutions/articles/64000255473-cover-and-interior-paper-stocks)
on 2026-09-02. The printer documentation states that the custom template is
generated from the selected trim, binding, paper, and final page count; it also
recommends 80# White Coated with Premium Color for image-rich interiors.
