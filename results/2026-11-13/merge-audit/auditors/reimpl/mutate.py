#!/usr/bin/env python3
"""mutate.py — mutation check of the library's own fixture (hooks/selftest-turn-gates.py), auditor key reimpl.

For each mutation: copy lib/hooks into work/reimpl/mut/<name>/, change ONE behaviour in the copy, run the
fixture from the copy, print its summary line. A mutation the fixture still passes is an unpinned behaviour.
Two mutations are controls that the fixture MUST catch (they prove the check can fail).

    python3 /tmp/claude-0/-home-user/ff01f16c-7b3f-5ea5-8051-7a95ac7cd1d1/scratchpad/merge-audit/work/reimpl/mutate.py
"""
import os
import shutil
import subprocess

PACK = "/tmp/claude-0/-home-user/ff01f16c-7b3f-5ea5-8051-7a95ac7cd1d1/scratchpad/merge-audit"
HERE = os.path.join(PACK, "work", "reimpl")
SRC = os.path.join(PACK, "lib", "hooks")
MUT = os.path.join(HERE, "mut")
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=os.path.join(HERE, "tmp"))

# (name, file, old, new, what it changes, expectation)
MUTATIONS = [
    ("M0-none", None, None, None, "no change (control: fixture passes)", "pass"),
    ("M1-negation-off", "turngate.py", "if not NEGATION.search(text[:m.start()]):", "if True:",
     "negation ignored entirely (control: fixture must FAIL)", "fail"),
    ("M2-clicks-off", "turngate.py", 'if "questions have been answered" in t:', 'if False and "questions have been answered" in t:',
     "no clickable answer ever recognised (control: fixture must FAIL)", "fail"),
    ("M3-word-only-merge", "turngate.py", r'MERGE_WORD = re.compile(r"\bmerg(e|ed|ing)\b", re.I)', r'MERGE_WORD = re.compile(r"\bmerge\b", re.I)',
     "'merged' / 'merging' no longer count as the word (the stated rule)", "?"),
    ("M4-window-zero", "turngate.py", r"(\w+\W+){0,1}$", r"(\w+\W+){0,0}$",
     "negation must sit DIRECTLY before the word", "?"),
    ("M5-window-four", "turngate.py", r"(\w+\W+){0,1}$", r"(\w+\W+){0,4}$",
     "negation may sit up to five words before the word", "?"),
    ("M6-curly-apostrophe", "turngate.py", r"(don'?t|do\s+not|", "(don['’]?t|can['’]?t|cannot|shouldn['’]?t|won['’]?t|do\\s+not|",
     "curly apostrophe and can't / cannot / shouldn't / won't are negations", "?"),
    ("M7-click-needs-lead", "turngate.py", 'if "questions have been answered" in t:', 'if t.startswith("Your questions have been answered"):',
     "an answer must START with the harness lead (a mid-text quote no longer counts)", "?"),
    ("M8-sched-needs-lead", "turngate.py", "SCHEDULED_HEADER.search(_result_text(b))", 'SCHEDULED_HEADER.search(_result_text(b)) and _result_text(b).startswith("[SYSTEM NOTIFICATION")',
     "a scheduled header counts only in a result that starts with the notification lead", "?"),
    ("M9-marker-prefix-only", "turngate.py", "if not t or any(m in t for m in HARNESS_MARKERS):", "if not t or t.lstrip().startswith(tuple(HARNESS_MARKERS)):",
     "a harness marker counts only at the START of a user row", "?"),
    ("M10-no-owner-denies-merge", "turn-gates-pretool.py", "    if li < 0:\n        sys.exit(0)", "    if li < 0:\n        if turngate.is_merge(block):\n            deny('no owner message')\n        sys.exit(0)",
     "a merge with no owner message in the transcript is denied", "?"),
    ("M11-number-without-hash", "turngate.py", 'r"#\\s?" + re.escape(target) + r"\\b"', 'r"\\b" + re.escape(target) + r"\\b"',
     "clause 3 accepts the PR number without '#'", "?"),
    ("M12-clause3-reads-reply", "turngate.py", "        return bool(says_merge(t) and target and re.search(",
     "        if re.match(r\"\\s*(no|stop|wait|not yet)\\b\", owner_text(rows, li) or \"\", re.I):\n            return False\n        return bool(says_merge(t) and target and re.search(",
     "clause 3 refuses when the owner's reply starts with no / stop / wait / not yet", "?"),
    ("M13-git-config-flag", "turngate.py", r"(-C\s+\S+\s+)?(commit|push)", r"((-C|-c)\s+\S+\s+)*(commit|push)",
     "git -c key=value commit / push count as outward", "?"),
    ("M14-commit-anything-outward-off", "turngate.py", 'OUTWARD_TOOL_SUFFIXES = ("merge_pull_request", "create_pull_request", "update_pull_request", "push_files",\n                         "create_or_update_file", "delete_file", "create_trigger", "update_trigger", "delete_trigger")',
     'OUTWARD_TOOL_SUFFIXES = ("merge_pull_request", "create_pull_request")',
     "update_pull_request, file pushes and scheduled-task tools no longer outward", "?"),
]

for name, fname, old, new, what, expect in MUTATIONS:
    dst = os.path.join(MUT, name)
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("__pycache__"))
    applied = "-"
    if fname:
        path = os.path.join(dst, fname)
        text = open(path).read()
        applied = "applied" if old in text else "NOT APPLIED (pattern not found)"
        open(path, "w").write(text.replace(old, new))
    r = subprocess.run(["python3", "selftest-turn-gates.py"], cwd=dst, capture_output=True, text=True, env=ENV)
    out = (r.stdout + r.stderr).strip().split("\n")
    summary = out[-1] if out else "(no output)"
    failed = [ln.strip()[:110] for ln in out if ln.strip().startswith("FAIL")]
    verdict = "still passes" if " 0 failed" in summary else "caught"
    print("%-32s %-9s | %-38s | %-13s | %s" % (name, applied, summary, verdict, what))
    for ln in failed[:3]:
        print("      " + ln)
