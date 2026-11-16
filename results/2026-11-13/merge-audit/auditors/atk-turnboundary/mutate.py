#!/usr/bin/env python3
"""Mutation check (atk-turnboundary): which turn-boundary behaviours do the library's own selftests pin?

For each mutation: copy lib/hooks (1ce99d5) to ./mut/<name>/, change ONE behaviour in the copy, run the copy's
selftests from the copy. "SURVIVES" = every selftest still passes = no test pins that behaviour.
Two control mutations at the top must be CAUGHT, or this harness is the broken part.

    python3 <this file>          (from any directory; writes only under its own directory)
"""
import os, shutil, subprocess, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
PACK = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(PACK, "lib", "hooks")
TMP = os.path.join(HERE, "tmp"); os.makedirs(TMP, exist_ok=True)
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=TMP)

MUTATIONS = [
    ("C0-no-mutation", []),
    ("C1-control-F1-ignores-scheduled-boundary", [("governance-enforce.py",
        "_li = turngate.turn_start(lines)", "_li = turngate.owner_index(lines)")]),
    ("C2-control-task-notification-is-owner", [("turngate.py",
        "if not t or any(m in t for m in HARNESS_MARKERS):", "if not t:")]),
    ("M1-no-owner-message-merge-DENIED-instead-of-allowed", [("turn-gates-pretool.py",
        "    if li < 0:\n        sys.exit(0)\n",
        "    if li < 0:\n        if turngate.is_merge(block):\n            deny('TURN-GATE (merge word): no owner message in the transcript')\n        sys.exit(0)\n")]),
    ("M2-isMeta-and-compact-summary-rows-count-as-owner", [("turngate.py",
        'if d.get("type") != "user" or d.get("isMeta") or d.get("isCompactSummary"):', 'if d.get("type") != "user":')]),
    ("M3-scheduled-index-takes-FIRST-run-not-latest", [("turngate.py",
        "               for b in c):\n            si = i\n", "               for b in c):\n            si = i if si < 0 else si\n")]),
    ("M4-header-form-dropped-plain-substring", [("turngate.py",
        'SCHEDULED_HEADER = re.compile(r"^--- Notification .*· origin: scheduled trigger", re.M)',
        'SCHEDULED_HEADER = re.compile(r"origin: scheduled trigger")')]),
    ("M5-any-past-scheduled-run-outranks-a-later-owner-message", [("turngate.py",
        "    return max(owner_index(rows), scheduled_index(rows))",
        "    return scheduled_index(rows) if scheduled_index(rows) >= 0 else owner_index(rows)")]),
    ("M6-every-tool-result-is-an-owner-click", [("turngate.py",
        'if "questions have been answered" in t:', "if True:")]),
    ("M7-only-ReadNotifications-results-can-start-a-scheduled-turn (stricter, the stated rule)", [("turngate.py",
        "def scheduled_index(rows):",
        "def _rn_ids(rows):\n    ids = set()\n    for d in rows:\n        m = d.get('message') if isinstance(d.get('message'), dict) else {}\n"
        "        for b in (m.get('content') or []) if isinstance(m.get('content'), list) else []:\n"
        "            if isinstance(b, dict) and b.get('type') == 'tool_use' and b.get('name') == 'ReadNotifications':\n                ids.add(b.get('id'))\n    return ids\n\n\n"
        "def scheduled_index(rows):"),
        ("turngate.py", 'b.get("type") == "tool_result" and SCHEDULED_HEADER.search(_result_text(b))',
         'b.get("type") == "tool_result" and b.get("tool_use_id") in _rn_ids(rows) and SCHEDULED_HEADER.search(_result_text(b))')]),
    ("M8-receipt-gate-turn-starts-only-at-NON-meta-string-rows", [("receipt-law-stop-gate.sh",
        "    if isinstance(content, str):\n", '    if isinstance(content, str) and not e.get("isMeta"):\n')]),
    ("M9-receipt-gate-turn-starts-at-ANY-user-row-even-tool-results", [("receipt-law-stop-gate.sh",
        "    if isinstance(content, str):\n", "    if True:\n")]),
    ("M10-prompt-class-half-forgets-the-prompt-after-a-scheduled-run", [("governance-enforce.py",
        "if not prompt:\n    sys.exit(0)\n",
        "try:\n    if turngate.scheduled_index(lines) > li:\n        prompt = None\nexcept Exception:\n    pass\nif not prompt:\n    sys.exit(0)\n")]),
]
TESTS = [("selftest-turn-gates.py", ["python3"]), ("selftest-governance-classify.py", ["python3"]), ("selftest-receipt-law.sh", ["bash"])]

for name, edits in MUTATIONS:
    key = name.split(" ")[0]
    dst = os.path.join(HERE, "mut", key)
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("__pycache__"))
    for fname, old, new in edits:
        p = os.path.join(dst, fname)
        s = open(p, encoding="utf-8").read()
        if s.count(old) != 1:
            print("HARNESS ERROR: %s: pattern occurs %d times in %s" % (name, s.count(old), fname)); sys.exit(2)
        open(p, "w", encoding="utf-8").write(s.replace(old, new))
    res = []
    for t, cmd in TESTS:
        r = subprocess.run(cmd + [os.path.join(dst, t)], capture_output=True, text=True, env=ENV, cwd=dst)
        tail = (r.stdout.strip().splitlines() or ["(no output)"])[-1].strip()
        fails = [l.strip()[:90] for l in r.stdout.splitlines() if l.strip().startswith("FAIL")]
        res.append((t, r.returncode, tail, fails))
    verdict = "SURVIVES" if all(rc == 0 for _, rc, _, _ in res) else "CAUGHT"
    print("%s %s" % (verdict, name))
    for t, rc, tail, fails in res:
        print("- %s exit %d %s" % (t, rc, tail))
        for f in fails[:4]:
            print("-- " + " ".join(f.split()))
