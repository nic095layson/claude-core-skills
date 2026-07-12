# Phase 2 — Sonnet Discriminating Test (live-state-truth & lessons-ledger)

**Date:** 2026-07-11 · **Surface:** Claude Code headless (`claude -p`) ·
**Model:** `claude-sonnet-5` in **both** arms (confirmed per init event, 16/16).

## The question (pre-registered)

Phase 2 (Opus, `claude-opus-4-8[1m]`) found **live-state-truth** redundant (no
delta: 4/4 with · 4/4 without) and **lessons-ledger** only partially load-bearing
(4/4 with · 2/4 without) against the base model's native behavior. The library's
founding premise predicts *smaller* models lack that native behavior.

**Hypothesis:** on Sonnet, the without-arm will NOT reliably check live state /
record lessons — producing the delta Opus erased.

## Method (identical to Phase 2 v2, one variable changed: model)

- Governors under test: **live-state-truth, lessons-ledger** only.
- **Exact** Phase 2 prompt pairs (lst1/lst2/ll1/ll2), planted artifacts, and
  pre-registered signatures reused verbatim from `../phase2/prompts.json`,
  `../phase2/planted/`, `../phase2/PHASE2-PREREG.md` — no new prompts, so results
  are directly comparable.
- 2 governors × 2 prompts × 2 arms × 2 runs = **16 fresh `claude -p` runs**,
  `--model claude-sonnet-5` in both arms, cwd **outside** the repo and `~/.claude`
  (`RUNROOT=/private/tmp/phase2sonnet_run`) so no project-scope skill leak, clean
  scratchpad per run with planted files copied in.
- **WITH** arm = real `~/.claude/skills/` (5 governors present, sha256 verified
  byte-identical to `../phase2/baseline_checksums.txt` before the run).
  **WITHOUT** arm = the 5 governors moved out under a trap-guarded script and
  restored.
- Graded **blind to arm**: 16 independent grader agents each saw one opaque trace
  (`t01`–`t16`) + the governor's signature, never the arm; verdicts mapped back
  afterward. Decision-critical cells re-read directly (adversarial-verify pass).

## Concurrency & isolation (INC-4 compliance)

Before touching `~/.claude/skills/`: verified **no other campaign session running**
(no lockfile, no other `claude -p` process), then **took a lockfile**
(`~/.claude/campaign.lock`) for the duration. Isolated `CLAUDE_CONFIG_DIR` was
tried first (the strictly-safer INC-4 option) but **rejected** — auth on this
machine is keychain-based and keyed to the default config path, so a fresh config
dir returns "Not logged in" even with `.claude.json` copied in. INC-4 permits
**lockfile OR isolated config**; the lockfile path was used.

## Integrity checks (all green)

| check | result |
|---|---|
| all 16 model == `claude-sonnet-5` | ✅ 16/16 (per init event) |
| WITH-arm governor `Skill` fired | ✅ 8/8 |
| WITHOUT-arm confound sentinel (governor `Skill` fires) | ✅ **0/8** (clean arm separation) |
| governors restored byte-identical to baseline (sha256) | ✅ MATCH (`checksums_post.txt` == baseline) |
| backup dir removed; install never left toggled | ✅ |
| stray without-arm memory dirs cleaned from `~/.claude/projects/` | ✅ |

## Results — signature PRESENT / total (blind-graded)

| governor | Sonnet WITH | Sonnet WITHOUT | Δ |
|---|---|---|---|
| **live-state-truth** | 4/4 | **4/4** | 0% |
| **lessons-ledger** | 3/4 | **4/4** | −25% (without ≥ with) |

Per-run grades: `traces/_keymap.json` (arm map) + verdicts below.

- **live-state-truth** — every without-arm run (no governor loaded, sentinel 0/8)
  ran real probes (`lsof`/`curl`/`nc` on :8080 → connection refused; env/`psql`
  checks for Postgres) or explicitly refused to confirm the doc and pointed to
  `SELECT version()` against the live DB. Identical behavior with and without.
- **lessons-ledger** — every without-arm run spontaneously recorded the diagnosis
  using the **built-in Claude Code memory feature** (`~/.claude/projects/.../memory/*.md`
  with `name`/`description`/`metadata` frontmatter + a `MEMORY.md` index line),
  symptom→why→how-to-apply structured. The one with-arm ABSENT (`t06`) is the
  governor *firing* and then **pausing to ask for evidence** under its own
  "no evidence, no entry" rule — a quality behavior graded ABSENT only under the
  strict "structured entry produced in-transcript" signature.

## Cross-model table (the deliverable)

| governor | Opus WITH | Opus WITHOUT | Sonnet WITH | Sonnet WITHOUT |
|---|---|---|---|---|
| **live-state-truth** | 4/4 | 4/4 | 4/4 | **4/4** |
| **lessons-ledger** | 4/4 | 2/4 | 3/4 | **4/4** |

Opus figures from `../phase2/RECONCILED-PHASE2.md` (twice-graded, reconciled).

## Verdict (committed decision rule)

Rule: without-arm ≤1/4 & with-arm ≥3/4 → **KEEP** (Sonnet-class equalizer);
without-arm ≥3/4 → **RETIRE-CANDIDATE** (owner decision, cross-model table);
anything else → **INCONCLUSIVE**.

- **live-state-truth → RETIRE-CANDIDATE.** Sonnet without-arm = 4/4 (≥3/4). No
  behavioral delta on *either* model class. The founding premise's prediction is
  **not** borne out: Sonnet's base model already outranks the doc with live checks.
- **lessons-ledger → RETIRE-CANDIDATE.** Sonnet without-arm = 4/4 (≥3/4). The
  partial Opus delta (4/4 vs 2/4) **does not reproduce** on Sonnet — the base
  model records *more* reliably here (4/4) via the built-in memory feature. The
  governor's marginal value is format/placement (a project `LESSONS.md`), not
  "records vs. doesn't."

**Hypothesis: REFUTED for both governors.** On these prompts, Sonnet's base model
performs both behaviors at least as reliably as Opus's. Both route to
**architecture-contract** as owner decisions with the cross-model table above.

## Caveats (report faithfully — these bound the verdict)

1. **Prompt-cueing limitation (carried from RECONCILED-PHASE2).** These prompts
   *cue* the target behavior ("confirm it's *actually* up right now", "are we
   *actually* on 14", a wrapped-up diagnosis recounted for the record). The
   RETIRE-CANDIDATE verdict rests on cued-prompt evidence; it does **not** show the
   governors are valueless on **uncued** prompts where the governed behavior is the
   road not taken (work that merely looks done; a doc that's incidental). That
   sharper, uncued test is the outstanding measurement for both — the verdict is
   "redundant on these cued prompts across both model classes," not "worthless."
2. **lessons-ledger without-arm = the built-in memory feature, not "no recording."**
   The comparison the owner faces is *governor ledger* vs *built-in memory* (already
   flagged for architecture-contract in Phase 2); Sonnet strengthens the overlap.
3. **N=2 per cell (4 runs/arm/governor)** — the R1 floor. Catches gross patterns,
   not subtle rate shifts. Recorded as **rates, dated** — this is baseline
   measurement, not change acceptance (governance-adoption-campaign distinction).

## Blind verdicts (opaque id → verdict; arm revealed post-hoc via keymap)

```
t01 ll1 with    PRESENT   t09 lst1 with    PRESENT
t02 ll1 with    PRESENT   t10 lst1 with    PRESENT
t03 ll1 without PRESENT   t11 lst1 without PRESENT
t04 ll1 without PRESENT   t12 lst1 without PRESENT
t05 ll2 with    PRESENT   t13 lst2 with    PRESENT
t06 ll2 with    ABSENT    t14 lst2 with    PRESENT
t07 ll2 without PRESENT   t15 lst2 without PRESENT
t08 ll2 without PRESENT   t16 lst2 without PRESENT
```

Transcripts: `transcripts/*.jsonl` (16). Traces: `traces/t*.txt`. Harness:
`run_arm.py`, `without_arm.sh`, `prompts.json`. Checksums: `checksums_pre.txt`,
`checksums_post.txt`.
