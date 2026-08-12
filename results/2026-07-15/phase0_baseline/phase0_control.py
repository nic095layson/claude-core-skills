#!/usr/bin/env python3
"""Positive control: do CUED should-fire prompts fire a governor in THIS exact
headless setup? If yes, the 0/9 uncued baseline is a real coverage finding, not a
'headless never auto-loads skills' artifact."""
import json, os, subprocess, time
from concurrent.futures import ThreadPoolExecutor
RUNROOT="/tmp/claude-0/-home-user-claude-core-skills/5ba2aae4-033b-5a4e-b487-3cd41d131f60/scratchpad/phase0_baseline"
TRANS=os.path.join(RUNROOT,"transcripts_control"); os.makedirs(TRANS,exist_ok=True)
MODEL="claude-opus-4-8"; RUNS=2
PROMPTS=[
 {"key":"c1_plangate_cued","prompt":"help me build a migration script for our postgres schema"},
 {"key":"c2_advverify_cued","prompt":"I finished writing this database migration script and I'm about to run it in production. Can you double-check it's correct and ready to ship before I do?"},
]
def run_one(job):
    p,n=job; out=os.path.join(TRANS,f"{p['key']}__r{n}.jsonl")
    if os.path.exists(out) and os.path.getsize(out)>0: return f"skip {p['key']} r{n}"
    cmd=["claude","-p",p["prompt"],"--model",MODEL,"--output-format","stream-json","--verbose"]
    t0=time.time()
    with open(out,"w") as fo,open(out+".err","w") as fe,open(os.devnull) as fin:
        try: rc=subprocess.run(cmd,cwd=RUNROOT,stdin=fin,stdout=fo,stderr=fe,timeout=300).returncode
        except subprocess.TimeoutExpired: rc="TIMEOUT"
    return f"done {p['key']} r{n} rc={rc} {time.time()-t0:.0f}s {os.path.getsize(out)}B"
jobs=[(p,n) for p in PROMPTS for n in range(1,RUNS+1)]
print(f"launching {len(jobs)} control runs",flush=True)
with ThreadPoolExecutor(max_workers=2) as ex:
    for r in ex.map(run_one,jobs): print(r,flush=True)
print("=== CONTROL DONE ===",flush=True)
