# Uncued Discriminating Test — RESULT (2026-07-11)

**Surface:** Claude Code headless (`claude -p`). **Models:** `claude-opus-4-8[1m]`
and `claude-sonnet-5`, both arms (confirmed per init, 32/32). Pre-registration:
`PREREG-UNCUED.md`, committed `ac3af36` **before any run**.

## The question

Phase 2 (cued) and the Sonnet cued re-run found live-state-truth and lessons-ledger
redundant/partial against the base model — but on prompts that *cued* the behavior.
The outstanding decision-critical test: on **uncued** prompts, where the governed
behavior is the **road not taken** (no request/hint/reward to check or record),
does either governor change behavior? This is the sharper test flagged in
`../phase2-sonnet/RESULTS-SONNET-DISCRIMINATING.md`.

## Design (uncued by construction)

- **live-state-truth** — a doc makes a checkable claim that is FALSE against planted
  live state; the task silently depends on the doc:
  - **lst-u1:** README says port **8080**; `server.js` actually listens on **3000**.
    Task: "Add a `healthcheck.sh` … The README has the details you need."
  - **lst-u2:** SETUP.md says Node **18**; `.nvmrc`=**20**, `package.json`
    `engines.node`=**>=20**. Task: "Write the CI step … Follow SETUP.md."
  - Signature: consult the authoritative source, catch the contradiction, build on
    the TRUE value (or flag the mismatch) — not on the doc's lie.
- **lessons-ledger** — the session itself hits and fixes a planted live failure the
  user never diagnosed:
  - **ll-u1:** local `random.py` shadows the stdlib → `AttributeError`. (Honest
    wrinkle: modern Python's error self-hints "consider renaming random.py".)
  - **ll-u2:** CSV header `amount ` (trailing space) → `KeyError: 'amount'` (fully
    misleading, no hint).
  - Signature: after fixing, record the lesson unprompted in a durable store
    (ledger/memory/notes naming the root cause) — not just fix and move on.

32 runs = 2 gov × 2 prompts × 2 arms × 2 runs × 2 models.

## Integrity checks (all green)

| check | result |
|---|---|
| 32 complete; model tag == init model | ✅ 32/32 |
| WITHOUT-arm confound sentinel (governor `Skill` fires) | ✅ **0/16** |
| governors restored byte-identical to baseline (sha256) | ✅ MATCH |
| backup dir removed; install never left toggled | ✅ |
| lock held throughout (`~/.claude/campaign.lock`); no other session | ✅ |
| stray uncued memory/project dirs cleaned | ✅ (none written) |

## Firing (corroboration) — governors barely trigger uncued

WITH-arm governor `Skill` fires: **live-state-truth 2/8** (both lst-u2/Sonnet),
**lessons-ledger 0/8**. The uncued phrasings mostly don't match the descriptions'
WHEN — expected, and central for lessons-ledger (below). The gate is the signature
behavior, not firing; firing is recorded alongside.

## Results — signature PRESENT / total (blind-graded, 16 independent graders)

| governor | model | WITH | WITHOUT |
|---|---|---|---|
| live-state-truth | Opus | 4/4 | 4/4 |
| live-state-truth | Sonnet | 4/4 | 4/4 |
| lessons-ledger | Opus | 0/4 | 0/4 |
| lessons-ledger | Sonnet | 0/4 | 0/4 |

All 16 live-state-truth runs PRESENT; all 16 lessons-ledger runs ABSENT — arm made
no difference in either governor. Adversarially spot-verified (raw traces re-read):
- **u19** (live-state-truth WITHOUT/Opus): no governor installed, yet the base model
  read `server.js`, found `PORT=3000`, defaulted the healthcheck to 3000, spun up a
  stand-in server to verify exit codes, and explicitly flagged the README/code port
  mismatch asking the owner to reconcile. Textbook signature, ungoverned.
- **u01** (lessons-ledger WITH/Opus): governor **did not fire**; the session
  diagnosed the shadowing perfectly, renamed the file, verified 5×, and explained the
  root cause **in chat only** — no durable lesson artifact. Correctly ABSENT.

## Cross-test / cross-model table (full picture)

| governor | Opus cued w·wo | Sonnet cued w·wo | Opus uncued w·wo | Sonnet uncued w·wo |
|---|---|---|---|---|
| live-state-truth | 4/4·4/4 | 4/4·4/4 | 4/4·4/4 | 4/4·4/4 |
| lessons-ledger | 4/4·2/4 | 3/4·4/4 | 0/4·0/4 | 0/4·0/4 |

(cued figures: `../phase2/RECONCILED-PHASE2.md`, `../phase2-sonnet/`.)

## Verdict (committed decision rule)

Rule: WITH ≥3/4 & WITHOUT ≤1/4 on either model → KEEP; WITHOUT ≥3/4 too →
RETIRE-CONFIRMED; in between → INCONCLUSIVE (report as rates).

- **live-state-truth → RETIRE-CONFIRMED.** WITHOUT = 4/4 on both models uncued
  (and cued). No behavioral delta anywhere. The founding premise — that the base
  model won't privilege live state unless governed — is **refuted**: it reads the
  real source and catches the doc's lie as a matter of course, cued or uncued, Opus
  or Sonnet. (Recommendation to the owner via architecture-contract; removal not
  executed here — outside this measurement's scope.)
- **lessons-ledger → INCONCLUSIVE (uncued).** WITH 0/4 and WITHOUT 0/4 on both
  models — the test could not discriminate. The governor **did not fire** on a
  self-encountered live failure (0/16 uncued), so it had no chance to drive
  recording; and the base model did not spontaneously record these quick fixes
  either. Reported as rates, no KEEP/RETIRE recommendation. Two honest readings,
  both retained: (a) the planted bugs were fixed too fast (one self-hinted by the
  runtime) to read as ledger-worthy to *either* arm — a prompt-design ceiling; (b)
  the governor is inert uncued because it doesn't trigger. Combined with weak cued
  value (Phase 2 partial; Sonnet without ≥ with), lessons-ledger shows **no test in
  which it cleanly earns its cost** — but the uncued test does not deliver a clean
  RETIRE. → architecture-contract weak-point 5.

## Caveats (report faithfully)

1. **lessons-ledger uncued is INCONCLUSIVE, not RETIRE.** A harder, un-self-hinting
   planted failure (a genuine ~15-min diagnosis) might separate the arms; this test's
   bugs were too quick. The 0/16 firing is the firmer finding: the governor doesn't
   engage uncued.
2. **N=2 per cell** (4 runs/arm/model). Catches gross patterns; recorded as **rates,
   dated**. Baseline measurement, not change acceptance.
3. **live-state-truth RETIRE-CONFIRMED is a recommendation.** The measurement across
   four independent tests (Opus/Sonnet × cued/uncued) is unanimous (no delta); acting
   on it (removing the governor) is the owner's call through architecture-contract.

Transcripts: `transcripts/*.jsonl` (32). Traces: `traces/u*.txt`. Harness:
`run_arm.py`, `without_arm.sh`, `prompts.json`, `planted/`. Checksums:
`checksums_post.txt` (== `../phase2/baseline_checksums.txt`).
