#!/usr/bin/env python3
"""FINAL ACCEPTANCE Part 2 runner — regression test of the 3 shipped governors
against the live personal-scope install. Fresh claude -p session per run, cwd in a
clean per-run dir OUTSIDE the repo and OUTSIDE ~/.claude (so only the personal-scope
install loads), model claude-opus-4-8[1m], stream-json. 2 runs per prompt."""
import json, os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed

REPO = "/Users/davidlayson/claude-core-skills"
BASE = os.path.dirname(os.path.abspath(__file__))          # scratchpad/accept
RUNROOT = os.path.join(BASE, "runs")
TRANS = os.path.join(BASE, "transcripts")
MODEL = "claude-opus-4-8[1m]"
RUNS = 2
WORKERS = 5

rp = os.path.realpath(RUNROOT) + "/"
assert not rp.startswith(os.path.realpath(REPO) + "/"), "RUNROOT must be OUTSIDE the repo tree"
assert not rp.startswith(os.path.realpath(os.path.expanduser("~/.claude")) + "/"), "RUNROOT must be OUTSIDE ~/.claude"
os.makedirs(TRANS, exist_ok=True)

# ---- Build the case list from the standing eval sets -----------------------
SELECT = {
    "plan-gate":          {"fire": [1, 2, 3], "silent": [4, 5]},
    "adversarial-verify": {"fire": [6, 7, 8], "silent": [4, 5]},
    "scope-fence":        {"fire": [1, 2, 3, 8], "silent": [4, 5]},
}
cases = []
for gov, sel in SELECT.items():
    evals = {e["id"]: e for e in json.load(open(f"{REPO}/evals/{gov}.json"))["evals"]}
    for cls in ("fire", "silent"):
        for i in sel[cls]:
            e = evals[i]
            cases.append({"key": f"{gov}__id{i}", "gov": gov, "id": i,
                          "expect": cls, "prompt": e["prompt"]})
# canary is plan-gate id4 ("what's 15% of 80?") — assert cross-governor silence there.

def run_one(case, n):
    key = case["key"]
    out = os.path.join(TRANS, f"{key}__r{n}.jsonl")
    if os.path.exists(out) and os.path.getsize(out) > 0:
        return f"skip {key} r{n}"
    wd = os.path.join(RUNROOT, key, f"r{n}")
    if os.path.exists(wd):
        shutil.rmtree(wd)
    os.makedirs(wd)                       # clean, empty scratchpad per run
    cmd = ["claude", "-p", case["prompt"], "--model", MODEL,
           "--output-format", "stream-json", "--verbose",
           "--dangerously-skip-permissions"]
    t0 = time.time()
    with open(out, "w") as fo, open(out + ".err", "w") as fe, open(os.devnull) as fin:
        try:
            rc = subprocess.run(cmd, cwd=wd, stdin=fin, stdout=fo, stderr=fe,
                                timeout=360).returncode
        except subprocess.TimeoutExpired:
            rc = "TIMEOUT"
    sz = os.path.getsize(out)
    if sz == 0:
        os.remove(out)
        return f"EMPTY {key} r{n} rc={rc} {time.time()-t0:.0f}s"
    return f"done {key} r{n} rc={rc} {time.time()-t0:.0f}s {sz}B"

jobs = [(c, n) for c in cases for n in range(1, RUNS + 1)]
print(f"=== {len(cases)} cases, {len(jobs)} runs, {WORKERS} workers, model={MODEL} ===", flush=True)
with ThreadPoolExecutor(max_workers=WORKERS) as ex:
    futs = {ex.submit(run_one, c, n): (c, n) for c, n in jobs}
    for f in as_completed(futs):
        print("  " + f.result(), flush=True)
print("=== ALL RUNS COMPLETE ===", flush=True)
