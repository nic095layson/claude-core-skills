#!/usr/bin/env python3
"""repro.py — READ-ONLY reproduction of the atk-f2 findings. Writes nothing in this directory or in the pack.

    python3 repro.py F2-1 | F2-2 | F2-3 | F2-4 | F2-5 | F2-6 | F2-7 | F2-8 | GAPS [mutant-name ...] | MORE | ROUTES

Every case is a kept pair under fx/:  <id>.jsonl (the transcript the hook reads)  and  <id>.call.json (the tool call,
the verdict the stated rule requires, and which copy of the hooks judges it). This script feeds each pair to that copy's
own turn-gates-pretool.py and prints what the hook answered. The generators that built the pairs are f2_*.py, gaps.py,
more.py (they DO write under fx/; you do not need to run them).
Lines marked REAL ask the real session record through pack/tools/replay_real.py with a probe copy of the hooks
(hooks-probe/, hooks-sched-*/; built by mkprobe.py and f2_6.py): labels only, no transcript text.
Output uses single spaces only, so that lines can be quoted exactly.
"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
PACK = os.path.abspath(os.path.join(HERE, "..", ".."))
FX = os.path.join(HERE, "fx")
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
REPLAY = os.path.join(PACK, "pack", "tools", "replay_real.py")


def one(s):
    return re.sub(r"\s+", " ", s).strip()


def hook(transcript, call, hooks_rel):
    payload = {"transcript_path": transcript, "tool_name": call["tool_name"], "tool_input": call["tool_input"],
               "session_id": "atkf2-repro", "hook_event_name": "PreToolUse"}
    r = subprocess.run(["python3", os.path.join(PACK, hooks_rel, "turn-gates-pretool.py")], input=json.dumps(payload),
                       capture_output=True, text=True, env=ENV)
    out = r.stdout.strip()
    if r.returncode != 0:
        return "EXIT%d" % r.returncode
    if not out:
        return "ALLOW"
    h = json.loads(out).get("hookSpecificOutput") or {}
    if h.get("permissionDecision") == "deny":
        return "DENY:SCHEDULED" if "scheduled run never merges" in h.get("permissionDecisionReason", "") else "DENY:MERGE-WORD"
    return "ALLOW"


def brief(path, limit=150):
    lines = []
    for raw in open(path, encoding="utf-8"):
        try:
            r = json.loads(raw)
            c = r["message"]["content"]
        except Exception:
            lines.append("other row: " + raw.strip()[:80])
            continue
        if isinstance(c, str):
            tag = "summary row (isCompactSummary): " if r.get("isCompactSummary") else "harness row (isMeta): " if r.get("isMeta") else "owner types: "
            lines.append(tag + c[:limit])
            continue
        for b in c:
            if b["type"] == "text":
                lines.append("assistant: " + b["text"][:limit])
            elif b["type"] == "tool_use" and b["name"] not in ("AskUserQuestion", "ReadNotifications"):
                lines.append("tool call: %s %s" % (b["name"], json.dumps(b["input"])[:90]))
            elif b["type"] == "tool_result":
                t = b["content"] if isinstance(b["content"], str) else json.dumps(b["content"])
                if t.startswith("Your questions have been answered"):
                    lines.append("owner clicks: " + t[len("Your questions have been answered: "):].replace(". You can now continue with these answers in mind.", "")[:limit])
                elif t.startswith("[SYSTEM NOTIFICATION"):
                    hdr = [l for l in t.splitlines() if l.startswith("--- Notification")]
                    body = t.split("---\n", 1)[-1].strip() if hdr else ""
                    lines.append("notification, origin: " + (hdr[0].split("origin: ")[1].split(" ·")[0][:48] if hdr else "(no header)")
                                 + ((", body: " + body[:80].replace("\n", " / ")) if body and body != "body" else ""))
                else:
                    lines.append("tool result: " + t[:limit].replace("\n", " / "))
    return [one(l) for l in lines]


def replay(prefix):
    calls = []
    for f in glob.glob(os.path.join(FX, prefix + "*.call.json")):
        c = json.load(open(f))
        c["id"] = os.path.basename(f)[:-len(".call.json")]
        calls.append(c)
    bad = 0
    for c in sorted(calls, key=lambda c: c.get("seq", 0)):
        t = os.path.join(FX, c["id"] + ".jsonl")
        got = hook(t, c, c.get("hooks", "lib/hooks"))
        want = (c.get("want") or "?").upper()
        ok = got.startswith(want)
        bad += not ok
        call = c["tool_name"].replace("mcp__github__", "github:").replace("mcp__GH__", "GH:")
        ti = c["tool_input"]
        call += (" #%s" % ti["pullNumber"] + (" (%s)" % ti["repo"] if ti.get("repo") not in (None, "claude-core-skills") else "")) if "pullNumber" in ti else \
                (" `%s`" % ti["command"][:100]) if "command" in ti else ""
        print(one("[%s] %s: rule requires %s, gate says %s%s" % (c["id"], "ok" if ok else "MISMATCH", want, got,
                                                               (" (" + c["label"] + ")") if c.get("label") else "")))
        if c.get("show"):
            for l in brief(t):
                print("    " + l)
            print("    CALL: %s [hooks: %s]" % (one(call), c.get("hooks", "lib/hooks")))
    print("-> %d case(s), %d where the gate's answer differs from what the rule requires" % (len(calls), bad))


def real_stop(hooks_dir, words, **env):
    r = subprocess.run([sys.executable, REPLAY, "--hooks", hooks_dir, "--what", "stop"], capture_output=True, text=True, env=dict(ENV, **env))
    return [(l[2:18], words.get(l.split("| now:")[1].split("/")[0].strip(), "?")) for l in r.stdout.splitlines() if l.startswith("  20") and "| now:" in l]


def real_pre(**env):
    r = subprocess.run([sys.executable, REPLAY, "--hooks", os.path.join(HERE, "hooks-probe"), "--what", "pre"], capture_output=True, text=True,
                       env=dict(ENV, ATK_NO_F3="1", **env))
    tot = [l for l in r.stdout.splitlines() if l.strip().startswith("totals:")]
    return tot[0].strip() if tot else r.stdout[-200:]


PROBE = os.path.join(HERE, "hooks-probe")
STOPWORDS = {"BLOCK:prompt-class": "no-owner-row", "BLOCK:F1": "OPEN", "allow": "closed", "BLOCK:receipt": "scheduled"}
SCHEDWORDS = {"BLOCK:F1": "ALLOW", "BLOCK:receipt": "deny(scheduled)", "allow": "deny(word)", "BLOCK:prompt-class": "probe-error"}


def main(what, rest):
    if what == "F2-1":
        replay("F2-1")
        pts = real_stop(PROBE, STOPWORDS, ATK_STOP_PROBE="1", ATK_ROUTES="3", ATK_R3_ANY="1")
        hit = [t for t, v in pts if v == "OPEN"]
        print("REAL: at %d of %d real stop points the assistant's last recorded text before the owner's message held an un-negated"
              " merge word and a '#<number>' (third route open for that number whatever the owner wrote): %s" % (len(hit), len(pts), " ".join(hit)))
    elif what == "F2-2":
        replay("F2-2")
        pts = real_stop(PROBE, STOPWORDS, ATK_STOP_PROBE="1")
        p1 = real_stop(PROBE, STOPWORDS, ATK_STOP_PROBE="1", ATK_ROUTES="1")
        print("REAL: a merge of PR #999999 (a PR nobody named) would pass at %d of %d real stop points: %s"
              % (sum(v == "OPEN" for _, v in pts), len(pts), " ".join(t for t, v in pts if v == "OPEN")))
        print("REAL: with only the owner's typed message counted: %d of %d (every opening comes from a click)" % (sum(v == "OPEN" for _, v in p1), len(p1)))
    elif what == "ROUTES":
        print("REAL merge calls, as shipped: " + real_pre())
        print("REAL, only the owner's typed message: " + real_pre(ATK_ROUTES="1"))
        print("REAL, only clickable answers: " + real_pre(ATK_ROUTES="2"))
        print("REAL, only clickable answers that belong to an AskUserQuestion call: " + real_pre(ATK_ROUTES="2", ATK_STRICT_ANSWERS="1"))
        print("REAL, only the assistant's last text: " + real_pre(ATK_ROUTES="3"))
    elif what in ("F2-3", "F2-4", "F2-8"):
        replay(what)
    elif what == "F2-5":
        settings = json.load(open(os.path.join(PACK, "lib", ".claude", "settings.json")))
        matcher = [g["matcher"] for g in settings["hooks"]["PreToolUse"] if "turn-gates-pretool.py" in g["hooks"][0]["command"]][0]
        print("wiring matcher (lib/.claude/settings.json): " + matcher)
        print("gh on this machine's PATH: %s (pack/session-tools.txt:51 says: \"The GitHub command line (gh) is NOT installed in this session\")" % shutil.which("gh"))
        for f in sorted(glob.glob(os.path.join(FX, "F2-5-*-owner.call.json"))):
            c = json.load(open(f))
            run = json.load(open(f.replace("-owner.call.json", "-run.call.json")))
            a = hook(f.replace(".call.json", ".jsonl"), c, c["hooks"])
            b = hook(f.replace("-owner.call.json", "-run.jsonl"), run, run["hooks"])
            arg = c["tool_input"].get("command", "") or json.dumps({k: v for k, v in c["tool_input"].items() if k in ("pullNumber", "branch", "path")})
            print(one("%s | hook is run: %s | owner typed 'ok': %s | in a scheduled run: %s | %s %s"
                      % (c["label"].split(" | ")[0], "yes" if re.search(matcher, c["tool_name"]) else "NO (matcher)", a, b, c["tool_name"], arg)))
    elif what == "F2-6":
        replay("F2-6")
        for name, d in (("merged hooks (lib/hooks)", "hooks-sched-lib"), ("account copy 0.1.4", "hooks-sched-account")):
            pts = real_stop(os.path.join(HERE, d), SCHEDWORDS)
            count = {}
            for _, v in pts:
                count[v] = count.get(v, 0) + 1
            print("REAL, %s: scheduled notification appended at each of %d real stop points, then merge of PR #36 -> %s; at the latest one (%s): %s"
                  % (name, len(pts), count, pts[-1][0], pts[-1][1]))
    elif what == "F2-7":
        replay("F2-7")
        c = json.load(open(os.path.join(FX, "F2-7-ctl1.call.json")))
        print("[F2-7x] transcript file does not exist: gate says %s" % hook(os.path.join(FX, "no-such-file.jsonl"), c, "lib/hooks"))
        pts = real_stop(PROBE, STOPWORDS, ATK_STOP_PROBE="1")
        print("REAL: %d real stop points; the first four: %s" % (len(pts), ", ".join("%s=%s" % p for p in pts[:4])))
        print("REAL: the transcript held no owner row and no scheduled row at %d of %d (the hook exits before the merge check there)" % (sum(v == "no-owner-row" for _, v in pts), len(pts)))
    elif what == "GAPS":
        names = rest or sorted(os.listdir(os.path.join(HERE, "mut")))
        for n in names:
            d = os.path.join(HERE, "mut", n)
            if not os.path.exists(os.path.join(d, "selftest-turn-gates.py")):
                continue
            changed = [f for f in ("turngate.py", "turn-gates-pretool.py") if open(os.path.join(d, f)).read() != open(os.path.join(PACK, "lib", "hooks", f)).read()]
            diff = subprocess.run(["diff", os.path.join(PACK, "lib", "hooks", changed[0]), os.path.join(d, changed[0])], capture_output=True, text=True).stdout if changed else ""
            r = subprocess.run(["python3", os.path.join(d, "selftest-turn-gates.py")], capture_output=True, text=True, env=ENV)
            tail = (r.stdout.strip().splitlines() or ["(no output)"])[-1]
            print("%s: %s, its selftest says '%s', changed file: %s" % (n, "SURVIVES" if r.returncode == 0 else "killed", tail, changed[0] if changed else "none"))
            if rest:
                print(diff)
        replay("G-")
    elif what == "MORE":
        replay("M")
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "", sys.argv[2:])
