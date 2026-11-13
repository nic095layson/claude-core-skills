#!/usr/bin/env python3
"""Row-shape catalog of a session transcript, content redacted. Usage: shape_catalog.py TRANSCRIPT HOOKS_DIR"""
import json, sys, re, collections
T, HOOKS = sys.argv[1], sys.argv[2]
sys.path.insert(0, HOOKS)
import turngate, govclass
rows = [json.loads(l) for l in open(T, encoding="utf-8", errors="replace") if l.strip()]
def text(r):
    return turngate._text(r.get("message")) if isinstance(r.get("message"), dict) else None
HARNESS_PREFIX = re.compile(r"^(<[a-zA-Z-]+|\[[A-Z][A-Za-z ]+|This session|Stop hook|Base directory|\(Re-invocation|Another Claude|Caveat:|GOV-ENFORCE)")
print("# Row-shape catalog (content redacted)\n")
print("rows:", len(rows))
c = collections.Counter()
for r in rows:
    t = r.get("type")
    if t == "user":
        m = r.get("message") or {}; cc = m.get("content")
        kind = "str" if isinstance(cc, str) else "list[" + ",".join(sorted({b.get("type","?") for b in cc if isinstance(b, dict)})) + "]" if isinstance(cc, list) else type(cc).__name__
        flags = "".join(f" {k}" for k in ("isMeta", "isCompactSummary", "isSidechain") if r.get(k))
        c[f"user content={kind}{flags}"] += 1
    elif t == "assistant":
        cc = (r.get("message") or {}).get("content") or []
        c["assistant blocks=" + ",".join(sorted({b.get("type","?") for b in cc if isinstance(b, dict)})) + (" isSidechain" if r.get("isSidechain") else "")] += 1
    elif t == "attachment":
        c["attachment type=" + str((r.get("attachment") or {}).get("type"))] += 1
    elif t == "system":
        c["system subtype=" + str(r.get("subtype"))] += 1
    else:
        c[f"{t} (keys: {','.join(sorted(k for k in r.keys())[:8])})"] += 1
print("\n## Row kinds and counts")
for k, v in sorted(c.items(), key=lambda x: -x[1]): print(f"{v:6}  {k}")

print("\n## User rows the turn gates accept as an OWNER message (turngate.owner_index filter), by leading text")
print("(harness-looking prefixes shown; the owner's own prompts are redacted to a length)")
acc = collections.Counter(); ex = {}
accepted = []
for i, r in enumerate(rows):
    if r.get("type") != "user" or r.get("isMeta") or r.get("isCompactSummary"): continue
    t = text(r)
    if not t or any(m in t for m in turngate.HARNESS_MARKERS): continue
    if t.startswith(("GOV-ENFORCE", "Stop hook feedback")): continue
    m = HARNESS_PREFIX.match(t.lstrip())
    key = ("HARNESS-LOOKING: " + t.lstrip()[:70].replace("\n", " ")) if m else "plain owner text"
    acc[key] += 1; accepted.append((i, r.get("timestamp", "")[:16], key, len(t), govclass.classify(t), govclass.cue(t)))
for k, v in sorted(acc.items(), key=lambda x: -x[1]): print(f"{v:5}  {k}")

print("\n## User rows SKIPPED by the owner filter, by reason and leading text (top 25)")
sk = collections.Counter()
for r in rows:
    if r.get("type") != "user": continue
    t = text(r)
    if r.get("isMeta"): sk["isMeta: " + (t or "")[:50].replace("\n", " ")] += 1; continue
    if r.get("isCompactSummary"): sk["isCompactSummary"] += 1; continue
    if not t: sk["no text (tool_result rows etc.)"] += 1; continue
    hit = [m for m in turngate.HARNESS_MARKERS if m in t]
    if hit: sk[f"marker {hit[0]!r} | starts: " + t.lstrip()[:45].replace("\n", " ")] += 1; continue
    if t.startswith(("GOV-ENFORCE", "Stop hook feedback")): sk["hook feedback: " + t[:40].replace("\n", " ")] += 1
for k, v in sorted(sk.items(), key=lambda x: -x[1])[:25]: print(f"{v:5}  {k}")

print("\n## Attachment rows: types, and a redacted skeleton of the kinds that carry owner input")
for r in rows:
    if r.get("type") == "attachment" and (r.get("attachment") or {}).get("type") in ("queued_command",):
        a = r["attachment"]
        print(json.dumps({k: (v if isinstance(v, (bool, int)) or k in ("type", "commandMode") else (f"<{type(v).__name__}:{len(v)}>" if hasattr(v, "__len__") else str(type(v).__name__))) for k, v in a.items()}))
        print("   origin:", json.dumps(a.get("origin")), "| top-level keys:", sorted(r.keys()))
        break
print("queued_command attachments:", sum(1 for r in rows if r.get("type") == "attachment" and (r.get("attachment") or {}).get("type") == "queued_command"))
print("  of which origin.kind == 'human':", sum(1 for r in rows if r.get("type") == "attachment" and (r.get("attachment") or {}).get("type") == "queued_command" and ((r["attachment"].get("origin") or {}).get("kind") == "human")))
qk = collections.Counter(json.dumps((r["attachment"].get("origin") or {}).get("kind")) + " mode=" + str(r["attachment"].get("commandMode")) for r in rows if r.get("type") == "attachment" and (r.get("attachment") or {}).get("type") == "queued_command")
print("  by origin.kind/commandMode:", dict(qk))

print("\n## tool_result texts by leading words (top 20; text after the lead is redacted)")
tr = collections.Counter()
for r in rows:
    cc = (r.get("message") or {}).get("content") if isinstance(r.get("message"), dict) else None
    if r.get("type") != "user" or not isinstance(cc, list): continue
    for b in cc:
        if isinstance(b, dict) and b.get("type") == "tool_result":
            t = turngate._result_text(b)
            tr[re.sub(r"[0-9a-f]{6,}|\d+", "N", t[:38].replace("\n", " "))] += 1
for k, v in sorted(tr.items(), key=lambda x: -x[1])[:20]: print(f"{v:5}  {k!r}")

print("\n## Notification headers seen in ReadNotifications results: distinct 'origin' values")
org = collections.Counter()
for r in rows:
    cc = (r.get("message") or {}).get("content") if isinstance(r.get("message"), dict) else None
    if r.get("type") != "user" or not isinstance(cc, list): continue
    for b in cc:
        if isinstance(b, dict) and b.get("type") == "tool_result":
            for m in re.finditer(r"^--- Notification \d+ of \d+ · id: \S+ · origin: (.*?) · queued at", turngate._result_text(b), re.M):
                org[m.group(1)] += 1
print(dict(org))
print("rows matched by turngate.SCHEDULED_HEADER:", [ (i, rows[i].get("timestamp","")[:16]) for i in range(len(rows)) if turngate.scheduled_index(rows[:i+1]) == i ][:20])

print("\n## AskUserQuestion answers: the exact text format (real examples, these are the owner's clicks)")
n = 0
for r in rows[::-1]:
    cc = (r.get("message") or {}).get("content") if isinstance(r.get("message"), dict) else None
    if r.get("type") != "user" or not isinstance(cc, list): continue
    for b in cc:
        if isinstance(b, dict) and b.get("type") == "tool_result" and "questions have been answered" in turngate._result_text(b):
            print("  ", repr(turngate._result_text(b)[:300])); n += 1
    if n >= 4: break
json.dump(accepted, open(sys.argv[3], "w")) if len(sys.argv) > 3 else None
