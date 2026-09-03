# Blake–Homer source register

**Prepared:** 2026-09-03  
**Purpose:** attribution control for the comic-size two-volume edition

The phrase “illustrated by Blake” is too imprecise for this edition. The
surviving Homer material associated with William Blake must be described by
role: John Flaxman supplied the designs, while Blake engraved some of the
additional 1805 *Iliad* plates. Blake is not the designer of those plates.

The repository uses this controlled vocabulary:

- **Blake-engraved historical plate:** a documented 1805 print made by Blake
  after a Flaxman design.
- **Historical reference:** a public-domain scan used as a source image or
  visual reference, with every artist role stated in the caption.
- **Blake-informed original supplement:** new CastaliaInstitute work whose
  visual language may study Blake’s line, symbolism, or visionary intensity;
  it is not a Blake work and must say so.

## Primary collection records

| Work / object | What the record establishes | Edition use |
|---|---|---|
| [Homer invoking the muse, British Museum 1867,1012.228](https://www.britishmuseum.org/collection/object/P_1867-1012-228) | Print made by William Blake after John Flaxman; 1805; one of five additional *Iliad* plates, three of which were engraved by Blake. | Eligible historical reference for the opening apparatus or a Blake-engraved *Iliad* plate, subject to scan and rights verification. |
| [Minerva repressing the fury of Achilles, British Museum 1973,U.1189.5](https://www.britishmuseum.org/collection/object/P_1973-U-1189-5) | Print made by William Blake after John Flaxman; 1805; *Iliad* plate. | Current local historical reference; credit remains Flaxman as designer and Blake as engraver. |
| [Thetis entreating Jupiter to honor Achilles, British Museum 1973,U.1189.9](https://www.britishmuseum.org/collection/object/P_1973-U-1189-9) | Print made by William Blake after John Flaxman; 1805; *Iliad* plate with Thetis, Jupiter, and constellations. | Eligible candidate for future source acquisition; not yet a local plate asset. |
| [The Iliad of Homer, National Gallery of Art 1981.57.5](https://www.nga.gov/artworks/60830-iliad-homer) | The 1805 volume contains 40 plates and identifies Blake among the associated artists, alongside Flaxman, Piroli, and Parker. | Independent collection corroboration for the historical edition record. |
| [Flaxman Homer studies, British Museum 1888,0503.8](https://www.britishmuseum.org/collection/object/P_1888-0503-8) | Flaxman’s Homer designs and publication history; the museum notes Flaxman’s influence on Blake. | Context only; do not caption the drawings as Blake’s. |

## Attribution boundary for the Odyssey

The current register does **not** claim that the 1805 *Odyssey* plates were
made by Blake. Collection and catalogue records describe the Odyssey as
Flaxman’s compositions and identify other engravers for the published set.
Until a plate-level primary record establishes a Blake role, Odyssey imagery
must be labeled either `historical-reference` with the documented roles or
`generated` as an explicitly original supplement.

## Repository rule

Before a historical plate enters `design/plate-manifest.csv`, the editor must
record the collection object number, plate title, designer, engraver, local
master checksum, rights statement, and exact Homer passage. A generated
candidate must retain its prompt, model/version record, checksum, and the
credit line **“Original concept by CastaliaInstitute; not by William Blake.”**
The automated provenance preflight checks field presence; an art director
must still verify the object and caption before promotion to `final`.
