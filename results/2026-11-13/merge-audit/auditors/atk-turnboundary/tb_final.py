#!/usr/bin/env python3
"""atk-turnboundary: last checks (owner text that begins like hook feedback; what must NOT survive an owner boundary).
Usage (any directory): python3 <this file>"""
import os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
os.environ["TMPDIR"] = os.path.join(HERE, "tmp"); os.makedirs(os.environ["TMPDIR"], exist_ok=True)
import tb
from tb import mk, MERGE, COMMIT, governed
print("== owner messages that BEGIN with hook-feedback words (owner_index line 74: startswith GOV-ENFORCE / Stop hook feedback)")
tb.merge("fin-control-owner-says-no", "deny:merge-word", [mk.owner("merge PR 26"), mk.say("merged #26"), mk.owner("The gate fired again. Do not merge PR 27 until I say.")], 27, "(control)")
tb.merge("fin-owner-msg-starts-GOV-ENFORCE", "deny:merge-word", [mk.owner("merge PR 26"), mk.say("merged #26"),
         mk.owner("GOV-ENFORCE fired again on that turn, why? Do not merge PR 27 until I say.")], 27, "<- owner pasted the hook's first word")
tb.stop("fin-owner-msg-starts-Stop-hook-feedback", "block:F1", [mk.owner("build it")] + governed() +
        [mk.owner("Stop hook feedback showed twice. Anyway: commit and push the rest."), mk.tool("Bash", **COMMIT), mk.say("done")], "<- previous turn's governors count")
print("== known answers: approvals and loads must NOT survive an owner boundary")
tb.merge("fin-click-does-not-survive-next-owner-msg", "deny:merge-word", [mk.owner("x"), mk.tool("AskUserQuestion", questions=[]), mk.answer('"Merge PR 26?"="Merge it"'),
         mk.tool(MERGE, pullNumber=26), mk.result("merged"), mk.say("done"), mk.owner("thanks, now look at PR 27")], 27)
tb.stop("fin-loads-do-not-survive-next-owner-msg", "block:F1", [mk.owner("build it")] + governed() + [mk.owner("Continue"), mk.tool("Bash", **COMMIT), mk.say("done")])
tb.merge("fin-sched-run-then-owner-merge-word", "allow", [mk.owner("x"), tb.RN(), mk.notif(mk.SCHED), mk.say("report"), mk.owner("merge PR 57")], 57, "(a scheduled run followed by ordinary work)")
tb.stop("fin-two-sched-runs-second-ungoverned", "block:F1", [mk.owner("x"), tb.RN(), mk.notif(mk.SCHED)] + governed() + [tb.RN(), mk.notif(mk.SCHED), mk.tool("Bash", **COMMIT), mk.say("done")],
        "(second run does not inherit the first run's loads)")
tb.stop("fin-two-sched-notifs-ONE-read-second-task-ungoverned", "AMBIGUOUS", [mk.owner("x"), tb.RN(), tb.multi(mk.SCHED, mk.SCHED)] + governed() + [mk.say("Now the second stored prompt."), mk.tool("Bash", **COMMIT), mk.say("done")],
        "<- two stored prompts delivered by one read are one turn: the second rides on the first's loads")
print("== a harness wake after the turn has stopped: is the owner's earlier click still their word? (documents silent)")
turn = [mk.owner("ship the QA loop"), mk.tool("AskUserQuestion", questions=[]), mk.answer('"Merge the QA-loop PRs (#34 library, #141 deck)?"="Merge both (Recommended)"'),
        mk.tool(MERGE, pullNumber=34), mk.result("merged"), mk.tool(MERGE, pullNumber=141), mk.result("merged"), mk.say("Both merged.")]
wake = [mk.harness("<task-notification>\n<task-type>queued-remote-event</task-type>\n</task-notification>"), tb.RN(), mk.notif(mk.GITHUB, "PR #150 opened by dependabot: checks passed")]
tb.merge("fin-control-next-owner-message-ends-approval", "deny:merge-word", turn + [mk.owner("thanks")] + wake, 150, "(control)")
tb.merge("fin-wake-after-stop-approval-persists", "AMBIGUOUS", turn + wake, 150, "<- unattended wake, PR 150 was never put to the owner")
import collections
try:
    L = [l.split("\t") for l in open(os.path.join(HERE, "probe-log.tsv")).read().splitlines()]
    w = [l for l in L if l[6].endswith("task-notification")]
    print("real-record: %d of %d real stop points were reached through a task-notification wake after an earlier stop; merge of an unrelated PR 99999 there: %s" % (
        len(w), len(L), dict(collections.Counter(l[8].split("=")[1] for l in w))))
    print("real-record: " + open(os.path.join(HERE, "probe-notif.tsv")).read().splitlines()[0] + " (all inside an owner turn by turngate.owner_index; none with a scheduled header)")
except Exception as e:
    print("     (probe files not present: %s)" % e)
