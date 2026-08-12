#!/usr/bin/env python3
"""UserPromptSubmit trigger (load-only, NO receipt ask — nothing to confabulate)."""
import sys, json, re
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
p=(data.get("prompt") or "").strip()
gov=classify(p) if p else []
if not gov: sys.exit(0)
names=" and ".join(gov)
ctx=(f"Governance auto-trigger (from your operating rules): this is governed work ({names}). "
     f"Load {names} with the Skill tool and follow its procedure BEFORE you produce the answer. "
     "If on inspection it is genuinely trivial, say so in one line and skip.")
print(json.dumps({"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":ctx}}))
