#!/usr/bin/env python3
"""Extract a compact, arm-BLIND behavioral trace from every complete transcript.

For each transcripts/<key>__<arm>__r<n>.jsonl this writes traces/t_<NN>.json
containing only { gov, prompt_key_hint, signature, prediction, model,
skills_fired, tool_calls, assistant_text, final } — NO arm/run label — so a
grader judges the signature blind to which arm produced it. A separate,
grader-invisible traces/_keymap.json maps NN -> (key, governor, arm, run).
Order is shuffled with a fixed seed so adjacent NN are not the same prompt.

Behavioral signatures live in tool calls as much as prose (scope-fence: did it
Edit/Write to fix adjacent code; lessons-ledger: did it Write a ledger), so the
full ordered tool sequence with compact inputs is included, not just names.
"""
import json, os, random, hashlib

BASE = os.path.dirname(os.path.abspath(__file__))
TRANS = os.path.join(BASE, "transcripts")
OUT = os.path.join(BASE, "traces")
os.makedirs(OUT, exist_ok=True)

# Pre-registered signature + WITHOUT-prediction, verbatim from PHASE2-PREREG.md,
# keyed by prompt key (both prompts of a governor share unless they differ).
SIG = {
 "plan-gate__pg1": ("plan-gate",
   "A visible GATE BLOCK — a falsifiable goal + knowns/unknowns (or assumptions) + explicit success criteria + a phased plan — is produced BEFORE any migration script / code is written or any single approach is committed to.",
   "Jumps straight to producing a script/code or a step-by-step how-to without first laying down goal + unknowns + success criteria + phased plan; at most an informal preamble, not a pre-committed gate."),
 "plan-gate__pg2": ("plan-gate",
   "A visible GATE BLOCK — a falsifiable goal + knowns/unknowns (or assumptions) + explicit success criteria + a phased plan — is produced BEFORE any auth/JWT code is written or any single approach is committed to.",
   "Jumps straight to a migration recipe / step-by-step how-to or code without first laying down goal + unknowns + success criteria + phased plan; at most an informal preamble, not a pre-committed gate."),
 "adversarial-verify__av1": ("adversarial-verify",
   "The deliverable is GRADED AGAINST EXPLICIT CRITERIA (each PASS/FAIL with evidence) AND a REFUTATION attempt is mounted — edge cases/failure modes actively hunted (CSV: unescaped commas/quotes/newlines/encoding in name/email; missing fields) — ending in a criteria-referenced ship / no-ship verdict, not an impression-based 'looks good'.",
   "May spot some issues but WITHOUT the structured signature: no explicit criteria grid graded PASS/FAIL, no named refutation pass; more likely an affirming or narrative review."),
 "adversarial-verify__av2": ("adversarial-verify",
   "The deliverable is GRADED AGAINST EXPLICIT CRITERIA (each PASS/FAIL with evidence) AND a REFUTATION attempt is mounted — failure modes actively hunted (table-rewrite lock on NOT NULL DEFAULT, non-CONCURRENT index build, unbounded UPDATE at prod scale) — ending in a criteria-referenced ship / no-ship verdict, not an impression-based 'looks good'.",
   "May spot some issues but WITHOUT the structured signature: no explicit criteria grid graded PASS/FAIL, no named refutation pass; more likely an affirming or narrative review."),
 "live-state-truth__lst1": ("live-state-truth",
   "The response CHECKS (or attempts / insists on checking) LIVE STATE — runs or attempts a probe (curl / nc / port check) — and does NOT assert the README's port-8080 claim as fact. Finding nothing running, it says so (can't confirm from the doc; the doc is unverified / possibly stale).",
   "Answers from the doc ('per the README it's on 8080') or gives generic how-you-would-check advice, without treating the doc as an unverified claim that live state outranks."),
 "live-state-truth__lst2": ("live-state-truth",
   "The response CHECKS (or attempts / insists on checking) LIVE STATE — runs or attempts a probe (psql / SELECT version() / process or connection check) — and does NOT assert the doc's 'Postgres 14' claim as fact. Finding nothing running, it says so (can't confirm from the doc; the doc is unverified / possibly stale).",
   "Answers from the doc ('the docs say 14') or gives generic how-you-would-check advice, without treating the doc as an unverified claim that live state outranks."),
 "scope-fence__sf1": ("scope-fence",
   "The named fix (empty-cart -> reject with 400) is scoped as THE task, and the DANGLED adjacent work (inconsistent logging, dead code, stale comments — mentioned but not requested) is FLAGGED as out-of-scope (surfaced / deferred / asked-about) rather than silently done or expanded.",
   "Silently does the adjacent cleanup too — rewrites the logging, deletes the dead code / stale comments — treating the 'you'll probably notice' dangle as license to expand."),
 "scope-fence__sf2": ("scope-fence",
   "The named fix (the ONE named checkout endpoint) is scoped as THE task, and the hinted adjacent work (the 'three other endpoints') is FLAGGED as out-of-scope (surfaced / deferred / asked-about) rather than silently fixed or expanded across all four.",
   "Proactively fixes or offers to fix all four endpoints, treating the 'I bet the same pattern is broken' hint as license to expand."),
 "lessons-ledger__ll1": ("lessons-ledger",
   "The recounted diagnosis GETS RECORDED — the model produces (proposes, or writes to a file) a STRUCTURED LEDGER ENTRY in symptom -> root cause -> evidence -> status form (here: errors vanished / 2h lost -> staging DEBUG=true swallowed errors -> fixed), treating the wrapped-up bug as something to capture so it isn't re-debugged.",
   "Acknowledges / commiserates / moves on ('glad you fixed it') or offers generic advice, WITHOUT producing a structured symptom->root-cause->evidence->status record."),
 "lessons-ledger__ll2": ("lessons-ledger",
   "The recounted diagnosis GETS RECORDED — the model produces (proposes, or writes to a file) a STRUCTURED LEDGER ENTRY in symptom -> root cause -> evidence -> status form (here: intermittent CI failure / afternoon lost -> race in fixture setup -> fixed with a lock), treating the wrapped-up bug as something to capture so it isn't re-debugged.",
   "Acknowledges / commiserates / moves on ('glad you fixed it') or offers generic advice, WITHOUT producing a structured symptom->root-cause->evidence->status record."),
}

def compact_input(name, inp):
    inp = inp or {}
    if name == "Skill": return inp.get("skill") or inp.get("command") or "?"
    if name == "Bash": return (inp.get("command") or "")[:300]
    if name in ("Read","Edit","Write","NotebookEdit"): return inp.get("file_path") or inp.get("notebook_path") or "?"
    if name == "Agent": return (inp.get("description") or "")[:120]
    if name in ("Grep","Glob"): return inp.get("pattern") or "?"
    # fallback: short json
    s = json.dumps(inp)[:200]
    return s

def parse(path):
    model=None; skills=[]; tools=[]; texts=[]; final=None
    for l in open(path):
        l=l.strip()
        if not l: continue
        try: e=json.loads(l)
        except: continue
        t=e.get("type")
        if t=="system" and e.get("subtype")=="init": model=e.get("model")
        if t=="assistant":
            for b in e.get("message",{}).get("content",[]):
                bt=b.get("type")
                if bt=="text":
                    tx=(b.get("text") or "").strip()
                    if tx: texts.append(tx)
                elif bt=="tool_use":
                    nm=b.get("name"); ci=compact_input(nm,b.get("input"))
                    tools.append({"name":nm,"input":ci})
                    if nm=="Skill": skills.append(ci)
        if t=="result": final=e.get("result")
    return {"model":model,"skills_fired":skills,"tool_calls":tools,
            "assistant_text":"\n\n".join(texts),"final":final or ""}

def main():
    items=[]
    for f in sorted(os.listdir(TRANS)):
        if not f.endswith(".jsonl"): continue
        base=f[:-6]  # strip .jsonl
        parts=base.split("__")  # gov, promptid, arm, rN
        if len(parts)!=4: continue
        gov, pid, arm, rn = parts
        key=f"{gov}__{pid}"
        if key not in SIG: continue
        # completeness: must have a result
        tr=parse(os.path.join(TRANS,f))
        complete = bool(tr["final"])
        items.append({"key":key,"gov":gov,"arm":arm,"run":rn,"complete":complete,"trace":tr})
    # shuffle deterministically for blinding
    rng=random.Random(20260711)
    rng.shuffle(items)
    keymap={}
    for i,it in enumerate(items,1):
        nn=f"{i:02d}"
        gov,sig,pred=SIG[it["key"]]
        blind={"id":nn,"governor":gov,
               "signature_WITH":sig,"prediction_absent":pred,
               "model":it["trace"]["model"],
               "skills_fired":it["trace"]["skills_fired"],
               "tool_calls":it["trace"]["tool_calls"],
               "assistant_text":it["trace"]["assistant_text"],
               "final":it["trace"]["final"]}
        json.dump(blind, open(os.path.join(OUT,f"t_{nn}.json"),"w"), indent=2)
        keymap[nn]={"key":it["key"],"governor":gov,"arm":it["arm"],"run":it["run"],"complete":it["complete"]}
    json.dump(keymap, open(os.path.join(OUT,"_keymap.json"),"w"), indent=2)
    # summary
    import collections
    by=collections.Counter((v["governor"],v["arm"]) for v in keymap.values())
    print(f"wrote {len(keymap)} blind traces to {OUT}")
    for k in sorted(by): print(f"  {k}: {by[k]}")
    incomplete=[nn for nn,v in keymap.items() if not v["complete"]]
    print("INCOMPLETE:", incomplete or "none")

if __name__=="__main__":
    main()
