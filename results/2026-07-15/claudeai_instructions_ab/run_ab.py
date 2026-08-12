import json,os,shutil,subprocess,time
from concurrent.futures import ThreadPoolExecutor
SCR="/tmp/claude-0/-home-user-claude-core-skills/5ba2aae4-033b-5a4e-b487-3cd41d131f60/scratchpad"
REPO="/home/user/claude-core-skills"
RUNROOT=f"{SCR}/claudeai_ab"; MODEL="claude-opus-4-8"; RUNS=3
SKDIR=f"{RUNROOT}/.claude/skills"; TRANS=f"{RUNROOT}/transcripts"; os.makedirs(TRANS,exist_ok=True)
CLEAN=dict(os.environ)
for k in ("CLAUDE_CODE_SESSION_ID","CLAUDE_CODE_REMOTE_SESSION_ID","CLAUDE_SESSION_INGRESS_TOKEN_FILE","CLAUDE_CODE_ENTRYPOINT","CLAUDE_CODE_CHILD_SESSION"):
    CLEAN.pop(k,None)
INSTR={"BASELINE":open(f"{SCR}/instr_OLD.txt").read(), "CANDIDATE":open(f"{SCR}/instr_NEW.txt").read()}
PROMPTS=[
 {"key":"U1","p":"You are an expert stock analyzer - please analyze Rivian automotive and provide your best advice into when the stock will hit a share price of $27.50"},
 {"key":"U2","p":"Draft a one-page recommendation on whether my team should adopt a four-day work week. I'm sending it to leadership tomorrow."},
 {"key":"S1","p":"what's 15% of 80?"},
 {"key":"S2","p":"Write me a short limerick about coffee."},
]
def setup():
    if os.path.exists(SKDIR): shutil.rmtree(SKDIR)
    for s in ("plan-gate","adversarial-verify","scope-fence"):
        os.makedirs(f"{SKDIR}/{s}"); shutil.copy2(f"{REPO}/.claude/skills/{s}/SKILL.md",f"{SKDIR}/{s}/SKILL.md")
def run_one(job):
    p,arm,n=job; out=f"{TRANS}/{p['key']}__{arm}__r{n}.jsonl"
    if os.path.exists(out) and os.path.getsize(out)>0: return f"skip {p['key']} {arm} r{n}"
    cmd=["claude","-p",p["p"],"--model",MODEL,"--output-format","stream-json","--verbose","--append-system-prompt",INSTR[arm]]
    t0=time.time()
    with open(out,"w") as fo,open(out+".err","w") as fe,open(os.devnull) as fin:
        try: rc=subprocess.run(cmd,cwd=RUNROOT,stdin=fin,stdout=fo,stderr=fe,timeout=300,env=CLEAN).returncode
        except subprocess.TimeoutExpired: rc="TO"
    return f"{p['key']} {arm} r{n} rc={rc} {time.time()-t0:.0f}s {os.path.getsize(out)}B"
setup()
for arm in ("BASELINE","CANDIDATE"):
    jobs=[(p,arm,n) for p in PROMPTS for n in range(1,RUNS+1)]
    print(f"=== ARM {arm} ({len(INSTR[arm])} chars injected): {len(jobs)} runs ===",flush=True)
    with ThreadPoolExecutor(max_workers=3) as ex:
        for r in ex.map(run_one,jobs): print(r,flush=True)
    print(f"=== ARM {arm} DONE ===",flush=True)
print("=== ALL DONE ===",flush=True)
