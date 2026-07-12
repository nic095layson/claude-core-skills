#!/usr/bin/env python3
"""Grade the FINAL ACCEPTANCE transcripts. FIRED := the case's own governor Skill
tool was invoked (same parser as Phase 1). Also flags: any retired-skill invocation
(sentinel), cross-governor co-fires, canary silence."""
import json, os, glob, sys
from collections import defaultdict

TRANS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "transcripts")
RETIRED = {"live-state-truth", "lessons-ledger"}

def skills_fired(path):
    fired = []
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        try:
            e = json.loads(line)
        except Exception:
            continue
        if e.get("type") == "assistant":
            for b in e.get("message", {}).get("content", []):
                if b.get("type") == "tool_use" and b.get("name") == "Skill":
                    inp = b.get("input", {}) or {}
                    fired.append(inp.get("skill") or inp.get("command") or "?")
    return fired

# key format: <gov>__id<N>__r<n>.jsonl
rows = []
for path in sorted(glob.glob(os.path.join(TRANS, "*.jsonl"))):
    base = os.path.basename(path)[:-6]
    keypart, run = base.rsplit("__r", 1)
    gov, idpart = keypart.split("__id")
    fired = skills_fired(path)
    rows.append({"gov": gov, "id": int(idpart), "run": int(run),
                 "fired": fired, "self_fired": gov in fired,
                 "retired": [s for s in fired if s in RETIRED]})

# selection classes
SEL = {
    "plan-gate":          {"fire": [1, 2, 3], "silent": [4, 5]},
    "adversarial-verify": {"fire": [6, 7, 8], "silent": [4, 5]},
    "scope-fence":        {"fire": [1, 2, 3, 8], "silent": [4, 5]},
}
ANCHOR = {
    "plan-gate":          {"fire_desc": "9/9 (100%)", "silent_desc": "4/4"},
    "adversarial-verify": {"fire_desc": "6/6 (100%)", "silent_desc": "4/4"},
    "scope-fence":        {"fire_desc": "id1 3/5, id2 2/2, id3 2/2 (~60-67%); id8 0/2", "silent_desc": "4/4"},
}

print(f"total transcripts graded: {len(rows)}\n")
bykey = defaultdict(list)
for r in rows:
    bykey[(r["gov"], r["id"])].append(r)

for gov in SEL:
    print(f"===== {gov} =====   anchor fire={ANCHOR[gov]['fire_desc']}  silent={ANCHOR[gov]['silent_desc']}")
    fire_ids = SEL[gov]["fire"]; silent_ids = SEL[gov]["silent"]
    ff = fn = 0; ss = st = 0
    for i in fire_ids:
        rs = sorted(bykey[(gov, i)], key=lambda x: x["run"])
        hits = sum(1 for x in rs if x["self_fired"])
        tag = " (supplementary)" if (gov == "scope-fence" and i == 8) else ""
        detail = "  ".join(f"r{x['run']}={'FIRE' if x['self_fired'] else 'silent'}{('/co:'+','.join(x['fired'])) if (x['fired'] and not x['self_fired']) else ''}" for x in rs)
        print(f"  should-FIRE id{i}{tag}: {hits}/{len(rs)}   [{detail}]")
        if not (gov == "scope-fence" and i == 8):
            ff += hits; fn += len(rs)
    print(f"  --> should-fire (core): {ff}/{fn}")
    for i in silent_ids:
        rs = sorted(bykey[(gov, i)], key=lambda x: x["run"])
        stay = sum(1 for x in rs if not x["self_fired"])
        detail = "  ".join(f"r{x['run']}={'silent' if not x['self_fired'] else 'FIRED'}{('/other:'+','.join(x['fired'])) if x['fired'] else ''}" for x in rs)
        print(f"  should-SILENT id{i}: {stay}/{len(rs)} stayed silent   [{detail}]")
        ss += stay; st += len(rs)
    print(f"  --> should-not-silent: {ss}/{st}\n")

# canary = plan-gate id4
print("===== CANARY (plan-gate id4, 'what's 15% of 80?') =====")
for x in sorted(bykey[("plan-gate", 4)], key=lambda r: r["run"]):
    print(f"  r{x['run']}: fired={x['fired'] or 'NOTHING'}  -> {'PASS' if not x['fired'] else 'FAIL(fired something)'}")

# retired-skill sentinel across ALL runs
print("\n===== RETIRED-SKILL SENTINEL (all runs) =====")
hits = [(r['gov'], r['id'], r['run'], r['retired']) for r in rows if r['retired']]
if hits:
    print("  !!! RETIRED SKILL FIRED:")
    for h in hits:
        print("   ", h)
else:
    print("  zero invocations of live-state-truth / lessons-ledger across all runs: PASS")

# any co-fire anywhere
print("\n===== CO-FIRE / MULTI-FIRE scan =====")
for r in rows:
    if len(set(r["fired"])) > 1:
        print(f"  {r['gov']} id{r['id']} r{r['run']}: multiple skills fired = {r['fired']}")
print("(none above = no multi-skill co-fires)")
