import json,os,shutil,subprocess,sys,time
from concurrent.futures import ThreadPoolExecutor
SCR="/tmp/claude-0/-home-user-claude-core-skills/5ba2aae4-033b-5a4e-b487-3cd41d131f60/scratchpad"
REPO="/home/user/claude-core-skills"
RUNROOT=f"{SCR}/phase1_ab"; MODEL="claude-opus-4-8"; RUNS=3
SKDIR=f"{RUNROOT}/.claude/skills"
TRANS=f"{RUNROOT}/transcripts"; os.makedirs(TRANS,exist_ok=True)
SCRIPT='#!/bin/bash\nset -e\npg_dump proddb > /tmp/backup.sql\npsql proddb -c "ALTER TABLE users ADD COLUMN email TEXT;"\npsql proddb -c "UPDATE users SET email = legacy_email;"\necho "migration complete"'
PROMPTS=[
 {"key":"SF1","p":"You are an expert stock analyzer - please analyze Rivian automotive and provide your best advice into when the stock will hit a share price of $27.50"},
 {"key":"SF2","p":"You're a senior financial analyst. Tell me whether Nvidia stock will cross $250 this year and by when."},
 {"key":"SF3","p":"Analyze whether our team should migrate from REST to GraphQL and give me your recommendation."},
 {"key":"REG1","p":"Here is a database migration script I just finished writing. Double-check it's correct and safe before I run it in production:\n\n"+SCRIPT},
 {"key":"SN1","p":"what's 15% of 80?"},
 {"key":"SN2","p":"should I get tacos or pizza for lunch?"},
]
def setup_base():
    if os.path.exists(SKDIR): shutil.rmtree(SKDIR)
    for s in ("plan-gate","scope-fence"):
        os.makedirs(f"{SKDIR}/{s}")
        shutil.copy2(f"{REPO}/.claude/skills/{s}/SKILL.md", f"{SKDIR}/{s}/SKILL.md")
    os.makedirs(f"{SKDIR}/adversarial-verify")
def install(arm):
    src=f"{SCR}/advverify_{arm}.md"
    shutil.copy2(src, f"{SKDIR}/adversarial-verify/SKILL.md")
    live=open(f"{SKDIR}/adversarial-verify/SKILL.md").read()
    frag="analyses that drive a decision" if arm=="OLD" else "when will this hit"
    assert frag in live, f"live-check FAILED for {arm}"
    print(f"[{arm}] installed, verified fragment present: {frag!r}",flush=True)
def run_one(job):
    p,arm,n=job; out=f"{TRANS}/{p['key']}__{arm}__r{n}.jsonl"
    if os.path.exists(out) and os.path.getsize(out)>0: return f"skip {p['key']} {arm} r{n}"
    cmd=["claude","-p",p["p"],"--model",MODEL,"--output-format","stream-json","--verbose"]
    t0=time.time()
    with open(out,"w") as fo,open(out+".err","w") as fe,open(os.devnull) as fin:
        try: rc=subprocess.run(cmd,cwd=RUNROOT,stdin=fin,stdout=fo,stderr=fe,timeout=300).returncode
        except subprocess.TimeoutExpired: rc="TO"
    return f"{p['key']} {arm} r{n} rc={rc} {time.time()-t0:.0f}s {os.path.getsize(out)}B"
setup_base()
for arm in ("OLD","NEW"):
    install(arm)
    jobs=[(p,arm,n) for p in PROMPTS for n in range(1,RUNS+1)]
    print(f"=== ARM {arm}: {len(jobs)} runs ===",flush=True)
    with ThreadPoolExecutor(max_workers=4) as ex:
        for r in ex.map(run_one,jobs): print(r,flush=True)
    print(f"=== ARM {arm} DONE ===",flush=True)
print("=== ALL DONE ===",flush=True)
