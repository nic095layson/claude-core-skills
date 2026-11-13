#!/usr/bin/env python3
"""Verdict-only probes of the real record through pack/tools/replay_real.py --hooks <patched copy> --what stop.

Each probe is a copy of lib/hooks with ONE change to the F1 rule. Only the replay tool reads the private snapshot;
this script sees and prints nothing but the tool's verdict lines (timestamps and allow/BLOCK labels), and for each
probe only the lines that differ from the unpatched run.

Run: python3 <this file> [probe-id ...]
"""
import os
import shutil
import subprocess
import sys

PACK = "/tmp/claude-0/-home-user/ff01f16c-7b3f-5ea5-8051-7a95ac7cd1d1/scratchpad/merge-audit"
SRC = PACK + "/lib/hooks"
OUT = PACK + "/work/atk-f1/probe"
REPLAY = PACK + "/pack/tools/replay_real.py"

TG, GE = "turngate.py", "governance-enforce.py"
SUFFIX_OLD = '''"create_or_update_file", "delete_file", "create_trigger", "update_trigger", "delete_trigger")'''
BASH_OLD = r'''OUTWARD_BASH = re.compile(r"\bgit\s+(-C\s+\S+\s+)?(commit|push)\b|\bgh\s+pr\s+(create|merge)\b")'''
NEED_OLD = "            if not (_pg and _av):"
EVENTS_OLD = '''    out = []
    for d in rows[start + 1:]:'''


def widen(*names):
    return SUFFIX_OLD[:-1] + ", " + ", ".join('"%s"' % n for n in names) + ")"


PROBES = [
    ("P0", "unpatched copy (must reproduce pack/replay-baseline.txt)", None, None, None),
    ("P1", "F1 requires ONLY plan-gate before the first outward action", GE, NEED_OLD, "            if not _pg:"),
    ("P2", "F1 requires ONLY adversarial-verify in the turn", GE, NEED_OLD, "            if not _av:"),
    ("P3", "also outward: update_pull_request_branch, enable_pr_auto_merge", TG, SUFFIX_OLD,
     widen("update_pull_request_branch", "enable_pr_auto_merge")),
    ("P4", "also outward: send_later, CronCreate, CronDelete, ScheduleWakeup (other ways to schedule)", TG, SUFFIX_OLD,
     widen("send_later", "CronCreate", "CronDelete", "ScheduleWakeup")),
    ("P5", "also outward: create_branch (a branch on the remote)", TG, SUFFIX_OLD, widen("create_branch")),
    ("P6", "also outward: issue / comment / review writes", TG, SUFFIX_OLD,
     widen("issue_write", "add_issue_comment", "pull_request_review_write", "add_comment_to_pending_review",
           "add_reply_to_pull_request_comment", "update_issue_comment", "sub_issue_write", "request_copilot_review")),
    ("P7", "also outward: delegation (Agent, Workflow, create_session, fire_trigger)", TG, SUFFIX_OLD,
     widen("Agent", "Workflow", "create_session", "fire_trigger")),
    ("P8", "also outward: mail / Drive / Docs / published files", TG, SUFFIX_OLD,
     widen("mcp__Gmail__send_message", "mcp__Gmail__reply", "mcp__Gmail__forward", "share_file", "mcp__Google_Drive__create_file",
           "mcp__Google_Drive__update_file", "mcp__Claude_Docs__create", "mcp__Claude_Docs__update", "Artifact", "SendUserFile")),
    ("P9", "also outward: git with other global options before commit|push (-c k=v, --no-pager, --git-dir=, quoted -C)", TG, BASH_OLD,
     BASH_OLD[:-2] + r'''|\bgit\s+((-c\s+\S+|-C\s+\"[^\"]*\"|-C\s+\S+|--\S+)\s+)+(commit|push)\b")'''),
    ("P10", "also outward: git revert | cherry-pick | merge | rebase | tag | am (commits or refs made without the word commit)", TG, BASH_OLD,
     BASH_OLD[:-2] + r'''|\bgit\s+(-C\s+\S+\s+)?(revert|cherry-pick|merge|rebase|tag|am)\b")'''),
    ("P11", "a tool call whose result is an error (denied, failed, rejected) is NOT counted", TG, EVENTS_OLD,
     '''    out = []
    _bad = set()
    for d in rows[start + 1:]:
        _m = d.get("message") or {}
        _c = _m.get("content") if isinstance(_m, dict) else None
        if d.get("type") == "user" and isinstance(_c, list):
            for _b in _c:
                if isinstance(_b, dict) and _b.get("type") == "tool_result" and _b.get("is_error"):
                    _bad.add(_b.get("tool_use_id"))
    rows = rows[:start + 1] + [d for d in rows[start + 1:] if not (
        d.get("type") == "assistant" and isinstance((d.get("message") or {}).get("content"), list) and any(
            isinstance(b, dict) and b.get("type") == "tool_use" and b.get("id") in _bad
            for b in d["message"]["content"]))]
    for d in rows[start + 1:]:'''),
]


def replay(hooks):
    r = subprocess.run([sys.executable, REPLAY, "--hooks", hooks, "--what", "stop"], capture_output=True, text=True,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    if r.returncode != 0:
        return None, r.stderr.strip().splitlines()[-1:] or ["exit %d" % r.returncode]
    return [ln for ln in r.stdout.splitlines() if ln.startswith("  ")], None


def main(want):
    os.makedirs(OUT, exist_ok=True)
    base = None
    for pid, what, fname, old, new in PROBES:
        if want and pid not in want and pid != "P0":
            continue
        d = os.path.join(OUT, pid, "hooks")
        if os.path.isdir(d):
            shutil.rmtree(d)
        shutil.copytree(SRC, d, ignore=shutil.ignore_patterns("__pycache__"))
        if fname:
            p = os.path.join(d, fname)
            s = open(p, encoding="utf-8").read()
            if s.count(old) != 1:
                print("%s NOT APPLIED (pattern found %d times): %s" % (pid, s.count(old), what))
                continue
            open(p, "w", encoding="utf-8").write(s.replace(old, new))
        lines, errmsg = replay(d)
        if lines is None:
            print("%s replay failed: %s" % (pid, errmsg))
            continue
        if pid == "P0":
            base = lines
            ref = [ln for ln in open(PACK + "/pack/replay-baseline.txt").read().split("== PRE")[0].splitlines() if ln.startswith("  ")]
            print("P0 %s: %d verdict lines, identical to pack/replay-baseline.txt: %s" % (what, len(lines), lines == ref))
            for ln in lines:
                if "BLOCK" in ln or "totals" in ln:
                    print("     " + ln.strip())
            continue
        changed = [(a, b) for a, b in zip(base, lines) if a != b]
        print("%s %s: %d line(s) differ from P0" % (pid, what, len(changed)))
        for a, b in changed:
            if "totals" in a:
                print("     totals now: " + b.split("totals:")[1].strip())
            else:
                print("     %s | was: %s | now: %s" % (a.strip()[:16], a.split("now:")[1].split("/")[0].strip(), b.split("now:")[1].split("/")[0].strip()))


if __name__ == "__main__":
    main(sys.argv[1:])
