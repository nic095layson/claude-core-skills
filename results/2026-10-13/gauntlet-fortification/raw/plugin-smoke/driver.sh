#!/usr/bin/env bash
# plugin-smoke driver (2026-10-13): does the governance plugin's hook layer fire under --plugin-dir?
# One headless run per arm (mechanism check, not the pre-registered behavioural A/B).
# Scratch project = the kit's CLAUDE.md verbatim, NO .claude/settings.json (so the wrapper must run,
# not defer). Governors come from the account-synced skills in this container.
set -u
OUT="$1"; REPO=/home/user/claude-core-skills; KIT=/home/user/fantasy-basketball-2026-27
PLUGIN="$REPO/plugin/core-governance"
P_INC="I don't agree that career averages are being taken into account. Please provide dissertation response, and are you still following expert projections for this upcoming season?"
P_TRIV="what time zone is the draft in?"
mk() { d="$1"; mkdir -p "$d"; cp "$KIT/CLAUDE.md" "$d/CLAUDE.md"; }
run() { d="$1"; p="$2"; ( cd "$d" && env -u CLAUDE_ADDITIONAL_DIRECTORIES -u CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD -u CLAUDE_PROJECT_DIR -u CLAUDE_CODE_SESSION_ID \
  timeout 900 claude -p "$p" --plugin-dir "$PLUGIN" --output-format stream-json --verbose --max-turns 12 --allowedTools "Skill,Read,Glob,Grep" > out.jsonl 2> err.txt; echo $? > exit.txt ); }
mk "$OUT/inc-1"; mk "$OUT/triv-1"
run "$OUT/inc-1" "$P_INC" & run "$OUT/triv-1" "$P_TRIV" &
wait
python3 - "$OUT" <<'PY'
import json, os, sys
ab=sys.argv[1]; rows=[]
for name in ["inc-1","triv-1"]:
    d=os.path.join(ab,name); loads=[]; blocks=0; result=""; cost=None; turns=0; trig=0; sid=None; model=None
    for raw in open(os.path.join(d,"out.jsonl"), errors="replace"):
        try: j=json.loads(raw)
        except: continue
        t=j.get("type")
        if t=="system" and j.get("subtype")=="init": sid=j.get("session_id"); model=j.get("model")
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
    rows.append({"run":name,"session_id":sid,"model":model,"exit":ex,"assistant_turns":turns,"governor_loads":loads,"gov_enforce_blocks":blocks,"trigger_context_seen":trig,"cost_usd":cost,"result_head":result})
json.dump(rows, open(os.path.join(ab,"summary.json"),"w"), indent=1)
for r in rows: print(f"{r['run']:7} exit={r['exit']} turns={r['assistant_turns']:2} loads={r['governor_loads']} blocks={r['gov_enforce_blocks']} trig={r['trigger_context_seen']} cost={r['cost_usd']} | {r['result_head'][:90]!r}")
PY
