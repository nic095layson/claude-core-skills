#!/usr/bin/env python3
"""Bands check: a report that quotes a headline figure must quote every FRAGILE constant's band (red-team
skill, step 8, rule 3: two error bars or none). Generalized 2026-10-19 from the fantasy-basketball kit's
check_bands.py (ledger INC-2026-10-19-01).

Why it exists: the incident's report said ±0.4 where the structural band was about ±3. A sampling error
quoted alone says "we ran it many times", which the reader hears as "we are sure"; the band is what they
needed. Writers read the sweep record, so the figures match by construction; a hand-typed band that drifted
from the record fails here.

Inputs
  --report PATH   the report (markdown or text)
  --sweep PATH    the sweep record: {"fragile": [name, ...],
                                     "constants": {name: {"tier", "variants": [{"label", "shift_mean"}]}}}

For each constant the sweep tiers FRAGILE, the report must contain the constant's name (the part after the
last dot, so a module prefix is optional), the word FRAGILE within 400 characters of that name, and each
variant's mean shift as a signed one-decimal figure (+3.4, -2.3; a unicode minus or en dash is accepted).
Prints 'BANDS CHECK: PASS — ...' / 'BANDS CHECK: FAIL' + problems. Exit 0 / 1.
"""
import argparse
import json
import re
import sys

WINDOW = 400


def _signed(x):
    return f"{float(x):+.1f}"


def check_text(text, sweep):
    """(ok, problems) for report text against a sweep record dict."""
    text = text.replace("−", "-").replace("–", "-")
    problems = []
    for key in sweep.get("fragile", []):
        c = sweep.get("constants", {}).get(key)
        name = str(key).split(".")[-1]
        if name not in text:
            problems.append(f"{key} is FRAGILE but the report never names it")
            continue
        pat = rf"{re.escape(name)}.{{0,{WINDOW}}}FRAGILE|FRAGILE.{{0,{WINDOW}}}{re.escape(name)}"
        if not re.search(pat, text, re.S):
            problems.append(f"{key}: the report names it but not as FRAGILE within {WINDOW} characters")
        for v in (c or {}).get("variants", []):
            # the sweep record carries the pre-formatted figure (shift_mean_1dp) so writer and checker read
            # the same string; a value on a rounding boundary (-2.35) otherwise splits them
            s = str(v.get("shift_mean_1dp") or _signed(v["shift_mean"]))
            if s not in text:
                problems.append(f"{key}: band figure {s} ({v.get('label', '?')}) is not quoted")
    return not problems, problems


def check(report_path, sweep_path):
    with open(report_path, encoding="utf-8") as f:
        text = f.read()
    with open(sweep_path, encoding="utf-8") as f:
        sweep = json.load(f)
    return check_text(text, sweep)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--report", required=True)
    ap.add_argument("--sweep", required=True)
    a = ap.parse_args(argv)
    ok, problems = check(a.report, a.sweep)
    with open(a.sweep, encoding="utf-8") as f:
        sw = json.load(f)
    if ok:
        print(f"BANDS CHECK: PASS — {len(sw.get('fragile', []))} FRAGILE band(s) quoted "
              f"({', '.join(sw.get('fragile', [])) or 'none'}); engine {sw.get('fingerprint', '?')}")
    else:
        print("BANDS CHECK: FAIL")
        for p in problems:
            print("  " + p)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
