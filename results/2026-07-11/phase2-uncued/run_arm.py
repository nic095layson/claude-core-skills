#!/usr/bin/env python3
"""Uncued discriminating test runner. Same isolation as Phase 2 v2: run dirs
OUTSIDE repo/~/.claude (RUNROOT) so no project-scope skill leak. Loops both models.
Usage: run_arm.py <with|without>   Env: RUNROOT (outside repo/~/.claude)."""
import json, os, shutil, subprocess, sys, time

BASE = "/private/tmp/phase2_uncued"
ARM = sys.argv[1]; assert ARM in ("with", "without")
RUNS = 2
MODELS = ["claude-opus-4-8[1m]", "claude-sonnet-5"]
RUNROOT = os.environ["RUNROOT"]
_rp = os.path.realpath(RUNROOT)
assert "claude-core-skills" not in _rp, "RUNROOT must be OUTSIDE the repo"
assert "/.claude" not in _rp, "RUNROOT must be OUTSIDE ~/.claude"

PROMPTS = json.load(open(os.path.join(BASE, "prompts.json")))["prompts"]
TRANS = os.path.join(BASE, "transcripts"); os.makedirs(TRANS, exist_ok=True)

def mtag(m): return "opus" if "opus" in m else "sonnet"

def run_one(p, model, n):
    key = p["key"]; mt = mtag(model)
    out = os.path.join(TRANS, f"{key}__{mt}__{ARM}__r{n}.jsonl")
    if os.path.exists(out) and os.path.getsize(out) > 0:
        print(f"  skip (exists): {key} {mt} r{n}", flush=True); return
    wd = os.path.join(RUNROOT, ARM, f"{key}__{mt}", f"r{n}")
    if os.path.exists(wd): shutil.rmtree(wd)
    os.makedirs(wd)
    src = os.path.join(BASE, "planted", p["planted"])
    for root, _, files in os.walk(src):
        for f in files:
            s = os.path.join(root, f); rel = os.path.relpath(s, src)
            d = os.path.join(wd, rel); os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(s, d)
    cmd = ["claude", "-p", p["prompt"], "--model", model,
           "--output-format", "stream-json", "--verbose", "--dangerously-skip-permissions"]
    t0 = time.time()
    with open(out, "w") as fo, open(out + ".err", "w") as fe, open(os.devnull) as fin:
        rc = subprocess.run(cmd, cwd=wd, stdin=fin, stdout=fo, stderr=fe).returncode
    print(f"  done: {key} {mt} r{n}  rc={rc}  {time.time()-t0:.0f}s  {os.path.getsize(out)}B", flush=True)

print(f"=== ARM: {ARM} (RUNROOT={RUNROOT}) ===", flush=True)
for model in MODELS:
    for p in PROMPTS:
        for n in range(1, RUNS + 1):
            try: run_one(p, model, n)
            except Exception as ex:
                o = os.path.join(TRANS, f"{p['key']}__{mtag(model)}__{ARM}__r{n}.jsonl")
                if os.path.exists(o) and os.path.getsize(o) == 0: os.remove(o)
                print(f"  ERROR {p['key']} {mtag(model)} r{n}: {ex!r}", flush=True)
print(f"=== ARM {ARM} complete ===", flush=True)
