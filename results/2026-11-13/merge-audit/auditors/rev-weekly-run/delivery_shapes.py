#!/usr/bin/env python3
"""delivery_shapes.py — does the gate recognise the weekly run under other shapes of the notification row?

Run:  python3 /tmp/claude-0/-home-user/ff01f16c-7b3f-5ea5-8051-7a95ac7cd1d1/scratchpad/merge-audit/work/rev-weekly-run/delivery_shapes.py

Each case: the owner's last message says "merge it"; then the weekly prompt arrives in the shape named; then the run
calls the merge tool. "deny:scheduled" = the gate saw a scheduled run. Hook set: the merged plugin 0.1.5.
Realism: D1 is the shape recorded in the kit session (kit/after-report-2026-11-04-turn-gate-scheduled.md section 1).
D2 (several notifications in one read) follows the header's own 'N of M' counter. D3-D5 are shapes NOT seen in
pack/real-row-shapes.md for a notification read; they are here to show what the recognition depends on.
"""
import os
import sys

PACK = "/tmp/claude-0/-home-user/ff01f16c-7b3f-5ea5-8051-7a95ac7cd1d1/scratchpad/merge-audit"
W = PACK + "/work/rev-weekly-run"
os.makedirs(W + "/tmp", exist_ok=True)
os.environ["TMPDIR"] = W + "/tmp"
sys.path.insert(0, W)
sys.dont_write_bytecode = True
import bb_cases as B  # noqa: E402
mk = B.mk
HOOKS = PACK + "/lib/plugin/core-governance/scripts"

PRE = "[SYSTEM NOTIFICATION - NOT USER INPUT]\nExactly %d notification%s queued for this session.\n" + mk.EXPLAIN + "\n\n"
HDR = "--- Notification %d of %d · id: dfc64dcd-000%d · origin: %s · queued at: 2026-11-16T14:43:00Z · reached this session 3s before this read ---\n"


def res(content):
    return {"type": "user", "message": {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "toolu_n", "content": content}]}}


one = PRE % (1, " was") + HDR % (1, 1, 1, mk.SCHED) + B.PROMPT + "\n"
two = PRE % (2, "s were") + HDR % (1, 2, 1, mk.GITHUB) + "CI passed on #34\n" + HDR % (2, 2, 2, mk.SCHED) + B.PROMPT + "\n"
CASES = [
    ("D1 one notification, tool_result content is a string (the recorded shape)", [res(one)]),
    ("D2 a GitHub and the scheduled notification in ONE read (string)", [res(two)]),
    ("D3 content is a list holding one text block", [res([{"type": "text", "text": one}])]),
    ("D4 content is a list of two text blocks: preamble | header+body", [res([{"type": "text", "text": PRE % (1, " was")},
                                                                               {"type": "text", "text": HDR % (1, 1, 1, mk.SCHED) + B.PROMPT}])]),
    ("D5 the stored prompt arrives as a plain user row (no ReadNotifications)", [mk.harness(B.PROMPT)]),
]
head = [mk.owner("merge it"), mk.say("Merged #34."), mk.tool("ReadNotifications")]
print("%-78s | merge tool in the run | Stop after an ungoverned push" % "shape of the row that delivers the weekly prompt")
for name, rows in CASES:
    r = head + rows
    v, _ = mk.run_pre(mk.write(r, keep_dir=B.FX, name=name[:2] + ".jsonl"), "mcp__github__merge_pull_request", B.MERGE35, hooks=HOOKS)
    # an owner turn that was fully governed, then the run pushes with no governor: block:F1 only if the run is its own turn
    g = [mk.owner("Continue")] + B.PG + [mk.tool("Bash", command="git push origin claude/x"), mk.result("ok")] + B.AV + [mk.say("done"), mk.tool("ReadNotifications")] \
        + rows + [mk.tool("Bash", command=B.PUSH), mk.result("ok"), mk.say("PR opened.")]
    s, _ = mk.run_stop(mk.write(g, keep_dir=B.FX, name=name[:2] + "-stop.jsonl"), hooks=HOOKS)
    print("%-78s | %-21s | %s" % (name, v, s))
