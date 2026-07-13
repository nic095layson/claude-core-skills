# Filling PDF forms (companion to the pdf skill)

Load this file ONLY when actually filling an AcroForm — read-only PDF work
never needs it. Every snippet below executed successfully 2026-07-13 against
a generated three-field AcroForm (text + checkbox + choice) with pypdf 6.14.2.

## 1. Enumerate before you write

Run the extractor first and work only from its output (the script path here
and in step 4 is relative to this skill's directory — from elsewhere, use the
full `.claude/skills/pdf/scripts/extract_fields.py`):

```bash
python3 scripts/extract_fields.py form.pdf
```

From the JSON, collect for each field you intend to fill:

- `name` — the exact key you must use; invented or paraphrased names no-op.
- `type` — text / button (checkbox, radio) / choice / signature.
- `states` — for checkboxes: the legal values. **The on-value is whichever
  entry is not `/Off`.** It is often `/Yes` but authors set custom export
  values (`/On`, `/1`, `/Male`, ...). Never assume `/Yes`; read it.
- `options` — for choice fields: the only legal values. Anything else is a
  silent failure in most viewers.

If the extractor prints `[]` but the document visibly shows form boxes, the
form is likely XFA-based or already flattened (assumption 2026-07-13,
untested here) — tell the user instead of drawing text onto the page.

## 2. Fill via PdfWriter round-trip

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("form.pdf")
writer = PdfWriter()
writer.append(reader)

values = {
    "full_name": "David Layson",  # text field
    "subscribe": "/Yes",          # checkbox: on-value from extractor "states"
    "state": "NY",                # choice: value from extractor "options"
}
# page=None updates every page that carries widgets for these fields.
writer.update_page_form_field_values(None, values, auto_regenerate=False)

# NeedAppearances=True asks viewers to rebuild widget appearances so the
# written values render instead of showing stale/blank boxes.
writer.set_need_appearances_writer(True)

with open("filled.pdf", "wb") as f:
    writer.write(f)
```

## 3. The auto_regenerate / NeedAppearances ordering trap

Verified 2026-07-13 against pypdf 6.14.2 source and output: the
`auto_regenerate` argument **is** the NeedAppearances switch — `True` sets
the flag, `False` clears it, `None` leaves it untouched. Consequence: the
widely-circulated recipe that calls `set_need_appearances_writer(True)`
*before* `update_page_form_field_values(..., auto_regenerate=False)` ends up
with NeedAppearances=False — values written but possibly rendered blank.
Set the flag AFTER the update call (as in step 2), and keep
`auto_regenerate=False` so the update itself does not fight your setting.

## 4. Verify before delivering (mandatory)

Re-extract the output file and diff expected vs actual. Any mismatch blocks
delivery — a fill that "ran without errors" is not a fill that worked:

```bash
python3 scripts/extract_fields.py filled.pdf > actual.json
python3 - <<'PY'
import json
expected = {"full_name": "David Layson", "subscribe": "/Yes", "state": "NY"}
actual = {f["name"]: f["value"] for f in json.load(open("actual.json"))}
bad = {k: (v, actual.get(k)) for k, v in expected.items() if actual.get(k) != v}
assert not bad, f"MISMATCH: {bad}"
print("all values round-tripped")
PY
```

Report the diff result in your delivery note. If a value did not round-trip,
check first that it was a legal `states`/`options` entry, then that the
field name matched the extractor output exactly.
