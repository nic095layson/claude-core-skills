#!/usr/bin/env python3
"""Turn each behavioral transcript into one ordered, readable trace (assistant text,
tool calls with a short input preview, Skill loads, hook events) so a grader can
see ORDER — e.g. whether a plan block preceded the first file edit. Traces are
written under MASKED names (arm hidden); the map is kept in mask_map.json and is
opened only after grading. Usage: extract_traces.py <glob-pattern> <set-label>"""
import json, os, glob, sys, random, hashlib

BASE = os.path.dirname(os.path.abspath(__file__))
TRANS = os.path.join(BASE, "transcripts")
OUT = os.path.join(BASE, "traces_masked")
os.makedirs(OUT, exist_ok=True)
pattern, label = sys.argv[1], sys.argv[2]
mapfile = os.path.join(BASE, f"mask_map_{label}.json")
mask = json.load(open(mapfile)) if os.path.exists(mapfile) else {}


def trace(path):
    lines, fired, served, blocks, reminder = [], [], None, 0, False
    for raw in open(path):
        raw = raw.strip()
        if not raw:
            continue
        if "Receipt law (adversarial-verify rule 6)" in raw:
            blocks += 1
        if "Scope check (scope-fence skill)" in raw:
            reminder = True
        try:
            e = json.loads(raw)
        except Exception:
            continue
        t = e.get("type")
        if t == "system" and e.get("model") and served is None:
            served = e["model"]
        elif t == "assistant":
            for b in e.get("message", {}).get("content", []):
                if b.get("type") == "text" and b.get("text", "").strip():
                    lines.append("ASSISTANT TEXT:\n" + b["text"].strip() + "\n")
                elif b.get("type") == "tool_use":
                    name = b.get("name"); inp = b.get("input", {}) or {}
                    if name == "Skill":
                        fired.append(inp.get("skill") or "?")
                        lines.append(f"[SKILL LOAD: {inp.get('skill')}]\n")
                    else:
                        prev = json.dumps(inp)[:300]
                        lines.append(f"[TOOL {name}: {prev}]\n")
        elif t == "user":
            for b in e.get("message", {}).get("content", []) if isinstance(e.get("message", {}).get("content"), list) else []:
                if b.get("type") == "tool_result":
                    c = b.get("content")
                    s = c if isinstance(c, str) else json.dumps(c)
                    lines.append(f"[TOOL RESULT: {s[:200]}]\n")
    return "\n".join(lines), fired, served, blocks, reminder


for path in sorted(glob.glob(os.path.join(TRANS, pattern))):
    base = os.path.basename(path)[:-6]
    if base not in mask:
        mask[base] = hashlib.sha256((base + str(random.random())).encode()).hexdigest()[:10]
    tr, fired, served, blocks, reminder = trace(path)
    key = base.split("__")[0] + "__" + base.split("__")[1]      # governor__promptkey, arm hidden
    with open(os.path.join(OUT, f"{label}__{mask[base]}.md"), "w") as f:
        f.write(f"# trace {mask[base]}  (case: {key})\n"
                f"served_model: {served} | skills_loaded: {fired or 'none'} | "
                f"stop_hook_blocks: {blocks} | scope_reminder_injected: {reminder}\n\n{tr}")
json.dump(mask, open(mapfile, "w"), indent=1)
print(f"wrote {len(mask)} masked traces for {label} -> {OUT}; map in {os.path.basename(mapfile)}")
