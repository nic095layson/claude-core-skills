#!/usr/bin/env python3
"""Join blind grading verdicts with the held-back keymap and compute the Phase 2
measurement table: per governor with-rate, without-rate, delta, and gate.

Inputs:
  traces/_keymap.json     id -> {key, governor, arm, run, complete}
  verdicts.json           id -> {primary_present, confidence, verifier_agree,
                                 final_present, ...}   (built from workflow output)
  traces/t_<id>.json      for skills_fired corroboration

Gate (measurement bar): signature present in >=3/4 with-library runs AND
visibly absent (0/4, or clearly <with) in without-library runs.
"""
import json, os, collections

BASE = os.path.dirname(os.path.abspath(__file__))
keymap = json.load(open(os.path.join(BASE, "traces", "_keymap.json")))
verdicts = json.load(open(os.path.join(BASE, "verdicts.json")))

GOVS = ["plan-gate", "adversarial-verify", "live-state-truth", "scope-fence", "lessons-ledger"]

def skills_for(nn):
    t = json.load(open(os.path.join(BASE, "traces", f"t_{nn}.json")))
    return t.get("skills_fired", [])

# per-transcript rows
rows = []
for nn, meta in keymap.items():
    v = verdicts.get(nn, {})
    rows.append({
        "id": nn, "governor": meta["governor"], "key": meta["key"],
        "arm": meta["arm"], "run": meta["run"],
        "final_present": v.get("final_present"),
        "primary_present": v.get("primary_present"),
        "verifier_agree": v.get("verifier_agree"),
        "skill_fired": meta["governor"] in skills_for(nn),
    })
rows.sort(key=lambda r: (GOVS.index(r["governor"]), r["key"], r["arm"], r["run"]))

# per-governor aggregation
print("=" * 100)
print(f"{'transcript':40} {'arm':8} {'signature':10} {'skillfired':10} {'primary→final'}")
print("-" * 100)
for r in rows:
    sig = "PRESENT" if r["final_present"] else "absent"
    flip = "" if r["primary_present"] == r["final_present"] else "  (VERIFIER FLIPPED)"
    print(f"{r['key']+'__'+r['arm']+'__r'+r['run']:40} {r['arm']:8} {sig:10} "
          f"{('yes' if r['skill_fired'] else 'no'):10} {r['primary_present']}→{r['final_present']}{flip}")

print("\n" + "=" * 118)
print("PER-GOVERNOR MEASUREMENT TABLE  (behavior = pre-registered signature; fire = governor Skill actually loaded)")
print("=" * 118)
hdr = f"{'governor':20} {'behav-with':11} {'behav-without':13} {'delta':7} {'fire-with':10} {'fire-without':13} {'GATE'}"
print(hdr); print("-" * len(hdr))
summary = []
leak = False
for g in GOVS:
    gw = [r for r in rows if r["governor"] == g and r["arm"] == "with"]
    go = [r for r in rows if r["governor"] == g and r["arm"] == "without"]
    w = sum(1 for r in gw if r["final_present"]); wn = len(gw)
    o = sum(1 for r in go if r["final_present"]); on = len(go)
    sfw = sum(1 for r in gw if r["skill_fired"])
    sfo = sum(1 for r in go if r["skill_fired"])   # CONFOUND SENTINEL: must be 0
    if sfo > 0: leak = True
    delta = (w / wn if wn else 0) - (o / on if on else 0)
    gate = "PASS" if (wn and w >= 3 and o == 0) else "FAIL"
    note = ""
    if o >= 3 and w >= 3:
        note = "WITHOUT also shows it — base model does it"
    if sfw == 0:
        note = (note + "; " if note else "") + "governor never fired (triggering-limited; with-arm=base model)"
    print(f"{g:20} {str(w)+'/'+str(wn):11} {str(o)+'/'+str(on):13} "
          f"{delta*100:+4.0f}%  {str(sfw)+'/'+str(wn):10} {str(sfo)+'/'+str(on):13} {gate}")
    if note: print(f"{'':20} └─ {note}")
    summary.append({"governor": g, "behav_with": f"{w}/{wn}", "behav_without": f"{o}/{on}",
                    "delta_pct": round(delta*100), "fire_with": f"{sfw}/{wn}",
                    "fire_without": f"{sfo}/{on}", "gate": gate, "note": note})
print("-" * len(hdr))
print(f"CONFOUND SENTINEL — governor fires in WITHOUT arm: {'!!! LEAK (control contaminated)' if leak else 'clean (0 across all governors)'}")

json.dump({"rows": rows, "summary": summary},
          open(os.path.join(BASE, "phase2_scored.json"), "w"), indent=2)
print("\nwrote phase2_scored.json")
