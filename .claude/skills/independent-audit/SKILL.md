---
name: independent-audit
description: Independent audit of work before it is trusted — a fresh-context auditor that never saw the session's reasoning re-runs every command a report or PR cites, plus three gates for what self-review misses — claims that something runs, exists, is wired or "changes nothing" with no receipt; new code that first meets real data in production; unattended runs that silently do nothing. Load before merging or publishing what a long session built, after a run of owner-caught errors, or when you hear "get an independent audit", "audit this before I merge", "have someone else check the claims", "replay it on real data", "check it against real past inputs", "will the scheduled run actually work?", "make sure it doesn't silently do nothing". Do NOT use to grade your own deliverable against its criteria (adversarial-verify), to attack a model's hand-set constants (red-team), to brief an ordinary subagent (delegation-discipline), or for a trivial change that claims nothing.
---

# Independent-Audit

The failure this skill exists for, from one project's worst two days (2026-10-19..21, 21 recorded
failures): the arithmetic was right every time, and the statements the system made **about itself**
were not. Nine failures were a confident sentence about whether something runs, exists or changes
anything, written with nothing run behind it ("the weekly pull keeps it green" — no script wrote that
file). Seven were new code meeting real data for the first time in production. The owner caught the
worst ones, and the session's own end-of-day audit added four errors of its own: the author re-checking
the author. Self-review cannot see what its author believes. This skill adds the three things it lacks:
a reader who did not write the work, a lint for claims with no receipt, and two gates that make the
real world test the work before the owner does.

## Terms (defined once)

- **Mechanism claim** — a sentence that says a thing runs, exists, is wired, verifies, supersedes,
  keeps something green, or changes nothing.
- **Receipt** — what makes a claim checkable beside it: a command, a commit, a PASS line, a record path,
  a count, or an honest status word (`NOT-ATTEMPTED`, `UNVERIFIED`, "did not check").
- **Independent auditor** — a fresh-context, read-only agent given only the artifact and the repository,
  never the author's conversation or reasoning.
- **Recorded real input** — an input the system actually received in production (yesterday's records,
  last week's files), kept in the repository; the opposite of a fixture written to fit the code.
- **Unattended run** — anything that runs with no one watching: a scheduled task, a nightly job, a fresh
  cloud session started by a trigger.

## Procedure

Scripts live beside this file in `scripts/` (stdlib Python; `<skill>` is this skill's directory).

1. **Lint the claims** (seconds, every report or PR body that states how the system behaves):
   ```
   python3 <skill>/scripts/claim_receipts.py REPORT.md [more.md]      # advisory: lists, exits 0
   ```
   For each flag, add the receipt (run the thing and cite it) or mark the status honestly. Never reword
   a flag away: a claim rephrased past the lint is still unreceipted.
2. **Run the independent auditor** (before a merge or publish that the owner will rely on): make a
   disposable copy of the repository (`git worktree add <tmp> HEAD`), then spawn ONE fresh-context agent
   with the contract in `auditor-brief.md`, filled in with the artifact paths, the copy's path and the
   claims list from step 1, with write/edit tools removed. It re-runs what the artifact cites and returns
   findings; it edits nothing. The copy matters: re-running a test suite writes caches, so read-only can be
   contained but not promised (found 2026-10-21 — the auditor reported its own stray `__pycache__`).
   Treat its report as leads (delegation-discipline): re-run the 2–3 most load-bearing FAIL findings
   yourself before acting, and put every finding — confirmed or not — in front of the owner.
3. **Replay real inputs** before merging a change to anything that consumes production data:
   ```
   python3 <skill>/scripts/replay_gate.py --cmd 'STEP {input_date}' --inputs 'RECORDS_GLOB' --pass-re '^STEP: PASS'
   ```
   Replay at least the most recent recorded inputs, and any input the change was written for. A step that
   exits 0 without its PASS line FAILs; no inputs FAILs.
4. **Preflight every unattended run** as its first step, from a spec in the project:
   ```
   python3 <skill>/scripts/preflight.py --spec PREFLIGHT.json
   ```
   Declare what the run assumes — the checkout, the branch, push access, credentials, tools, writable
   output — so a missing one prints one FAIL line at second zero instead of a silent nothing.
5. **Report** with the auditor's table and each gate's PASS/FAIL line verbatim; the owner decides.

## Output format

The auditor returns (and the report carries) this table:

```
| # | claim (file:line)                       | auditor action                   | result                      | verdict |
| 1 | "status feed runs every morning" (r:36) | grep run-ledger 'status feed'    | 3 rows, last 2026-10-21 PASS | PASS    |
| 2 | "keeps it green" (r:12)                 | grep writers of provenance.csv   | no writer found             | FAIL    |
| 3 | "changes nothing" (r:95)                | re-ran league_sim --seeds 2      | 21.1 → 23.3                 | FAIL    |
```

Verdicts: PASS (re-run agrees), FAIL (re-run contradicts), UNCHECKED (could not run — say why).

## Rules, each with its reason

1. **The auditor never sees the author's reasoning** — a reviewer handed the author's story checks the
   story; one handed only the artifact checks the artifact.
2. **The auditor writes nothing and fixes nothing** — an auditor that repairs grades its own repair, the
   same circle this skill exists to break; repairs are the owner's to approve.
3. **Receipts beside the claim, not somewhere in the report** — a receipt three paragraphs away vouches
   for a different sentence (the receipt-law gate's 2026-10-19 lesson, generalized).
4. **Real inputs over fixtures** — a fixture is written by someone who already knows what the code
   expects; production data was not.
5. **An unchecked run is a failed run** — no inputs replayed, a spec that cannot be read, a browser
   that cannot start: each is FAIL, because "nothing went wrong" and "nothing ran" look identical.
6. **Flags are requests for receipts, never verdicts** — the lint cannot tell a true claim from a false
   one; it can only tell a checkable one from an uncheckable one.

## Proportionality (the anti-ceremony valve)

- A change that states nothing about how the system behaves, touches no production input and starts no
  unattended run: none of this applies.
- A small PR with a sentence or two of claims: step 1 only, a minute.
- A long session's output before merge, a post-mortem, or anything after the owner caught an error: all
  five steps.

## Volatile facts (dated)

- Authored 2026-10-21 from one project's records (`fantasy-basketball-2026-27`, after-reports
  2026-10-19..21; the 21-failure inventory is this library's
  `results/2026-10-21/independent-audit/`). *verified (records), candidate (value)*
- claim_receipts precision on that project's 15 after-reports, hand-graded 2026-10-21: 3 of 7 flags
  real (0.43), below the pre-registered 0.5 bar, so it ships **advisory only**; after the red team's two
  fixes (RT-1 a neighbouring list item no longer lends its receipt; RT-2 quoted and struck text is
  reported, not asserted) 3 of 5 (0.6) — post-hoc, on the same reports, so it does not lift the advisory
  status. Recall on the five recovered false claims 5/5; on a planted fixture 1 of 4 (its vocabulary misses
  "pushes", "writes", "keeps <path> current") — the auditor carries that class. *measured*
- Trigger evals 2026-10-21, `claude-opus-5-5`, N=2, isolated: should-fire 6/6, should-not silent 4/4
  (the near-misses loaded adversarial-verify and red-team). *measured*
- Auditor, planted-claim test (4 true, 4 false claims), fresh headless sessions, write tools removed:
  final brief 15 of 16 verdicts right over 2 runs (one false claim marked UNCHECKED, not FAIL); 0 of 8
  true claims ever marked FAIL; both runs also flagged an unplanted weakness (a test that passes
  regardless). Pre-registered bar "8/8 in each run" met in 1 of 2. *measured, N=2*
- replay_gate on real records: the pre-fix code of both deck incidents FAILs on the real 10/21 morning;
  the fixed code passes 2 of 2 mornings. *measured*

## When NOT to use this skill

- Grading your own deliverable against its success criteria → **adversarial-verify** (this skill is the
  outside reader that comes after it, not a replacement).
- Attacking a model's hand-set constants and quoting structural bands → **red-team**.
- Briefing an ordinary subagent for work, not audit → **delegation-discipline**.
- Checking one doc claim against live state while working → just run the check (live-state-truth's
  doctrine); this skill is for auditing finished work.
- A one-line change that claims nothing → no ceremony.

## Provenance and maintenance

Authored 2026-10-21 at the owner's request ("Build all the recommended, then red team to confirm the
integrity and effectiveness … This is not just for Fantasy Basketball, but Claude Global"), after an
audit of the fantasy kit's 10/19–10/21 failures recommended three safeguards and two external skills
were reviewed and declined (Apache Magpie `audit-finding-fix`: a lint fixer, not an auditor;
mcpmarket `repair-skill`: audits SKILL.md files, not session work). Lineage: adversarial-verify rules
8–9 (verify at the source; a broadly-failing check indicts the checker), delegation-discipline (the
auditor's brief is its contract; reports are leads), the receipt-law Stop gate (receipts beside the
claim), red-team rule 2 (the attacker has not read the code). No project fact enters the procedure.

Re-verify: `python3 .claude/skills/independent-audit/scripts/test_independent_audit.py` (expect all ok).
Update when: the auditor's effectiveness or the lint's precision is re-measured (replace the dated
lines), a project adopts it with different gates (fold the difference in, dated), or the lint's claim
lexicon changes (re-run the precision measurement — a lexicon change is a new variant).
