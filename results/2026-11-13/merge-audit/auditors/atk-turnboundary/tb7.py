#!/usr/bin/env python3
"""atk-turnboundary TB-7: the Stop gate's prompt-class half does not use the scheduled-run boundary.
Usage (any directory): python3 <this file>"""
import os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
os.environ["TMPDIR"] = os.path.join(HERE, "tmp"); os.makedirs(os.environ["TMPDIR"], exist_ok=True)
import tb
from tb import mk, RN, keep
Q = "quick sanity check: 2+2=4, right?"
run = [RN(), mk.notif(mk.SCHED), mk.tool("Bash", command="bash .claude/skills/independent-audit/scripts/weekly_review.sh"), mk.result("3 sections printed"),
       mk.say("Weekly review: no new corrections this week and nothing drifted. Nothing to propose.")]
def stop(name, expected, rows, note=""):
    v, reason = mk.run_stop(keep(name, rows))
    print("%s %s | stop | rule requires=%s | hooks say=%s | %s" % ("ok" if v == expected else "DIFF", name, expected, v, note))
    if v != "allow":
        print("reason: " + reason[:170])
stop("tb7-control-owner-trivia-question-alone", "allow", [mk.owner(Q), mk.say("Yes, 4.")], "(control: the owner's turn itself passes, trivia allowance)")
stop("tb7-control-run-after-ungoverned-owner-msg", "allow", [mk.owner("thanks"), mk.say("Welcome.")] + run, "(control: the same scheduled run after 'thanks')")
stop("tb7-same-run-after-owner-trivia-question", "allow", [mk.owner(Q), mk.say("Yes, 4.")] + run, "<- the same scheduled run, blocked for the owner's earlier question")
build = "Build a script that processes the three sample files and outputs valid JSON."
stop("tb7-run-rides-on-owner-turn-plan-gate", "allow", [mk.owner(build), mk.skill("plan-gate"), mk.say("Goal: x"), mk.say("Here is the script.")] + run,
     "(informational: here the run passes only because the OWNER's turn loaded plan-gate)")
