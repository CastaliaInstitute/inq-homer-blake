# Image provenance audit

**Audit date:** 2026-09-02  
**Enforcement:** `ruby scripts/preflight_provenance.rb`

## Historical plates

The two acquired scans derive from The Metropolitan Museum of Art record for
*The Iliad of Homer Engraved From the Compositions of John Flaxman, R.A.,
Sculptor*, object `1970.565.63`, published 1805. The museum identifies John
Flaxman as designer, William Blake, Tommaso Piroli, and James Parker as
engravers, and marks the object **Public Domain**. The repository therefore
credits Flaxman as designer and names the engraver for each selected plate; it
does not describe either scan as a Blake composition.

| Local master | Met image identifier | Object record | Local SHA-256 | Dimensions / profile |
|---|---|---|---|---|
| `assets/source/iliad/met-337355-dp-14470-001.jpg` | `DP-14470-001.jpg` | [Met 337355](https://www.metmuseum.org/art/collection/search/337355) | `975fbdacbcc620c8b990635ee668c7c98b1e3caa208747326e6cbd29164bce6e` | 3621 × 2342 px, 300 dpi, sRGB |
| `assets/source/iliad/met-337355-dp-15151-001.jpg` | `DP-15151-001.jpg` | [Met 337355](https://www.metmuseum.org/art/collection/search/337355) | `2352006448d93bd52c770ea1200481c9d620f7e8652c815fb75f77591c8d28e3` | 3590 × 2404 px, 300 dpi, sRGB |

The source manifest retains the direct Met image URLs, object number, access
date, title, plate title, and credit line. Any crop or tonal derivative must
retain the source master and acquire its own checksum and manifest row.

## Original supplements

The Apollo, Athena, and Patroclus/Eurypylus plates are CastaliaInstitute
concept candidates. They are original generated work, not William Blake works
and not transformations of a specific Blake plate. Each record retains its
prompt file, date, dimensions, curation status, and explicit credit. The v2
Apollo/Athena candidates are 2100 × 3000 px (approximately 300 dpi at 7 × 10
inches); the new Iliad Book 11 candidate is 1050 × 1498 px and is preview
resolution. All remain `concept-review` until a print master, color profile,
and human art-direction approval are recorded.

| Candidate | Local SHA-256 | Status |
|---|---|---|
| `assets/generated/iliad/book-01-apollo-v2.png` | `0205d034e2685de2ee11a7645877512e8b4d36f13b0b1d050a72823f6919594e` | concept-review |
| `assets/generated/odyssey/book-01-athena-v2.png` | `0e749d23c2cf47856cb4a70cf99dc5c34ed8849e0712de23eb48e4e50d040490` | concept-review |
| `assets/generated/iliad/book-11-patroclus-eurypylus-v1.png` | `18978c055749ffdec4876f76d6591a573d69f655ccc8e684da062c5181c14da3` | concept-review |

Run `shasum -a 256` against the local files after any asset replacement and
update this dossier together with the relevant manifest record. The automated
preflight checks the attribution and file relationships; it does not convert
a concept candidate into a final print master.
