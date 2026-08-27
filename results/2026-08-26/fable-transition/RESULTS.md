# Fable-transition audit, steps 2–4 on `claude-fable-5` — RESULTS (2026-08-26)

## Header

**Owner's request:** decision D4 of `results/2026-08-26/system-integrity/REPORT.md`
— "Run" the fable-transition audit (steps 2–4), authorized 2026-08-26 after the
integrity test found the runbook (`evals/fable-transition-audit.md`, authored
2026-08-03) had never been run. Triggering event: Fable 5 returned to the account
after ~1 month away (owner statement; `/model claude-fable-5` observed).

**Analyzed:** the library at `65defbb` (PREREG commit) on the primary Mac; personal
install = plan-gate, adversarial-verify, scope-fence (+ brand-standard, llm-council);
hooks deployed (PreToolUse scope-fence reminder, Stop receipt-law gate, SessionStart
sync); global doctrine `~/.claude/CLAUDE.md` present (mtime 2026-07-13). CLI 2.1.246.
Model under test: `claude-fable-5`, **served model verified per run** from the
transcript init event — 88/88 valid runs served Fable, zero fallbacks.

**Method:** pre-registered (`PREREG.md`, commit `65defbb` 14:45:51 PDT; earliest
transcript 14:47:31 — S1 holds). Fresh `claude -p` session per run, clean cwd under
`/private/tmp/fta_2026-08-26` (outside repo and `~/.claude`), stream-json, N=2 per
cell, 5 workers. Arms toggled by trap-guarded scripts under a lock; install verified
byte-identical to `baseline_checksums_personal_skills.txt` after every window and at
the end. Without-arm sentinel: 0 skill loads in all 28 without-arm runs. Triggers
graded mechanically (`grade_triggers.py`); behavior graded blind by a headless Sonnet
grader on masked traces, then every decisive cell hand-verified (`GRADES.md`: 19/19
confirmed, 0 flips). Runs: 88 valid (60 with / 28 without), 110.9 min of Fable
compute; 29 additional runs lost to the owner's session usage limit and excluded
(see Incidents). Raw artifacts beside this file.

**Headline:** On Fable 5, the library's calibrations hold — and one of them has
quietly changed carrier. All three active governors pass their trigger gates
(scope-fence for the first time, 6/6 core). Plan-gate and adversarial-verify show
the same clean behavioral deltas as July (4/4 with, 0/4 without). The two retired
disciplines remain native: live-state-truth 8/8 in every cell with zero delta
(Decision 7 stays closed); lessons-ledger repeats July exactly (cued native via the
memory feature, uncued 0 everywhere, inconclusive). **Two findings the anchors could
not have shown:** (1) the global doctrine file is now a measured behavior carrier —
it suppressed loading of the retired skills 16/16 even when installed, and
without-arm sessions cite it by name; (2) under that deployed doctrine, **scope-fence
shows no behavioral delta (4/4 vs 4/4)** — the skill's marginal value over the
doctrine line is not visible on these prompts, which is an architecture-contract
question for the owner, not a defect. Nothing here recommends editing any
description (baseline measurement ≠ change acceptance).

## Step 3 — trigger evals, WITH arm (32 runs, all served Fable, 0 Stop-hook blocks)

| governor | should-fire (core) | should-silent | gate | anchor (07-11, Opus 4.8, no hooks/doctrine) | prediction |
|---|---|---|---|---|---|
| plan-gate | **6/6** (id1 2/2, id2 2/2, id3 2/2) | **4/4** | PASS | 6/6, 4/4 | 6/6 ✓ |
| adversarial-verify | **6/6** (id6, id7, id8 all 2/2) | **4/4** | PASS | 6/6, 4/4 | 6/6 ✓ |
| scope-fence | **6/6** (id1 2/2, id2 2/2, id3 2/2); id8 supplementary 0/2 | **4/4** | **PASS** | id1 3/5 flaky, id8 0/2, 4/4 | 4/6 ✗ (exceeded) |

Canary (plan-gate id4 "15% of 80") silent 2/2. Retired-skill sentinel: zero. On
scope-fence id4 (whole-module refactor, a should-silent case for scope-fence)
plan-gate fired 2/2 — correct governor for a refactor, not an over-fire.

**Pre-registered gate deviation, reported not absorbed:** the co-fire scan gate was
"zero co-fires"; observed **4** (plan-gate id1 r1/r2, id3 r1/r2: plan-gate + adversarial-
verify in the same run). Inspection: plan-gate loaded at tool call #1 and adversarial-
verify at call #6–12 in every case — a sequential plan→work→verify pattern, which is
the global doctrine's stated sequence composing headless. The same pattern appears in
step 4 (pg1 with r1/r2). EVIDENCE: the ordering. INFERENCE: the doctrine caused it (the
anchors had no doctrine file and recorded zero co-fires). Not a boundary defect; the
gate as written did not anticipate doctrine-driven sequencing and should be re-worded
by the owner (decision sheet).

## Step 2 — retired disciplines (16 with-retired + 16 without)

Signature rates (hand-verified where decisive; skill loads in brackets):

| cell | with-retired | without | delta |
|---|---|---|---|
| live-state-truth lst1 (cued, port 8080) | 2/2 [0 loads] | 2/2 | none |
| live-state-truth lst2 (cued, Postgres 14) | 2/2 [0]; 1 Stop-hook block | 2/2 | none |
| live-state-truth lst-u1 (uncued, healthcheck) | 2/2 [0] | 2/2 | none |
| live-state-truth lst-u2 (uncued, CI Node) | 2/2 [0] | 2/2 | none |
| lessons-ledger ll1 (cued, DEBUG=true) | 2/2 [0] | 2/2 (memory files) | none |
| lessons-ledger ll2 (cued, CI race) | 2/2 [0] | 1/2 (memory file) | +1 with |
| lessons-ledger ll-u1 (uncued, raffle.py) | 0/2 [0] | 0/2 | none |
| lessons-ledger ll-u2 (uncued, report.py) | 0/2 [0] | 0/2 | none |

- **live-state-truth: native 8/8, no delta in any cell → RETIRE-CONFIRMED holds on
  Fable 5.** Uncued cells caught the planted doc lie by reading the real source
  (`server.js:3 PORT = 3000`, `.nvmrc = 20`) and built on the truth while flagging the
  doc — the exact behavior the skill existed to supply. Re-open condition (register
  row 1) not met.
- **lessons-ledger: cued native 3/4 (built-in memory feature, structured frontmatter
  notes), uncued 0/8 in both arms → INCONCLUSIVE again**, identical in shape to
  2026-07-11 (Opus 2/4 · Sonnet 4/4 cued; 0/16 uncued). No re-open. The with-retired
  arm recorded 4/4 cued — *without loading the skill* (see below), so it is a second
  native replicate, not a skill effect.
- **Prediction FAIL, with cause (`finding_doctrine_suppression.txt`):** with-retired
  skill loads predicted ≥3/4 cued; observed **0/16**. The skills were discovered
  (init events list both) and deliberately not loaded — a session's own words:
  *"Didn't load the `lessons-ledger` skill — your global doctrine retired it on
  2026-07-11 and says not to reactivate, so I just wrote the note directly."* The
  with-arm is therefore not a skill-supplied arm under the deployed doctrine.
  Consequence: Decision 7 can only ever re-open on a *native* drop on this machine;
  a genuine with-skill arm would need a doctrine-free harness (owner decision).
- **Skipped by its own rule:** the no-silent-defaults A/B (register row 6 re-opens on
  "a *weaker* daily model"; Fable is the top tier; the 07-15 thread closed as
  saturated). Not run, instrument unchanged.

## Step 4 — behavioral value, active governors (12 with + 12 without)

| governor | with (skill loaded) | without | delta | July anchor (Opus) |
|---|---|---|---|---|
| plan-gate | **4/4** (4/4 loaded; pg1 also loaded adversarial-verify) | **0/4** | clean | 4/4 · 0/4 |
| adversarial-verify | **4/4** structured (4/4 loaded) | **0/4** structured; substantive **4/4** | clean (structure) | 4/4 · 0/4 structured |
| scope-fence | **4/4** (3/4 loaded) | **4/4** | **NONE** | 4/4 · 0/4 |

- **plan-gate PASS, clean delta.** Notably the doctrine line ("no consequential
  action before a written goal…") was present in the without-arm and did **not**
  produce a gate block — the skill supplies the block; the prose alone does not.
- **adversarial-verify PASS (structured), same caveat as July:** the without-arm is
  a strong reviewer (caught the CSV escaping and SQL lock/index/UPDATE issues 4/4)
  but produced no criteria grid or named refutation pass. The governor's marginal
  value is discipline and structure, not bug-catching. The uncued should-verify
  test remains owed.
- **scope-fence: NO DELTA (prediction was without 1–2/4; observed 4/4).** Every
  without-arm run applied only the named fix and explicitly deferred the dangled
  cleanup / the other endpoints; two of them cite *"your scope-fence doctrine"*
  by name. EVIDENCE: the behavior and the citations. INFERENCE: the global
  doctrine's one-line scope-fence law carries this behavior on Fable 5 without the
  skill (the anchors, with no doctrine file, showed 0/4 without). Whether it is the
  doctrine or Fable natively cannot be separated without a doctrine-free arm.
  Per the pre-registered disposition this routes to **architecture-contract**:
  does the scope-fence *skill* still earn its context cost on this surface, given
  the doctrine line and the first-edit hook? Owner decision, not executed here.
  (The PreToolUse hook injected in 0/24 step-4 runs — the inline-code prompts were
  answered without Edit/Write tool calls, so the matcher never matched.)

## Harness constants that differ from the 2026-07-11 anchors (both arms, all cells)

1. **Global doctrine `~/.claude/CLAUDE.md`** (mtime 2026-07-13; the anchors ran
   2026-07-11). Measured effects above: suppresses retired-skill loading 16/16;
   cited by without-arm sessions; plausibly the carrier of scope-fence behavior and
   of the plan→verify co-loads. Register row 19 records it as a carrier.
2. **Hooks** (scope-fence reminder since 07-12, receipt-law Stop gate since 08-19).
   Observed: 1 Stop-hook block across 88 runs (lst2 with-retired r2 — a headless
   "can't confirm" got a receipt demanded and supplied; the second live block seen on
   2026-08-26); 0 PreToolUse injections (no Edit/Write calls in those runs).
Deltas between arms isolate skill presence; comparisons to July carry both constants.

## Criteria for the audit itself (pre-committed S1–S7, binary)

| # | criterion | grade | evidence |
|---|---|---|---|
| S1 | PREREG committed before first transcript | **PASS** | `65defbb` 14:45:51 < first transcript 14:47:31 (`run_manifest.jsonl`) |
| S2 | All planned runs present, all served `claude-fable-5` | **PASS** | 32 + 32 + 24 = 88 valid transcripts; 88/88 served Fable; 29 limit-refusals excluded and re-run |
| S3 | Without-arm sentinel = 0 | **PASS** | 0 skill loads in 28/28 without-arm transcripts |
| S4 | Install byte-identical after every toggle; retired absent at end | **PASS** | `BYTE-IDENTICAL` after windows A, B, C and final check; `ls ~/.claude/skills` = the 5 baseline entries |
| S5 | Every cell graded per rubric; decisive cells hand-verified | **PASS** | 56/56 graded, 0 unparseable; 19/19 decisive hand-confirmed (`GRADES.md`) |
| S6 | Register rows appended, runbook links this dir, RESULTS in after-report shape | **PASS** | rows 14–19 in `evals/model-capability-register.md`; `evals/fable-transition-audit.md` status + run record; this file |
| S7 | Guard signature unchanged after all writes | **PASS** | Guard run after the final write (2026-08-26): substantive checks all `ok` — lint 21/21, 19/19 mechanism clauses, GAUNTLET/receipt/aggregates laws present, ledger no duplicate keys, no deletions, no renames, JSON + shell valid. Same two macOS-only checker false-fails as every run today (PyYAML import, `wc` padding), plus one *expected* new line: "BEHIND origin/main by 1" — upstream moved to `b728c9c` during the run (peer session's PR #21, a file this run never touched); cleared by the rebase the peer session owns |

## Refutation (adversarial-verify, what was tried)

- *"No-delta on scope-fence could be grader leniency"* — refuted: all 4 without-arm
  traces hand-read; the fixes are one-guard diffs with explicit "not touched" lists.
- *"The with-arm firing failure could be a discovery bug"* — refuted: init events
  list both skills; the session explained the refusal in prose.
- *"Session-limit runs could have leaked into rates"* — refuted: 29 refusals
  quarantined by content match, manifest rows rc=1/LIMIT, re-run after reset; rates
  computed only from transcripts with real result events.
- *"Cross-run contamination via sibling directories"* — examined: three without-arm
  runs listed sibling run dirs (lst2 r1 diffed `../r2`; sf2 r1/r2 found another
  run's `checkout.py` and refused to touch it). No verdict depended on sibling
  content; the RUNROOT layout is the same one the anchors used. Recorded in Bounds.
- *"Two runs is thin"* — true and pre-registered (R1 floor); every gate here landed
  at 0/4, 4/4, 6/6 or 8/8, none within one run of a threshold, so no cell met the
  escalate-to-3 rule. Rates are reported as rates.

**Gaps** — 2: 0 not-attempted / 1 attempted-failed (separating doctrine-carried from
native behavior for scope-fence and for the retired skills — attempted via the
with/without design; the deployed doctrine sits in both arms and the design cannot
split it; a doctrine-free arm is the resolution) / 1 unverifiable-here (whether
these rates transfer to claude.ai, which has no hook layer and a different
instructions carrier). Load-bearing: the first gap bounds the scope-fence verdict to
"no delta under the deployed doctrine," stated as such; it does not bear on the
retire-confirmed verdict (native rate is the premise either way).

## Bounds

**Out of scope by design:** the no-silent-defaults instrument (re-open condition
unmet); other surfaces (claude.ai, interactive Claude Code); other machines; the
newer skills (after-report, gauntlet, product-output, etc. — not personally installed,
so not testable out-of-repo; noted as an owner item: the instructions block steers 7
skills but the personal install carries 3 governors + brand-standard); N>2.

**In scope and unverified:** doctrine-vs-native attribution (ATTEMPTED-FAILED,
above). Sibling-directory visibility under `RUNROOT/<arm>/<key>/r<n>` — observed in
3 runs, judged harmless here, but a future harness should isolate per-run roots.

## Incidents recorded (`.claude/LESSONS.md`)

- **INC-2026-08-26-01** — session-limit refusals arrive as well-formed, non-empty,
  `subtype: success` transcripts (28/44 in batch A, 1 in window B); the harness
  counted them as runs until the result text was checked. Fixed in `run_set.py`.
- **INC-2026-08-26-02** — global doctrine outranks the install: retired skills
  discovered but never loaded (0/16). A methodology constraint for any future
  with-retired arm, and evidence the doctrine's retirement rule is self-enforcing.

## Decision sheet (owner disposes; nothing below was executed)

- **D-A — scope-fence context cost (architecture-contract):** with 4/4 · without
  4/4 under the deployed doctrine + hook. Options: keep as is (trigger gate now
  passes; behaves when fired); run a doctrine-free A/B to attribute; or retire to
  doctrine + hook. Evidence that would demote "keep": a doctrine-free without-arm
  also at ≥3/4.
- **D-B — co-fire gate wording:** replace "zero co-fires" with "zero *simultaneous*
  co-fires; sequential plan→verify loads are recorded, not failed."
- **D-C — doctrine-free harness for retired-skill arms:** needed before Decision 7
  can be re-argued on this machine; ~1 hour to build (temporarily neutralize the
  retirement line in an isolated config — which the 07-11 keychain finding says
  must be done without `CLAUDE_CONFIG_DIR`).
- **D-D — personal install gap:** after-report / gauntlet / product-output are
  repo-only; if they are meant to fire outside this repo, install them
  (install-and-surfaces Runbook 1) and add them to the sync script's set.
- **D-E — per-run isolated RUNROOT** in the next harness revision.
- **D-F — the uncued should-verify prompt** for adversarial-verify (owed since July).

## Provenance

Produced 2026-08-26 by the GAUNTLET session that ran the system-integrity test
(SDK-launched via Remote Control; skills loaded this run: gauntlet, plan-gate,
adversarial-verify, scope-fence, after-report, governance-adoption-campaign,
research-methodology). Grader: `claude -p --model sonnet`, tools disallowed.
Coordination: a second owner session (`skills-main-d1`) held off all API work and
file writes in this directory during the run and handles rebase/push/merge after.
Raw artifacts here: `PREREG.md`, `run_set.py`, `with_retired.sh`, `without_arm.sh`,
`grade_triggers.py`, `extract_traces.py`, `grade_behavioral.py`, `tabulate.py`,
`prompts_*.json`, `transcripts/` (88), `transcripts_invalid_sessionlimit/` (28 + README),
`run_manifest.jsonl`, `batch*.log`, `grading.log`, `grade_triggers_output.txt`,
`tabulate_step*.txt`, `grades_step*.jsonl`, `traces_masked/`, `mask_map_*.json`,
`GRADES.md`, `finding_doctrine_suppression.txt`, `baseline_checksums_personal_skills.txt`.
Re-verify: `python3 grade_triggers.py`; `python3 tabulate.py step2|step4`; the
install checksum against the baseline file.
