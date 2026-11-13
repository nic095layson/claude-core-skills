#!/usr/bin/env python3
"""F2-7: when the transcript the hook reads holds no owner message, the hook exits before the merge check: every merge passes.

Rule: lib/hooks/turn-gates-pretool.py:45 ("A scheduled run carries no owner message, so it carries no owner word to
merge: it never merges."); lib/hooks/README.md:15-16 ("a PR merge is denied without the owner's word").
Code: turn-gates-pretool.py:42-43 `if li < 0: sys.exit(0)` runs before the check; turngate.py:205-206 `if li < 0:
return False` (the check itself would refuse) is never reached.
Part 2 asks the REAL record through pack/tools/replay_real.py (labels only): at which real stop points did the
transcript hold no owner row and no scheduled row.
"""
import os
import subprocess
import sys
from h2 import O, S, M, pr, pair, notif, case, mk, PACK, HERE, FX, flat

boundary = {"type": "system", "subtype": "compact_boundary", "content": "Conversation compacted"}
summary = mk.compact_summary("This session is being continued from a previous conversation that ran out of context. Summary: the weekly "
                             "scheduled review was running; draft PR #36 is open. The owner's standing rule: do not merge without his word.")
slash = mk.harness("<command-name>/council</command-name>\n<command-message>council</command-message>\n<command-args>should we ship the QA loop?</command-args>")

print("== controls ==")
case("F2-7-ctl1", [O("ok")], M, pr(36), "deny", show=False, label="an owner row without the word")
case("F2-7-ctl2", [O("ok"), notif(mk.SCHED)], M, pr(36), "deny", show=False, label="a scheduled run")

print("\n== part 1: no owner row in the file ==")
case("F2-7a", [boundary, summary, S("Continuing the weekly review."), pair("Bash", {"command": "git status --short"}, "")], M, pr(36), "deny", show=False,
     label="the file starts at a compaction boundary (system compact_boundary + isCompactSummary row), as the real record does")
case("F2-7b", [slash, S("Council verdict: ship.")], M, pr(34), "deny", show=False, label="the session's only owner input so far is a slash command (marker row)")
case("F2-7c", [], M, pr(34), "deny", show=False, label="empty transcript")
case("F2-7d", flat([O("ok")]) + ["x"], M, pr(34), "deny", show=False,
     label="owner 'ok' + one line that is a JSON string, not an object (without that line: DENY, see ctl1)")

print("\n== part 2: the REAL record (stop probe; 'no-owner-row' = the hook would have exited before any merge check) ==")
r = subprocess.run([sys.executable, os.path.join(PACK, "pack", "tools", "replay_real.py"), "--hooks", os.path.join(HERE, "hooks-probe"), "--what", "stop"],
                   capture_output=True, text=True, env=dict(os.environ, ATK_STOP_PROBE="1"))
WORDS = {"BLOCK:prompt-class": "no-owner-row", "BLOCK:F1": "open-for-any-PR", "allow": "closed", "BLOCK:receipt": "scheduled"}
pts = [(l[2:18], WORDS.get(l.split("| now:")[1].split("/")[0].strip(), "?")) for l in r.stdout.splitlines() if l.startswith("  20") and "| now:" in l]
print("   %d real stop points; first four: %s" % (len(pts), "  ".join("%s=%s" % p for p in pts[:4])))
print("   no-owner-row at %d of %d; open-for-any-PR at %d of %d" % (sum(v == "no-owner-row" for _, v in pts), len(pts), sum(v == "open-for-any-PR" for _, v in pts), len(pts)))
print("   pack/tools/replay_real.py:6-7 says of the record: " + " ".join(l.strip() for l in open(os.path.join(PACK, "pack", "tools", "replay_real.py")).read().splitlines()[5:7]))
