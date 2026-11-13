#!/usr/bin/env python3
"""Test gaps: what lib/hooks/selftest-turn-gates.py (F2 and S cases) does not pin.

Claim: lib/hooks/turn-gates-pretool.py:14-15 ("pinned by hooks/selftest-turn-gates.py"); lib/hooks/README.md:1-3 ("a
scheduled run is a turn of its own, and never merges ... fixture cases S1, S2, S5 fail on the 2026-11-02 hooks").
Part 1 rebuilds every mutant from lib/hooks (one behaviour changed in a private copy) and runs the mutant's own
selftest. Part 2 shows that mutant A (the whole "a scheduled run never merges" block deleted, selftest still 44/44)
lets a scheduled run merge where the merged hooks deny.
"""
import os
import subprocess
import sys
from h2 import O, S, M, pr, click, notif, case, mk, HERE, LIB

print("== part 1: mutants against the library's selftest (SURVIVES = the selftest still reports 0 failed) ==")
sys.stdout.flush()
subprocess.run([sys.executable, os.path.join(HERE, "mutate.py")])
A = os.path.join(HERE, "mut", "A-no-scheduled-deny")
print("\n== part 2: scheduled runs on mutant A (block deleted) vs the merged hooks ==")
rows1 = [O("thanks"), S("Draft PR #36 is open. Ready to merge #36 on your word."), notif(mk.SCHED, "Weekly QA self-improvement review ...")]
rows2 = [O("thanks"), notif(mk.SCHED, "Weekly QA self-improvement review ..."), click(("Merge the weekly-review PR #36?", "Merge it (Recommended)"))]
for cid, rows, why in (("G-a", rows1, "the assistant's last text before the run names #36"), ("G-b", rows2, "a card answered inside the run")):
    case(cid + "-lib", rows, M, pr(36), "deny", hooks=LIB, show=False, label="merged hooks; " + why)
    case(cid + "-mutA", rows, M, pr(36), "deny", hooks=A, show=False, label="mutant A (selftest 44/44); " + why)
