# Image provenance audit

**Audit date:** 2026-09-03
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

The generated manifest contains CastaliaInstitute concept candidates for the
Apollo, Athena, dream, assembly, storm, Helen, Pylos hospitality, Patroclus,
Cyclops, Priam, Odysseus-and-Telemachus, father-and-son, Penelope, and
Ithaca-return subjects.
They are original generated work, not William Blake works and not
transformations of a specific Blake plate. Each record retains its prompt file,
date, dimensions, curation status, and explicit credit. The v2 Apollo/Athena
candidates are 2100 × 3000 px (approximately 300 dpi at comic-size trim
inches). Placement derivatives for several earlier candidates are enlargements
for layout review rather than native print masters. All remain
`concept-review` until a print master, color profile, and human art-direction
approval are recorded.

| Candidate | Local SHA-256 | Status |
|---|---|---|
| `assets/generated/iliad/book-01-apollo-v2.png` | `0205d034e2685de2ee11a7645877512e8b4d36f13b0b1d050a72823f6919594e` | concept-review |
| `assets/generated/odyssey/book-01-athena-v2.png` | `0e749d23c2cf47856cb4a70cf99dc5c34ed8849e0712de23eb48e4e50d040490` | concept-review |
| `assets/generated/iliad/book-11-patroclus-eurypylus-v1.png` | `18978c055749ffdec4876f76d6591a573d69f655ccc8e684da062c5181c14da3` | concept-review |
| `assets/generated/odyssey/book-09-polyphemus-escape-v1.png` | `6830d7c703ccdd54ba6faf33c0a9abc73a34cfbaacc0295de82c53108cf853ea` | concept-review |
| `assets/generated/odyssey/book-05-raft-v2.png` | `f3cfb4639ea76b6cb8fb805b3b9ebba8eb2cd9fd2084d96e38d786b2daf71da2` | concept-review |
| `assets/generated/iliad/book-24-priam-achilles-v1.png` | `086edfbd4669873fa76ccd567b8728ef326eaa5a4db095a9d9766672205ef85a` | concept-review |
| `assets/generated/iliad/book-24-priam-achilles-v2.png` | `6b4959925b21a9d87f47a983c546464a120384c915e4616b9fee8f814aae41d2` | concept-review |
| `assets/generated/odyssey/book-22-hall-v1.png` | `9beb4be8ed49e579185bca7cd0b6d1fc7f5969bcf52147a09ae4a275fe24334c` | concept-review |
| `assets/generated/iliad/book-16-patroclus-v2.png` | `9ea4fe09507f1fe67ce442081f4bba1e6fd3d3d21da106d2bf0bb20e3440cc7b` | concept-review |
| `assets/generated/iliad/book-11-patroclus-eurypylus-v2.png` | `3a2a0f735b6fc7d5e7a321b3a8a4af0db9a8662092131bb73c87bc8a78d111a1` | concept-review |
| `assets/generated/odyssey/book-23-penelope-bed-v1.png` | `f4882bfe27ebb315333a3a8fe2d643e43fe4a95261692480fcd28ed8634231fa` | concept-review |
| `assets/generated/odyssey/book-16-father-son-v1.png` | `41b5cbc3d6198a221302faf228aef57c04a761c753ec75601139d6d20c01fc05` | concept-review |
| `assets/generated/odyssey/book-13-return-v1.png` | `4f2fe7749e848c354c7783876d56a2b333dcdd1557c78fbc41e4a30c3a1371ba` | concept-review |
| `assets/generated/odyssey/book-03-pylos-v1.png` | `a3db94f87366acb0791ff97b6d55809e80b3c7bdc9b28948350cfe74cbbf5cd5` | concept-review |

Run `shasum -a 256` against the local files after any asset replacement and
update this dossier together with the relevant manifest record. The automated
preflight checks the attribution and file relationships; it does not convert
a concept candidate into a final print master.
