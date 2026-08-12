import json,os,shutil,subprocess,time
from concurrent.futures import ThreadPoolExecutor
SCR="/tmp/claude-0/-home-user-claude-core-skills/5ba2aae4-033b-5a4e-b487-3cd41d131f60/scratchpad"
RUNROOT=f"{SCR}/alwayson_ab"; MODEL="claude-opus-4-8"; RUNS=3
TRANS=f"{RUNROOT}/transcripts"; CLEAN=dict(os.environ)
for k in ("CLAUDE_CODE_SESSION_ID","CLAUDE_CODE_REMOTE_SESSION_ID","CLAUDE_SESSION_INGRESS_TOKEN_FILE","CLAUDE_CODE_ENTRYPOINT","CLAUDE_CODE_CHILD_SESSION"):
    CLEAN.pop(k,None)
INSTR=open(f"{SCR}/instr_alwayson.txt").read()
ARMS={"trivia_nokeyword":"what's 15% of 80?", "casual_nokeyword":"what should I have for lunch, tacos or pizza?"}
def run_one(job):
    arm,n=job; out=f"{TRANS}/{arm}__r{n}.jsonl"
    if os.path.exists(out) and os.path.getsize(out)>0: return f"skip {arm} r{n}"
    cmd=["claude","-p",ARMS[arm],"--model",MODEL,"--output-format","stream-json","--verbose","--append-system-prompt",INSTR]
    with open(out,"w") as fo,open(out+".err","w") as fe,open(os.devnull) as fin:
        rc=subprocess.run(cmd,cwd=RUNROOT,stdin=fin,stdout=fo,stderr=fe,timeout=120,env=CLEAN).returncode
    return f"{arm} r{n} rc={rc} {os.path.getsize(out)}B"
jobs=[(a,n) for a in ARMS for n in range(1,RUNS+1)]
with ThreadPoolExecutor(max_workers=3) as ex:
    for r in ex.map(run_one,jobs): print(r,flush=True)
print("DONE",flush=True)
