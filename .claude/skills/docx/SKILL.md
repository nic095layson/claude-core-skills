---
name: docx
description: >-
  Generate and edit genuine Word .docx files with python-docx — real built-in
  styles (Title, Heading 1/2, List Bullet/Number), tables with header rows,
  page setup, images — and modify or fill EXISTING documents run-by-run so
  their formatting survives. Load whenever the deliverable is a .docx: "write
  this as a Word doc", "create a .docx", "save it as a Word document", "fill
  in this Word template", "edit this docx without breaking formatting", "add
  a section to the report.docx". Also covers .docx-to-PDF conversion via
  LibreOffice — the authoring route when the ask is a NEW PDF from scratch. Do NOT load for slide decks (pptx owns those), spreadsheets or
  tabular data (xlsx), reading or extracting from an existing PDF (pdf), or
  output that will live as Markdown or plain text — that needs no skill. For
  anything external in David's name, brand-standard supplies the fonts,
  colors, and voice and wins on identity; this skill supplies the Word
  mechanics underneath it.
---

# Word Documents (.docx)

A .docx deliverable must be a document Word itself would have made: built-in
styles, real tables, intact run formatting. This skill prevents the two ways
sessions fake it. Creation-side: Markdown renamed to .docx, or headings faked
with bold+font-size runs — breaking Word's navigation pane, TOC fields, and
every tool that keys on style names. Edit-side: round-tripping an existing
document through plain text, which silently destroys its run formatting.

## Terms

- **run** — a stretch of text in a paragraph sharing one character format
  (bold, font, size). Formatting lives on runs, not paragraphs.
- **style** — a named format definition built into Word ("Heading 1",
  "List Bullet"). Set it by name; Word supplies the look.
- **section** — a block of pages sharing page setup (margins, orientation).

## Procedure

1. **Install check** — availability is container-local, never assume:
   `python3 -c "import docx" 2>/dev/null || pip install python-docx`
2. **Create with built-in styles.** Never fake a heading with a bold run:
   ```python
   from docx import Document
   from docx.shared import Inches
   doc = Document()
   doc.add_paragraph("Quarterly Report", style="Title")
   doc.add_heading("Overview", level=1)             # -> style "Heading 1"
   doc.add_heading("Key results", level=2)          # -> style "Heading 2"
   doc.add_paragraph("Body copy stays in Normal.")  # default style: Normal
   doc.add_paragraph("First point", style="List Bullet")
   doc.add_paragraph("Collect data", style="List Number")
   ```
3. **Tables get a real header row** (bold runs in row 0, a built-in table style):
   ```python
   table = doc.add_table(rows=1, cols=3)
   table.style = "Light Grid Accent 1"
   for cell, name in zip(table.rows[0].cells, ("Metric", "Q1", "Q2")):
       cell.paragraphs[0].add_run(name).bold = True
   for cell, val in zip(table.add_row().cells, ("Revenue", "1.2M", "1.5M")):
       cell.text = val
   ```
4. **Page setup lives on sections:**
   ```python
   section = doc.sections[0]
   section.top_margin = section.bottom_margin = Inches(1)
   section.left_margin = section.right_margin = Inches(1)
   ```
5. **Images take an explicit width** (unsized pictures land at native DPI and
   blow out the page): `doc.add_picture("logo.png", width=Inches(2))`.
   Then `doc.save("report.docx")`.
6. **Edit an EXISTING document in place.** Open it, locate the paragraph,
   change run text — never rebuild paragraphs you didn't author:
   ```python
   doc = Document("report.docx")
   target = next(p for p in doc.paragraphs if "Body copy" in p.text)
   target.runs[0].text = target.runs[0].text.replace("stays in", "was edited in")
   doc.save("report.docx")
   ```
7. **Fill a template run-by-run.** Naive `para.text = para.text.replace(...)`
   collapses the paragraph to a single unformatted run — every bold name and
   styled field dies. Replace inside runs instead:
   ```python
   def fill_template(path, out_path, mapping):
       doc = Document(path)
       paragraphs = list(doc.paragraphs)
       for table in doc.tables:              # placeholders hide in tables too
           for row in table.rows:
               for cell in row.cells:
                   paragraphs.extend(cell.paragraphs)
       for para in paragraphs:
           for run in para.runs:             # run-by-run: formatting survives
               for key, val in mapping.items():
                   if key in run.text:
                       run.text = run.text.replace(key, val)
       doc.save(out_path)
   fill_template("template.docx", "letter.docx",
                 {"{{NAME}}": "Joanne", "{{ORDER}}": "A-1042"})
   ```
   Word sometimes splits a placeholder across runs (edit history does this).
   If a key isn't found, inspect `[r.text for r in para.runs]` and fix the
   template — retype the placeholder in one go — rather than cross-run surgery.
8. **Convert to PDF when asked** — `which soffice || which libreoffice`, then:
   `soffice --headless --convert-to pdf --outdir . report.docx && ls report.pdf`
   Check the artifact, not the exit code — soffice exits 0 even when conversion
   fails (verified 2026-07-13). The binary alone is not enough either: a
   core-only install fails with "source file could not be loaded" — fix:
   `apt-get update && apt-get install -y libreoffice-writer` (facts below).
9. **Verify by reopening before delivering** — a clean save proves nothing:
   ```python
   doc = Document("report.docx")
   assert any(p.style.name == "Heading 1" for p in doc.paragraphs)
   assert doc.tables and doc.tables[0].rows[0].cells[0].text == "Metric"
   ```

## Rules

- **Set styles by built-in name, never bold+size fakes** — navigation pane,
  TOC fields, and downstream tooling key on style names; a visually identical
  fake is invisible to all of them.
- **Preserve the run structure you found; never round-trip through plain text
  or Markdown** — formatting lives on runs, and a paragraph rebuilt from its
  plain text is a one-way loss.
- **One source of truth for repeated values** — a name or total appearing five
  times gets filled from one mapping dict, so no copy can drift.
- **Reopen and assert before delivery** — python-docx not erroring proves
  nothing about what Word will show; the reopen check costs three lines.

## Edge cases and proportionality

- Content that will live in chat, Markdown, or a README needs no skill and no
  python-docx — write it directly; ceremony here is waste.
- A doc generated THIS session from a script: re-run the script with the fix
  instead of surgically editing the output — the script is the source of truth.
- A template whose placeholders are shattered across runs: fix the template
  once; do not build a cross-run replacement engine for one letter.
- Branded documents (brand-standard loaded): customize the style OBJECTS —
  style names stay intact for navigation/TOC while the look follows the brand
  (verified 2026-07-13, round-trips):
  ```python
  from docx.shared import RGBColor
  doc.styles["Heading 1"].font.name = "Eurostile"
  doc.styles["Heading 1"].font.color.rgb = RGBColor(0x0F, 0x43, 0x6E)
  doc.styles["Normal"].font.name = "Poppins"
  ```

## Volatile facts (dated)

- **verified 2026-07-13:** python3 3.11.15 + python-docx 1.2.0 in this
  container; every snippet above executed here this date.
- **verified 2026-07-13:** `soffice` was present here yet conversion FAILED
  until `libreoffice-writer` was installed; then succeeded (`writer_pdf_Export`).
- **assumption (2026-07-13):** macOS full installs ship all filters; binary at
  `/Applications/LibreOffice.app/Contents/MacOS/soffice` — untested here.
- All container-local — re-check per session and install what's missing.

## When NOT to use this skill

- Slide decks and presentations → **pptx**.
- Spreadsheets, tabular data, anything with formulas → **xlsx**.
- Reading, extracting from, form-filling, or redacting an existing PDF →
  **pdf**. (Creating a brand-new PDF: author it here, then convert — step 8.)
- Styled HTML pages or artifacts → **frontend-design**.
- Look, voice, fonts, colors of anything in David's name → **brand-standard**
  wins on identity; this skill only executes the mechanics in Word.
- Authoring or restructuring skills like this one → **skill-authoring**.

## Provenance and maintenance

Authored 2026-07-13 for this library on the owner's request, modeled on the
corresponding Anthropic docx agent-skill concept. Every Python and shell
snippet above ran in the session container 2026-07-13: create → reopen →
assert, in-place edit keeping style and run count, template fill keeping a
bold run, soffice PDF conversion (after installing libreoffice-writer).

Re-verify: python-docx — `python3 -c "import docx; print(docx.__version__)"`;
conversion —
`soffice --headless --convert-to pdf --outdir . report.docx && ls report.pdf`.
Update when: python-docx major-versions (style/section API may shift), the
surface gains or loses LibreOffice, or a real template defeats run-by-run
filling — extend step 7 via skill-authoring's checklist, never by loosening
the no-plain-text rule.
