#!/usr/bin/env python3
"""List AcroForm field metadata from a PDF as a JSON array.

Usage: python3 extract_fields.py FILE.pdf

Prints a JSON array to stdout: one object per field with name, type,
current value, page (0-based, null if no widget found), options for
choice fields, and states (the legal on/off values) for checkboxes and
radio buttons. A PDF with no AcroForm prints [] plus a note on stderr.

Dependency: pypdf only (pip install pypdf).
"""
import argparse
import json
import sys

from pypdf import PdfReader

TYPE_NAMES = {"/Tx": "text", "/Btn": "button", "/Ch": "choice", "/Sig": "signature"}


def qualified_name(annot_obj):
    """Fully-qualified field name for a widget annotation (walks /Parent)."""
    name = annot_obj.get("/T")
    parent = annot_obj.get("/Parent")
    while parent is not None:
        pobj = parent.get_object()
        t = pobj.get("/T")
        if t:
            name = f"{t}.{name}" if name else t
        parent = pobj.get("/Parent")
    return str(name) if name else None


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Print AcroForm field metadata from a PDF as JSON."
    )
    ap.add_argument("pdf", help="path to the PDF to inspect")
    args = ap.parse_args()

    reader = PdfReader(args.pdf)
    fields = reader.get_fields()
    if not fields:
        print("[]")
        print(f"note: no AcroForm fields in {args.pdf}", file=sys.stderr)
        return 0

    # Map fully-qualified field name -> 0-based page index via widget annots.
    pages = {}
    for index, page in enumerate(reader.pages):
        for annot in page.get("/Annots") or []:
            name = qualified_name(annot.get_object())
            if name and name not in pages:
                pages[name] = index

    out = []
    for name, field in fields.items():
        value = field.get("/V")
        entry = {
            "name": str(name),
            "type": TYPE_NAMES.get(field.get("/FT"), str(field.get("/FT"))),
            "value": None if value is None else str(value),
            "page": pages.get(str(name)),
        }
        options = field.get("/Opt")  # choice fields: exportable options
        if options is not None:
            entry["options"] = [str(o) for o in options]
        # checkbox/radio legal states incl. /Off — button fields only; pypdf
        # also mirrors /Opt into /_States_ for choice fields, which would
        # duplicate "options" here.
        states = field.get("/_States_") if field.get("/FT") == "/Btn" else None
        if states is not None:
            entry["states"] = [str(s) for s in states]
        out.append(entry)

    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
