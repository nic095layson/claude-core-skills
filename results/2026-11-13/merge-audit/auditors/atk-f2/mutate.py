#!/usr/bin/env python3
"""Mutation check for the F2 and S cases of hooks/selftest-turn-gates.py.

For each mutant: copy lib/hooks into work/atk-f2/mut/<name>/, change ONE behaviour in the copy, run the copy's own
selftest-turn-gates.py. "SURVIVES" = the selftest still reports 0 failed, so no case pins that behaviour.
Usage: python3 mutate.py            (rebuilds every mutant, prints one line each)
"""
import os
import shutil
import subprocess
import sys

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
HERE = os.path.dirname(os.path.abspath(__file__))
PACK = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(PACK, "lib", "hooks")
OUT = os.path.join(HERE, "mut")

SCHED_BLOCK = '''    # A scheduled run carries no owner message, so it carries no owner word to merge: it never merges.
    if turngate.is_merge(block) and li > oi:
        target = turngate.merge_target(block)
        deny("TURN-GATE (merge word): a scheduled run never merges" + (f" PR #{target}" if target else "")
             + ". Record it as an open decision in the run's report; the owner merges on their own word.")
'''
NEG = r'''NEGATION = re.compile(r"\b(don'?t|do\s+not|dont|never|not|no|without|hold\s+off(\s+on)?|wait\s+(to|before))\W+(\w+\W+){0,1}$", re.I)'''

MUTANTS = [
    # name, file, old, new, what it changes
    ("control-unchanged", None, None, None, "no change (the check itself: must report 0 failed)"),
    ("control-known-kill", "turngate.py", 'MERGE_WORD = re.compile(r"\\bmerg(e|ed|ing)\\b", re.I)',
     'MERGE_WORD = re.compile(r"\\bmerg\\w*", re.I)', "'mergeable' counts as the word (a case pins this: must FAIL)"),
    ("A-no-scheduled-deny", "turn-gates-pretool.py", SCHED_BLOCK, "", "delete the whole 'a scheduled run never merges' block"),
    ("B-merge-only", "turngate.py", 'MERGE_WORD = re.compile(r"\\bmerg(e|ed|ing)\\b", re.I)',
     'MERGE_WORD = re.compile(r"\\bmerge\\b", re.I)', "the word is 'merge' only: 'merged'/'merging' no longer count"),
    ("C-negation-dont-only", "turngate.py", NEG,
     r'''NEGATION = re.compile(r"\b(don'?t|do\s+not)\W+(\w+\W+){0,1}$", re.I)''',
     "negations never/not/no/without/hold off/wait to|before/dont removed"),
    ("D-negation-window-0", "turngate.py", NEG, NEG.replace("{0,1}", "{0,0}"), "negation must be immediately before the word"),
    ("D2-negation-window-6", "turngate.py", NEG, NEG.replace("{0,1}", "{0,6}"), "negation up to six words before the word"),
    ("E-first-server-only", "turngate.py", 'return name.endswith("merge_pull_request") or',
     'return name == "mcp__github__merge_pull_request" or', "only the mcp__github__ merge tool is a merge (mcp__GH__ ungated)"),
    ("F-any-tool-result-is-a-click", "turngate.py", 'if "questions have been answered" in t:   # an AskUserQuestion answer: the owner\'s own click',
     'if True:', "every tool_result is read as a clickable answer"),
    ("H-no-owner-row-denies", "turn-gates-pretool.py", "    if li < 0:\n        sys.exit(0)\n",
     "    if li < 0 and not turngate.is_merge(block):\n        sys.exit(0)\n", "a merge with no owner row in the transcript is denied instead of allowed"),
    ("I-no-pull_number-alias", "turngate.py", 'n = inp.get("pullNumber") or inp.get("pull_number")', 'n = inp.get("pullNumber")',
     "the snake_case key is not read"),
    ("J-answers-any-click-in-session", "turngate.py", "    for kind, payload in events(rows, li):\n        if kind == \"answer\"",
     "    for kind, payload in events(rows, -1):\n        if kind == \"answer\"", "a click from ANY earlier turn authorises"),
    ("K-route3-any-earlier-text", "turngate.py",
     '        return bool(says_merge(t) and target and re.search(r"#\\s?" + re.escape(target) + r"\\b", t))\n    return False',
     '        if says_merge(t) and target and re.search(r"#\\s?" + re.escape(target) + r"\\b", t):\n            return True\n    return False',
     "ANY earlier assistant text naming merge + #N authorises, not only the last one"),
    ("L-no-gh-cli", "turngate.py", 'MERGE_BASH = re.compile(r"\\bgh\\s+pr\\s+merge\\b")', 'MERGE_BASH = re.compile(r"\\bgh\\s+pr\\s+merge\\s+--auto\\b")',
     "the CLI merge is gated only with --auto"),
]


def build(name, fname, old, new):
    dst = os.path.join(OUT, name)
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("__pycache__"))
    if fname:
        p = os.path.join(dst, fname)
        s = open(p, encoding="utf-8").read()
        n = s.count(old)
        if n != 1:
            return dst, "PATCH-NOT-APPLIED (pattern found %d times)" % n
        open(p, "w", encoding="utf-8").write(s.replace(old, new))
    return dst, None


def main():
    only = sys.argv[1:] or None
    for name, fname, old, new, what in MUTANTS:
        if only and name not in only:
            continue
        dst, err = build(name, fname, old, new)
        if err:
            print("%-32s %s" % (name, err))
            continue
        r = subprocess.run(["python3", os.path.join(dst, "selftest-turn-gates.py")], capture_output=True, text=True)
        lines = r.stdout.strip().splitlines()
        tail = lines[-1] if lines else "(no output)"
        failed = [l.strip() for l in lines if l.strip().startswith("FAIL")]
        verdict = "SURVIVES" if (r.returncode == 0 and not failed) else "killed"
        print("%-32s %-8s %s | %s" % (name, verdict, tail, what))
        for f in failed[:4]:
            print("%-32s          -> %s" % ("", f[:150]))


if __name__ == "__main__":
    main()
