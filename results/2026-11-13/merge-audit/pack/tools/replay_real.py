#!/usr/bin/env python3
"""replay_real.py — run a hooks directory over the REAL session record and print verdicts only (no content).

    python3 replay_real.py [--hooks DIR] [--what stop|pre|prompt|all]

The record is the orchestrator's private snapshot of this session's transcript (2026-10-21 23:24Z onward:
the file starts at the last compaction boundary). You may run this tool; do not open the snapshot yourself.
  stop    at every point where the session really stopped (the transcript's stop_hook_summary rows): what the
          hooks installed at the time did, and what DIR's governance-enforce.py / receipt-law gate say now
  pre     at every real tool call that DIR's turngate treats as a write or a merge: the pretool verdict now
  prompt  at every real owner message: what DIR's governance-trigger.py would inject (kind only)
"""
import argparse, json, os, subprocess, sys, tempfile, uuid, collections
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
ap = argparse.ArgumentParser(); ap.add_argument("--hooks", default=os.path.join(ROOT, "lib", "hooks")); ap.add_argument("--what", default="all")
ap.add_argument("--snapshot", default=os.path.join(ROOT, "records", "transcript-snapshot.jsonl"))
a = ap.parse_args()
sys.path.insert(0, a.hooks)
import turngate, govclass
raw = [l for l in open(a.snapshot, encoding="utf-8", errors="replace").read().splitlines() if l.strip()]
rows = [json.loads(l) for l in raw]

def slice_file(n):
    fd, p = tempfile.mkstemp(suffix=".jsonl")
    with os.fdopen(fd, "w") as fh: fh.write("\n".join(raw[:n]) + "\n")
    return p

def run(script, payload):
    path = os.path.join(a.hooks, script)
    if not os.path.exists(path): return "no-hook", ""
    cmd = ["bash", path] if script.endswith(".sh") else ["python3", path]
    r = subprocess.run(cmd, input=json.dumps(payload), capture_output=True, text=True)
    o = r.stdout.strip()
    if not o: return "allow", ""
    try: j = json.loads(o)
    except Exception: return "unparsed", o[:80]
    if j.get("decision") == "block":
        rs = j.get("reason", "")
        return ("BLOCK:F1" if "outward action" in rs else "BLOCK:receipt" if rs.startswith("Receipt law") else "BLOCK:prompt-class"), rs[:110]
    h = j.get("hookSpecificOutput") or {}
    if h.get("permissionDecision") == "deny":
        rs = h.get("permissionDecisionReason", "")
        return ("DENY:scheduled" if "scheduled run never merges" in rs else "DENY:merge-word"), rs[:110]
    ctx = h.get("additionalContext") or ""
    if "plan shown, advisory" in ctx: return "ADVISE:plan-shown", ""
    return "context", ctx

def owner_rows():
    out = []
    for i, d in enumerate(rows):
        if d.get("type") != "user" or d.get("isMeta") or d.get("isCompactSummary"): continue
        t = turngate._text(d.get("message"))
        if not t or any(m in t for m in turngate.HARNESS_MARKERS) or t.startswith(("GOV-ENFORCE", "Stop hook feedback")): continue
        out.append((i, t))
    return out

if a.what in ("stop", "all"):
    print("== STOP: every real stop point (ts | then: what the installed hooks reported | now: enforce / receipt)")
    c = collections.Counter()
    for i, d in enumerate(rows):
        if d.get("type") == "system" and d.get("subtype") == "stop_hook_summary":
            then = "; ".join(e[:44].replace("\n", " ") for e in d.get("hookErrors") or []) or "-"
            p = slice_file(i)
            e, _ = run("governance-enforce.py", {"transcript_path": p, "stop_hook_active": False, "session_id": "replay"})
            r, _ = run("receipt-law-stop-gate.sh", {"transcript_path": p, "stop_hook_active": False, "session_id": "replay-" + uuid.uuid4().hex})
            os.unlink(p); c[e] += 1; c["receipt:" + r] += 1
            print(f"  {d.get('timestamp','')[:16]} | then: {then:46} | now: {e:18} / {r}")
    print("  totals:", dict(c))

if a.what in ("pre", "all"):
    print("== PRE: every real write-class or merge tool call (verdict now), grouped by owner turn")
    own = [i for i, _ in owner_rows()]
    c = collections.Counter(); per = collections.OrderedDict()
    for j, d in enumerate(rows):
        if d.get("type") != "assistant": continue
        for b in (d.get("message") or {}).get("content") or []:
            if not (isinstance(b, dict) and b.get("type") == "tool_use"): continue
            blk = {"name": b.get("name"), "input": b.get("input") or {}}
            if not (turngate.is_merge(blk) or turngate.is_write(blk)): continue
            p = slice_file(j)
            v, _ = run("turn-gates-pretool.py", {"transcript_path": p, "tool_name": blk["name"], "tool_input": blk["input"], "session_id": "replay-" + uuid.uuid4().hex})
            os.unlink(p)
            kind = "merge" if turngate.is_merge(blk) else "outward" if turngate.is_outward(blk) else "write"
            c[(kind, v)] += 1
            turn = max([o for o in own if o < j], default=-1)
            per.setdefault(turn, collections.Counter())[(kind, v)] += 1
    for turn, cc in per.items():
        ts = rows[turn].get("timestamp", "")[:16] if turn >= 0 else "(before first owner message)"
        print(f"  turn from {ts}: " + ", ".join(f"{k}:{v} x{n}" for (k, v), n in cc.items()))
    print("  totals:", {f"{k}:{v}": n for (k, v), n in c.items()})

if a.what in ("prompt", "all"):
    print("== PROMPT: every real owner message (ts | chars | classes | cue? | what the trigger injects now)")
    for i, t in owner_rows():
        p = slice_file(i)
        v, ctx = run("governance-trigger.py", {"transcript_path": p, "prompt": t})
        os.unlink(p)
        kinds = [k for k, s in (("auto-trigger", "Governance auto-trigger"), ("dispute", "questioning or disputing"), ("cue", "Governance cue"), ("requirement-note", "Governance note"), ("card-reminder", "Decision-cards reminder")) if s in ctx]
        print(f"  {rows[i].get('timestamp','')[:16]} | {len(t):5} | {','.join(govclass.classify(t)) or '-':28} | {str(govclass.cue(t)):5} | {'+'.join(kinds) or 'silent'}")
