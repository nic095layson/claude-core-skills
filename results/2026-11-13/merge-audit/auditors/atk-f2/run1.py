#!/usr/bin/env python3
"""Replay ONE kept case.   python3 run1.py <fixture.jsonl> <call.json> [hooks_dir]

Prints the last few transcript rows that matter (owner / assistant text / answers), the tool call, and the
hook's raw stdout plus the verdict. Nothing is written anywhere.
"""
import json
import os
import subprocess
import sys

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
HERE = os.path.dirname(os.path.abspath(__file__))
PACK = os.path.abspath(os.path.join(HERE, "..", ".."))
fixture, callf = sys.argv[1], sys.argv[2]
hooks = sys.argv[3] if len(sys.argv) > 3 else os.path.join(PACK, "lib", "hooks")
call = json.load(open(callf))


def show(row):
    m = row.get("message") or {}
    c = m.get("content")
    tag = row.get("type", "?")
    if row.get("isMeta"):
        tag += "[isMeta]"
    if isinstance(c, str):
        return "%s: %s" % (tag, c[:230])
    out = []
    for b in c or []:
        if not isinstance(b, dict):
            continue
        if b.get("type") == "text":
            out.append("text: " + b.get("text", "")[:230])
        elif b.get("type") == "tool_use":
            out.append("tool_use %s %s" % (b.get("name"), json.dumps(b.get("input"))[:160]))
        elif b.get("type") == "tool_result":
            cc = b.get("content")
            out.append("tool_result: " + (cc if isinstance(cc, str) else json.dumps(cc))[:230].replace("\n", " | "))
    return "%s: %s" % (tag, " ; ".join(out))


if os.path.exists(fixture):
    for line in open(fixture):
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except Exception:
            print("  row  (unparsable line)")
            continue
        if row.get("type") in ("user", "assistant"):
            print("  row  " + show(row))
        else:
            print("  row  type=%s %s" % (row.get("type"), json.dumps(row)[:200]))
else:
    print("  (no transcript file at %s)" % fixture)
print("  CALL %s %s" % (call["tool_name"], json.dumps(call["tool_input"])[:300]))
payload = {"transcript_path": fixture, "tool_name": call["tool_name"], "tool_input": call["tool_input"],
           "session_id": "atkf2-run1", "hook_event_name": "PreToolUse"}
payload.update(call.get("extra_payload") or {})
r = subprocess.run(["python3", os.path.join(hooks, "turn-gates-pretool.py")], input=json.dumps(payload),
                   capture_output=True, text=True)
out = r.stdout.strip()
verdict = "ALLOW (hook printed nothing)"
if out:
    try:
        h = json.loads(out).get("hookSpecificOutput") or {}
        if h.get("permissionDecision") == "deny":
            verdict = "DENY: " + h.get("permissionDecisionReason", "")[:260]
        elif h.get("additionalContext"):
            verdict = "ALLOW with advisory: " + h["additionalContext"][:160]
        else:
            verdict = "ALLOW (output: %s)" % out[:200]
    except Exception:
        verdict = "UNPARSED stdout: " + out[:200]
print("  HOOK exit=%d  hooks=%s" % (r.returncode, os.path.relpath(hooks, PACK)))
if r.stderr.strip():
    print("  STDERR " + r.stderr.strip()[:300])
print("  VERDICT " + verdict)
