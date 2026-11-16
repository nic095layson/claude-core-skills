#!/usr/bin/env python3
"""Yes/no detectors over the real record, through pack/tools/replay_real.py --hooks <patched copy> --what stop.

Each detector replaces F1's decision with one structural question about the transcript at each real stop point
(row flags, tool names, a regex over shell commands). The answer comes back as the replay tool's verdict label only
(BLOCK:F1 = yes, allow = no); no content is read or printed by this script.

Run: python3 <this file>
"""
import os
import shutil
import subprocess
import sys

PACK = "/tmp/claude-0/-home-user/ff01f16c-7b3f-5ea5-8051-7a95ac7cd1d1/scratchpad/merge-audit"
SRC = PACK + "/lib/hooks"
OUT = PACK + "/work/atk-f1/probe"
REPLAY = PACK + "/pack/tools/replay_real.py"
ANCHOR = "    _li = turngate.turn_start(lines)   # 2026-11-04: a scheduled run is a turn of its own\n"

HEAD = '''    import re as _re
    def _yes():
        print(json.dumps({"decision": "block", "reason": "probe: outward action"}))
    _li0 = turngate.turn_start(lines)
    _turn = lines[_li0 + 1:] if _li0 >= 0 else []
    _ev0 = turngate.events(lines, _li0) if _li0 >= 0 else []
    def _tools(rows):
        for d in rows:
            m = d.get("message") if isinstance(d, dict) else None
            c = m.get("content") if isinstance(m, dict) else None
            if isinstance(d, dict) and d.get("type") == "assistant" and isinstance(c, list):
                for b in c:
                    if isinstance(b, dict) and b.get("type") == "tool_use":
                        yield b
'''
TAIL = "    sys.exit(0)\n"

DETECTORS = [
    ("D1", "any row flagged isSidechain true anywhere in the transcript so far",
     '''    if any(isinstance(d, dict) and d.get("isSidechain") is True for d in lines):
        _yes()
'''),
    ("D2", "an Agent / Task / Workflow tool call anywhere in the transcript so far",
     '''    if any(b.get("name") in ("Agent", "Task", "Workflow") for b in _tools(lines)):
        _yes()
'''),
    ("D3", "an Agent / Task / Workflow tool call in the CURRENT turn",
     '''    if any(b.get("name") in ("Agent", "Task", "Workflow") for b in _tools(_turn)):
        _yes()
'''),
    ("D4", "the current turn has a shell command the gate counts as outward ONLY by mention (the match disappears once quoted strings, heredoc bodies and # comments are removed, or the command is a --dry-run / --help)",
     '''    def _mention(cmd):
        if not turngate.OUTWARD_BASH.search(cmd):
            return False
        s = _re.sub(r"<<-?\\s*['\\"]?(\\w+)['\\"]?.*?\\n\\1\\b", " ", cmd, flags=_re.S)
        s = _re.sub(r"'[^']*'|\\"(?:[^\\"\\\\\\\\]|\\\\\\\\.)*\\"", " ", s)
        s = _re.sub(r"(^|\\s)#.*", " ", s)
        if not turngate.OUTWARD_BASH.search(s):
            return True
        return bool(_re.search(r"\\b(commit|push)\\b[^|;&\\n]*--(dry-run|help)\\b", s))
    if any(b.get("name") == "Bash" and _mention(turngate._cmd(b)) for b in _tools(_turn)):
        _yes()
'''),
    ("D5", "the current turn has a call the gate counts as outward whose tool_result is an error (denied, failed, rejected)",
     '''    _bad = set()
    for d in _turn:
        m = d.get("message") if isinstance(d, dict) else None
        c = m.get("content") if isinstance(m, dict) else None
        if isinstance(d, dict) and d.get("type") == "user" and isinstance(c, list):
            _bad |= {b.get("tool_use_id") for b in c if isinstance(b, dict) and b.get("type") == "tool_result" and b.get("is_error")}
    if any(turngate.is_outward(b) and b.get("id") in _bad for b in _tools(_turn)):
        _yes()
'''),
    ("D6", "the current turn has a 'Stop hook feedback' row (a Stop hook blocked) FOLLOWED by a call the gate counts as outward",
     '''    _fb = -1
    for i, d in enumerate(_turn):
        if isinstance(d, dict) and d.get("type") == "user" and d.get("isMeta") and str(turngate._text(d.get("message")) or "").startswith("Stop hook feedback"):
            _fb = i
    if _fb >= 0 and any(turngate.is_outward(b) for b in _tools(_turn[_fb + 1:])):
        _yes()
'''),
    ("D7", "the current turn has at least one call the gate counts as outward (reference count)",
     '''    if any(turngate.is_outward(b) for b in _tools(_turn)):
        _yes()
'''),
    ("D8", "no turn can be found at this stop (turn_start is -1: no owner message and no scheduled-run header in the file so far)",
     '''    if _li0 < 0:
        _yes()
'''),
    ("D9", "no turn can be found AND the transcript so far already holds a call the gate counts as outward",
     '''    if _li0 < 0 and any(turngate.is_outward(b) for b in _tools(lines)):
        _yes()
'''),
    ("D10", "anywhere so far: a shell command with git global options before commit|push that the merged pattern does NOT match (-c k=v, --no-pager, --git-dir=, quoted -C path)",
     '''    _x = _re.compile(r"\\bgit\\s+((-c\\s+\\S+|-C\\s+\\"[^\\"]*\\"|-C\\s+\\S+|--\\S+)\\s+)+(commit|push)\\b")
    if any(b.get("name") == "Bash" and _x.search(turngate._cmd(b)) and not turngate.OUTWARD_BASH.search(turngate._cmd(b)) for b in _tools(lines)):
        _yes()
'''),
    ("D11", "anywhere so far: git revert | cherry-pick | merge | rebase | tag | am in a shell command",
     '''    _x = _re.compile(r"\\bgit\\s+(-C\\s+\\S+\\s+)?(revert|cherry-pick|merge|rebase|tag|am)\\b")
    if any(b.get("name") == "Bash" and _x.search(turngate._cmd(b)) for b in _tools(lines)):
        _yes()
'''),
    ("D12", "anywhere so far: update_pull_request_branch, enable_pr_auto_merge, send_later, CronCreate, CronDelete or ScheduleWakeup",
     '''    if any(str(b.get("name") or "").endswith(("update_pull_request_branch", "enable_pr_auto_merge", "send_later", "CronCreate", "CronDelete", "ScheduleWakeup")) for b in _tools(lines)):
        _yes()
'''),
    ("D13", "anywhere so far: create_branch, issue_write, add_issue_comment, pull_request_review_write, actions_run_trigger, fire_trigger, create_session or send_message",
     '''    if any(str(b.get("name") or "").endswith(("create_branch", "issue_write", "add_issue_comment", "pull_request_review_write", "actions_run_trigger", "fire_trigger", "create_session", "send_message")) for b in _tools(lines)):
        _yes()
'''),
]


def build(did, body):
    d = os.path.join(OUT, did, "hooks")
    if os.path.isdir(d):
        shutil.rmtree(d)
    shutil.copytree(SRC, d, ignore=shutil.ignore_patterns("__pycache__"))
    p = os.path.join(d, "governance-enforce.py")
    s = open(p, encoding="utf-8").read()
    assert s.count(ANCHOR) == 1
    open(p, "w", encoding="utf-8").write(s.replace(ANCHOR, HEAD + body + TAIL + ANCHOR))
    return d


def selfcheck():
    """Known answers on synthetic transcripts, before the detectors are trusted on the real record."""
    sys.dont_write_bytecode = True
    sys.path.insert(0, PACK + "/pack/tools")
    import mk
    O = mk.owner("Continue")

    def bash(c):
        return mk.tool("Bash", command=c)

    def with_result(row, is_error):
        res = mk.result("x", row["message"]["content"][0]["id"])
        res["message"]["content"][0]["is_error"] = is_error
        return [row, res]
    side = dict(mk.skill("plan-gate"), isSidechain=True)
    agent = mk.tool("Agent", prompt="p")
    fb = mk.meta("Stop hook feedback: GOV-ENFORCE: x")
    known = {
        "D1": [([O, side], True), ([O, mk.skill("plan-gate")], False)],
        "D2": [([agent, O, mk.say("x")], True), ([O, mk.say("x")], False)],
        "D3": [([agent, O, mk.say("x")], False), ([O, agent], True)],
        "D4": [([O, bash('grep -rn "git commit" hooks/')], True), ([O, bash('git commit -m "fix push"')], False),
               ([O, bash("cat > /tmp/s.sh <<'EOF'\ngit commit -m x\ngit push\nEOF")], True), ([O, bash("git push --dry-run origin main")], True),
               ([O, bash("git add -A && git commit -qm x")], False), ([O, bash("git status  # then git push")], True),
               ([O, bash("git push -u origin feat")], False), ([O, bash("git log --oneline -3")], False)],
        "D5": [([O] + with_result(bash("git push"), True), True), ([O] + with_result(bash("git push"), False), False)],
        "D6": [([O, mk.say("x"), fb, bash("git push")], True), ([O, bash("git push"), fb, mk.say("x")], False)],
        "D7": [([O, bash("git commit -m x")], True), ([O, mk.tool("Edit", file_path="/r/a", old_string="a", new_string="b")], False)],
        "D10": [([O, bash("git -c user.name=a commit -m x")], True), ([O, bash("git -C /r commit -m x")], False), ([O, bash("git status")], False)],
        "D11": [([O, bash("git revert --no-edit HEAD")], True), ([O, bash("git commit -m x")], False)],
        "D12": [([O, mk.tool("mcp__claude-code-remote__send_later", message="m", delay_minutes=5)], True), ([O, mk.tool("mcp__github__update_pull_request", pullNumber=1)], False)],
        "D13": [([O, mk.tool("mcp__github__create_branch", branch="x")], True), ([O, mk.tool("mcp__github__push_files", branch="x")], False)],
        "D8": [([mk.compact_summary("s"), bash("git push")], True), ([O, bash("git push")], False)],
        "D9": [([mk.compact_summary("s"), bash("git push")], True), ([mk.compact_summary("s"), mk.say("x")], False), ([O, bash("git push")], False)],
    }
    bad = 0
    for did, what, body in DETECTORS:
        d = build(did, body)
        got = [(mk.run_stop(rows, hooks=d)[0] == "block:F1") for rows, _ in known[did]]
        want = [w for _, w in known[did]]
        bad += got != want
        print("%s self-check %s  got %s want %s" % (did, "ok  " if got == want else "FAIL", got, want))
    print("== detector self-check: %d/%d detectors correct on known answers ==" % (len(DETECTORS) - bad, len(DETECTORS)))
    return bad == 0


def main():
    global DETECTORS
    if sys.argv[1:]:
        DETECTORS = [d for d in DETECTORS if d[0] in sys.argv[1:]]
    os.makedirs(OUT, exist_ok=True)
    if not selfcheck():
        print("self-check failed: not running on the real record")
        return
    for did, what, body in DETECTORS:
        d = build(did, body)
        r = subprocess.run([sys.executable, REPLAY, "--hooks", d, "--what", "stop"], capture_output=True, text=True,
                           env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        lines = [ln for ln in r.stdout.splitlines() if ln.startswith("  2026")]
        yes = [ln.strip()[:16] for ln in lines if "BLOCK:F1" in ln]
        odd = [ln for ln in lines if "BLOCK:F1" not in ln and "now: allow" not in ln]
        print("%s %s\n     yes at %d of %d real stop points%s%s" % (
            did, what, len(yes), len(lines), (": " + ", ".join(yes)) if yes else "", ("   UNEXPECTED LABELS: %d" % len(odd)) if odd else ""))
        if r.returncode != 0:
            print("     replay exit %d: %s" % (r.returncode, r.stderr.strip().splitlines()[-1:]))


if __name__ == "__main__":
    main()
