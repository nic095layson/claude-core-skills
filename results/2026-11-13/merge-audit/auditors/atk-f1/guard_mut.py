#!/usr/bin/env python3
"""Does the library's whole pre-commit guard notice F1 being weakened?  Runs in the private worktree work/atk-f1/wt.

Step 1  guard on the untouched worktree (baseline).
Step 2  two LOGIC changes applied to hooks/ AND to the plugin copy (so the parity check stays green):
          (a) F1 is skipped whenever the turn has more than one outward action (e.g. commit AND push);
          (b) a Skill call counts as a governor load when the governor's name appears anywhere in its input.
        Then the guard again, and the weakened hook's verdict on two ungoverned turns.
Step 3  restore; one CONSTANT change (the three scheduled-task suffixes removed), registry check only: control,
        expected to be caught.
The worktree is restored (git checkout -- .) at the end.

Run: python3 <this file>
"""
import os
import shutil
import subprocess
import sys

PACK = "/tmp/claude-0/-home-user/ff01f16c-7b3f-5ea5-8051-7a95ac7cd1d1/scratchpad/merge-audit"
WT = PACK + "/work/atk-f1/wt"
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
sys.dont_write_bytecode = True
sys.path.insert(0, PACK + "/pack/tools")
import mk  # noqa: E402

KEEP = ("turn-gates fixture", "hand-set value", "plugin parity", "classifier + Stop-gate", "RESULT")


def sh(cmd):
    return subprocess.run(cmd, cwd=WT, capture_output=True, text=True, env=ENV)


def guard(label):
    r = sh(["bash", ".claude/skills/diagnostics-and-tooling/scripts/guard_essentials.sh"])
    lines = (r.stdout + r.stderr).splitlines()
    bad = [ln for ln in lines if ln.strip().startswith(("FAIL", "bad", "XX")) or " FAIL" in ln[:8]]
    print("-- guard, %s: exit %d, %d lines" % (label, r.returncode, len(lines)))
    for ln in lines:
        if any(k in ln for k in KEEP) or ln in bad:
            print("   " + ln.strip()[:150])


def patch(rel, old, new):
    for base in ("hooks", "plugin/core-governance/scripts"):
        p = os.path.join(WT, base, rel)
        s = open(p, encoding="utf-8").read()
        assert s.count(old) == 1, (rel, s.count(old))
        open(p, "w", encoding="utf-8").write(s.replace(old, new))


def restore():
    sh(["git", "checkout", "--", "."])
    for d in ("hooks/__pycache__", "plugin/core-governance/scripts/__pycache__"):
        shutil.rmtree(os.path.join(WT, d), ignore_errors=True)


def main():
    restore()
    guard("untouched worktree at 1ce99d5")
    patch("governance-enforce.py", "        if _first is not None:",
          "        if _first is not None and sum(1 for kind, b in _ev if kind == 'tool' and turngate.is_outward(b)) == 1:")
    patch("turngate.py", '''    return str((block.get("input") or {}).get("skill") or "").split(":")[-1].strip()''',
          '''    _s = json.dumps(block.get("input") or {})
    return next((g for g in GOVERNORS if g in _s), "")''')
    print("-- files changed in the worktree: " + ", ".join(ln.strip() for ln in sh(["git", "status", "--short"]).stdout.splitlines()))
    guard("with the two F1 logic changes")
    O = mk.owner("Continue")
    two = [O, mk.tool("Bash", command="git add -A && git commit -qm x"), mk.tool("Bash", command="git push -u origin feat"), mk.say("done")]
    g3 = [O, mk.tool("Skill", skill="after-report", args="no plan-gate this time"), mk.tool("Skill", skill="lessons-ledger", args="adversarial-verify was skipped"),
          mk.tool("Bash", command="git push"), mk.say("done")]
    for label, rows in (("commit then push, no governor", two), ("two OTHER skills whose args name the governors, then push", g3)):
        print("   weakened hooks: %-55s -> %s   | merged hooks -> %s" % (
            label, mk.run_stop(rows, hooks=WT + "/hooks")[0], mk.run_stop(rows, hooks=PACK + "/lib/hooks")[0]))
    restore()
    patch("turngate.py", '''"create_or_update_file", "delete_file", "create_trigger", "update_trigger", "delete_trigger")''',
          '''"create_or_update_file", "delete_file")''')
    r = sh([sys.executable, ".claude/skills/red-team/scripts/registry_check.py", "--root", "."])
    print("-- control, a CONSTANT change (scheduled-task suffixes removed): registry_check exit %d" % r.returncode)
    for ln in (r.stdout + r.stderr).splitlines():
        if "TURN_OUTWARD" in ln or "DRIFT" in ln.upper() or "FAIL" in ln.upper():
            print("   " + ln.strip()[:150])
    r = sh([sys.executable, "hooks/selftest-turn-gates.py"])
    print("   selftest-turn-gates.py on the same change: exit %d %s" % (r.returncode, r.stdout.strip().splitlines()[-1]))
    restore()
    print("-- worktree restored: git status --short prints %r" % sh(["git", "status", "--short"]).stdout.strip())


if __name__ == "__main__":
    main()
