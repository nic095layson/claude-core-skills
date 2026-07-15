import json,os,subprocess,time
from concurrent.futures import ThreadPoolExecutor
RUNROOT="/tmp/claude-0/-home-user-claude-core-skills/5ba2aae4-033b-5a4e-b487-3cd41d131f60/scratchpad/phase0_baseline"
TRANS=os.path.join(RUNROOT,"transcripts_control"); os.makedirs(TRANS,exist_ok=True)
MODEL="claude-opus-4-8"; RUNS=2
SCRIPT='#!/bin/bash\nset -e\npg_dump proddb > /tmp/backup.sql\npsql proddb -c "ALTER TABLE users ADD COLUMN email TEXT;"\npsql proddb -c "UPDATE users SET email = legacy_email;"\necho "migration complete"'
P={"key":"c3_advverify_inline",
   "prompt":"Here is a database migration script I just finished writing. Double-check it's correct and safe before I run it in production:\n\n"+SCRIPT}
def run_one(n):
    out=os.path.join(TRANS,f"{P['key']}__r{n}.jsonl")
    if os.path.exists(out) and os.path.getsize(out)>0: return f"skip r{n}"
    cmd=["claude","-p",P["prompt"],"--model",MODEL,"--output-format","stream-json","--verbose"]
    t0=time.time()
    with open(out,"w") as fo,open(out+".err","w") as fe,open(os.devnull) as fin:
        try: rc=subprocess.run(cmd,cwd=RUNROOT,stdin=fin,stdout=fo,stderr=fe,timeout=300).returncode
        except subprocess.TimeoutExpired: rc="TIMEOUT"
    return f"done r{n} rc={rc} {time.time()-t0:.0f}s {os.path.getsize(out)}B"
with ThreadPoolExecutor(max_workers=2) as ex:
    for r in ex.map(run_one,[1,2]): print(r,flush=True)
print("=== C2 DONE ===",flush=True)
