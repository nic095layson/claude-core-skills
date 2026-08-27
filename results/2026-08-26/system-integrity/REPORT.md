# System integration, validation, and integrity test — 2026-08-26

## Header

**Owner's request (near verbatim):** "It's been a month since I've last had
Fable capability. Can you conduct a full Claude system integration, validation,
and integrity test that Gauntlet, operational procedure logic are all holding
as we worked on previously?" (GAUNTLET run — the word was present.)

**Analyzed:** repo `claude-core-skills` at `5b90b19` (== `origin/main`; working
tree carries one declared modification, the 2026-08-26 instructions edit, plus
this report's directory), the personal install surface on the primary Mac
(`~/.claude/skills/`, `~/.claude/hooks/`, `~/.claude/settings.json`), and the
session's own live behavior. All measurements 2026-08-26.

**Method:** guard_essentials.sh executed 4× today (consistent signature each
run); lint via the guard's loop (21/21) with `lint_skill.sh` read to establish
what its PASS covers; independent regex frontmatter/description sweep;
installed-vs-repo `diff` for 4 skills and 2 hooks; hook selftest run twice
(10/10 both); pipe-tests of the PreToolUse reminder (both paths); known-answer
probe of the guard's mechanism detector (planted absent string → detector said
ABSENT); live-fire observations recorded from this session; Claude Code hooks
docs fetched for the SessionStart question. Raw outputs committed beside this
report. Verification pass: adversarial-verify, all six steps, grades below.

**Headline:** The governance system is holding on this machine's Claude Code
surface. Every mechanical integrity property holds; all four sequenced
governors plus scope-fence loaded live today; the Stop hook produced its
**first-ever observed live block** earlier today and behaved exactly as
designed; installed copies byte-match repo HEAD. Two qualifications: the guard
script itself has two macOS-only checker bugs (its FAILs today are all
environmental — verified, not assumed), and the SessionStart sync hook has no
firing evidence today, unresolved from inside this session (one-step owner
test below). The behavioral layer (do skills *trigger* at the right rates)
remains UNMEASURED, as it was before this run — nothing here claims otherwise.

## Criteria (pre-committed in the plan-gate block, graded binary)

| # | Criterion | Grade | Evidence |
|---|---|---|---|
| C1 | Guard substantive checks all ok; every FAIL traced + property hand-verified | **PASS** | `guard-run-raw.txt`: 22 FAILs = 21 frontmatter (cause: `python3 -c "import yaml"` → ModuleNotFoundError, reproduced; property verified via lint fallback parser 21/21 + regex sweep) + 1 char count (cause: BSD `wc` left-pads, poisoning the grep pattern — reproduced; property verified: measured 5295 = stated 5,295, `carrier-measure-raw.txt`) |
| C2 | 21/21 skills lint PASS | **PASS** | Guard check 1 "lint: 21/21 skills PASS"; `lint_skill.sh` read — its PASS covers frontmatter (PyYAML-free fallback), name==dir, description presence + trigger language + ≤1024, body non-trivial |
| C3 | 21/21 frontmatter parses independently; descriptions ≤1024 | **PASS** | Regex sweep: 0 parse failures, 0 name mismatches, 0 over-limit; longest = plan-gate at 1000 chars (24 from the ceiling — inside lint's WARN band) |
| C4 | All governor/gauntlet mechanism clauses present | **PASS** | Guard checks 2–3: 19/19 `ok` (`guard-run-raw.txt`); detector validated on a known-absent string (said ABSENT) |
| C5 | Hooks syntax-valid, registered, parity, ≥1 live firing, SessionStart status **explained** | **FAIL** (one clause) | Four clauses PASS: syntax ok (guard + sweep); registration present (`hook-registration-raw.txt`); both installed hooks byte-match repo (`install-parity-raw.txt`); Stop hook live-BLOCKED a real turn today, PreToolUse live-fired 2026-08-25 (two real-session sentinels, `sentinel-evidence-raw.txt`) and again 2026-08-26 on this report's Write. The failing clause: SessionStart did not run today (0 log entries; every code path logs; log wrote fine 2026-08-25 ×5) and **why** is unresolved from inside — see Bounds |
| C6 | Instructions carrier internally consistent | **PASS** | GAUNTLET + receipt law + aggregates law all `ok` in guard; stated 5,295 = measured 5295 (hand, guard's method) |
| C7 | Ledger: no duplicate keys | **PASS** | Guard: "ledger: no duplicate keys" |
| C8 | Tree matches origin/main except declared changes | **PASS** | `git status`: only the instructions edit + this results dir; HEAD == origin/main == the Documents/GitHub clone, all at `5b90b19` |
| C9 | Dated report + raw logs exist here | **PASS** | This file + 8 raw artifacts in this directory |

## Component verdicts (tiered: LIVE-VERIFIED > MECHANICALLY-VERIFIED > ATTESTED > OPEN)

- **Gauntlet + governor mechanisms** — LIVE-VERIFIED. All five skills loaded via
  the Skill tool this run (gauntlet, plan-gate, adversarial-verify, scope-fence,
  after-report); all 19 mechanism clauses present; full sequence executed with
  the plan-gate block emitted pre-work. Demotion condition: a load failing or a
  clause grep missing.
- **Stop hook (receipt-law gate)** — LIVE-VERIFIED, upgraded today. First
  observed live BLOCK (2026-08-26): it caught a real unreceipted "couldn't
  check" claim, cited the turn's 9 lookups, and passed the corrected turn.
  Until today the blocking path was fixture-proven only (hooks/README.md's own
  honest limit). Selftest 10/10 twice today.
- **PreToolUse hook (scope-fence reminder)** — LIVE-VERIFIED. Real-session
  sentinels 2026-08-25 (19:26, 21:35) and 2026-08-26 (this report's Write);
  pipe-test both paths PASS today.
- **SessionStart hook (sync-governance)** — OPEN. Mechanism sound (script read;
  fail-open design; ran ×5 on 2026-08-25, last 21:40). Zero log entries today
  despite a registration with no matcher (fires on all SessionStart events per
  docs, fetched 2026-08-26). EVIDENCE: it did not run today. INFERENCE
  (labeled): SDK-launched/non-interactive sessions like this one may not emit
  SessionStart — the docs' quoted surface list (terminal, IDE, desktop, web)
  does not name SDK sessions either way. Resolution is a one-step owner test
  (decision sheet, D1).
- **Installed-copy parity** — MECHANICALLY-VERIFIED. 4/4 repo-sourced personal
  skills and 2/2 installed hooks byte-match repo HEAD; `llm-council` is
  personal-only, which the sync script permits by design. Structural note: the
  sync pulls via the *Documents/GitHub* clone (currently at the same commit,
  clean), so local edits here reach installed copies only after push — by
  design, not drift.
- **Instructions carrier (claude.ai)** — ATTESTED. File is internally
  consistent (C6). Box == file rests on the owner's statement today ("Input to
  instructions"), assumption A1: the box is authenticated claude.ai UI state;
  no tool in this environment reaches it (UNVERIFIABLE from here — what was
  available: local filesystem, git, unauthenticated connectors, web fetch
  without login; none touches account settings).
- **Ledger, evals, scripts** — MECHANICALLY-VERIFIED. No duplicate keys; all
  eval JSON valid; all shell syntax valid (guard checks 5/7).

## Refutation (adversarial-verify, what was tried)

- *"The run proves checks pass, not that governors change behavior"* — correct,
  and the report claims only mechanical + integration health. Trigger rates:
  see Bounds.
- *"Guard PASSes could be vacuous"* — refuted for the mechanism detector by the
  known-answer probe; refuted for lint by reading its source (real fallback
  parser, not a silent skip).
- *"A checker that fails everything is broken"* (rule 9) — applied in both
  directions: the 21 frontmatter FAILs indicted the checker (missing PyYAML,
  verified), and the passing checks were probed rather than trusted.
- *"Two checkouts could be serving different content"* — measured: both at
  `5b90b19`, other clone clean.
- Surprises handled explicitly, not absorbed: SessionStart silence (→ OPEN,
  D1); hooks/README stale vs live state (→ D3, favorable direction: the hook
  it calls "NOT installed" is installed, registered 2026-08-19, and live-blocked
  today).

**Gaps** — 3: 0 not-attempted / 1 attempted-failed (SessionStart "why" — 
attempts: registration read, script read, log grep, docs fetch; cannot
re-trigger a session start from inside a session) / 2 unverifiable (A1 box
state; A2 model identity — weights not introspectable, `/model` stdout
recorded in `model-mix-snapshot.txt`). Load-bearing: only the SessionStart gap
touches a verdict (its component stays OPEN, both resolutions stated in D1);
A1 is carried as ATTESTED; A2 bears on nothing here — the integrity results
are model-independent.

## Bounds

**Out of scope by design:** behavioral trigger-rate evals (all governor eval
JSONs remain authored-NOT-RUN, unchanged by this report; running them is the
fable-transition-audit / governance-adoption-campaign work, owner-gated — D4);
claude.ai surface state (box contents, uploaded skill roster); model-weight
introspection; the other machine(s) — "installed" here means this Mac only.

**In scope and unverified:** why SessionStart produced no log entry today
(ATTEMPTED-FAILED, receipts above). Under resolution (a) — SDK sessions don't
emit the event — the hook layer is fully healthy. Under resolution (b) — the
event fired and the hook didn't run — there is a real integration defect on
this machine and it needs diagnosis before the hook layer is called fully
healthy. Nothing else in the report changes under either resolution.

## Decision sheet (owner disposes; nothing below was executed)

- **D1 — SessionStart test (≈10 seconds):** open a normal interactive terminal
  session, then `tail -1 ~/.claude/hooks/sync-governance.log`. A fresh entry →
  resolution (a), close the OPEN verdict. No entry → resolution (b), diagnose.
- **D2 — Fix the guard's two macOS bugs (≈10 min):** strip `wc` padding
  (`tr -d ' '`) in check 3; move `import yaml` out of the per-file try in
  check 4 (or install PyYAML). Until then every local guard run false-fails
  with this exact signature.
- **D3 — Update hooks/README.md receipt-law section (≈5 min):** it still says
  "PROPOSED, NOT installed" and "no live BLOCK was observed." Both are now
  false in the favorable direction: installed + registered (settings mtime
  2026-08-19), first live BLOCK observed 2026-08-26, correct behavior.
  Optionally record the first-live-block as a dated note (LESSONS entry not
  required — nothing failed).
- **D4 — Run fable-transition-audit steps 2–4 (≈1 working day):** the runbook
  (authored 2026-08-03, never run) exists for exactly this event — the model
  mix changed. Step 1 (mix snapshot) is done and committed here. Steps 2–4 are
  the actual behavioral re-measurement and are the only thing that converts
  "mechanically holding" into "behaviorally holding."
- **D5 — Commit today's work:** the instructions edit (owner-approved and
  pasted) + this results directory. Guard has been run on both sides.

## Provenance

Produced 2026-08-26 by the GAUNTLET run in the owner's Claude Code session
(SDK-launched; model per A2 — `/model claude-fable-5` observed, weights not
introspectable). Skills loaded: gauntlet, plan-gate, adversarial-verify,
scope-fence, after-report. Sources: this repo at `5b90b19`; live probes of
`~/.claude/` surfaces; `code.claude.com/docs/en/hooks` (fetched 2026-08-26).
Raw artifacts beside this file: `guard-run-raw.txt`,
`selftest-receipt-law-raw.txt`, `install-parity-raw.txt`,
`hook-registration-raw.txt`, `sessionstart-evidence-raw.txt`,
`sentinel-evidence-raw.txt`, `model-mix-snapshot.txt`,
`carrier-measure-raw.txt`. Re-verify pointers: guard signature →
`bash .claude/skills/diagnostics-and-tooling/scripts/guard_essentials.sh`;
SessionStart → D1; carrier → copy the box out and diff against the paste
block.

## Addendum — 2026-08-26, later same day (owner asked D1 be run from here)

The SessionStart component's OPEN verdict is substantially resolved. A headless
CLI session (`claude -p`, launched 14:35 from this session) emitted
SessionStart: the sync hook ran and logged `2026-08-26 14:35:31 pull: Already
up to date.` (log 706 → 707 lines; `sessionstart-probe-raw.txt`). EVIDENCE:
script, registration, and firing all work on this machine today under headless
CLI launch. The residual is narrow: this SDK-harness-launched session itself
logged nothing at its own start, so SDK launch evidently does not emit the
event — INFERENCE from the launch-path difference, harness behavior rather
than a defect in this repo's hook. Component verdict: OPEN → LIVE-VERIFIED
(CLI paths), with the SDK-launch caveat noted. The interactive-terminal case
remains untested in the strictest sense but sits on the proven side of the
launch-path split.
