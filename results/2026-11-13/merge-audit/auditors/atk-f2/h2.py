#!/usr/bin/env python3
"""Round-2 harness (after reading the source). Fixtures use only row shapes listed in pack/real-row-shapes.md:
  user content=str (an owner message) · assistant blocks=text · assistant blocks=tool_use · user content=list[tool_result]
tool_use ids and tool_result ids are linked, AskUserQuestion answers use the exact real text format, notification
results use the real header format. Every case is kept as fx/<id>.jsonl + fx/<id>.call.json (replay: run1.py).
"""
import json
import os
import sys
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
PACK = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(PACK, "pack", "tools"))
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["TMPDIR"] = os.path.join(HERE, "tmp")
os.makedirs(os.environ["TMPDIR"], exist_ok=True)
sys.dont_write_bytecode = True
import mk  # noqa: E402

FX = os.path.join(HERE, "fx")
LIB = os.path.join(PACK, "lib", "hooks")
PLUGIN = os.path.join(PACK, "lib", "plugin", "core-governance", "scripts")
ACCOUNT = os.path.join(PACK, "account", "plugin", "core-governance", "scripts")
M = "mcp__github__merge_pull_request"
M2 = "mcp__GH__merge_pull_request"
GHM = "gh pr " + "merge"      # the three words, never typed on a shell command line

O, S = mk.owner, mk.say
_SEQ = 0


def pr(n, repo="claude-core-skills", **kw):
    d = {"owner": "nic095layson", "repo": repo, "pullNumber": n}
    d.update(kw)
    return d


def pair(name, inp, result_text):
    """An assistant tool call and its tool_result row, ids linked (two rows)."""
    tid = "toolu_" + uuid.uuid4().hex[:16]
    return [{"type": "assistant", "message": {"role": "assistant", "content": [
                {"type": "tool_use", "id": tid, "name": name, "input": inp}]}},
            {"type": "user", "message": {"role": "user", "content": [
                {"type": "tool_result", "tool_use_id": tid, "content": result_text}]}}]


def click(*qa, options=None):
    """An AskUserQuestion call and the owner's click, real answer format. qa = (question, chosen), ..."""
    qs = [{"question": q, "header": "Decision", "multiSelect": False,
           "options": [{"label": a, "description": ""}] + [{"label": o, "description": ""} for o in (options or [])]}
          for q, a in qa]
    text = ("Your questions have been answered: " + ", ".join('"%s"="%s"' % (q, a) for q, a in qa)
            + ". You can now continue with these answers in mind.")
    return pair("AskUserQuestion", {"questions": qs}, text)


def notif(origin, body="body"):
    r = mk.notif(origin, body)
    return pair("ReadNotifications", {}, r["message"]["content"][0]["content"])


def flat(rows):
    out = []
    for r in rows:
        out.extend(r if isinstance(r, list) else [r])
    return out


def brief(rows, limit=150):
    lines = []
    for r in rows:
        c = r["message"]["content"]
        if isinstance(c, str):
            lines.append(("harness row : (isMeta) " if r.get("isMeta") else "owner types : ") + c[:limit])
            continue
        for b in c:
            if b["type"] == "text":
                lines.append("assistant   : " + b["text"][:limit])
            elif b["type"] == "tool_use":
                if b["name"] in ("AskUserQuestion", "ReadNotifications"):
                    continue
                lines.append("tool call   : %s %s" % (b["name"], json.dumps(b["input"])[:90]))
            elif b["type"] == "tool_result":
                t = b["content"]
                if t.startswith("Your questions have been answered"):
                    lines.append("owner clicks: " + t[len("Your questions have been answered: "):-len(". You can now continue with these answers in mind.")][:limit])
                elif t.startswith("[SYSTEM NOTIFICATION"):
                    hdr = [l for l in t.splitlines() if l.startswith("--- Notification")]
                    body = t.split("---\n", 1)[-1].strip() if hdr else ""
                    lines.append("notification: " + (hdr[0][:28] + " … origin: " + hdr[0].split("origin: ")[1].split(" ·")[0][:40] if hdr else "(no header)")
                                 + ((" | body: " + body[:70].replace("\n", " / ")) if body and body != "body" else ""))
                else:
                    lines.append("tool result : " + t[:limit].replace("\n", " / "))
    return lines


def case(cid, rows, tool_name, tool_input, want, hooks=None, show=True, label=None, quiet=False):
    rows = flat(rows)
    global _SEQ
    _SEQ += 1
    path = mk.write(rows, keep_dir=FX, name=cid + ".jsonl")
    with open(os.path.join(FX, cid + ".call.json"), "w") as fh:
        json.dump({"tool_name": tool_name, "tool_input": tool_input, "want": want, "label": label or "", "show": bool(show),
                   "hooks": os.path.relpath(hooks or LIB, PACK), "seq": _SEQ}, fh)
    got, detail = mk.run_pre(path, tool_name, tool_input, hooks=hooks, session_id="atkf2-" + cid)
    ok = (got == want) or (want == "deny" and got.startswith("deny"))
    call = tool_name.replace("mcp__github__", "github:").replace("mcp__GH__", "GH:")
    if "pullNumber" in tool_input:
        call += " #%s" % tool_input["pullNumber"] + (" (%s)" % tool_input["repo"] if tool_input.get("repo") not in (None, "claude-core-skills") else "")
    elif "command" in tool_input:
        call += " `%s`" % tool_input["command"][:80]
    if quiet:
        return got, detail
    print("[%s] %s  rule requires: %-5s  gate says: %s%s" % (cid, "ok      " if ok else "MISMATCH", want.upper(), got.upper(),
                                                           ("   (" + label + ")") if label else ""))
    if show:
        for l in brief(rows):
            print("      " + l)
        print("      CALL        : " + call)
    return got, detail
