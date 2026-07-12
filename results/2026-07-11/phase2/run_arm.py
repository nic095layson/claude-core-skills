#!/usr/bin/env python3
"""Run one arm (with|without) of the Phase 2 behavioral A/B: 10 prompts x 2 runs.
Each run: fresh isolated working dir + planted files, `claude -p` stream-json.
Transcripts -> transcripts/<key>__<arm>__r<n>.jsonl. Resumable (skips non-empty)."""
import json, os, shutil, subprocess, sys, time

BASE = os.path.dirname(os.path.abspath(__file__))
ARM = sys.argv[1]  # "with" | "without"
assert ARM in ("with", "without")
RUNS = 2

cfg = json.load(open(os.path.join(BASE, "prompts.json")))
MODEL = cfg["model"]
# v2: session working dir MUST be OUTSIDE the repo so no project-scope
# .claude/skills governors load. Only user-scope ~/.claude/skills applies here,
# which is exactly the variable the two arms toggle. (/tmp has no .claude ancestor.)
RUNROOT = os.environ.get("PHASE2_RUNROOT", "/tmp/phase2_rundirs_594d5c68")
RUNDIRS = os.path.join(RUNROOT, ARM)
TRANS = os.path.join(BASE, "transcripts")  # transcripts are output, stay in-repo
os.makedirs(TRANS, exist_ok=True)

def run_one(p, n):
    key = p["key"]
    out = os.path.join(TRANS, f"{key}__{ARM}__r{n}.jsonl")
    if os.path.exists(out) and os.path.getsize(out) > 0:
        print(f"  skip (exists): {key} r{n}", flush=True)
        return
    wd = os.path.join(RUNDIRS, key, f"r{n}")
    if os.path.exists(wd):
        shutil.rmtree(wd)
    os.makedirs(wd)
    if p.get("planted"):
        src = os.path.join(BASE, "planted", p["planted"])
        for root, _, files in os.walk(src):
            for f in files:
                s = os.path.join(root, f)
                rel = os.path.relpath(s, src)
                d = os.path.join(wd, rel)
                os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copy2(s, d)
    cmd = ["claude", "-p", p["prompt"], "--model", MODEL,
           "--output-format", "stream-json", "--verbose",
           "--dangerously-skip-permissions"]
    t0 = time.time()
    with open(out, "w") as fo, open(out + ".err", "w") as fe, open(os.devnull) as fin:
        rc = subprocess.run(cmd, cwd=wd, stdin=fin, stdout=fo, stderr=fe).returncode
    dt = time.time() - t0
    sz = os.path.getsize(out)
    print(f"  done: {key} r{n}  rc={rc}  {dt:.0f}s  {sz}B", flush=True)

print(f"=== ARM: {ARM} ===", flush=True)
for p in cfg["prompts"]:
    for n in range(1, RUNS + 1):
        try:
            run_one(p, n)
        except Exception as ex:
            # one failed run must not abort the arm; leave no partial file behind
            out = os.path.join(TRANS, f"{p['key']}__{ARM}__r{n}.jsonl")
            if os.path.exists(out) and os.path.getsize(out) == 0:
                os.remove(out)
            print(f"  ERROR: {p['key']} r{n}: {ex!r}", flush=True)
print(f"=== ARM {ARM} complete ===", flush=True)
