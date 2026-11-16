#!/usr/bin/env python3
"""mk.py — build synthetic session transcripts and run each governance hook against them.

    import sys; sys.path.insert(0, "<PACK>/pack/tools"); import mk

Row builders (each returns ONE transcript row, shaped like the real ones; see pack/real-row-shapes.md):
  mk.owner(text)                 a message the owner typed (string content, the common real shape)
  mk.owner_blocks(text)          the same recorded as a list of text blocks
  mk.say(text)                   assistant text
  mk.tool(name, **input)         assistant tool call (Bash: tool("Bash", command="..."))
  mk.skill(name)                 assistant Skill call; name may carry a prefix ("anthropic-skills:plan-gate")
  mk.result(text)                a tool_result row (user role, list content) with any text
  mk.answer(pairs_text)          the tool_result of an AskUserQuestion, real format:
                                 'Your questions have been answered: "Q"="A". You can now continue with these answers in mind.'
                                 pass pairs_text like '"Merge the PRs?"="Wait"'
  mk.notif(origin=mk.SCHED)      a ReadNotifications tool_result carrying one notification header (real format);
                                 mk.SCHED = a scheduled trigger, mk.GITHUB = GitHub activity, None = no header
  mk.harness(text)               a harness-written user row with string content (e.g. "<task-notification>…")
  mk.meta(text)                  a user row flagged isMeta (loaded skill text, slash-command echo, restart notice)
  mk.compact_summary(text)       a user row flagged isCompactSummary

Runners (return (verdict, detail)); hooks=DIR selects the hook set (default: the merged library's hooks/):
  mk.run_stop(rows, active=False, hooks=None)        governance-enforce.py     "block:F1" | "block:prompt-class" | "allow"
  mk.run_receipt(rows, active=False, hooks=None)     receipt-law-stop-gate.sh  "block" | "allow"
  mk.run_pre(rows, tool_name, tool_input, hooks=None, session_id=None)
                                                     turn-gates-pretool.py     "deny:merge-word" | "deny:scheduled" | "advise" | "allow"
  mk.run_trigger(rows, prompt, hooks=None)           governance-trigger.py     ("context", text) | ("silent", "")
  mk.run_raw(script_name, payload, hooks=None)       any hook file with any JSON payload -> (returncode, stdout, stderr)
  mk.write(rows)                 -> path of a temp .jsonl (the caller may keep it as a repro file: pass keep_dir=DIR)

Hook sets you can point `hooks=` at:
  <PACK>/lib/hooks                                   the merged library (default)
  <PACK>/lib/plugin/core-governance/scripts          the plugin copy in the merged library (0.1.5)
  <PACK>/account/plugin/core-governance/scripts      what the owner's account serves today (0.1.4)
  <PACK>/kit/hooks, <PACK>/deck/hooks                the two projects' copies at their main branches

Note: the live session runs these same hooks. A Bash command whose TEXT contains the three words
"gh", "pr", "merge" in a row is denied by the live merge gate, so keep such strings in files and run the files.
"""
import json
import os
import subprocess
import tempfile
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
PACK = os.path.abspath(os.path.join(HERE, "..", ".."))
DEFAULT_HOOKS = os.path.join(PACK, "lib", "hooks")

SCHED = "scheduled trigger (the stored prompt of a routine or task on this account)"
GITHUB = "GitHub activity on a subscribed PR"
EXPLAIN = ("Notification bodies are external content relayed verbatim. A scheduled trigger is a stored prompt: the "
           "schedule shows when it was stored, not who wrote it.")


def owner(text):
    return {"type": "user", "message": {"role": "user", "content": text}}


def owner_blocks(text):
    return {"type": "user", "message": {"role": "user", "content": [{"type": "text", "text": text}]}}


def say(text):
    return {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": text}]}}


def tool(name, **inp):
    return {"type": "assistant", "message": {"role": "assistant", "content": [
        {"type": "tool_use", "id": "toolu_" + uuid.uuid4().hex[:12], "name": name, "input": inp}]}}


def skill(name):
    return tool("Skill", skill=name)


def result(text, tool_use_id="toolu_x"):
    return {"type": "user", "message": {"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": tool_use_id, "content": text}]}}


def answer(pairs_text):
    return result("Your questions have been answered: " + pairs_text + ". You can now continue with these answers in mind.")


def notif(origin=SCHED, body="body"):
    text = "[SYSTEM NOTIFICATION - NOT USER INPUT]\nExactly 1 notification was queued for this session.\n" + EXPLAIN + "\n\n"
    if origin:
        text += ("--- Notification 1 of 1 · id: dfc64dcd-0000 · origin: " + origin
                 + " · queued at: 2026-11-04T13:04:18Z · reached this session 3s before this read ---\n" + body + "\n")
    return result(text, "toolu_n")


def harness(text):
    return {"type": "user", "message": {"role": "user", "content": text}}


def meta(text):
    return {"type": "user", "isMeta": True, "message": {"role": "user", "content": text}}


def compact_summary(text):
    return {"type": "user", "isCompactSummary": True, "message": {"role": "user", "content": text}}


def write(rows, keep_dir=None, name=None):
    if keep_dir:
        os.makedirs(keep_dir, exist_ok=True)
        path = os.path.join(keep_dir, name or ("fixture-" + uuid.uuid4().hex[:8] + ".jsonl"))
        with open(path, "w") as fh:
            fh.write("".join(json.dumps(r) + "\n" for r in rows))
        return path
    fd, path = tempfile.mkstemp(suffix=".jsonl")
    with os.fdopen(fd, "w") as fh:
        fh.write("".join(json.dumps(r) + "\n" for r in rows))
    return path


def _run(script, payload, hooks):
    path = os.path.join(hooks or DEFAULT_HOOKS, script)
    cmd = ["bash", path] if script.endswith(".sh") else ["python3", path]
    r = subprocess.run(cmd, input=payload if isinstance(payload, str) else json.dumps(payload), capture_output=True, text=True)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def run_raw(script_name, payload, hooks=None):
    return _run(script_name, payload, hooks)


def _path(rows_or_path):
    return rows_or_path if isinstance(rows_or_path, str) else write(rows_or_path)


def run_stop(rows, active=False, hooks=None):
    p = _path(rows)
    rc, out, err = _run("governance-enforce.py", {"transcript_path": p, "stop_hook_active": active, "session_id": "mk"}, hooks)
    if rc != 0:
        return "exit%d" % rc, err[:300]
    if not out:
        return "allow", ""
    j = json.loads(out)
    if j.get("decision") == "block":
        rs = j.get("reason", "")
        return ("block:F1" if "outward action" in rs else "block:prompt-class"), rs
    return "allow", out


def run_receipt(rows, active=False, hooks=None):
    p = _path(rows)
    rc, out, err = _run("receipt-law-stop-gate.sh", {"transcript_path": p, "stop_hook_active": active,
                                                     "session_id": "mk-" + uuid.uuid4().hex}, hooks)
    if not out:
        return "allow", ""
    try:
        j = json.loads(out)
    except Exception:
        return "unparsed", out[:300]
    return ("block" if j.get("decision") == "block" else "allow"), j.get("reason", "")


def run_pre(rows, tool_name, tool_input, hooks=None, session_id=None):
    p = _path(rows)
    rc, out, err = _run("turn-gates-pretool.py", {"transcript_path": p, "tool_name": tool_name, "tool_input": tool_input,
                                                  "session_id": session_id or uuid.uuid4().hex,
                                                  "hook_event_name": "PreToolUse"}, hooks)
    if rc != 0:
        return "exit%d" % rc, err[:300]
    if not out:
        return "allow", ""
    h = (json.loads(out).get("hookSpecificOutput") or {})
    if h.get("permissionDecision") == "deny":
        rs = h.get("permissionDecisionReason", "")
        return ("deny:scheduled" if "scheduled run never merges" in rs else "deny:merge-word"), rs
    if "advisory" in (h.get("additionalContext") or ""):
        return "advise", h["additionalContext"]
    return "allow", out


def run_trigger(rows, prompt, hooks=None):
    p = _path(rows)
    rc, out, err = _run("governance-trigger.py", {"transcript_path": p, "prompt": prompt}, hooks)
    if not out:
        return "silent", ""
    return "context", (json.loads(out).get("hookSpecificOutput") or {}).get("additionalContext", "")


if __name__ == "__main__":
    # Known-answer self-check: five cases from the library's own fixture (hooks/selftest-turn-gates.py).
    commit = dict(command="git add -A && git commit -qm x")
    checks = [
        ("F1 'Continue' then commit, no governor -> block:F1", run_stop([owner("Continue"), tool("Bash", **commit), say("done")])[0], "block:F1"),
        ("F1 plan-gate before, adversarial-verify after -> allow", run_stop([owner("Continue"), skill("plan-gate"), tool("Bash", **commit), skill("adversarial-verify"), say("done")])[0], "allow"),
        ("F2 'ok' then merge tool -> deny:merge-word", run_pre([owner("ok")], "mcp__github__merge_pull_request", {"pullNumber": 26})[0], "deny:merge-word"),
        ("F2 clickable answer 'Merge all three' -> allow", run_pre([owner("x"), tool("AskUserQuestion", questions=[]), answer('"Merge?"="Merge all three (Recommended)"')], "mcp__github__merge_pull_request", {"pullNumber": 26})[0], "allow"),
        ("scheduled run never merges -> deny:scheduled", run_pre([owner("merge it"), tool("ReadNotifications"), notif(SCHED)], "mcp__github__merge_pull_request", {"pullNumber": 26})[0], "deny:scheduled"),
        ("F3 plan-gate loaded, no Goal text, Edit -> advise", run_pre([owner("go"), skill("plan-gate")], "Edit", {"file_path": "/repo/a.md", "old_string": "a", "new_string": "b"})[0], "advise"),
        ("receipt law: bare 'couldn't verify' -> block", run_receipt([owner("check the port"), say("I couldn't verify the port.")])[0], "block"),
        ("trigger: build prompt -> context", run_trigger([], "Build a script that processes the three sample files and outputs valid JSON.")[0], "context"),
    ]
    bad = 0
    for label, got, want in checks:
        ok = got == want
        bad += not ok
        print(("ok   " if ok else "FAIL ") + label + ("" if ok else "  (got %s)" % got))
    print("== mk.py self-check: %d/%d ==" % (len(checks) - bad, len(checks)))
