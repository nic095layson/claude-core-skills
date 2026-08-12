import json,os,shutil,subprocess,time
from concurrent.futures import ThreadPoolExecutor
SCR="/tmp/claude-0/-home-user-claude-core-skills/5ba2aae4-033b-5a4e-b487-3cd41d131f60/scratchpad"
REPO="/home/user/claude-core-skills"
RUNROOT=f"{SCR}/gauntlet_ab"; MODEL="claude-opus-4-8"; RUNS=3
SKDIR=f"{RUNROOT}/.claude/skills"; TRANS=f"{RUNROOT}/transcripts"; os.makedirs(TRANS,exist_ok=True)
CLEAN=dict(os.environ)
for k in ("CLAUDE_CODE_SESSION_ID","CLAUDE_CODE_REMOTE_SESSION_ID","CLAUDE_SESSION_INGRESS_TOKEN_FILE","CLAUDE_CODE_ENTRYPOINT","CLAUDE_CODE_CHILD_SESSION"):
    CLEAN.pop(k,None)
INSTR=open(f"{SCR}/instr_gauntlet.txt").read()
BASE="You are an expert stock analyzer - please analyze Rivian automotive and provide your best advice into when the stock will hit a share price of $27.50"
ARMS={
 "no_trigger": BASE,                       # control: definition present, but user didn't type GAUNTLET
 "gauntlet":   BASE+"  GAUNTLET",          # user appends the codeword
 "gauntlet_trivia": "what's 15% of 80? GAUNTLET",  # over-fire control: codeword on trivia
}
def setup():
    if os.path.exists(SKDIR): shutil.rmtree(SKDIR)
    for s in ("plan-gate","adversarial-verify","scope-fence"):
        os.makedirs(f"{SKDIR}/{s}"); shutil.copy2(f"{REPO}/.claude/skills/{s}/SKILL.md",f"{SKDIR}/{s}/SKILL.md")
def run_one(job):
    arm,n=job; out=f"{TRANS}/{arm}__r{n}.jsonl"
    if os.path.exists(out) and os.path.getsize(out)>0: return f"skip {arm} r{n}"
    cmd=["claude","-p",ARMS[arm],"--model",MODEL,"--output-format","stream-json","--verbose","--append-system-prompt",INSTR]
    t0=time.time()
    with open(out,"w") as fo,open(out+".err","w") as fe,open(os.devnull) as fin:
        try: rc=subprocess.run(cmd,cwd=RUNROOT,stdin=fin,stdout=fo,stderr=fe,timeout=300,env=CLEAN).returncode
        except subprocess.TimeoutExpired: rc="TO"
    return f"{arm} r{n} rc={rc} {time.time()-t0:.0f}s {os.path.getsize(out)}B"
setup()
jobs=[(a,n) for a in ARMS for n in range(1,RUNS+1)]
print(f"gauntlet test: {len(jobs)} runs",flush=True)
with ThreadPoolExecutor(max_workers=3) as ex:
    for r in ex.map(run_one,jobs): print(r,flush=True)
print("=== ALL DONE ===",flush=True)
