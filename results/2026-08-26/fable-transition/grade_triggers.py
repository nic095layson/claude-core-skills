#!/usr/bin/env python3
"""Grade step-3 trigger transcripts. FIRED := the case's own governor Skill tool was
invoked (same parser as every prior campaign run). Also: served model per run,
retired-skill sentinel, canary silence, co-fire scan, Stop-hook block count.
Transcript name: <gov>__id<N>__with__r<n>.jsonl"""
import json, os, glob
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
TRANS = os.path.join(BASE, "transcripts")
RETIRED = {"live-state-truth", "lessons-ledger"}
SEL = {
    "plan-gate":          {"fire": [1, 2, 3], "silent": [4, 5]},
    "adversarial-verify": {"fire": [6, 7, 8], "silent": [4, 5]},
    "scope-fence":        {"fire": [1, 2, 3, 8], "silent": [4, 5]},
}
ANCHOR = {   # 2026-07-11 FINAL ACCEPTANCE, claude-opus-4-8[1m], no hooks
    "plan-gate":          "fire 6/6, silent 4/4",
    "adversarial-verify": "fire 6/6, silent 4/4",
    "scope-fence":        "core 6/6 that run (id1 flaky 3/5 anchor), id8 0/2, silent 4/4",
}


def parse(path):
    fired, served, blocks = [], None, 0
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        if "Receipt law (adversarial-verify rule 6)" in line:
            blocks += 1
        try:
            e = json.loads(line)
        except Exception:
            continue
        if e.get("type") == "system" and e.get("model") and served is None:
            served = e["model"]
        if e.get("type") == "assistant":
            for b in e.get("message", {}).get("content", []):
                if b.get("type") == "tool_use" and b.get("name") == "Skill":
                    inp = b.get("input", {}) or {}
                    fired.append(inp.get("skill") or inp.get("command") or "?")
    return fired, served, blocks


rows = []
for path in sorted(glob.glob(os.path.join(TRANS, "*__id*__with__r*.jsonl"))):
    base = os.path.basename(path)[:-6]
    keypart, run = base.rsplit("__r", 1)
    keypart = keypart[: -len("__with")]
    gov, idpart = keypart.split("__id")
    fired, served, blocks = parse(path)
    rows.append({"gov": gov, "id": int(idpart), "run": int(run), "fired": fired,
                 "self": gov in fired, "retired": [s for s in fired if s in RETIRED],
                 "served": served, "blocks": blocks})

print(f"transcripts graded: {len(rows)}")
off = [r for r in rows if r["served"] != "claude-fable-5"]
print(f"served-model check: {len(rows)-len(off)}/{len(rows)} served claude-fable-5"
      + (f"   !! OFF-MODEL: {[(r['gov'], r['id'], r['run'], r['served']) for r in off]}" if off else ""))
print(f"Stop-hook blocks observed: {sum(r['blocks'] for r in rows)} across all runs\n")

bykey = defaultdict(list)
for r in rows:
    bykey[(r["gov"], r["id"])].append(r)

for gov in SEL:
    print(f"===== {gov} =====   anchor: {ANCHOR[gov]}")
    ff = fn = ss = st = 0
    for i in SEL[gov]["fire"]:
        rs = sorted(bykey[(gov, i)], key=lambda x: x["run"])
        hits = sum(1 for x in rs if x["self"])
        supp = (gov == "scope-fence" and i == 8)
        det = "  ".join(f"r{x['run']}={'FIRE' if x['self'] else 'silent'}"
                        + (f"/other:{','.join(x['fired'])}" if x["fired"] and not x["self"] else "") for x in rs)
        print(f"  should-FIRE id{i}{' (supplementary)' if supp else ''}: {hits}/{len(rs)}   [{det}]")
        if not supp:
            ff += hits; fn += len(rs)
    print(f"  --> should-fire (core): {ff}/{fn}   gate >=5/6 : {'PASS' if fn and ff/fn >= 5/6 else 'FAIL'}")
    for i in SEL[gov]["silent"]:
        rs = sorted(bykey[(gov, i)], key=lambda x: x["run"])
        stay = sum(1 for x in rs if not x["self"])
        det = "  ".join(f"r{x['run']}={'silent' if not x['self'] else 'FIRED'}"
                        + (f"/other:{','.join(x['fired'])}" if x["fired"] else "") for x in rs)
        print(f"  should-SILENT id{i}: {stay}/{len(rs)} silent   [{det}]")
        ss += stay; st += len(rs)
    print(f"  --> should-not-silent: {ss}/{st}   gate >=3/4 : {'PASS' if st and ss/st >= 3/4 else 'FAIL'}\n")

print("===== CANARY (plan-gate id4) =====")
for x in sorted(bykey[("plan-gate", 4)], key=lambda r: r["run"]):
    print(f"  r{x['run']}: fired={x['fired'] or 'NOTHING'} -> {'PASS' if not x['fired'] else 'FAIL'}")
print("\n===== RETIRED-SKILL SENTINEL =====")
hits = [(r["gov"], r["id"], r["run"], r["retired"]) for r in rows if r["retired"]]
print("  !!! " + str(hits) if hits else "  zero retired-skill invocations: PASS")
print("\n===== CO-FIRE scan =====")
multi = [(r["gov"], r["id"], r["run"], r["fired"]) for r in rows if len(set(r["fired"])) > 1]
print("  " + str(multi) if multi else "  none")
