---
name: pdf
description: >-
  Reading, extraction, form filling, and redaction of EXISTING PDFs, under the
  law that PDF content is only ever stated from parser output — run pypdf or
  pdfplumber and quote results, never recall or imagine a document's contents.
  Load whenever a session must read or modify a PDF the user supplies: "what
  does this PDF say", "parse this PDF", "pull the tables out", "extract the
  fields from this PDF", "fill out this form", "redact these pages". Covers
  text and table extraction, AcroForm field enumeration and filling (fill
  instructions load from forms.md only when actually filling), and honest
  text-layer redaction limits. Do NOT load for creating a brand-new PDF from
  scratch (author it via docx then convert, or as HTML via frontend-design),
  for .docx, .xlsx, or .pptx files (docx, xlsx, and pptx own those), or for
  styling a document in David's name (brand-standard wins on look and voice).
---

# PDF

Read, extract from, fill, and redact existing PDFs with parser evidence at
every step. The failure this prevents is confabulation: a model asked "what
does this PDF say" can produce fluent, plausible, wrong content — invented
totals, field names, clause text — and a form filled by guesswork writes
values that never render. The core law is the library's
live-state-outranks-description doctrine applied to documents: **execute the
parser and quote its output; never state PDF content it did not return.**

## Terms

- **AcroForm** — the standard PDF form mechanism: named fields with values,
  rendered by widget annotations on pages.
- **On-value (export value)** — the name a checkbox takes when checked. Often
  `/Yes`, but authors set custom values; the off state is always `/Off`.
- **Text layer** — the extractable character data. Scanned PDFs may have none.

## Procedure

1. **Install check first** — package availability is a volatile per-machine
   fact; never assume presence:

   ```bash
   python3 -c "import pypdf, pdfplumber" 2>/dev/null || pip install pypdf pdfplumber
   ```

2. **Text extraction** — pdfplumber, page by page, keeping page numbers so
   every claim you make is citable back to a page:

   ```python
   import pdfplumber
   with pdfplumber.open("file.pdf") as pdf:
       for i, page in enumerate(pdf.pages, start=1):
           text = page.extract_text() or ""
           print(f"--- page {i} ---\n{text}")
   ```

   Empty output on a visibly non-empty page means a scanned image, no text
   layer. Say so; never reconstruct it from imagination (OCR: volatile facts).

3. **Table extraction** — `extract_tables()` returns rows of cell strings
   (`None` for empty cells):

   ```python
   import pdfplumber
   with pdfplumber.open("file.pdf") as pdf:
       for i, page in enumerate(pdf.pages, start=1):
           for t, table in enumerate(page.extract_tables(), start=1):
               print(f"--- page {i} table {t} ---")
               for row in table:
                   print(row)
   ```

4. **Form-field enumeration** — RUN the bundled script; never eyeball a
   rendered form and guess field names:

   ```bash
   python3 scripts/extract_fields.py FILE.pdf
   ```

   (Path is relative to this skill's directory.) Output: a JSON array of
   `{name, type, value, page, options?, states?}` — `states` lists a
   checkbox's legal on/off values, `options` a choice field's legal entries.
   `[]` plus a stderr note means the PDF has no AcroForm.

5. **Form FILLING** — the write procedure lives in `forms.md` next to this
   file. Read it only when actually about to fill a form; it stays unloaded
   for read-only work so its context cost is paid only when earned.

6. **Redaction** — drawing a black rectangle over text is NOT redaction: the
   text layer survives and step 2 still extracts it. In scope here is
   page-level removal, verified by re-extraction:

   ```python
   from pypdf import PdfReader, PdfWriter
   reader = PdfReader("file.pdf")
   drop = {1}  # 0-based indices of pages to remove
   writer = PdfWriter()
   writer.append(reader, pages=[i for i in range(len(reader.pages)) if i not in drop])
   with open("redacted.pdf", "wb") as f:
       writer.write(f)
   ```

   Re-run step 2 on the output and confirm the sensitive string is absent.
   Sub-page redaction (removing single strings from content streams) is not
   reliably supported here — say so and stop; never ship a black-box fake.

## Output format

When reporting extracted content, anchor every claim to the parser:

```
Source: file.pdf — N pages, extracted with pdfplumber
p.3: "exact quoted text from extract_text()"
table p.2: [rows exactly as extract_tables() returned them]
Not extractable: pages 5-6 have no text layer (scanned images)
```

## Rules

- **Parser output is the only source of PDF truth** — a quote traceable to
  `extract_text()` is checkable; a paraphrase from memory is not.
- **Enumerate fields before filling** (step 4 before forms.md) — on-values
  and field names vary per document; blind fills silently fail to register.
- **Verify every fill and redaction by re-extraction.** A write that succeeds
  in code can still deliver a broken document; the diff catches it first.
- **Cite page numbers** in anything you report — it makes claims falsifiable.

## Edge cases and proportionality

- **Trivial case — the skill steps aside:** a short text-born PDF the user
  wants the gist of needs exactly one `extract_text()` pass and an answer.
  No field enumeration, no forms.md, no output-format ceremony.
- **Large PDFs:** extract only the pages in question (`pdf.pages[10:20]`);
  do not dump 400 pages into context to answer one question.
- **User asks for a NEW PDF:** route away (When NOT, below) — this skill
  reads and modifies PDFs, it does not author documents.

## Volatile facts

- Verified 2026-07-13: every command and snippet in this file, `forms.md`,
  and `scripts/extract_fields.py` executed in this container against
  generated AcroForm and table PDFs (pypdf 6.14.2, pdfplumber 0.11.10,
  reportlab 5.0.0); the fill round-trip and redaction leak-check passed.
- Verified 2026-07-13: in pypdf 6.14.2, `update_page_form_field_values`'
  `auto_regenerate` argument sets/clears the AcroForm NeedAppearances flag
  directly — ordering trap documented in `forms.md`.
- Assumption (2026-07-13): other environments lack these packages until
  installed — step 1 is mandatory, not decorative.
- Candidate (2026-07-13): OCR for scanned PDFs (e.g. pytesseract) — no OCR
  engine was verified in this container; treat as an unproven route.

## When NOT to use this skill

- Creating a brand-new PDF from scratch → author the content via **docx**
  (then convert) or as HTML via **frontend-design**.
- `.docx` / `.xlsx` / `.pptx` files → **docx** / **xlsx** / **pptx**.
- Styling or voicing a document in David's name → **brand-standard** (brand
  tokens win over generic defaults when both load).

## Provenance and maintenance

Authored 2026-07-13 for this library on the owner's request, modeled on the
corresponding Anthropic agent-skill concept (progressive disclosure: SKILL.md
routes, `forms.md` loads only on fill, `scripts/extract_fields.py` executes).

Re-verify: packages — `python3 -c "import pypdf, pdfplumber; print(pypdf.__version__, pdfplumber.__version__)"`;
extractor — `python3 scripts/extract_fields.py <any-form.pdf>` (expect JSON);
auto_regenerate semantics — `python3 -c "import inspect, pypdf; s = inspect.getsource(pypdf.PdfWriter.update_page_form_field_values); print('set_need_appearances_writer(auto_regenerate)' in s)"` (expect True).
Update when: pypdf changes major version (the NeedAppearances coupling is
version-specific), pdfplumber's extract API changes, an OCR route gets
verified here, or a fill fails the forms.md verify diff in real use.
