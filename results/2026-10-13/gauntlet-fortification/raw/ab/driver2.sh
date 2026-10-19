#!/usr/bin/env bash
# Rerun of the ON arm after the isMeta fix; session id un-inherited per INC-14.
set -u
AB="$1"; REPO=/home/user/claude-core-skills; KIT=/home/user/nic095layson/fantasy-basketball-2026-27
P_INC="I don't agree that career averages are being taken into account. Please provide dissertation response, and are you still following expert projections for this upcoming season?"
mk() { d="$1"; mkdir -p "$d/.claude/skills"; cp "$KIT/CLAUDE.md" "$d/CLAUDE.md"
  for s in plan-gate scope-fence adversarial-verify; do cp -r "$REPO/.claude/skills/$s" "$d/.claude/skills/"; done
  cp "$REPO/.claude/settings.json" "$d/.claude/settings.json"; mkdir -p "$d/hooks"; cp "$REPO"/hooks/*.py "$REPO"/hooks/*.sh "$d/hooks/"; }
run() { d="$1"; p="$2"; ( cd "$d" && env -u CLAUDE_ADDITIONAL_DIRECTORIES -u CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD -u CLAUDE_PROJECT_DIR -u CLAUDE_CODE_SESSION_ID \
  timeout 900 claude -p "$p" --output-format stream-json --verbose --max-turns 12 --allowedTools "Skill,Read,Glob,Grep" > out.jsonl 2> err.txt; echo $? > exit.txt ); }
mk "$AB/on-3"; mk "$AB/on-4"
run "$AB/on-3" "$P_INC" & run "$AB/on-4" "$P_INC" &
wait
python3 - "$AB" <<'PY'
import json, os, sys
ab=sys.argv[1]; rows=[]
for name in ["on-3","on-4"]:
    d=os.path.join(ab,name); loads=[]; blocks=0; result=""; cost=None; turns=0; trig=0; sid=None
    for raw in open(os.path.join(d,"out.jsonl"), errors="replace"):
        try: j=json.loads(raw)
        except: continue
        t=j.get("type")
        if t=="system" and j.get("subtype")=="init": sid=j.get("session_id")
        if t=="assistant":
            turns+=1
            for b in (j.get("message") or {}).get("content") or []:
                if isinstance(b,dict) and b.get("type")=="tool_use" and b.get("name")=="Skill":
                    s=json.dumps(b.get("input",{}))
                    for g in ("plan-gate","scope-fence","adversarial-verify"):
                        if g in s: loads.append(g)
        if t=="user":
            for b in (j.get("message") or {}).get("content") or []:
                txt=b.get("text","") if isinstance(b,dict) else str(b)
                if "GOV-ENFORCE" in txt: blocks+=1
        if "Governance auto-trigger" in raw: trig+=1
        if t=="result": result=(j.get("result") or "")[:300]; cost=j.get("total_cost_usd")
    ex=open(os.path.join(d,"exit.txt")).read().strip()
    rows.append({"run":name,"session_id":sid,"exit":ex,"assistant_turns":turns,"governor_loads":loads,"gov_enforce_blocks":blocks,"trigger_context_seen":trig,"cost_usd":cost,"result_head":result})
json.dump(rows, open(os.path.join(ab,"summary2.json"),"w"), indent=1)
for r in rows: print(f"{r['run']:6} sid={str(r['session_id'])[:8]} exit={r['exit']} turns={r['assistant_turns']:2} loads={r['governor_loads']} blocks={r['gov_enforce_blocks']} trig={r['trigger_context_seen']} cost={r['cost_usd']} | {r['result_head'][:80]!r}")
PY
