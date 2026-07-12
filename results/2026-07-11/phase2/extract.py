#!/usr/bin/env python3
"""Extract per-transcript grading inputs: which Skill(s) fired, tool-call summary,
and the full final assistant text. Usage: extract.py <transcript.jsonl>"""
import json, sys

def load(path):
    events = []
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except Exception:
            pass
    return events

def summarize(path):
    ev = load(path)
    skills, tools, final, model = [], [], None, None
    for e in ev:
        if e.get("type") == "system" and e.get("subtype") == "init":
            model = e.get("model")
        if e.get("type") == "assistant":
            for block in e.get("message", {}).get("content", []):
                if block.get("type") == "tool_use":
                    nm = block.get("name")
                    inp = block.get("input", {}) or {}
                    if nm == "Skill":
                        skills.append(inp.get("skill") or inp.get("command") or "?")
                    tools.append(nm + ("(" + str(inp.get("skill")) + ")" if nm == "Skill" else ""))
        if e.get("type") == "result":
            final = e.get("result")
    return {"model": model, "skills_fired": skills, "tool_seq": tools, "final": final or ""}

if __name__ == "__main__":
    s = summarize(sys.argv[1])
    print("MODEL:", s["model"])
    print("SKILLS_FIRED:", s["skills_fired"])
    print("TOOL_SEQ:", s["tool_seq"])
    print("=" * 80)
    print(s["final"])
