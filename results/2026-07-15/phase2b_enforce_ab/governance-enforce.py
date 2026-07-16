#!/usr/bin/env python3
"""Stop hook: if the turn is governed-class AND no governor Skill loaded this turn,
BLOCK and force the model to load it. Single-retry (stop_hook_active) => loop-safe."""
import sys, json, os, re
GOV_ALL={"plan-gate","adversarial-verify","scope-fence"}
def classify(p):
    p=p.lower()
    analysis=re.search(r'\b(analy[sz]\w*|advis\w*|advice|recommend\w*|forecast\w*|predict\w*|assess\w*|evaluat\w*|outlook|is this a (good|sound|bad)\b|worth (buying|investing|it)\b|when will\b.{0,40}\b(hit|reach|cross|top|bottom)|should (i|we)\b.{0,60}\b(invest|buy|sell|adopt|switch|migrate|choose|pick|hire))',p)
    review=re.search(r'\b(review|double.?check|check (this|my|the|it)|is this (correct|right|safe|ready)|ready to ship|before i (ship|run|deploy|merge)|sanity.?check|looks? (right|good|correct))\b',p)
    build=re.search(r'\b(build|create|implement|migrat\w*|refactor\w*|rewrite|design a|draft (a|the|me)?|write (a|the|me)|set ?up|configure|scaffold|stand up|wire up)\b',p)
    gov=[]
    if analysis or review: gov.append("adversarial-verify")
    if build: gov.append("plan-gate")
    return gov
try: data=json.load(sys.stdin)
except Exception: sys.exit(0)
if data.get("stop_hook_active"): sys.exit(0)  # already forced one retry -> allow (loop-safe)
tp=data.get("transcript_path")
if not tp or not os.path.exists(tp): sys.exit(0)
lines=[]
for l in open(tp):
    l=l.strip()
    if not l: continue
    try: lines.append(json.loads(l))
    except Exception: pass
prompt=None; li=-1
for i,d in enumerate(lines):
    m=d.get("message",{})
    if d.get("type")=="user" and isinstance(m,dict) and isinstance(m.get("content"),str):
        c=m["content"]
        if not c.startswith("GOV-ENFORCE"):
            prompt=c; li=i
if not prompt: sys.exit(0)
gov=classify(prompt)
if not gov: sys.exit(0)  # not governed -> allow
loaded=set()
for d in lines[li:]:
    m=d.get("message",{})
    if d.get("type")=="assistant" and isinstance(m,dict):
        for b in (m.get("content") or []):
            if isinstance(b,dict) and b.get("type")=="tool_use" and b.get("name")=="Skill":
                inp=json.dumps(b.get("input",{}))
                for g in GOV_ALL:
                    if g in inp: loaded.add(g)
if loaded & set(gov): sys.exit(0)  # complied
reason=("GOV-ENFORCE: this is governed work ("+", ".join(gov)+") and you finished WITHOUT loading it. "
        "Load "+gov[0]+" with the Skill tool now, follow its procedure, and revise your answer before finishing.")
print(json.dumps({"decision":"block","reason":reason}))
