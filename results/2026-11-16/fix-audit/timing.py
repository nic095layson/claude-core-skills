#!/usr/bin/env python3
"""Run time of every gated hook call on one large synthetic session record (finding AC-6 of the outside audit).

    python3 results/2026-11-16/fix-audit/timing.py --hooks hooks [--megabytes 48] [--work DIR]

The record is built with the committed row builder (`<hooks>/selftest_rows.py`), on the recipe of
`results/2026-11-15/turn-gates-fix/timing.txt` and `results/2026-11-15/receipt-gate-fix/timing.py`: rounds of an
owner message, two governor loads (plan-gate, adversarial-verify), a read-only shell call, a file read (with a
9,000-character result), a commit-and-push shell call, an answer and a completed stop; then one more owner message
that orders the merge of pull request 34. The number of rounds is chosen so that the file comes out at about
--megabytes (a probe of 100 rounds is written first and measured).

Each hook is then run ONCE, the way the wiring runs it: the interpreter named in `.claude/settings.json`
(`python3 <hook>` or `bash <hook>`), the hook's input as JSON on standard input, CLAUDE_PROJECT_DIR set to the
folder above the hooks, a fresh TMPDIR, and the work folder as the working directory. Python's compiled-code cache
is pointed into the work folder (PYTHONPYCACHEPREFIX) and filled once, untimed, before the first call
(`python3 -m compileall`), so the hooks folder is not written to and every call finds its modules compiled, as on
a machine where the hooks have run before. The calls:

    Stop gate            governance-enforce.py       Stop
    receipt gate         receipt-law-stop-gate.sh    Stop
    pre merge tool       turn-gates-pretool.py       mcp__github__merge_pull_request, pull request 34
    pre Bash push        turn-gates-pretool.py       Bash, a commit followed by a push of a named branch
    pre Bash ls          turn-gates-pretool.py       Bash, ls
    pre Edit             turn-gates-pretool.py       Edit of a file outside any scratch folder

Printed per call: the wall time, the CPU time of the child and its own children (user + system, from
getrusage(RUSAGE_CHILDREN) before and after), the exit status, and what it printed (silent, or the decision word).
One run of the hooks per invocation: run the tool several times for several samples. On a machine shared with other
work the wall times are noisy; the CPU times less so.

Standard library only; Python 3.8 or later. Writes only in --work (default: a new temporary folder, removed after).
"""
import argparse
import json
import os
import resource
import shutil
import subprocess
import sys
import tempfile
import time

sys.dont_write_bytecode = True        # the hooks folder is copied byte for byte elsewhere: leave no cache in it

PAD = "x" * 9000                      # the file read's result, as in the receipt gate's timing tool
PROBE_ROUNDS = 100                    # rounds written to measure the size of one round
MERGE_PR = 34
BRANCH_PUSH = "git add -A && git commit -qm x && git push -u origin claude/x"
EDIT_PATH = "/work/acme/lib/a.md"     # not under any scratch folder, so the write is judged
MERGE_TOOL = "mcp__github__merge_pull_request"


def rounds_rows(R, n):
    rows = []
    for i in range(n):
        rows += R.flat(R.owner("Continue with step %d" % i), R.skill("plan-gate"), R.skill("adversarial-verify"),
                       R.bash("git status", "clean"), R.call("Read", PAD, file_path="/work/acme/lib/a.md"),
                       R.bash(BRANCH_PUSH, "ok"),
                       R.say("Step %d done: read the file, committed and pushed. %s" % (i, "Details follow. " * 20)),
                       R.stop())
    return rows


def build(R, work, megabytes):
    tail = [R.owner("Merge #%d" % MERGE_PR)]
    probe = R.write(rounds_rows(R, PROBE_ROUNDS) + tail, os.path.join(work, "probe.jsonl"))
    per_round = os.path.getsize(probe) / PROBE_ROUNDS
    os.remove(probe)
    n = max(1, int(round(megabytes * 1e6 / per_round)))
    rows = rounds_rows(R, n) + tail
    path = R.write(rows, os.path.join(work, "record.jsonl"))
    return path, n, len(rows)


def verdict_of(out):
    out = out.strip()
    if not out:
        return "silent"
    try:
        j = json.loads(out)
    except ValueError:
        return "printed text"
    if j.get("decision"):
        return j["decision"]
    spec = j.get("hookSpecificOutput") or {}
    if spec.get("permissionDecision"):
        return spec["permissionDecision"]
    if spec.get("additionalContext"):
        return "advisory"
    return "printed json"


def run_once(argv, payload, env, cwd):
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    began = time.perf_counter()
    p = subprocess.run(argv, input=json.dumps(payload), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       universal_newlines=True, env=env, cwd=cwd)
    wall = time.perf_counter() - began
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    cpu = (after.ru_utime - before.ru_utime) + (after.ru_stime - before.ru_stime)
    return wall, cpu, p.returncode, verdict_of(p.stdout)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--hooks", required=True, help="the hooks folder to time")
    ap.add_argument("--megabytes", type=float, default=48.0, help="size of the synthetic record (default 48)")
    ap.add_argument("--work", help="folder for the record and the hooks' state (default: a new temporary folder)")
    a = ap.parse_args()

    hooks = os.path.abspath(a.hooks)
    sys.path.insert(0, hooks)
    import selftest_rows as R                       # the committed row builder of the hooks under test

    own_work = a.work is None
    work = os.path.abspath(a.work) if a.work else tempfile.mkdtemp(prefix="hook-timing-")
    os.makedirs(work, exist_ok=True)
    try:
        record, n, nrows = build(R, work, a.megabytes)
        size = os.path.getsize(record) / 1e6
        print("synthetic record: %.1f MB, %d rows (%d rounds), python %s" % (size, nrows, n, sys.version.split()[0]))

        env = dict(os.environ)
        env["CLAUDE_PROJECT_DIR"] = os.path.dirname(hooks)
        env["PYTHONPYCACHEPREFIX"] = os.path.join(work, "pycache")
        subprocess.run(["python3", "-m", "compileall", "-q", hooks], env=env, stdout=subprocess.DEVNULL, check=True)
        cwd = os.path.join(work, "cwd")
        os.makedirs(cwd, exist_ok=True)
        base = {"session_id": "timing", "transcript_path": record, "cwd": cwd}
        stop = dict(base, hook_event_name="Stop", stop_hook_active=False)

        def pre(tool_name, tool_input):
            return dict(base, hook_event_name="PreToolUse", tool_name=tool_name, tool_input=tool_input)

        py = lambda f: ["python3", os.path.join(hooks, f)]
        sh = lambda f: ["bash", os.path.join(hooks, f)]
        calls = [
            ("Stop gate (governance-enforce.py)", py("governance-enforce.py"), stop),
            ("receipt gate (receipt-law-stop-gate.sh)", sh("receipt-law-stop-gate.sh"), stop),
            ("pre merge tool", py("turn-gates-pretool.py"),
             pre(MERGE_TOOL, {"owner": "acme", "repo": "lib", "pullNumber": MERGE_PR, "merge_method": "squash"})),
            ("pre Bash commit+push", py("turn-gates-pretool.py"), pre("Bash", {"command": BRANCH_PUSH})),
            ("pre Bash ls", py("turn-gates-pretool.py"), pre("Bash", {"command": "ls"})),
            ("pre Edit", py("turn-gates-pretool.py"),
             pre("Edit", {"file_path": EDIT_PATH, "old_string": "a", "new_string": "b"})),
        ]
        print("%-42s %8s %8s %5s  %s" % ("call", "wall s", "cpu s", "exit", "printed"))
        for label, argv, payload in calls:
            tmp = os.path.join(work, "tmp-" + str(calls.index((label, argv, payload))))
            os.makedirs(tmp, exist_ok=True)
            env["TMPDIR"] = tmp
            wall, cpu, status, said = run_once(argv, payload, env, cwd)
            print("%-42s %8.2f %8.2f %5d  %s" % (label, wall, cpu, status, said))
    finally:
        if own_work:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
