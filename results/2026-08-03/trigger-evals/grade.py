#!/usr/bin/env python3
"""Grade trigger-eval transcripts — 2026-08-03.
FIRED := a Skill tool_use invoking the target skill appears in the transcript.
Also records: model, num_turns, which skills (if any) were invoked instead."""
import json, glob, os, collections

SP = "/tmp/claude-0/-home-user-claude-core-skills/04c31d0a-d4ca-53ab-a47d-c619ba8c98e6/scratchpad/evalrun"
EVALS = "/home/user/claude-core-skills/evals"
SKILLS = ["delegation-discipline", "after-report", "application-tailor", "correspondence"]

def skill_invocations(path):
    invoked, model = [], None
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if ev.get("type") == "system" and ev.get("subtype") == "init":
                model = ev.get("model")
            msg = ev.get("message") or {}
            for block in (msg.get("content") or []):
                if isinstance(block, dict) and block.get("type") == "tool_use" and block.get("name") == "Skill":
                    invoked.append((block.get("input") or {}).get("skill") or (block.get("input") or {}).get("command", "?"))
    return invoked, model

rows, models = [], collections.Counter()
for skill in SKILLS:
    spec = json.load(open(f"{EVALS}/{skill}.json"))
    for i, case in enumerate(spec["evals"], 1):
        expect_fire = case["expected_output"].startswith("FIRES")
        for run in (1, 2):
            path = f"{SP}/transcripts/{skill}-id{i}-r{run}.jsonl"
            if not os.path.exists(path) or os.path.getsize(path) == 0:
                rows.append((skill, i, run, expect_fire, None, "MISSING", None))
                continue
            invoked, model = skill_invocations(path)
            models[model] += 1
            fired = skill in invoked
            ok = fired == expect_fire
            rows.append((skill, i, run, expect_fire, fired, "PASS" if ok else "FAIL", ",".join(invoked) or "-"))

print(f"models observed: {dict(models)}\n")
print(f"{'skill':<24}{'id':<4}{'run':<4}{'expect':<8}{'fired':<7}{'grade':<7}invoked")
agg = collections.defaultdict(lambda: [0, 0, 0, 0])  # sf_pass, sf_total, sn_pass, sn_total
for skill, i, run, expect, fired, grade, invoked in rows:
    print(f"{skill:<24}{i:<4}{run:<4}{'FIRE' if expect else 'SILENT':<8}{str(fired):<7}{grade:<7}{invoked}")
    a = agg[skill]
    if expect:
        a[1] += 1; a[0] += grade == "PASS"
    else:
        a[3] += 1; a[2] += grade == "PASS"
print()
for skill in SKILLS:
    sfp, sft, snp, snt = agg[skill]
    sf_ok = sft and sfp / sft >= 5/6
    sn_ok = snt and snp / snt >= 3/4
    print(f"{skill:<24} should-fire {sfp}/{sft}  should-not {snp}/{snt}  "
          f"gate(>=83% SF, >=75% SN): {'PASS' if sf_ok and sn_ok else 'FAIL'}")
