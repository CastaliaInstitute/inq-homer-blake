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

The generated manifest contains CastaliaInstitute concept candidates for the
Apollo, Athena, dream, assembly, storm, Helen, Patroclus, Cyclops, Priam,
Odysseus-and-Telemachus, father-and-son, Penelope, and Ithaca-return subjects.
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
| `assets/generated/iliad/book-24-priam-achilles-v1.png` | `086edfbd4669873fa76ccd567b8728ef326eaa5a4db095a9d9766672205ef85a` | concept-review |
| `assets/generated/odyssey/book-22-hall-v1.png` | `9beb4be8ed49e579185bca7cd0b6d1fc7f5969bcf52147a09ae4a275fe24334c` | concept-review |
| `assets/generated/iliad/book-16-patroclus-v2.png` | `9ea4fe09507f1fe67ce442081f4bba1e6fd3d3d21da106d2bf0bb20e3440cc7b` | concept-review |
| `assets/generated/iliad/book-11-patroclus-eurypylus-v2.png` | `eacc7b1728f09c81e176dbc9bc4c11b623d6ab0904f3a1e29540e095dc623960` | concept-review |
| `assets/generated/odyssey/book-23-penelope-bed-v1.png` | `88478a50d4c2e319ef088999364fbd16ca8f0c10a7ef8861d67fa5c902d92ce3` | concept-review |
| `assets/generated/odyssey/book-16-father-son-v1.png` | `3aaf7cde0ce97e98b380a87f029422cd3f90364526b6674bf4dea2bfcc0d526e` | concept-review |
| `assets/generated/odyssey/book-13-return-v1.png` | `6c6301bc0b5608836a228ef1630272266e0aacdedf50b9c8d5cf13245fba5b52` | concept-review |

Run `shasum -a 256` against the local files after any asset replacement and
update this dossier together with the relevant manifest record. The automated
preflight checks the attribution and file relationships; it does not convert
a concept candidate into a final print master.
