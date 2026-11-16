#!/usr/bin/env python3
"""stop_rule.py — the weekly task's stop rule on concrete pull-request histories.

Run:  python3 /tmp/claude-0/-home-user/ff01f16c-7b3f-5ea5-8051-7a95ac7cd1d1/scratchpad/merge-audit/work/rev-weekly-run/stop_rule.py

This is a model of the RULE TEXT, not of any code (no code implements the rule; a session must decide it from what the
GitHub tools return). It evaluates, on the same history, the rule the owner was TOLD and the rule as STORED, and
prints where they part.

TOLD    pack/pr34-and-claims.md:47  "it switches itself off after 3 runs in a row with nothing you merge"
        lib/results/2026-11-12/qa-loop/AUDIT.md:83  "if 3 runs in a row produce nothing you merge, it stops"
        lib/experiments/hypothesis-2026-11-12-qa-loop.md:12  "stops itself after 3 consecutive runs whose PRs were not merged"
STORED  pack/trigger-prompt.md:21  "List the library's pull requests whose title starts "Weekly QA review" ... If the
        three most recent ones are all closed without merge or still open and untouched by the owner, do not open a
        fourth: disable this scheduled task"

The stored rule leaves "untouched by the owner" undefined. Two readings a session could take from GitHub data:
  S-a  touched = the owner's login did something on the PR after it was opened (comment, review, push, label, edit)
  S-b  touched = any activity by the owner's login, opening included. (The session opens the PR with the owner's GitHub
       connection; whether GitHub shows the session's actions under the owner's login is NOT in the pack: unknown.)
"""

# a run = (what the run left on GitHub, what the owner then did)
#   pr: None (the run opened no PR) or dict(state=open|closed, merged=bool, owner_events=int after opening)
def pr(state, merged=False, owner_events=0):
    return dict(state=state, merged=merged, owner_events=owner_events)


HISTORIES = [
    ("H1 three runs, three draft PRs, the owner never opens GitHub",
     [pr("open"), pr("open"), pr("open")], "nothing merged"),
    ("H2 three runs, three draft PRs, the owner reads each and comments 'not now', merges none",
     [pr("open", owner_events=1), pr("open", owner_events=1), pr("open", owner_events=1)], "nothing merged"),
    ("H3 three runs, each fails before step 6 (push refused, GitHub tools absent, run cut short): no PR exists",
     [None, None, None], "nothing merged"),
    ("H4 ten such failing runs", [None] * 10, "nothing merged"),
    ("H5 three runs; the owner closes each PR unmerged",
     [pr("closed"), pr("closed"), pr("closed")], "nothing merged"),
    ("H6 one merged long ago, then two closed unmerged, then one run that opened no PR",
     [pr("closed", merged=True), pr("closed"), pr("closed"), None], "nothing merged in the last 3 runs"),
    ("H7 three runs; the owner answers in the chat each week, has one proposal built and merges THAT pull request; report PRs left open",
     [dict(pr("open"), built_and_merged=True), dict(pr("open"), built_and_merged=True), dict(pr("open"), built_and_merged=True)],
     "something the run produced was merged each week"),
]


def told(runs):
    last3 = runs[-3:]
    return len(last3) == 3 and all(not (p and (p["merged"] or p.get("built_and_merged"))) for p in last3)


def stored(runs, touched):
    prs = [p for p in runs if p is not None][-3:]          # "the three most recent ones" (pull requests, not runs)
    if len(prs) < 3:
        return False
    return all((p["state"] == "closed" and not p["merged"]) or (p["state"] == "open" and not touched(p)) for p in prs)


def t_a(p):
    return p["owner_events"] > 0


def t_b(p):
    return True   # the PR itself was opened under the owner's login


print("%-104s | %-6s | %-10s | %-10s" % ("history (what the fourth run, or the run after the last one listed, finds)", "TOLD", "STORED S-a", "STORED S-b"))
for name, runs, _ in HISTORIES:
    row = ["STOP" if told(runs) else "go on", "STOP" if stored(runs, t_a) else "go on", "STOP" if stored(runs, t_b) else "go on"]
    flag = "" if len(set(row)) == 1 else "   <-- the readings part"
    print("%-104s | %-6s | %-10s | %-10s%s" % (name[:104], row[0], row[1], row[2], flag))

# Evidence for S-b from the pack: who GitHub records as the author of a merge the SESSION made with its merge tool
# (pack/replay-baseline.txt: the owner turn from 2026-11-12T21:23 made the merge calls; PR #34 merged 21:35:59Z).
import subprocess
PACK = "/tmp/claude-0/-home-user/ff01f16c-7b3f-5ea5-8051-7a95ac7cd1d1/scratchpad/merge-audit"
out = subprocess.run(["git", "-C", PACK + "/lib", "log", "-1", "--format=%h author=%an committer=%cn | %s", "1ce99d5"],
                     capture_output=True, text=True).stdout.strip()
print("\nGitHub's record of a merge the session itself performed:  " + out)
print("-> the session acts under the owner's login, so GitHub's author fields cannot tell the owner's touch from the session's own.")
