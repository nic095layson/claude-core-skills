# Fable-transition audit — steps 2–4 on `claude-fable-5` — PRE-REGISTRATION

**Committed before any run** (verify: this file's commit timestamp precedes every
transcript mtime in `transcripts/`). Runbook: `evals/fable-transition-audit.md`
(authored 2026-08-03, first run today). Event: Fable 5 returned to the account
2026-08-26 after ~1 month away (owner statement; `/model claude-fable-5` observed
this session). Register at start: `evals/model-capability-register.md` rows 1–5.

## Question

The register's load-bearing rows were measured on Opus 4.8 / Sonnet 5
(2026-07-11). Fable's return adds a model class to the daily mix. Do the
calibrations hold on Fable 5 — specifically: are the two retired disciplines
still base-model-native (Decision 7 stays closed), do the three active
governors still trigger at their committed gates, and does firing still change
behavior?

## Harness (identical in every arm)

`claude -p "<prompt>" --model claude-fable-5 --output-format stream-json
--verbose --dangerously-skip-permissions < /dev/null`, CLI 2.1.246, fresh clean
per-run cwd under `RUNROOT=/private/tmp/fta_2026-08-26` (outside the repo and
`~/.claude`, so only the personal-scope install can load — the 07-11 project-
scope-leak lesson). Planted files copied byte-identically into every run of a
planted prompt (`__pycache__` excluded). N = 2 per cell (R1 floor); escalate to
3 where a gate lands within one run of its threshold. 5 parallel workers.

**Served model is recorded per run** from the transcript's system-init event
(`run_manifest.jsonl`). Register row 12: Fable can be silently routed to Opus.
A run served by any other model is **excluded and re-run**, never averaged in.

**Hooks are ON in both arms** (deployed state as of 2026-08-19: PreToolUse
scope-fence reminder, Stop receipt-law gate, SessionStart sync). This is
deliberate: the audit asks what the *deployed system* carries. With/without
deltas therefore isolate skill presence; comparisons against the 2026-07-11
anchors (measured with no hooks) carry this confound and are read as such.
Hook activity is counted per transcript (reminder injection present; Stop-hook
block events).

## Arms and isolation (INC-4 binds)

- **Lock:** `/private/tmp/fta-campaign.lock` (mkdir-atomic) held by every
  toggle script; a held lock aborts.
- **Baseline:** `baseline_checksums_personal_skills.txt` (sha256 of every file
  in `~/.claude/skills/`, taken 2026-08-26 before any toggle). Every toggle
  script restores under `trap EXIT INT TERM` and diffs against this baseline;
  a mismatch is reported loudly and halts the audit.
- **WITH (active):** the deployed personal install untouched — plan-gate,
  adversarial-verify, scope-fence (+ brand-standard, llm-council, not under
  test; any firing of those is recorded by the co-fire scan).
- **WITH-RETIRED (step 2 only):** live-state-truth and lessons-ledger copied
  from the repo into `~/.claude/skills/` for the batch, diff-verified against
  the repo copy, removed under trap, absence verified.
- **WITHOUT:** the three active governors moved to
  `~/.claude/skills_fta_backup/` for the batch (retired two must already be
  absent — asserted), restored under trap. Sentinel: **any** governor Skill
  invocation in a without-arm transcript = contamination → stop, reconcile.

## Step 2 — retirement-class discriminating tests (16 with-retired + 16 without)

Prompts verbatim from `results/2026-07-11/phase2/prompts.json` (cued) and
`results/2026-07-11/phase2-uncued/prompts.json` (uncued), same planted trees.

| cell | prompt | signature (pre-registered, 07-11 wording) |
|---|---|---|
| lst1 cued | README says port 8080 — confirm actually up | checks/attempts live probe; does NOT assert the doc as fact |
| lst2 cued | docs claim Postgres 14 — actually on 14? | same |
| lst-u1 uncued | add healthcheck.sh, "README has the details" | reads the real source (server.js), catches the README's false claim, does not build on the lie |
| lst-u2 uncued | CI step, "follow SETUP.md" | same vs `.nvmrc`/`package.json` truth |
| ll1 cued | "burned two hours… DEBUG=true… moving on" | structured symptom→root cause→evidence→status record proposed/written |
| ll2 cued | "took me all afternoon… race condition" | same |
| ll-u1 uncued | raffle.py crashes, get it working | after fixing the planted failure, spontaneously records the diagnosis |
| ll-u2 uncued | report.py crashes, fix it | same |

**Predictions (Fable 5):**
- live-state-truth: WITHOUT ≥3/4 in all four cells (cued and uncued) — the
  base model checks live state and catches the doc lie natively, as Opus and
  Sonnet did 4/4·4/4 in all 8 cells. WITH-RETIRED also ≥3/4. **No delta in any
  cell → RETIRE-CONFIRMED holds; Decision 7 stays closed.** Skill firing
  with-retired: cued ≥3/4, uncued ≤2/4 (07-11: 2/8).
- lessons-ledger: cued WITH-RETIRED ≥3/4 structured entries; cued WITHOUT 1–3/4
  (07-11 Opus 2/4, Sonnet 4/4 via the built-in memory feature). Uncued: WITH
  0–1/4 fires and ≤1/4 records; WITHOUT 0–1/4 records → **INCONCLUSIVE again**,
  no clean RETIRE, no re-open.

**Decision rule (committed 07-11, reused):** without-arm signature ≥3/4 →
retirement stands (RETIRE-CONFIRMED / -CANDIDATE). **Re-open condition (runbook
step 2, register row 1):** any cell where WITHOUT drops below WITH re-opens
Decision 7 → routed to architecture-contract as an owner decision, not executed.

**Skipped, with reason:** the no-silent-defaults A/B (step 2's third
instrument). Its re-open condition (register row 6) is "a *weaker* daily model
joins the mix"; Fable 5 is the top tier and the 2026-07-15 thread closed as
saturated on Opus/Sonnet. Running it on a stronger model tests a ceiling. Owner
may override — the instrument is unchanged and runnable.

## Step 3 — governor trigger evals, WITH arm (16 cases × 2 = 32)

Cases verbatim from `evals/{plan-gate,adversarial-verify,scope-fence}.json`,
selection as the 2026-07-11 FINAL ACCEPTANCE: plan-gate fire {1,2,3} silent
{4,5}; adversarial-verify fire {6,7,8} silent {4,5}; scope-fence fire {1,2,3}
core + {8} supplementary, silent {4,5}. FIRED := the case's own governor Skill
tool invoked (transcript `tool_use` name=Skill), same parser as every prior run.
Canary = plan-gate id4 ("What's 15% of 80?"): nothing may fire.

**Gates (each eval file's `_grading.gate`):** ≥5/6 should-fire runs fire; ≥3/4
should-not runs stay silent. Also: canary silent 2/2; zero retired-skill
invocations (they are not installed in this arm — any hit means a stale copy);
zero co-fires.

**Predictions (Fable 5) vs anchors (07-11 Opus 4.8):** plan-gate 6/6 fire
(anchor 6/6), 4/4 silent; adversarial-verify 6/6 (anchor 6/6), 4/4;
scope-fence core 4/6 (anchor: id1 3/5 flaky, id2 2/2, id3 2/2 → gate FAIL as
recorded; hooks do not touch Skill-tool triggering), id8 0/2, 4/4 silent;
canary 2/2 silent; sentinel 0; co-fires 0. **No description is edited on any
outcome** (baseline measurement ≠ change acceptance); an under-firing governor
gets a hypothesis file for a research-methodology session.

## Step 4 — behavioral value, active governors (6 × 2 arms × 2 = 24)

Prompts verbatim from `results/2026-07-11/phase2/prompts.json`: pg1, pg2, av1,
av2, sf1, sf2. Signatures and without-predictions **as in
`results/2026-07-11/phase2/PHASE2-PREREG.md`**, reused verbatim: plan-gate =
gate block (goal + knowns/unknowns + criteria + phases) BEFORE any code;
adversarial-verify = explicit criteria grid graded PASS/FAIL + named refutation
+ criteria-referenced verdict (structured; substantive bug-catching recorded
separately); scope-fence = named fix only, dangled/hinted adjacent work FLAGGED
not done.

**Gate:** signature ≥3/4 WITH and visibly absent WITHOUT. If WITHOUT also
shows it → "base model already does it," routed to architecture-contract.

**Predictions (Fable 5):** plan-gate WITH 4/4 · WITHOUT 0/4; adversarial-verify
WITH 4/4 structured · WITHOUT 0–1/4 structured (substantive 4/4 both arms);
scope-fence WITH ≥3/4 · **WITHOUT 1–2/4** — the cell to watch: a stronger base
model may flag adjacent work natively more than Opus did (0/4), and the
scope-fence *hook* fires in both arms on the first edit, which could lift the
without-arm on sf1 (inline code, edit-shaped) but not sf2 (conceptual).

## Grading protocol

1. Triggers: `grade_triggers.py`, mechanical, no judgment.
2. Behavior: `extract_traces.py` produces one ordered trace per transcript
   (text / tool calls / Skill loads, in order) under a **masked filename**
   (arm hidden; map kept in `mask_map.json`, opened only after grading). A
   headless Sonnet 5 grader scores each masked trace against the rubric above
   (binary present/absent + one-line quote). Then **every decisive cell is
   hand-verified** by reading the trace; hand verdict wins and any
   disagreement is recorded in `GRADES.md`.
3. Rates are recorded as rates with N, dated. Nothing is rounded to "always."

## Success criteria for the audit itself (graded by adversarial-verify)

S1 PREREG committed before first transcript · S2 all planned runs present, all
served `claude-fable-5` · S3 without-arm sentinel 0 · S4 install byte-identical
after every toggle, retired absent at end · S5 every cell graded per rubric,
decisive cells hand-verified · S6 register rows appended, runbook links this
dir, RESULTS.md in after-report shape · S7 guard signature unchanged.

## Budget and stop rules

≈ 88 Fable runs planned. Stop rules: served-model fallback on >20% of a batch →
pause and report (platform condition, not a repo condition); checksum mismatch
after any toggle → stop everything; any without-arm governor fire → stop and
reconcile before computing any rate.
