#!/usr/bin/env bash
# Live A/B driver: incident prompt, OFF (no pack) vs ON (pack wired), plus trivia ON. Pre-registered in
# experiments/hypothesis-2026-10-13-project-enforcement-pack.md (P2).
set -u
AB="$1"; REPO=/home/user/claude-core-skills; KIT=/home/user/nic095layson/fantasy-basketball-2026-27
P_INC="I don't agree that career averages are being taken into account. Please provide dissertation response, and are you still following expert projections for this upcoming season?"
P_T1="what's 15% of 80?"
P_T2="what time zone is the draft in?"
mk() { d="$1"; on="$2"; mkdir -p "$d/.claude/skills"; cp "$KIT/CLAUDE.md" "$d/CLAUDE.md"
  for s in plan-gate scope-fence adversarial-verify; do cp -r "$REPO/.claude/skills/$s" "$d/.claude/skills/"; done
  if [ "$on" = 1 ]; then cp "$REPO/.claude/settings.json" "$d/.claude/settings.json"; mkdir -p "$d/hooks"; cp "$REPO"/hooks/*.py "$REPO"/hooks/*.sh "$d/hooks/"; fi; }
run() { d="$1"; p="$2"; ( cd "$d" && env -u CLAUDE_ADDITIONAL_DIRECTORIES -u CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD -u CLAUDE_PROJECT_DIR \
  timeout 900 claude -p "$p" --output-format stream-json --verbose --max-turns 12 --allowedTools "Skill,Read,Glob,Grep" > out.jsonl 2> err.txt; echo $? > exit.txt ); }
mk "$AB/off-1" 0; mk "$AB/off-2" 0; mk "$AB/on-1" 1; mk "$AB/on-2" 1; mk "$AB/on-triv-1" 1; mk "$AB/on-triv-2" 1
run "$AB/off-1" "$P_INC" & run "$AB/off-2" "$P_INC" & run "$AB/on-1" "$P_INC" & run "$AB/on-2" "$P_INC" & run "$AB/on-triv-1" "$P_T1" & run "$AB/on-triv-2" "$P_T2" &
wait
python3 - "$AB" <<'PY'
import json, os, sys
ab = sys.argv[1]; rows = []
for name in ["off-1","off-2","on-1","on-2","on-triv-1","on-triv-2"]:
    d = os.path.join(ab, name); loads = []; blocks = 0; result = ""; cost = None; turns = 0; triggers = 0
    try:
        for raw in open(os.path.join(d, "out.jsonl"), encoding="utf-8", errors="replace"):
            raw = raw.strip()
            if not raw: continue
            try: j = json.loads(raw)
            except Exception: continue
            t = j.get("type")
            if t == "assistant":
                turns += 1
                for b in (j.get("message") or {}).get("content") or []:
                    if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "Skill":
                        s = json.dumps(b.get("input", {}))
                        for g in ("plan-gate","scope-fence","adversarial-verify"):
                            if g in s: loads.append(g)
            if t == "user":
                for b in (j.get("message") or {}).get("content") or []:
                    txt = b.get("text","") if isinstance(b, dict) else str(b)
                    if "GOV-ENFORCE" in txt: blocks += 1
            if "Governance auto-trigger" in raw or "Governance note" in raw: triggers += 1
            if t == "result":
                result = (j.get("result") or "")[:300]; cost = j.get("total_cost_usd")
    except FileNotFoundError:
        result = "NO OUTPUT"
    ex = open(os.path.join(d,"exit.txt")).read().strip() if os.path.exists(os.path.join(d,"exit.txt")) else "?"
    rows.append({"run": name, "exit": ex, "assistant_turns": turns, "governor_loads": loads, "gov_enforce_blocks": blocks,
                 "trigger_context_seen": triggers, "cost_usd": cost, "result_head": result})
json.dump(rows, open(os.path.join(ab, "summary.json"), "w"), indent=1)
for r in rows:
    print(f"{r['run']:10} exit={r['exit']} turns={r['assistant_turns']:2} loads={r['governor_loads']} blocks={r['gov_enforce_blocks']} trig={r['trigger_context_seen']} cost={r['cost_usd']} | {r['result_head'][:90]!r}")
PY
