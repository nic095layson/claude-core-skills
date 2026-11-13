#!/usr/bin/env python3
"""Walk the weekly run as a transcript, tool call by tool call, through every gate, with two hook sets.

Run:  python3 /tmp/claude-0/-home-user/ff01f16c-7b3f-5ea5-8051-7a95ac7cd1d1/scratchpad/merge-audit/work/rev-weekly-run/run_walk.py [variant ...]

For each assistant tool call it prints whether the PreToolUse turn gate is wired to that tool at all (the matcher
in lib/plugin/core-governance/hooks/hooks.json) and, if so, the gate's verdict given the rows before the call.
At the end of the run it prints the two Stop gates' verdicts. Hook sentinels go to work/rev-weekly-run/tmp.
"""
import os
import re
import sys

PACK = "/tmp/claude-0/-home-user/ff01f16c-7b3f-5ea5-8051-7a95ac7cd1d1/scratchpad/merge-audit"
W = PACK + "/work/rev-weekly-run"
os.makedirs(W + "/tmp", exist_ok=True)
os.environ["TMPDIR"] = W + "/tmp"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True
sys.path.insert(0, W)
import bb_cases as B  # noqa: E402  (row builders for the seven steps)
mk = B.mk

SETS = [("merged 0.1.5", PACK + "/lib/plugin/core-governance/scripts"),
        ("account 0.1.4", PACK + "/account/plugin/core-governance/scripts")]
# PreToolUse matcher of the turn gate, copied from lib/plugin/core-governance/hooks/hooks.json
MATCHER = re.compile(r"^(?:Edit|Write|NotebookEdit|Bash|mcp__.*__(merge_pull_request|create_pull_request|update_pull_request|"
                     r"push_files|create_or_update_file|delete_file))$")

# variant: the plan table is NOT recorded in the transcript (pack/real-text-recording.txt: all three plan tables of
# 2026-11-12 are missing from the operations session's transcript)
PG_UNRECORDED = [mk.skill("plan-gate"), mk.result("Launching skill: plan-gate")]

VARIANTS = {
    "as-ordered": B.QUIET + B.FULL,
    "as-ordered-plan-text-unrecorded": B.QUIET + B.wake() + PG_UNRECORDED + B.s1() + B.s2_list() + B.s3() + B.s4() + B.s5() + B.AV + B.s6() + B.s7(),
    "stop-path": B.QUIET + B.wake() + B.PG + B.s1() + B.s2_list("[three unmerged]") + B.s2_disable(),
    "no-governors": B.QUIET + B.wake() + B.s1() + B.s2_list() + B.s3() + B.s4() + B.s5() + B.s6() + B.s7(),
    "no-governors-gives-up-before-push": B.QUIET + B.wake() + B.s1() + B.s2_list() + B.s3() + B.s4() + B.s5()
                                           + [mk.say("Push was not attempted; report left in the working tree.")],
}


def short(name, inp):
    if name == "Bash":
        return "Bash: " + inp.get("command", "")[:88]
    if name == "Skill":
        return "Skill: " + inp.get("skill", "")
    if name == "Write":
        return "Write: " + inp.get("file_path", "")[-52:]
    return name


def walk(vname, rows):
    path = mk.write(rows, keep_dir=B.FX, name="walk-" + vname + ".jsonl")
    print("\n=== variant: %s  (fixture %s, %d rows)" % (vname, path.replace(PACK + "/", ""), len(rows)))
    print("%-92s | %-9s | %-16s | %-16s" % ("tool call, in order", "gate wired", SETS[0][0], SETS[1][0]))
    for i, d in enumerate(rows):
        if d.get("type") != "assistant":
            continue
        for b in d["message"]["content"]:
            if b.get("type") != "tool_use":
                continue
            name, inp = b["name"], b["input"]
            wired = bool(MATCHER.match(name))
            got = []
            for label, hooks in SETS:
                if not wired:
                    got.append("not run")
                    continue
                v, _ = mk.run_pre(rows[:i], name, inp, hooks=hooks, session_id="walk-" + vname + "-" + label.split()[1])
                got.append(v)
            print("%-92s | %-9s | %-16s | %-16s" % (short(name, inp)[:92], "yes" if wired else "NO", got[0], got[1]))
    for label, hooks in SETS:
        v, why = mk.run_stop(path, hooks=hooks)
        r, rwhy = mk.run_receipt(path, hooks=hooks)
        print("END OF RUN  %-14s Stop gate: %-10s receipt gate: %-6s %s" % (label, v, r, ("| " + why[:150]) if why else ""))


if __name__ == "__main__":
    pick = sys.argv[1:] or list(VARIANTS)
    for v in pick:
        walk(v, VARIANTS[v])
