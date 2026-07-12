# FINAL SYSTEM ACCEPTANCE TEST — shipped configuration (3 active governors)

**Date:** 2026-07-11 (run spanning into 2026-07-12 local).
**Surface:** Claude Code **headless** (`claude -p`), personal-scope install (`~/.claude/skills/`).
**Model:** `claude-opus-4-8[1m]` — the same model/variant the acceptance anchors were
measured on (RESULTS-AB, length-compliance); confirmed from every run's `init` event
(32/32, independent re-parse).
**Config under test:** architecture-contract **Decision 7** — three active governors:
**plan-gate, adversarial-verify, scope-fence**. live-state-truth and lessons-ledger retired.
**Governance:** research-methodology + governance-adoption-campaign protocol; concurrency
rule observed (lock held, no concurrent campaign session, byte-identical restoration verified).

**Verdict: PASS.** This is a **regression** test against last-measured rates, not a new gate.
Every active governor's should-fire and should-not-silent rates are within one run of — or
better than — its last measured rates; the canary fired nothing 2/2; **zero** invocations of
either retired governor across all 32 runs (no stale copy anywhere); zero co-fires.

---

## Part 1 — static state (all must pass before any live run)

| # | Check | Result |
|---|---|---|
| 1 | Working tree clean, HEAD == origin/main | **PASS** — both at `bd40138`, `git status` clean |
| 2 | Lint audit 13/13 PASS, 0 FAIL (env PyYAML WARN exempt) | **PASS** — 13 PASS / 0 FAIL; PyYAML absent in env → WARN only, exempt |
| 3 | Personal install = the 3 governors, each byte-identical to repo | **PASS (with note)** — plan-gate, adversarial-verify, scope-fence present and **dir-for-dir byte-identical** repo↔personal (sha256 below). **Note:** `~/.claude/skills/` also contains `llm-council`, an unrelated pre-existing utility skill — not a governor and not a retired governor, so it does not affect acceptance, but it means the install is not *strictly* "only the three." Flagged, not changed. |
| 4 | live-state-truth & lessons-ledger ABSENT everywhere outside the repo | **PASS** — absent from `~/.claude/skills/`; broad `$HOME` scan found no stray retired-governor dirs outside the repo |
| 5 | `instructions/claude-ai-custom-instructions.md` exists and names only the 3 active governors | **PASS** — exists; names plan-gate / adversarial-verify / scope-fence; names each retired governor **0** times as a skill ("three custom skills installed") |

**sha256 (baseline, personal == repo for all three):**
```
plan-gate          7e0c29156c9a8f6d59de966d98f59310869561fd99f70c426ba4a63973ab14f8
adversarial-verify 188d48e5a01adb33fc96c108c396d36e41fc4df8ef5942b3dd4f91b9c16c3399
scope-fence        53566c0c38771c2a82478dcc0da06dcac3f13e22e1a3fc0638d6f78e3a8c2b9b
```

---

## Part 2 — live behavioral regression

**Method:** fresh `claude -p` session per run, cwd in a clean per-run dir **outside the repo
and outside `~/.claude`** (so only the personal-scope install loads — the project-scope-leak
confound from Phase 2 v1 is structurally excluded and re-verified: no ancestor `.claude`),
clean/empty scratchpad per run, stream-json transcript. **2 runs per prompt.**
**FIRED** := a `tool_use` with `name:"Skill"`, `input.skill:"<governor>"` in the transcript —
the same parser as Phase 1 / the A/B (cross-checked by an independent re-parse; both agree).
Standing eval sets: `evals/<gov>.json`. Runner + grader + all 32 transcripts committed under
`results/2026-07-11/final-acceptance/`.

**Case selection** (post-reword should-fire cases + should-not near-misses, per governor):
- **plan-gate** — should-fire id1/2/3; should-not id4/5.
- **adversarial-verify** — should-fire id6/7/8 (the post-reword inline-artifact cases; ids 1–3
  are the pre-reword prompt-confounded originals, excluded); should-not id4/5.
- **scope-fence** — should-fire id1/2/3 (the last-measured set); should-not id4/5. id8 run as a
  **supplementary** standing case (valid but never measured under the trimmed description; id6/id7
  excluded — the eval file itself declares them design errors, not valid should-fire tests).

### Expected (last measured) vs Observed

| governor | class | last measured (anchor) | observed (this run) | within one run? | verdict |
|---|---|---|---|---|---|
| **plan-gate** | should-fire | 9/9 (100%) — id1/2/3 | **6/6 (100%)** — id1 2/2, id2 2/2, id3 2/2 | yes (=) | **PASS** |
| **plan-gate** | should-not-silent | 4/4 (100%) | **4/4 (100%)** — id4 2/2, id5 2/2 | yes (=) | **PASS** |
| **adversarial-verify** | should-fire | 6/6 (100%) — id6/7/8 | **6/6 (100%)** — id6 2/2, id7 2/2, id8 2/2 | yes (=) | **PASS** |
| **adversarial-verify** | should-not-silent | 4/4 (100%) | **4/4 (100%)** — id4 2/2, id5 2/2 | yes (=) | **PASS** |
| **scope-fence** | should-fire (core id1/2/3) | ~60–67% — id1 3/5, id2 2/2, id3 2/2 | **6/6 (100%)** — id1 2/2, id2 2/2, id3 2/2 | yes (↑, not a regression) | **PASS** |
| **scope-fence** | should-not-silent | 4/4 (100%) | **4/4 (100%)** — id4 2/2, id5 2/2 | yes (=) | **PASS** |
| **scope-fence** | id8 (supplementary) | 0/2 (under NEW1/OLD; never under trim) | 1/2 (r1 silent, r2 fire) | yes (↑) | informational |

**Canary** ("what's 15% of 80?", = plan-gate id4): **2/2 fired NOTHING** (direct answer "12", no
governor loaded). **PASS.**

**Retired-skill sentinel** (all 32 runs): **zero** invocations of live-state-truth or
lessons-ledger. Total Skill invocations across the suite were exactly `{plan-gate: 6,
adversarial-verify: 6, scope-fence: 7}` — every fire is an expected should-fire case, so there
were **zero over-fires, zero cross-governor co-fires, and no stale retired copy firing anywhere.**
**PASS.**

### Reading the scope-fence result honestly

scope-fence's core should-fire came in at **6/6 here vs a ~60–67% anchor** — the improvement is
concentrated in **id1**, the one historically-flaky case (0/2 under the over-length NEW1 →
3/5 under the trim → 2/2 here). This is consistent with the already-recorded length-compliance
finding that the shorter, less-diluted description matches id1's "while you're in that file" cue
more reliably; two consecutive fires at N=2 is a favorable fluctuation **within one run** of the
3/5 anchor, **not** a regression. Per research-methodology R3, **two heads do not flip a
known-flaky coin**: this does **not** promote scope-fence's Phase-1 trigger gate from FAIL to
PASS. The gate for scope-fence **remains FAIL** — description-based triggering of the
"restrain adjacent work while editing concrete code" class has a measured ceiling, and
**Claude Code hooks remain the open path** (architecture-contract weak-point 3). What this run
establishes is narrower and is all it was asked to: scope-fence has **not regressed**, and its
behavioral signature still fires (behavioral corroboration below).

### Behavioral corroboration (fires are substantive, not empty tool-loads)

- **scope-fence id1 r1** — after loading scope-fence: *"In scope (what I'll fix): … Adjacent — I'll
  flag, not silently fix: …"* — the signature (scope the named bug, flag logging/dead-code as
  adjacent) is present.
- **plan-gate id2 r1** — produced the gate block: **Goal** (falsifiable), **Assumptions I'm
  carrying**, a phased dual-run migration plan — before proposing edits.

---

## Rollout status (this surface: Claude Code headless, personal-scope)

**Regression-clean on ship date, 2026-07-11.** The three shipped governors behave on this surface
as last measured:

- **plan-gate** — trigger gate PASS (6/6 should-fire, 4/4 silent); behaviorally confirmed. **Shipped.**
- **adversarial-verify** — trigger gate PASS (6/6 should-fire, 4/4 silent); behaviorally confirmed. **Shipped.**
- **scope-fence** — trigger gate **remains FAIL** (hooks are the open path); measured rate is
  at/above prior and did not regress; behavioral signature holds. **Shipped as adopted wording**
  per the owner decision, gate status unchanged.

Other surfaces (interactive Claude Code, claude.ai) remain **OPEN** — the claude.ai `.skill`
uploads still need the owner re-upload noted in the campaign; nothing here measures them.

---

## Provenance

Runner: `final-acceptance/runner.py` (out-of-repo cwd guard by real path-prefix; 5-worker pool;
360s/run timeout). Grader: `final-acceptance/grade.py`. Raw output: `final-acceptance/GRADE-OUTPUT.txt`.
Transcripts: `final-acceptance/transcripts/*.jsonl` (32). Baseline checksums:
`final-acceptance/baseline_checksums.txt`. Anchors sourced from `results/2026-07-11/RESULTS-AB.md`
and `experiments/hypothesis-2026-07-11-length-compliance.md`. No skill descriptions or bodies were
edited by this run (a regression test does not edit; had any governor regressed beyond one run, the
protocol was to record the offending prompts/rates, flag for a research-methodology session, and
report FAILED — that branch did not fire).
