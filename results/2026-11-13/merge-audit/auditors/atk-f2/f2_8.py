#!/usr/bin/env python3
"""F2-8: honest merges the gate refuses (the owner said yes), and a search the gate takes for a merge.

Rule: lib/experiments/hypothesis-2026-10-29-turn-gates.md:22 (a PR merge is denied UNLESS the word is in the owner's
latest message, in a clickable answer after it, or in the assistant's last text before that message together with the
PR's number); lib/CLAUDE.md:88 (doctrine rule 4: decisions are offered as clickable options).
"""
from h2 import O, S, M, pr, pair, click, notif, case, mk, GHM

Q = "Merge the QA-loop PRs (#34 library, #141 deck)?"
print("== control ==")
case("F2-8-ctl", [O("Looks good, merge it.")], M, pr(34), "allow", show=False, label="Looks good, merge it.")

print("\n== against the letter of the rule ==")
case("F2-8a", [S("Both are green. Shall I merge PR 34 and PR 141?"), O("yes, both")], M, pr(34), "allow",
     label="the assistant's last text has the word and the PR's number, written without '#'")
case("F2-8b", [S("Ready to merge: https://github.com/nic095layson/claude-core-skills/pull/34"), O("yes")], M, pr(34), "allow", show=False,
     label="the PR named by its URL")
case("F2-8c", [O("List every place the hooks match a CLI command.")], "Bash", {"command": "grep -rn '%s' hooks/ docs/" % GHM}, "allow",
     label="not a merge: a read-only search for the gate's own pattern")
for k, t in (("d", "No objections, merge it."), ("e", "No concerns — merge both."), ("f", "Yes, why not, merge it.")):
    case("F2-8" + k, [O(t)], M, pr(34), "allow", show=False, label=t + "   <- an order; the 'no'/'not' belongs to another clause")

print("\n== within the letter of the rule, and the owner still said yes ==")
case("F2-8g", [O("what's next?"), click((Q, "Yes, both (Recommended)"), options=["Wait"])], M, pr(34), "allow",
     label="a card whose option does not repeat the word")
case("F2-8h", [O("Merge #34."), S("On it."), O("And fix the typo in the README while you're there.")], M, pr(34), "allow",
     label="a second message arrives before the merge")
case("F2-8i", [S("PR #34 is ready. Shall I merge #34?"), mk.meta("Stop hook feedback: GOV-ENFORCE: this is governed work (adversarial-verify not loaded)"),
               pair("Skill", {"skill": "adversarial-verify"}, "Launching skill: adversarial-verify"),
               S("adversarial-verify is loaded; the report above stands."), O("yes")], M, pr(34), "allow",
     label="the library's own Stop gate made the assistant write one more text after its question")
case("F2-8j", [O("Merge #34 as soon as CI is green."),
               pair("mcp__claude-code-remote__send_later", {"delay_minutes": 5, "message": "Re-check CI on #34"}, "scheduled"),
               notif(mk.SCHED, "Re-check CI on #34")], M, pr(34), "allow",
     label="a scheduled reminder is read later in the same turn")
case("F2-8k", [O("thanks"), notif(mk.SCHED, "Weekly QA self-improvement review ..."),
               click(("Merge the weekly-review PR #36?", "Merge it (Recommended)"))], M, pr(36), "allow",
     label="the owner answers a card left by a scheduled run")
