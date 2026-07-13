---
name: xlsx
description: >-
  Generate and edit genuine Excel .xlsx workbooks with openpyxl — typed cells
  (numbers as numbers, dates as dates), live formulas written as formulas
  ("=SUM(B2:B10)"), real number formats (currency, percent, thousands),
  styled headers, freeze panes, native sortable tables, conditional
  formatting, charts, and multi-sheet layouts (data/calcs/summary) — not a
  CSV renamed .xlsx. Load whenever the deliverable — or the file to read or
  edit — is a spreadsheet: "make me a spreadsheet", "turn this CSV into an
  Excel file", "add formulas/totals to this sheet", "build a budget/tracker
  workbook", "what's in this xlsx". Do NOT load for slides
  built from this data (pptx — it pairs with this skill for CSV-to-board-deck
  work), prose reports (docx), or pulling tables out of a PDF (pdf extracts
  first, then here); a quick CSV the user will keep as CSV needs no skill.
  For workbooks in David's name, brand-standard wins on fonts and colors;
  this skill supplies the Excel mechanics underneath.
---

# Excel Workbooks (.xlsx)

An .xlsx deliverable must be a workbook Excel itself would have made. This
skill prevents the two ways sessions fake it: a CSV renamed .xlsx — where
"12" sorts as text and SUM returns 0 — and dead precomputed totals pasted
where formulas belong, which go stale the moment the user edits an input.

## Terms

- **typed cell** — value is `int`/`float`/`date`, not a look-alike string.
- **live formula** — cell value IS the formula string (`"=SUM(...)"`); Excel
  computes it on open and recomputes when inputs change.
- **cached value** — what Excel stored at last save; `data_only=True` reads it.

## Procedure

1. **Install check** — availability is container-local, never assume:
   `python3 -c "import openpyxl" 2>/dev/null || pip install openpyxl`
2. **CSV/data → typed cells + per-row formulas.** `csv.reader` yields
   strings — convert every numeric/date field before writing:
   ```python
   import csv
   from datetime import date
   from openpyxl import Workbook
   wb = Workbook()
   ws = wb.active
   ws.title = "Data"
   ws.append(["Date", "Item", "Qty", "Unit Price", "Total"])
   rows = list(csv.reader(open("sales.csv", newline="")))[1:]  # skip header
   for i, (d, item, qty, price) in enumerate(rows, start=2):
       ws.cell(row=i, column=1, value=date.fromisoformat(d))  # real date — adapt parsing to the source's date format
       ws.cell(row=i, column=2, value=item)
       ws.cell(row=i, column=3, value=int(qty))      # int, not "12"
       ws.cell(row=i, column=4, value=float(price))  # float, not "4.50"
       ws.cell(row=i, column=5, value=f"=C{i}*D{i}") # live formula
   last = ws.max_row
   ws.cell(row=last + 1, column=5, value=f"=SUM(E2:E{last})")  # totals row
   ```
3. **Know the caveat pair; tell the user when it matters.** (a) openpyxl
   never evaluates formulas — a formula cell reads back as its string. (b)
   `data_only=True` returns only Excel's cached value — `None` if no app ever
   calculated the file. Need the numbers? Compute them in Python alongside.
4. **Number formats, header styling, widths, freeze panes:**
   ```python
   from openpyxl.styles import Font, PatternFill
   for c in ws["D"][1:] + ws["E"][1:]:
       c.number_format = '"$"#,##0.00'               # currency + thousands
   for c in ws["A"][1:]:
       c.number_format = "yyyy-mm-dd"
   for c in ws[1]:
       c.font = Font(bold=True, color="FFFFFF")
       # generic example fill — workbooks in David's name take brand-standard's
       # exact values instead (Space Blue 0F436E), never a lookalike
       c.fill = PatternFill("solid", fgColor="1F4E79")
   ws.column_dimensions["B"].width = 14              # per-column widths
   ws.freeze_panes = "A2"        # row 1 stays visible while scrolling
   ```
5. **Native table** (sortable/filterable; `displayName` workbook-unique, no
   spaces; `ref` includes the header row) **+ conditional formatting:**
   ```python
   from openpyxl.worksheet.table import Table, TableStyleInfo
   tab = Table(displayName="Sales", ref=f"A1:E{last}")
   tab.tableStyleInfo = TableStyleInfo(name="TableStyleMedium9",
                                       showRowStripes=True)
   ws.add_table(tab)
   from openpyxl.formatting.rule import CellIsRule
   ws.conditional_formatting.add(f"E2:E{last}", CellIsRule(
       operator="greaterThan", formula=["100"],
       fill=PatternFill("solid", fgColor="FFC7CE")))
   ```
6. **A chart, when asked** — native and editable, not a pasted image:
   ```python
   from openpyxl.chart import BarChart, Reference
   chart = BarChart()
   data = Reference(ws, min_col=5, min_row=1, max_row=last)  # header names series
   chart.add_data(data, titles_from_data=True)
   chart.set_categories(Reference(ws, min_col=2, min_row=2, max_row=last))
   ws.add_chart(chart, "G2")
   ```
7. **Multi-sheet layout** (data/calcs/summary) — cross-sheet formulas:
   ```python
   summary = wb.create_sheet("Summary")
   summary["A1"], summary["B1"] = "Grand total", f"=SUM(Data!E2:E{last})"
   summary["A2"], summary["B2"] = "Margin", 0.245
   summary["B2"].number_format = "0.0%"      # shows 24.5%, not a bare 0.245
   wb.save("sales.xlsx")
   ```
8. **Edit EXISTING workbooks in normal mode; verify by reopening** — a
   clean save proves nothing:
   ```python
   from openpyxl import load_workbook
   wb = load_workbook("sales.xlsx")   # never data_only=True for editing
   wb["Data"]["C2"] = 15              # change the input; formulas stay live
   wb.save("sales.xlsx")
   wb = load_workbook("sales.xlsx")                  # formulas as strings
   assert wb["Data"]["E2"].value == "=C2*D2"
   assert isinstance(wb["Data"]["C2"].value, int)    # typed, not "12"
   assert "Sales" in wb["Data"].tables
   cached = load_workbook("sales.xlsx", data_only=True)["Data"]["E2"].value
   print("cached:", cached)   # None here — Excel has never calculated it
   ```

## Rules

- **Formulas over precomputed values** — the user will change inputs; a
  pasted total is wrong the moment they do, and nothing flags it.
- **Typed cells, always** — sorting, filtering, SUM/AVERAGE, and pivots all
  break silently on numbers-as-strings.
- **Explicit number formats** — a bare `0.1` that means 10% misleads.
- **Never save a workbook loaded with `data_only=True`** — the save replaces
  every formula with its cached value (here: `None`), a one-way loss.
- **Reopen and assert before delivery** — openpyxl not erroring proves
  nothing about what Excel will show; the check costs four lines.

## Edge cases and proportionality

- A quick CSV kept as CSV needs no skill and no openpyxl — write it and
  stop; a bare NUMBER ("what do these sum to?") gets computed and answered.
- A tiny one-tab grid with no computation: typed cells + a bold header row
  is enough — skip tables, charts, and formatting nobody asked for.
- A workbook generated THIS session by a script: re-run the script with the
  fix rather than surgically editing the output.

## Volatile facts (dated)

- **verified 2026-07-13:** python3 3.11.15 + openpyxl 3.1.5 (container-local
  — re-check per session, install what's missing); every snippet ran this
  date. Normal reopen returned `'=C2*D2'`; `data_only=True` returned `None`.
- **verified 2026-07-13:** loading `data_only=True` then saving produced a
  workbook whose formula cells read back `None` — formulas gone for good.
- **verified 2026-07-13:** table, chart part, freeze panes, and formats
  survived a load→edit→save round trip; a written `date` reads back `datetime`.
- **assumption (2026-07-13):** Excel-authored workbooks with parts openpyxl
  does not model (pivots, slicers, VBA without `keep_vba=True`) can lose
  them on a round trip — untested here.

## When NOT to use this skill

- Slides built from this data → **pptx** (the CSV→xlsx→board-deck combo:
  this skill makes the workbook, pptx the deck).
- Prose reports → **docx**; web dashboards and HTML artifacts →
  **frontend-design**.
- Extracting tables FROM a PDF → **pdf** first (parser output only), then
  this skill to build the workbook from what it extracted.
- Look, fonts, colors of workbooks in David's name → **brand-standard** wins
  on identity; authoring skills like this one → **skill-authoring**.

## Provenance and maintenance

Authored 2026-07-13 for this library on the owner's request, modeled on the
corresponding Anthropic xlsx agent-skill concept. Every snippet ran in this
container 2026-07-13: CSV→typed workbook (formulas, formats, table, chart,
freeze panes, second sheet); both reopen modes; data_only save-loss; edit.

Re-verify: `python3 -c "import openpyxl; print(openpyxl.__version__)"`;
the cache caveat (after running the Procedure snippets, which create sales.xlsx) —
`python3 -c "from openpyxl import load_workbook; print(load_workbook('sales.xlsx', data_only=True)['Data']['E2'].value)"`.
Update when: openpyxl major-versions (table/chart API may shift), a surface
gains a calculating engine (softens the None-cache caveat), or a real
Excel-authored round trip settles the loss assumption above.
