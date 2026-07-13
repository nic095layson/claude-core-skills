---
name: pptx
description: >-
  Generating genuine PowerPoint .pptx decks with python-pptx — real slides on real
  layouts with editable native charts and tables, not a document chopped into pages.
  Load whenever a session must produce or extend slides: "make a deck / slides", "turn
  this into a presentation", "board-ready", "put these numbers into a few slides",
  "add a chart slide". Covers starting from an existing template so its masters and
  theme carry over, picking layouts by name and filling placeholders, bullet levels,
  native tables, editable charts from data, speaker notes, and the
  CSV/xlsx-to-board-deck pipeline. Do NOT load for prose documents or reports (docx);
  when the numbers or the analysis belong in a spreadsheet, that is xlsx (which pairs
  with this skill for CSV-to-board-deck work); reading existing PDFs is pdf; and decks
  in David's name also load brand-standard — it supplies Eurostile/Poppins and Space
  Blue while this skill does the slide mechanics.
---

# PPTX

Build real PowerPoint decks with python-pptx. The failure this prevents is the
doc-chopped-into-pages deck: free-floating textboxes that ignore the theme, a
screenshot of a chart nobody can audit, formatting that drifts slide to slide. A
genuine deck takes its **layouts** (named slide blueprints) from the **master**
(the template's theme layer: fonts, colors), fills **placeholders** (a layout's
pre-positioned, theme-styled slots), and ships charts as editable native parts.

## Procedure

1. **Install check first** — package availability is a volatile per-machine
   fact; never assume presence (add `openpyxl` for .xlsx data sources):

   ```bash
   python3 -c "import pptx" 2>/dev/null || pip install python-pptx
   ```

2. **Start from a template when one exists** — `Presentation("template.pptx")`
   inherits its masters, layouts, and theme wholesale: the single
   highest-leverage move for an on-brand deck. Survey the layouts first:

   ```python
   from pptx import Presentation
   prs = Presentation("template.pptx")   # omit the argument for the bare default deck
   for i, layout in enumerate(prs.slide_layouts):
       print(i, layout.name)
   ```

   Names and indices vary per template — pick by name with
   `prs.slide_layouts.get_by_name("Title and Content")`. Default deck (verified
   2026-07-13): 0 "Title Slide", 1 "Title and Content", 2 "Section Header", 5 "Title Only".

3. **Fill placeholders, never free textboxes** — a title slide, then bullets
   with levels (`tf.text` is the first bullet; `add_paragraph()` + `level` nest):

   ```python
   slide = prs.slides.add_slide(prs.slide_layouts[0])    # "Title Slide"
   slide.shapes.title.text = "Q2 Revenue Review"
   slide.placeholders[1].text = "Prepared 2026-07-13"    # subtitle placeholder
   slide = prs.slides.add_slide(prs.slide_layouts[1])    # "Title and Content"
   slide.shapes.title.text = "Takeaways"
   tf = slide.placeholders[1].text_frame
   tf.text = "West region drove the quarter"             # first bullet, level 0
   p = tf.add_paragraph(); p.text = "+21% vs Q1"; p.level = 1
   ```

4. **Native table and speaker notes** — real PowerPoint parts, not tab-aligned
   text. (Charts: `CategoryChartData` + `add_chart` in the worked example below
   makes a real editable chart; `LINE` / `BAR_CLUSTERED` swap in the same way.)

   ```python
   from pptx.util import Inches
   table = slide.shapes.add_table(rows=3, cols=2, left=Inches(1), top=Inches(2),
                                  width=Inches(8), height=Inches(2)).table
   table.cell(0, 0).text = "Region"; table.cell(0, 1).text = "Revenue ($k)"
   slide.notes_slide.notes_text_frame.text = "Lead with the West number."
   ```

5. **Save, then verify by reopening** — a save that succeeds can still be a
   broken or empty deck:

   ```python
   prs.save("deck.pptx")
   check = Presentation("deck.pptx")
   # 2 = slides added above; a real template may ship its own starting slides,
   # so count those first (n0 = len(Presentation("template.pptx").slides)).
   assert len(check.slides) == 2, f"expected 2 slides, got {len(check.slides)}"
   assert any(sh.has_table for s in check.slides for sh in s.shapes), "no table"
   ```

## Output format — the CSV → board-deck worked example

The board-deck shape repeats a trio per data section: **section-header → chart
slide (title states the takeaway) → takeaway bullets.** End to end (verified
2026-07-13 against a 9-row sales.csv):

```python
import csv, collections
from pptx import Presentation
from pptx.util import Inches
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

totals = collections.defaultdict(float)             # 1. aggregate first
with open("sales.csv", newline="") as f:            #    (.xlsx source? read via openpyxl)
    for row in csv.DictReader(f):
        totals[row["region"]] += float(row["revenue"])

prs = Presentation()                                # 2. or Presentation("template.pptx")
s = prs.slides.add_slide(prs.slide_layouts[2])      # 3. section title ("Section Header")
s.shapes.title.text = "Revenue by Region"
s = prs.slides.add_slide(prs.slide_layouts[5])      # 4. chart slide — takeaway as title
s.shapes.title.text = "West leads; Midwest trails"
data = CategoryChartData()
data.categories = list(totals)
data.add_series("Q2 revenue ($)", tuple(totals.values()))
s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED,
                   Inches(1), Inches(1.8), Inches(8), Inches(4.8), data)
s = prs.slides.add_slide(prs.slide_layouts[1])      # 5. takeaway bullets
s.shapes.title.text = "Takeaways"
best = max(totals, key=totals.get)
s.placeholders[1].text_frame.text = f"{best} is the growth engine: ${totals[best]:,.0f}"
prs.save("board_deck.pptx")
check = Presentation("board_deck.pptx")             # 6. verify before delivering
assert len(check.slides) == 3
assert any(sh.has_chart for sl in check.slides for sh in sl.shapes)
```

## Rules

- **Placeholders over textboxes** — theme fonts, sizes, and positions follow
  the master through a placeholder; a textbox freezes today's guesses.
- **Template first when one exists** — recreating a corporate look shape by
  shape is drift waiting to happen; inheriting the master gets it for free.
- **Charts stay editable** — a native chart lets the audience check the numbers
  (right-click > Edit Data); a pasted image asks them to trust a picture.
- **One idea per slide; the title states the takeaway** — boards scan titles;
  "West leads; Midwest trails" survives a skim, "Q2 Chart" does not.

## Edge cases and proportionality

- **Trivial case — the skill steps aside:** three plain text slides, no data, no
  template → default deck, layouts 0–1, save; skip survey, charts, verify ceremony.
- **Template layouts don't match:** survey first (step 2), pick the closest
  named layout; use "Blank" + textboxes only when no placeholder fits, and say so.
- **Big data:** aggregate before charting; cap categories (top N + "other") —
  a 500-bar chart is unreadable and bloats the file.
- **Deleting/reordering slides:** python-pptx has no public API for it (verified
  2026-07-13) — build in final order; state the limit, don't hack slide XML.

## Volatile facts

- Verified 2026-07-13: every fenced snippet above ran in this container
  (python-pptx 1.0.2, openpyxl 3.1.5); reopen assertions passed — slide counts,
  chart categories/values round-trip, bullet levels, notes, masters inherited.
- Assumption (2026-07-13): other environments lack python-pptx until installed
  (step 1 is mandatory), and visual fidelity in desktop PowerPoint/Keynote is
  untested — no Office app exists here; verification was python-pptx round-trip only.

## When NOT to use this skill

- Prose documents, reports, letters → **docx** — a deck is not a paged document.
- The numbers live in / the analysis belongs in a spreadsheet → **xlsx**; the two
  pair for CSV-to-board-deck work (xlsx owns aggregation, this skill presents).
- Reading or extracting from PDFs → **pdf**.
- Decks in David's name → load **brand-standard** too: its tokens (Eurostile
  display / Poppins body, Space Blue) win over generic defaults; this skill
  supplies the slide mechanics.

## Provenance and maintenance

Authored 2026-07-13 for this library on the owner's request, modeled on the
corresponding Anthropic agent-skill concept (the pptx document skill:
template-first, placeholders, native charts).

Re-verify: packages — `python3 -c "import pptx, openpyxl; print(pptx.__version__, openpyxl.__version__)"`;
layouts — `python3 -c "from pptx import Presentation; [print(i, l.name) for i, l in enumerate(Presentation().slide_layouts)]"`;
deletion limit — `python3 -c "from pptx import Presentation; print([m for m in dir(Presentation().slides) if not m.startswith('_')])"` (expect no delete/remove/move).
Update when: python-pptx changes major version (chart/placeholder APIs are
version-specific), a real template lacks the named layouts, or slide deletion gains a public API.
