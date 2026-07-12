#!/usr/bin/env python3
"""CORRECTED Phase 2 runner. Fixes the project-scope-leak confound: run dirs live
OUTSIDE the repo tree (under RUNROOT) so the repo's project-scope .claude/skills/
does NOT load, making personal-scope install the true independent variable.
Transcripts still land in the repo's transcripts_v2/ for commit.

Usage: run_arm_v2.py <with|without>
Env: RUNROOT must be set to a dir OUTSIDE the repo."""
import json, os, shutil, subprocess, sys, time

BASE = os.path.dirname(os.path.abspath(__file__))
ARM = sys.argv[1]
assert ARM in ("with", "without")
RUNS = 2
RUNROOT = os.environ["RUNROOT"]  # outside-repo, outside-~/.claude scratch root
_rp = os.path.realpath(RUNROOT)
assert "claude-core-skills" not in _rp, "RUNROOT must be OUTSIDE the repo"
assert "/.claude" not in _rp, "RUNROOT must be OUTSIDE ~/.claude (else .claude ancestor discovery leaks skills)"

cfg = json.load(open(os.path.join(BASE, "prompts.json")))
MODEL = cfg["model"]
TRANS = os.path.join(BASE, "transcripts_v2")
os.makedirs(TRANS, exist_ok=True)

def run_one(p, n):
    key = p["key"]
    out = os.path.join(TRANS, f"{key}__{ARM}__r{n}.jsonl")
    if os.path.exists(out) and os.path.getsize(out) > 0:
        print(f"  skip (exists): {key} r{n}", flush=True); return
    wd = os.path.join(RUNROOT, ARM, key, f"r{n}")
    if os.path.exists(wd):
        shutil.rmtree(wd)
    os.makedirs(wd)
    if p.get("planted"):
        src = os.path.join(BASE, "planted", p["planted"])
        for root, _, files in os.walk(src):
            for f in files:
                s = os.path.join(root, f); rel = os.path.relpath(s, src)
                d = os.path.join(wd, rel); os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copy2(s, d)
    cmd = ["claude", "-p", p["prompt"], "--model", MODEL,
           "--output-format", "stream-json", "--verbose", "--dangerously-skip-permissions"]
    t0 = time.time()
    with open(out, "w") as fo, open(out + ".err", "w") as fe, open(os.devnull) as fin:
        rc = subprocess.run(cmd, cwd=wd, stdin=fin, stdout=fo, stderr=fe).returncode
    print(f"  done: {key} r{n}  rc={rc}  {time.time()-t0:.0f}s  {os.path.getsize(out)}B", flush=True)

print(f"=== ARM: {ARM} (RUNROOT={RUNROOT}) ===", flush=True)
for p in cfg["prompts"]:
    for n in range(1, RUNS + 1):
        try:
            run_one(p, n)
        except Exception as ex:
            o = os.path.join(TRANS, f"{p['key']}__{ARM}__r{n}.jsonl")
            if os.path.exists(o) and os.path.getsize(o) == 0:
                os.remove(o)
            print(f"  ERROR {p['key']} r{n}: {ex!r}", flush=True)
print(f"=== ARM {ARM} complete ===", flush=True)
