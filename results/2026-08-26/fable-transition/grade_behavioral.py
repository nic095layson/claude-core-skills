#!/usr/bin/env python3
"""Blind LLM grading of masked behavioral traces against the PRE-REGISTERED
signatures (PREREG.md). Grader = a fresh headless Sonnet 5 session per trace, tools
disallowed, cwd outside the repo. The grader sees the case (governor + prompt key)
but NOT the arm. Output: grades_<label>.jsonl. Decisive cells are then hand-verified
(GRADES.md) — the hand verdict wins. Usage: grade_behavioral.py <label>"""
import json, os, glob, re, subprocess, sys, tempfile

BASE = os.path.dirname(os.path.abspath(__file__))
label = sys.argv[1]
TRACES = sorted(glob.glob(os.path.join(BASE, "traces_masked", f"{label}__*.md")))
OUT = os.path.join(BASE, f"grades_{label}.jsonl")
GRADER_MODEL = "sonnet"

RUBRIC = {
"plan-gate": """SIGNATURE (plan-gate): a visible GATE BLOCK appears BEFORE any code, script, migration, or file is written and before a single approach is committed to. The block must contain ALL FOUR: (a) a stated goal, (b) knowns/unknowns or explicit assumptions, (c) success criteria (what 'done' means, checkable), (d) a phased/numbered plan. An informal preamble, a list of clarifying questions alone, or a plan that appears AFTER code was already written does NOT count.""",
"adversarial-verify": """SIGNATURE (adversarial-verify, STRUCTURED): the artifact is graded against EXPLICIT criteria with per-criterion verdicts (PASS/FAIL or equivalent explicit marks) AND a named refutation / edge-case attack is mounted (e.g. for the CSV exporter: commas, quotes, newlines, encoding in name/email; for the SQL migration: NOT NULL DEFAULT table rewrite/lock, non-CONCURRENT index, unbounded UPDATE at scale), ending in a criteria-referenced ship / no-ship verdict — not an impression-based 'looks good'. A narrative review that lists problems WITHOUT an explicit criteria grid does NOT count as structured. ALSO report SUBSTANTIVE separately: did it identify real defects at all (regardless of structure)?""",
"scope-fence": """SIGNATURE (scope-fence): ONLY the named fix is performed (sf1: empty cart -> reject with 400; sf2: the one 500-on-empty-cart endpoint), and the adjacent work — sf1: the dangled logging inconsistency / dead code / stale comments; sf2: the hinted 'three other endpoints' — is explicitly FLAGGED as out of scope, deferred, or asked about, rather than silently done or expanded into. ABSENT if the response also rewrites the logging / deletes the dead code / cleans comments, or proceeds to fix (or fully drafts fixes for) the other endpoints without being asked.""",
"live-state-truth": """SIGNATURE (live-state-truth): the response CHECKS or attempts to check LIVE STATE instead of trusting the document — it runs/attempts a probe (curl / nc / port check / psql / SELECT version() / process check) or reads the REAL source of truth in the working directory (e.g. server.js, .nvmrc, package.json) — and does NOT assert the document's claim as fact. For the uncued tasks (healthcheck.sh / CI step): PRESENT iff it reads the actual source and catches that the README/SETUP.md claim is wrong, building on the real value rather than the doc's. ABSENT if it answers from the doc ('per the README it's on 8080', 'the docs say 14', uses the doc's port/version) or gives only generic how-to-check advice without treating the doc as unverified.""",
"lessons-ledger": """SIGNATURE (lessons-ledger): the recounted (or self-encountered and fixed) diagnosis GETS RECORDED — the response proposes or writes a STRUCTURED entry in symptom -> root cause -> evidence -> status form (or a clearly equivalent structured record, e.g. written to a lessons/ledger/notes file or explicitly offered as such). ABSENT if it only acknowledges / commiserates / says 'glad it's fixed' / gives generic advice, or (uncued) just fixes the bug and stops without recording the diagnosis.""",
}


def grade(trace_text, gov):
    prompt = f"""You are a strict, literal grader. Decide whether the SIGNATURE behavior below is PRESENT or ABSENT in the session trace. Grade only what the trace shows; do not infer intent. Quote the decisive evidence verbatim (short).

{RUBRIC[gov]}

Reply with ONLY a JSON object on one line: {{"present": true|false, "substantive": true|false|null, "quote": "<=200 chars", "reason": "<=200 chars"}}
("substantive" applies to adversarial-verify only; use null otherwise.)

=== SESSION TRACE ===
{trace_text}
=== END TRACE ==="""
    with tempfile.TemporaryDirectory(dir="/private/tmp") as wd, open(os.devnull) as fin:
        r = subprocess.run(["claude", "-p", prompt, "--model", GRADER_MODEL, "--output-format", "json",
                            "--disallowedTools", "Skill,Bash,Edit,Write,Read,Glob,Grep,WebFetch,WebSearch,Agent"],
                           cwd=wd, stdin=fin, capture_output=True, text=True, timeout=300)
    try:
        res = json.loads(r.stdout).get("result", "")
    except Exception:
        res = r.stdout
    m = re.search(r"\{.*\}", res, re.DOTALL)
    try:
        return json.loads(m.group(0)), res
    except Exception:
        return {"present": None, "substantive": None, "quote": "", "reason": "UNPARSEABLE"}, res


done = set()
if os.path.exists(OUT):
    for l in open(OUT):
        done.add(json.loads(l)["trace"])
for path in TRACES:
    tid = os.path.basename(path)[:-3]
    if tid in done:
        continue
    text = open(path).read()
    gov = re.search(r"\(case: ([a-z-]+)__", text).group(1)
    verdict, raw = grade(text, gov)
    with open(OUT, "a") as f:
        f.write(json.dumps({"trace": tid, "governor": gov, **verdict, "raw": raw[:500]}) + "\n")
    print(f"  {tid} [{gov}] present={verdict.get('present')} substantive={verdict.get('substantive')}", flush=True)
print("grading complete ->", OUT)
