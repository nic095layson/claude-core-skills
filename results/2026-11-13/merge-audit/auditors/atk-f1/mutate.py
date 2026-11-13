#!/usr/bin/env python3
"""Mutation check for the F1 cases of hooks/selftest-turn-gates.py (COMMON.md section 5).

For each mutation: copy lib/hooks into work/atk-f1/mut/<id>/hooks, change ONE behaviour in the copy, run the copy's
selftest-turn-gates.py. "SURVIVES" = the suite still passes, so that behaviour is not pinned by it.
Controls (C*) are mutations the suite is expected to catch; they prove this harness can see a failure.

Run: python3 <this file>
"""
import os
import shutil
import subprocess
import sys

PACK = "/tmp/claude-0/-home-user/ff01f16c-7b3f-5ea5-8051-7a95ac7cd1d1/scratchpad/merge-audit"
SRC = PACK + "/lib/hooks"
OUT = PACK + "/work/atk-f1/mut"

TG, GE = "turngate.py", "governance-enforce.py"
SUFFIX_OLD = '''OUTWARD_TOOL_SUFFIXES = ("merge_pull_request", "create_pull_request", "update_pull_request", "push_files",
                         "create_or_update_file", "delete_file", "create_trigger", "update_trigger", "delete_trigger")'''
BASH_OLD = r'''OUTWARD_BASH = re.compile(r"\bgit\s+(-C\s+\S+\s+)?(commit|push)\b|\bgh\s+pr\s+(create|merge)\b")'''
SKILL_OLD = '''    return str((block.get("input") or {}).get("skill") or "").split(":")[-1].strip()'''

MUTATIONS = [
    ("M1a", "file-push tools no longer outward (push_files, create_or_update_file, delete_file)", TG, SUFFIX_OLD,
     '''OUTWARD_TOOL_SUFFIXES = ("merge_pull_request", "create_pull_request", "update_pull_request",
                         "create_trigger", "update_trigger", "delete_trigger")'''),
    ("M1b", "scheduled-task tools no longer outward (create/update/delete_trigger)", TG, SUFFIX_OLD,
     '''OUTWARD_TOOL_SUFFIXES = ("merge_pull_request", "create_pull_request", "update_pull_request", "push_files",
                         "create_or_update_file", "delete_file")'''),
    ("M1c", "update_pull_request no longer outward", TG, SUFFIX_OLD,
     '''OUTWARD_TOOL_SUFFIXES = ("merge_pull_request", "create_pull_request", "push_files",
                         "create_or_update_file", "delete_file", "create_trigger", "update_trigger", "delete_trigger")'''),
    ("M2", "shell `gh pr create` / `gh pr merge` no longer outward for F1", TG, BASH_OLD,
     r'''OUTWARD_BASH = re.compile(r"\bgit\s+(-C\s+\S+\s+)?(commit|push)\b")'''),
    ("M3", "`git -C <dir> commit|push` no longer outward", TG, BASH_OLD,
     r'''OUTWARD_BASH = re.compile(r"\bgit\s+(commit|push)\b|\bgh\s+pr\s+(create|merge)\b")'''),
    ("M4", "a Skill call counts as a governor load when the governor's name appears ANYWHERE in its input (attack G3)", TG, SKILL_OLD,
     '''    _s = json.dumps(block.get("input") or {})
    return next((g for g in GOVERNORS if g in _s), "")'''),
    ("M5", "F1's own error handler re-raises instead of failing open", GE,
     "except Exception:\n    pass  # fail open: the prompt-class gate below still runs",
     "except Exception:\n    raise"),
    ("M6", "F1 block reason no longer tells the assistant what to do (remedy sentences removed)", GE,
     '''+ " and ".join(_miss) + ". Load the missing governor with the Skill tool now and follow it."''',
     '''+ " and ".join(_miss) + "."'''),
    ("M7", "F1 is skipped whenever the turn has more than one outward action (e.g. commit AND push)", GE,
     "        if _first is not None:",
     "        if _first is not None and sum(1 for kind, b in _ev if kind == 'tool' and turngate.is_outward(b)) == 1:"),
    ("C1", "CONTROL plan-gate may load anywhere in the turn (not only before the first outward action)", GE,
     "for kind, b in _ev[:_first])", "for kind, b in _ev)"),
    ("C2", "CONTROL `git commit` no longer outward", TG, BASH_OLD,
     r'''OUTWARD_BASH = re.compile(r"\bgit\s+(-C\s+\S+\s+)?(push)\b|\bgh\s+pr\s+(create|merge)\b")'''),
    ("C3", "CONTROL adversarial-verify must come AFTER the first outward action (the pre-narrowing rule)", GE,
     '''_av = any(kind == "tool" and turngate.skill_name(b) == "adversarial-verify" for kind, b in _ev)''',
     '''_av = any(kind == "tool" and turngate.skill_name(b) == "adversarial-verify" for kind, b in _ev[_first:])'''),
    ("C4", "CONTROL scope prefix not stripped from the Skill name", TG, SKILL_OLD,
     '''    return str((block.get("input") or {}).get("skill") or "").strip()'''),
]


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    base = subprocess.run([sys.executable, SRC + "/selftest-turn-gates.py"], capture_output=True, text=True,
                          env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    print("unmutated lib/hooks: exit %d  %s" % (base.returncode, base.stdout.strip().splitlines()[-1]))
    for mid, what, fname, old, new in MUTATIONS:
        d = os.path.join(OUT, mid, "hooks")
        shutil.copytree(SRC, d, ignore=shutil.ignore_patterns("__pycache__"))
        p = os.path.join(d, fname)
        s = open(p, encoding="utf-8").read()
        if s.count(old) != 1:
            print("%-4s NOT APPLIED (pattern found %d times) %s" % (mid, s.count(old), what))
            continue
        open(p, "w", encoding="utf-8").write(s.replace(old, new))
        r = subprocess.run([sys.executable, os.path.join(d, "selftest-turn-gates.py")], capture_output=True, text=True,
                           env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        lines = r.stdout.strip().splitlines()
        fails = [ln.strip()[:110] for ln in lines if ln.strip().startswith("FAIL")]
        verdict = "SURVIVES (not pinned)" if r.returncode == 0 else "caught"
        print("%-4s %-22s exit %d  %s  | %s" % (mid, verdict, r.returncode, lines[-1] if lines else "(no output)", what))
        for f in fails[:4]:
            print("       " + f)


if __name__ == "__main__":
    main()
