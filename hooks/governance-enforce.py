#!/usr/bin/env python3
"""Stop hook: two rules, both on the turn model in turngate.py.

Outward actions. The stretch this stop answers for (the rows since the owner's latest message or the latest
completed stop) committed, pushed, created, updated or merged a pull request, pushed a file or changed a
scheduled task: plan-gate must have been loaded in the governance turn before the first such action, and
adversarial-verify anywhere in it. After a compaction both must be loaded again before the next such action.
The rule itself is turngate.f1_decision. Blocks at most F1_MAX_BLOCKS times in one stretch.

Prompt class. The owner's prompts of the turn (the typed message, a slash command's arguments, messages sent
while the assistant worked) are governed-class work (govclass.py) and the governor each class needs was not
loaded: block, at most PROMPT_CLASS_MAX_BLOCKS times in one stretch. Judged only at the first stop after the
owner's message: a scheduled run, and work woken after a completed stop, carry no prompt of the owner's.

What counts as loaded: a Skill call in the governance turn whose name, after any scope prefix, is the
governor's, and whose result is not an error. Governor text a compaction carried over does not count.

The retry flag (stop_hook_active) is true after ANY Stop hook blocked, for the rest of the turn, so it does not
mean "this hook already blocked": each rule counts its own earlier blocks from the record. Only when the flag
is set and the record shows no block at all does a rule let the stop go.

Which way a failure goes: an input or a record that cannot be read, an error here or in turngate.py, and this
hook's own deadline all ALLOW the stop. Every path ends with exit status 0 and prints one JSON object or nothing.
"""
import json
import os
import signal
import sys
import threading
import time

HOOK_DEADLINE_SECONDS = 8           # under the wired timeout: this hook ends itself, quietly, before it is cut off
TRIVIA_MAX_CHARS = 400
TRIVIA_CLASSES = ("review",)        # the only classes a short answer with no tool call may pass without a governor
ACTION_WORDS = {"merge": "merge", "push_default": "push to a default branch", "push": "push", "commit": "commit",
                "pr_write": "pull-request change", "file_push": "file push", "schedule": "scheduled-task change"}
REASON_F1 = ("GOV-ENFORCE: this turn took an outward action (%s) without %s. Load the missing governor with the "
             "Skill tool now and follow it.")
REASON_F1_PLAN_LATE = (" The plan comes after the action this time: say so plainly to the owner, then state the goal "
                       "and what was done.")
REASON_F1_COMPACTION = (" The governors were loaded before a compaction; what a compaction carries over does not "
                        "count, so they must be loaded again before the next commit, push or merge.")
REASON_F1_ANY_PROMPT = " This applies however short the owner's message was ('continue', 'proceed')."
REASON_PROMPT_CLASS = ("GOV-ENFORCE: this is governed work (%s) and you finished WITHOUT loading %s. Load %s with the "
                       "Skill tool now, follow its procedure, and revise your answer before finishing. Governor text "
                       "already in your context from before a compaction does not count: it was loaded for an "
                       "earlier task.")

_answered = threading.Lock()                # taken by whoever ends the hook


def finish(answer):
    """Print the one answer (or nothing) and end with status 0. Only the first caller prints."""
    if not _answered.acquire(False):
        return
    try:
        if answer is not None:
            sys.stdout.write(json.dumps(answer) + "\n")
        sys.stdout.flush()
    except Exception:
        pass
    os._exit(0)


def on_deadline(*_unused):
    finish(None)                            # a Stop hook does not hold ordinary work on its own failure


def arm_deadline():
    if hasattr(signal, "SIGALRM"):
        signal.signal(signal.SIGALRM, on_deadline)
        signal.alarm(HOOK_DEADLINE_SECONDS)
    else:
        timer = threading.Timer(HOOK_DEADLINE_SECONDS, on_deadline)
        timer.daemon = True
        timer.start()


def block(reason):
    return {"decision": "block", "reason": reason}


def outward_rule(turngate, model, path, active):
    blocked, missing, kinds = turngate.f1_decision(model, turngate.ledger_read(path), active)
    if not blocked:
        return None
    reason = REASON_F1 % (", ".join(ACTION_WORDS.get(k, k) for k in kinds), " and ".join(missing))
    if any(m in (turngate.MISSING_PLAN, turngate.MISSING_PLAN_RELOAD) for m in missing):
        reason += REASON_F1_PLAN_LATE
    if any(m in (turngate.MISSING_PLAN_RELOAD, turngate.MISSING_VERIFY_RELOAD) for m in missing):
        reason += REASON_F1_COMPACTION
    reason += (" " + model.f1_note) if model.f1_note else REASON_F1_ANY_PROMPT
    return block(reason)


def prompt_class_rule(turngate, govclass, model, data, active):
    if model.gov_kind != "owner":
        return None                         # a scheduled run, or no owner message on record: no prompt to classify
    if any(row > model.gov_start for row in model.stops_done + model.idle_wakes):
        return None                         # the answer to that prompt was judged at its own stop
    classes = sorted(set(c for prompt in model.owner_prompts() for c in govclass.classify(prompt)
                         if c in govclass.ENFORCED))
    if not classes:
        return None
    needed = set(govclass.GOVERNORS_FOR[c][0] for c in classes)      # the primary governor of every matched class
    loaded = set(governor for _row, _block, governor in model.loads(model.gov_start))
    if needed <= loaded:
        return None
    said = model.prose(model.gov_start, data.get("last_assistant_message"))
    if (all(c in TRIVIA_CLASSES for c in classes) and model.tools_ran(model.gov_start) == 0
            and len("".join(said).strip()) < TRIVIA_MAX_CHARS):
        return None                         # a short answer to a quick check, with no tool call: no governed work
    start = model.stretch_start
    if active and not model.feedback(start):
        return None                         # the flag is set and the record shows no block: the one retry
    if len(model.feedback(start, turngate.own_prompt_class_block)) >= turngate.PROMPT_CLASS_MAX_BLOCKS:
        return None
    missing = sorted(needed - loaded)
    return block(REASON_PROMPT_CLASS % (", ".join(sorted(needed)), "it" if len(needed) == 1 else "all of it", missing[0]))


def main():
    data = json.loads(sys.stdin.read())
    if not isinstance(data, dict):
        return None
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import govclass
    import turngate
    path = data.get("transcript_path")
    rows = turngate.load(path) if isinstance(path, str) and path else []
    if not any(row.get("type") != "BAD" for row in rows):
        return None                         # no record to judge
    model = turngate.Model(rows)
    active = bool(data.get("stop_hook_active"))
    return (outward_rule(turngate, model, path, active)
            or prompt_class_rule(turngate, govclass, model, data, active))


if __name__ == "__main__":
    arm_deadline()
    try:
        answer = main()
    except BaseException:
        answer = None
    finish(answer)
    time.sleep(HOOK_DEADLINE_SECONDS)       # reached only while the deadline's timer thread is ending the hook
    os._exit(0)
