#!/usr/bin/env python3
"""Orchestrator's own second reproduction (own fixtures, nothing reused from the finders) of the findings
that only ONE agent reported and no second agent re-ran. Columns: finding | case | rule requires | merged hooks say."""
import os, shutil, subprocess, sys, tempfile
P = "/tmp/claude-0/-home-user/ff01f16c-7b3f-5ea5-8051-7a95ac7cd1d1/scratchpad/merge-audit"
sys.path.insert(0, P + "/pack/tools")
import mk
M = "mcp__github__merge_pull_request"
commit = lambda: mk.tool("Bash", command="git add -A && git commit -qm x")
push = lambda: mk.tool("Bash", command="git push -u origin claude/x")
err = lambda: {"type": "user", "message": {"role": "user", "content": [
    {"type": "tool_result", "tool_use_id": "t", "is_error": True, "content": "Error: Unknown skill"}]}}
rows_out = []
def show(fid, label, want, got):
    rows_out.append((fid, label, want, got, "" if got == want else "  <-- differs"))

# TB-5 receipt gate: a bare inability claim, then a harness-written string row (a skill re-invocation echo), then a closing line
base = [mk.owner("check whether the service is reachable"), mk.say("I couldn't verify whether the service is reachable.")]
show("ctl", "receipt: bare claim, stop right after it", "block", mk.run_receipt(base)[0])
show("TB-5", "receipt: same claim, then a skill re-invocation row (string, isMeta), then 'Done.'", "block",
     mk.run_receipt(base + [mk.skill("plan-gate"), mk.meta("(Re-invocation of /plan-gate - the skill instructions were previously loaded)"), mk.say("Done.")])[0])
show("TB-5", "receipt: same claim, then a task-notification row, then 'Done.'", "block",
     mk.run_receipt(base + [mk.harness("<task-notification><status>completed</status></task-notification>"), mk.say("Done.")])[0])

# TB-7 prompt-class half and a scheduled run
sched = [mk.tool("ReadNotifications"), mk.notif(mk.SCHED), mk.tool("Bash", command="ls"), mk.result("a b"), mk.say("Weekly report: nothing drifted.")]
show("ctl", "stop: scheduled run after the owner's 'thanks'", "allow", mk.run_stop([mk.owner("thanks"), mk.say("Welcome.")] + sched)[0])
show("TB-7", "stop: the SAME scheduled run after the owner's one-line review question", "allow",
     mk.run_stop([mk.owner("Quick sanity check: is this right, 2+2=4?"), mk.say("Yes.")] + sched)[0])

# F1-1 delegate does the outward work
show("ctl", "stop: main turn commits, no governor", "block:F1", mk.run_stop([mk.owner("Continue"), commit(), mk.result("ok"), mk.say("done")])[0])
show("F1-1", "stop: main turn only calls Agent; the delegate commits and pushes; no governor", "block:F1",
     mk.run_stop([mk.owner("Continue"), mk.tool("Agent", description="ship it", prompt="commit and push the change"), mk.result("Committed and pushed; PR opened."), mk.say("done")])[0])

# F1-2 after any Stop block, F1 does not look again
show("F1-2", "stop (retry flag set after ANOTHER hook's block): ungoverned commit + push since", "block:F1",
     mk.run_stop([mk.owner("Continue"), mk.say("I couldn't verify it."), commit(), mk.result("ok"), push(), mk.result("ok"), mk.say("done")], active=True)[0])

# F1-5 the same miss is raised again at every later stop of the turn
t = [mk.owner("Continue"), push(), mk.result("ok"), mk.say("pushed")]
after = t + [mk.skill("plan-gate"), mk.skill("adversarial-verify"), mk.say("The plan comes after the action this time. Goal: ... Verified: ...")]
show("ctl", "stop 1: ungoverned push", "block:F1", mk.run_stop(t)[0])
show("F1-5", "stop 3: both governors loaded as ordered, then a notification wake and one line", "allow",
     mk.run_stop(after + [mk.harness("<task-notification><status>completed</status></task-notification>"), mk.say("Noted.")])[0])

# F1-8 a Skill call that errored counts as a load
show("F1-8", "stop: Skill(plan-gate) and Skill(adversarial-verify) both returned an error; then commit", "block:F1",
     mk.run_stop([mk.owner("Continue"), mk.skill("plan-gate"), err(), mk.skill("adversarial-verify"), err(), commit(), mk.result("ok"), mk.say("done")])[0])

# F2-8 honest merge refused: the assistant named the PR without '#', the owner said yes
show("F2-8", "merge 34 after assistant 'Shall I merge PR 34 and PR 141?' and owner 'yes, both'", "allow",
     mk.run_pre([mk.owner("status?"), mk.say("Both are green. Shall I merge PR 34 and PR 141?"), mk.owner("yes, both")], M, {"pullNumber": 34})[0])
show("F2-8", "merge after a click on 'Yes, both (Recommended)' to the question 'Merge the two PRs?'", "allow",
     mk.run_pre([mk.owner("status?"), mk.tool("AskUserQuestion", questions=[]), mk.answer('"Merge the two PRs?"="Yes, both (Recommended)"')], M, {"pullNumber": 34})[0])

# TB-6 an unattended wake after the turn stopped still carries the earlier click
show("TB-6", "merge of an unrelated PR 150 after: click 'Merge both', merges, stop, then a task-notification wake", "(not stated)",
     mk.run_pre([mk.owner("build it"), mk.tool("AskUserQuestion", questions=[]), mk.answer('"Merge the PRs?"="Merge both (Recommended)"'),
                 mk.tool(M, pullNumber=34), mk.result("merged"), mk.say("Merged."),
                 mk.harness("<task-notification><status>completed</status></task-notification>"), mk.say("A check finished.")], M, {"pullNumber": 150})[0])

print("%-5s | %-13s | %-18s | %s" % ("id", "rule requires", "merged hooks say", "case"))
for fid, label, want, got, flag in rows_out:
    print("%-5s | %-13s | %-18s | %s%s" % (fid, want, got, label, flag))

# TB-8 / F1-7 / RI-5: one mutation of my own. Make "no owner message" DENY a merge (the opposite of today) and run the library's selftest.
d = tempfile.mkdtemp(prefix="mut-")
shutil.copytree(P + "/lib/hooks", d + "/hooks", ignore=shutil.ignore_patterns("__pycache__"))
f = d + "/hooks/turn-gates-pretool.py"; s = open(f).read()
old = "    if li < 0:\n        sys.exit(0)\n"
assert s.count(old) == 1, "mutation target not found exactly once"
open(f, "w").write(s.replace(old, "    if li < 0:\n        deny('mutant: no owner message') if turngate.is_merge(block) else sys.exit(0)\n"))
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
a = subprocess.run(["python3", P + "/lib/hooks/selftest-turn-gates.py"], capture_output=True, text=True, env=env).stdout.strip().split("\n")[-1]
b = subprocess.run(["python3", d + "/hooks/selftest-turn-gates.py"], capture_output=True, text=True, env=env).stdout.strip().split("\n")[-1]
chk = mk.run_pre([mk.compact_summary("continued"), mk.say("Continuing.")], M, {"pullNumber": 9}, hooks=d + "/hooks")[0]
print("\nmutation of my own (a merge with no owner message is DENIED instead of allowed):")
print("  unmutated selftest:", a); print("  mutated selftest:  ", b); print("  mutant really denies that case:", chk)
shutil.rmtree(d)
