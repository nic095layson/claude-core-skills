#!/usr/bin/env python3
"""A-2: rerun the live classifier (hooks/govclass.py) on the sealed held-out set C of 2026-10-13, unchanged.

Positives = intended_label GOVERNED; a positive counts as caught when any matched class is ENFORCED (the Stop
gate would require a governor). Negatives = every other label; a negative enforced is a false enforcement.
Writes A01-sealed-set-C-rerun.json (fingerprint = git tree of hooks/) and prints the misses.
"""
import hashlib, json, os, subprocess, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "hooks"))
from govclass import classify, ENFORCED  # noqa: E402
d = json.load(open(os.path.join(ROOT, "results/2026-10-13/system-validation/raw/heldout-set-C.json")))
rows = [dict(id=i["id"], label=i["intended_label"], classes=classify(i["text"]),
             enforced=any(c in ENFORCED for c in classify(i["text"])), text=i["text"]) for i in d["items"]]
pos = [r for r in rows if r["label"] == "GOVERNED"]; neg = [r for r in rows if r["label"] != "GOVERNED"]
fp = subprocess.run(["git", "-C", ROOT, "rev-parse", "--short", "HEAD:hooks"], capture_output=True, text=True).stdout.strip()
rec = dict(fingerprint=fp, fingerprint_of="git tree of hooks/",
           govclass_sha256_8=hashlib.sha256(open(os.path.join(ROOT, "hooks/govclass.py"), "rb").read()).hexdigest()[:8],
           recall=f"{sum(r['enforced'] for r in pos)}/{len(pos)}",
           false_enforcement=f"{sum(r['enforced'] for r in neg)}/{len(neg)}", rows=rows)
json.dump(rec, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "A01-sealed-set-C-rerun.json"), "w"), indent=1)
print(f"govclass {rec['govclass_sha256_8']} on hooks tree {fp}: recall {rec['recall']}, false enforcement {rec['false_enforcement']}")
for r in pos:
    if not r["enforced"]: print("  missed:", r["text"][:120])
for r in neg:
    if r["enforced"]: print("  false enforcement:", r["label"], r["classes"], r["text"][:100])
