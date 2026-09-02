# Page-map rules

`design/page-map.csv` is the reconciliation layer between approved editorial
content and rendered pages.

Every final row must identify:

- the volume and page number;
- page type and epic/book context;
- the source range or reason for a blank page;
- the text and image files used;
- the caption record when an image appears;
- proof status and release notes.

Sample-proof rows use `*-proof` volume names and `verified-sample` status. They
must not be mistaken for final volume pagination. Final volume rows will use
the actual volume slug and numeric page count after the binding and page maps
are locked.
