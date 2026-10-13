# Operational Process Tree (2026-10-12)

Owner-requested companion to `results/2026-10-09/ai-rules-of-engagement/`: a
single-page visual of the operating logic, gates, and checks, as a standard
independent of any project, model, or vendor. It shows the checks and balances:
every gate has a check, and every check shows where the work goes when it fails.

## Files

| File | What |
|---|---|
| `Operational-Process-Tree_2026-10-12.pdf` | One page, vector, 1800 x 1790 px canvas (1350 x 1343 pt). Fit-to-page when printing. |
| `Operational-Process-Tree_2026-10-12.png` | Same page at 2x (3600 x 3580 px) for slides and chat. |
| `Operational-Process-Tree_2026-10-12.svg` | The vector source; opens in a browser or Illustrator. |
| `build_tree.py` | Generator. The node lists are the auditable content; layout is computed. `python3 build_tree.py` |
| `render_tree.js` | Renders `tree.html` to PNG and PDF through Chromium (Playwright). `node render_tree.js` |
| `tree.html` | Render wrapper for the SVG. |

## What the page shows

- **Centre, the order of operations** (document Section 4): Request, Triage,
  then seven numbered steps to Delivered. Each gate step is followed by a
  diamond check; the pass path continues down the spine, the fail path goes to
  a tinted outcome box that states what happens instead. Two fail paths loop
  back: a failed plan check returns to the Plan Gate; a failed verification
  returns to Execute.
- **Three continuous checks during execution** (Sections 3 and 5): adjacent
  problem (L8), result differs from prediction (surprise handling), state
  mismatch before a write (H3).
- **Left, the ten laws** (Section 3) and how the rules are enforced
  (instructions, skills, machine checks, hooks), with the two design lessons
  from Section 6.
- **Right, the seven mechanical controls** (Section 6), each labelled with the
  step it binds.

## Owner decisions recorded (2026-10-12, in-session)

- Standalone diagram, not inserted into the Rules of Engagement document
  (the owner called that document final on 2026-10-09). Insertion offered.
- Vendor-neutral, matching the document.
- Content scope: lifecycle gates and the controls that can refuse work; not
  every rule in the standard.

## Verification (adversarial-verify, this session)

- **Traceability (C1):** 50 of 50 node terms found verbatim in the document's
  text (pandoc plain-text extraction of the v1.0 .docx), checked by script.
  Three terms initially missed on wording ("write nothing", "never reported
  as done", "mechanical gates"); the diagram was reworded to the document's
  own phrasing ("nothing is written", "counts as not done", "machine checks").
- **Both outcomes per check (C2):** every diamond has a pass caption on the
  spine and a fail arrow to an outcome box; the three in-work checks carry
  "Yes:" / "No:" in the outcome text. Inspected on the rendered image.
- **Fits one page (C3):** the generator asserts the spine ends above the
  legend; first layouts failed that assertion twice (1475 and 1703 px on a
  1240 and 1640 px page) and the page was sized to 1790 px with tightened gaps.
- **Brand (C4):** Space Blue, Muted Space Blue, and the grey ramp only;
  Poppins for text; display font declared as Eurostile with Poppins SemiBold
  fallback. `pdffonts` shows only Poppins faces embedded.
- **Determinism:** two consecutive build+render runs produced byte-identical
  SVG and PNG (md5 checked).
- **Layout defects found on inspection and fixed across four render passes:**
  spine overflow; three in-work outcome boxes colliding with their diamonds;
  clipped lines in steps 3, 4 and 7; yes/no labels colliding with box edges;
  a gap in the spine between steps 3 and 4; diamond text wider than the
  diamond; the verification loop-back arrow crossing an outcome box.

## Not checked / bounds

- **Eurostile** is commercial and not installed in the build environment.
  Headings render in Poppins SemiBold here. The SVG declares Eurostile first,
  so it renders in Eurostile wherever that font is installed.
- **Print size.** The page is a custom size, not Letter or Tabloid. It is
  legible at Tabloid (11 x 17) fit-to-page; at Letter the 10.5 px captions
  become small. Not test-printed.
- **The page's font list reported "system fonts only"** from Chromium's
  `document.fonts`; that API lists only web-loaded fonts, so it is not evidence
  either way. The embedded-font check in the PDF is the evidence.
