#!/usr/bin/env python3
"""score_classifier.py <govclass_dir> <heldout.json> <split|all> [--show-misses] -> metrics for one classifier on one split.
Positive = gold GOVERNED. Enforced = any class in ENFORCED. Negatives = REQUIREMENT, CONTINUATION, SILENT."""
import json, sys, importlib.util
cdir, path, split = sys.argv[1], sys.argv[2], sys.argv[3]; show = "--show-misses" in sys.argv
spec = importlib.util.spec_from_file_location("gc", f"{cdir}/govclass.py"); gc = importlib.util.module_from_spec(spec); spec.loader.exec_module(gc)
GOLD_GOV = {"build": {"plan-gate"}, "analysis": {"adversarial-verify"}, "review": {"adversarial-verify"}, "dispute": {"adversarial-verify", "scope-fence"}}
items = [it for it in json.load(open(path))["items"] if split == "all" or it.get("split") == split]
tp = fn = fp = tn = gmatch = 0; misses = []; fps = []
for it in items:
    gold = it["gold"]["label"]; cls = gc.classify(it["text"]); enf = [c for c in cls if c in gc.ENFORCED]
    if gold == "GOVERNED":
        if enf:
            tp += 1
            want = set().union(*[GOLD_GOV[c] for c in it["gold"]["classes"]]) if it["gold"]["classes"] else set()
            if set(gc.governors(enf)) & want: gmatch += 1
        else: fn += 1; misses.append((it["id"], it["gold"]["classes"], it["text"][:110]))
    else:
        if enf: fp += 1; fps.append((it["id"], gold, enf, it["text"][:110]))
        else: tn += 1
pos, neg = tp + fn, fp + tn
out = {"split": split, "n": len(items), "governed": pos, "negatives": neg, "recall": f"{tp}/{pos}", "false_enforcement": f"{fp}/{neg}",
       "governor_match_on_hits": f"{gmatch}/{tp}"}
print(json.dumps(out))
if show:
    for m in misses: print("  MISS", m)
    for f in fps: print("  FALSE-ENFORCE", f)
