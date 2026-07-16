import json,os,subprocess,time
from concurrent.futures import ThreadPoolExecutor
SCR="/tmp/claude-0/-home-user-claude-core-skills/5ba2aae4-033b-5a4e-b487-3cd41d131f60/scratchpad"
RUNROOT=f"{SCR}/phase2b_ab"; MODEL="claude-opus-4-8"; RUNS=3
TRANS=f"{RUNROOT}/transcripts_clean"; os.makedirs(TRANS,exist_ok=True)
# strip inherited session env so each nested run gets its OWN session id + transcript
CLEAN=dict(os.environ)
for k in ("CLAUDE_CODE_SESSION_ID","CLAUDE_CODE_REMOTE_SESSION_ID","CLAUDE_SESSION_INGRESS_TOKEN_FILE",
          "CLAUDE_CODE_ENTRYPOINT","CLAUDE_CODE_CHILD_SESSION"):
    CLEAN.pop(k,None)
SCRIPT='#!/bin/bash\nset -e\npg_dump proddb > /tmp/backup.sql\npsql proddb -c "ALTER TABLE users ADD COLUMN email TEXT;"\npsql proddb -c "UPDATE users SET email = legacy_email;"\necho done'
PROMPTS=[
 {"key":"SF1","p":"You are an expert stock analyzer - please analyze Rivian automotive and provide your best advice into when the stock will hit a share price of $27.50"},
 {"key":"SF2","p":"You're a senior financial analyst. Tell me whether Nvidia stock will cross $250 this year and by when."},
 {"key":"SF3","p":"Analyze whether our team should migrate from REST to GraphQL and give me your recommendation."},
 {"key":"REG1","p":"Here is a database migration script I just finished writing. Double-check it's correct and safe before I run it in production:\n\n"+SCRIPT},
 {"key":"SN1","p":"what's 15% of 80?"},
 {"key":"SN2","p":"should I get tacos or pizza for lunch?"},
]
def run_one(job):
    p,n=job; out=f"{TRANS}/{p['key']}__ENFORCE__r{n}.jsonl"
    if os.path.exists(out) and os.path.getsize(out)>0: return f"skip {p['key']} r{n}"
    cmd=["claude","-p",p["p"],"--model",MODEL,"--output-format","stream-json","--verbose"]
    t0=time.time()
    with open(out,"w") as fo,open(out+".err","w") as fe,open(os.devnull) as fin:
        try: rc=subprocess.run(cmd,cwd=RUNROOT,stdin=fin,stdout=fo,stderr=fe,timeout=360,env=CLEAN).returncode
        except subprocess.TimeoutExpired: rc="TO"
    return f"{p['key']} r{n} rc={rc} {time.time()-t0:.0f}s {os.path.getsize(out)}B"
jobs=[(p,n) for p in PROMPTS for n in range(1,RUNS+1)]
print(f"clean ENFORCE re-run: {len(jobs)} runs, fresh session per run, concurrency 2",flush=True)
with ThreadPoolExecutor(max_workers=2) as ex:
    for r in ex.map(run_one,jobs): print(r,flush=True)
print("=== CLEAN DONE ===",flush=True)
