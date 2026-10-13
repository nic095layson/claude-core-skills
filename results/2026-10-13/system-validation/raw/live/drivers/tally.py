#!/usr/bin/env python3
"""tally.py <run_dir>... -> one JSON row per run: governor loads, trigger context, GOV-ENFORCE blocks, writes, cost."""
import json, os, sys, re
GOV = ("plan-gate", "scope-fence", "adversarial-verify", "gauntlet", "after-report")
WRITE_TOOLS = ("Write", "Edit", "NotebookEdit")
rows = []
for d in sys.argv[1:]:
    p = os.path.join(d, "out.jsonl")
    r = {"run": os.path.basename(d), "exit": None, "model": None, "loads": [], "load_turn_index": None, "trigger_ctx": 0,
         "blocks": 0, "hook_events": {}, "writes": [], "bash_writes": [], "first_bash_turn": None, "turns": 0,
         "cost_usd": None, "result_subtype": None, "result_head": ""}
    try: r["exit"] = open(os.path.join(d, "exit.txt")).read().strip()
    except Exception: pass
    if not os.path.exists(p):
        rows.append(r); continue
    for raw in open(p, errors="replace"):
        try: j = json.loads(raw)
        except Exception: continue
        t = j.get("type"); st = j.get("subtype")
        if t == "system" and st == "init": r["model"] = j.get("model")
        if t == "system" and st in ("hook_started", "hook_response"):
            k = f'{j.get("hook_event")}:{st}'; r["hook_events"][k] = r["hook_events"].get(k, 0) + 1
        # Count only real hook output. A mention inside a tool_result (the model reading a hook's source
        # file) is not a trigger or a block: the first version counted those and reported blocks that never
        # happened (2026-10-13, corrected the same day).
        if t == "system" and st == "hook_response":
            o = j.get("output") or ""
            if j.get("hook_event") == "UserPromptSubmit" and "Governance auto-trigger" in o: r["trigger_ctx"] += 1
            if j.get("hook_event") == "Stop" and '"decision": "block"' in o: r["blocks"] += 1
        if t == "assistant":
            r["turns"] += 1
            for b in (j.get("message") or {}).get("content") or []:
                if not isinstance(b, dict) or b.get("type") != "tool_use": continue
                name, inp = b.get("name"), b.get("input", {})
                if name == "Skill":
                    s = json.dumps(inp)
                    for g in GOV:
                        if g in s:
                            r["loads"].append(g)
                            if r["load_turn_index"] is None: r["load_turn_index"] = r["turns"]
                if name in WRITE_TOOLS: r["writes"].append(inp.get("file_path", "?"))
                if name == "Bash":
                    c = inp.get("command", "")
                    if r["first_bash_turn"] is None: r["first_bash_turn"] = r["turns"]
                    if re.search(r"(>\s*[\w./-]+\.(py|csv|json|md|txt))|(\btee\b)|(open\([^)]*,\s*['\"]w)|(to_csv\()|(\bsed -i\b)", c):
                        r["bash_writes"].append(c[:160])
        if t == "user":
            c = (j.get("message") or {}).get("content")
            texts = [c] if isinstance(c, str) else [b.get("text", "") for b in (c or []) if isinstance(b, dict) and b.get("type") == "text"]
            if any(x.startswith("Stop hook feedback") or x.startswith("GOV-ENFORCE: this is governed work") for x in texts):
                r["block_feedback_entries"] = r.get("block_feedback_entries", 0) + 1
        if t == "result":
            r["cost_usd"] = j.get("total_cost_usd"); r["result_subtype"] = j.get("subtype"); r["result_head"] = (j.get("result") or "")[:160]
    rows.append(r)
print(json.dumps(rows, indent=1))
