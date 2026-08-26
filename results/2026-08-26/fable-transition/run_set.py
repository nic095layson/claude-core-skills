#!/usr/bin/env python3
"""Fable-transition audit runner (2026-08-26). One fresh `claude -p` session per run,
cwd in a clean per-run dir OUTSIDE the repo and OUTSIDE ~/.claude (so the personal-
scope install is the only skill source), stream-json, N runs per prompt, parallel
workers. Records the SERVED model per run from the transcript's system-init event
(register row 12: Fable can be silently routed to Opus; a run served by another
model is excluded and re-run, never averaged in).

Usage: run_set.py <prompts.json> <arm-label>      Env: RUNROOT (outside repo/~/.claude)
"""
import json, os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed

REPO = "/Users/davidlayson/claude-core-skills"
BASE = os.path.dirname(os.path.abspath(__file__))
PROMPTS, ARM = sys.argv[1], sys.argv[2]
RUNROOT = os.environ["RUNROOT"]
_rp = os.path.realpath(RUNROOT)
assert not _rp.startswith(os.path.realpath(REPO) + "/"), "RUNROOT must be OUTSIDE the repo"
assert "/.claude" not in _rp, "RUNROOT must be OUTSIDE ~/.claude (ancestor discovery leaks skills)"

cfg = json.load(open(os.path.join(BASE, PROMPTS)))
MODEL = cfg["model"]
RUNS = cfg.get("runs", 2)
WORKERS = cfg.get("workers", 5)
TRANS = os.path.join(BASE, "transcripts")
os.makedirs(TRANS, exist_ok=True)
MANIFEST = os.path.join(BASE, "run_manifest.jsonl")


def served_model(path):
    for line in open(path):
        try:
            e = json.loads(line)
        except Exception:
            continue
        if e.get("type") == "system" and e.get("model"):
            return e["model"]
    return None


def run_one(p, n):
    key = p["key"]
    out = os.path.join(TRANS, f"{key}__{ARM}__r{n}.jsonl")
    if os.path.exists(out) and os.path.getsize(out) > 0:
        return f"skip {key} {ARM} r{n} (exists)"
    wd = os.path.join(RUNROOT, ARM, key, f"r{n}")
    if os.path.exists(wd):
        shutil.rmtree(wd)
    os.makedirs(wd)                                   # clean scratchpad per run
    if p.get("planted"):
        for root, dirs, files in os.walk(p["planted"]):
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            for f in files:
                s = os.path.join(root, f)
                rel = os.path.relpath(s, p["planted"])
                d = os.path.join(wd, rel)
                os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copy2(s, d)
    cmd = ["claude", "-p", p["prompt"], "--model", MODEL,
           "--output-format", "stream-json", "--verbose",
           "--dangerously-skip-permissions"]
    t0 = time.time()
    with open(out, "w") as fo, open(out + ".err", "w") as fe, open(os.devnull) as fin:
        try:
            rc = subprocess.run(cmd, cwd=wd, stdin=fin, stdout=fo, stderr=fe,
                                timeout=600).returncode
        except subprocess.TimeoutExpired:
            rc = "TIMEOUT"
    sz = os.path.getsize(out)
    if sz == 0:
        os.remove(out)
        return f"EMPTY {key} {ARM} r{n} rc={rc} {time.time()-t0:.0f}s"
    sm = served_model(out)
    with open(MANIFEST, "a") as m:
        m.write(json.dumps({"key": key, "arm": ARM, "run": n, "rc": rc,
                            "secs": round(time.time() - t0), "bytes": sz,
                            "requested_model": MODEL, "served_model": sm,
                            "finished": time.strftime("%Y-%m-%d %H:%M:%S")}) + "\n")
    flag = "" if sm == MODEL else f"   !! SERVED {sm}"
    return f"done {key} {ARM} r{n} rc={rc} {time.time()-t0:.0f}s {sz}B{flag}"


jobs = [(p, n) for p in cfg["prompts"] for n in range(1, RUNS + 1)]
print(f"=== {PROMPTS} arm={ARM}: {len(cfg['prompts'])} prompts x {RUNS} = {len(jobs)} runs, "
      f"{WORKERS} workers, model={MODEL}, RUNROOT={RUNROOT} ===", flush=True)
with ThreadPoolExecutor(max_workers=WORKERS) as ex:
    futs = [ex.submit(run_one, p, n) for p, n in jobs]
    for f in as_completed(futs):
        print("  " + f.result(), flush=True)
print("=== COMPLETE ===", flush=True)
