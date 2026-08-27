#!/usr/bin/env python3
"""Un-mask the blind grades and tabulate per governor x prompt x arm. Also reads the
trace headers for corroborating facts (skills loaded, served model, hook activity).
Prints the cells and flags the DECISIVE ones (any with-arm miss, any without-arm hit,
any grader UNPARSEABLE) for mandatory hand verification. Usage: tabulate.py <label>"""
import json, os, re, sys, glob
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
label = sys.argv[1]
mask = json.load(open(os.path.join(BASE, f"mask_map_{label}.json")))
unmask = {v: k for k, v in mask.items()}
grades = [json.loads(l) for l in open(os.path.join(BASE, f"grades_{label}.jsonl"))]

cells = defaultdict(list)
for g in grades:
    token = g["trace"].split("__", 1)[1]
    base = unmask[token]                      # e.g. plan-gate__pg1__with__r1
    gov, pk, arm, run = base.split("__")
    hdr = open(os.path.join(BASE, "traces_masked", g["trace"] + ".md")).read().split("\n")[1]
    skills = re.search(r"skills_loaded: (.*?) \|", hdr).group(1)
    served = re.search(r"served_model: (.*?) \|", hdr).group(1)
    blocks = re.search(r"stop_hook_blocks: (\d+)", hdr).group(1)
    remind = re.search(r"scope_reminder_injected: (\w+)", hdr).group(1)
    cells[(gov, pk, arm)].append({"run": run, "present": g.get("present"), "subst": g.get("substantive"),
                                  "skills": skills, "served": served, "blocks": int(blocks),
                                  "remind": remind, "quote": g.get("quote", ""), "trace": g["trace"]})

decisive = []
print(f"=== {label}: {len(grades)} graded traces ===\n")
for gov in sorted({k[0] for k in cells}):
    print(f"##### {gov}")
    for pk in sorted({k[1] for k in cells if k[0] == gov}):
        for arm in ("with", "without"):
            rs = sorted(cells.get((gov, pk, arm), []), key=lambda r: r["run"])
            if not rs:
                continue
            hits = sum(1 for r in rs if r["present"] is True)
            det = "  ".join(f"{r['run']}={'P' if r['present'] else ('A' if r['present'] is False else '?')}"
                            f"[skills:{r['skills']};blk:{r['blocks']};rem:{r['remind']}]" for r in rs)
            print(f"  {pk:>8} {arm:>7}: signature {hits}/{len(rs)}   {det}")
            for r in rs:
                if (arm == "with" and r["present"] is not True) or (arm == "without" and r["present"] is not False):
                    decisive.append((gov, pk, arm, r["run"], r["trace"], r["quote"]))
            off = [r for r in rs if r["served"] != "claude-fable-5"]
            if off:
                print(f"           !! served-model off: {[(r['run'], r['served']) for r in off]}")
    print()
print("=== DECISIVE CELLS (hand-verify each; hand verdict wins) ===")
for d in decisive:
    print(f"  {d[0]} {d[1]} {d[2]} r{d[3]}  trace={d[4]}  grader-quote: {d[5][:120]}")
print(f"({len(decisive)} decisive)")
