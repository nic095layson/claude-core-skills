#!/usr/bin/env python3
"""UserPromptSubmit governance trigger. Classifies the incoming prompt; for
governed-class work injects a turn-fresh instruction to LOAD the applicable
governor (Skill tool) before answering + emit a receipt. Silent on trivia
(anti-ceremony). First-cut classifier: keyword/pattern, dependency-light."""
import sys, json, re
try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)
p = ((data.get("prompt") or "")).lower().strip()
if not p:
    sys.exit(0)

analysis = re.search(r'\b(analy[sz]\w*|advis\w*|advice|recommend\w*|forecast\w*|predict\w*|assess\w*|evaluat\w*|outlook|is this a (good|sound|bad)\b|worth (buying|investing|it)\b|when will\b.{0,40}\b(hit|reach|cross|top|bottom)|should (i|we)\b.{0,60}\b(invest|buy|sell|adopt|switch|migrate|choose|pick|hire))', p)
review   = re.search(r'\b(review|double.?check|check (this|my|the|it)|is this (correct|right|safe|ready)|ready to ship|before i (ship|run|deploy|merge)|sanity.?check|looks? (right|good|correct))\b', p)
build    = re.search(r'\b(build|create|implement|migrat\w*|refactor\w*|rewrite|design a|draft (a|the|me)?|write (a|the|me)|set ?up|configure|scaffold|stand up|wire up)\b', p)

gov = []
if analysis or review: gov.append("adversarial-verify")
if build: gov.append("plan-gate")
if not gov:
    sys.exit(0)  # not governed -> stay silent

names = " and ".join(gov)
ctx = ("Governance auto-trigger (from your operating rules): this request is classified as "
       f"governed work ({names}). BEFORE you produce the answer, load {names} with the Skill "
       "tool and follow the procedure it defines; then end your reply with a one-line "
       f"governance receipt (e.g. `Governance: {gov[0]} ✓`). If on inspection this is "
       "genuinely trivial, say so in one line and skip — do not manufacture ceremony.")
print(json.dumps({"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":ctx}}))
sys.exit(0)
