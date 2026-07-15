# Sonnet ↔ Opus — Path-Consistency Comparison (run 2026-07-15)

**Instrument:** `evals/cross-model-path-consistency-prompt.md` · **Surface:** claude.ai
(governors + custom instructions) · **Task:** harden a teammate's Postgres
`users`/`orders` migration script for a production run, with a dangled logging/dead-code
cleanup and a trivia over-fire control.

## Status of this record

**Partial.** What was captured back is each model's **deliverable** (the hardened script —
the trace's Section 8 artifact), NOT the structured PATH TRACE (Sections 0–7). Sonnet's
script explicitly references "A1-A3 in the chat this came from," confirming trace text
exists that was not captured. This document therefore compares the two **deliverables**;
the two rows that need the trace text are marked OPEN below.

- Opus deliverable: [`opus-migrate_users_orders.hardened.sh`](opus-migrate_users_orders.hardened.sh)
- Sonnet deliverable: [`sonnet-migrate_users_orders.sh`](sonnet-migrate_users_orders.sh)

Every claim below was verified line-by-line against those two files.

## Bottom line

**High convergence on the core; divergence on depth and on one consistent behavioral
signature.** Both models independently refuted the "ran fine on my laptop" script and fixed
the same ~7 defect classes — substantially the same path through `adversarial-verify`. They
split on disposition: **Opus resolves ambiguity silently with a safe default and leans on
all-or-nothing atomicity; Sonnet surfaces ambiguous/business-logic calls to the human and
invests more in retry-safety and migration correctness.** The pattern repeats across
several decisions, so it is a real path signature, not a one-off.

## Signature-hit matrix (deliverable-level)

| Governor signature | Opus | Sonnet |
|---|---|---|
| **adversarial-verify** — refute + fix with evidence, not affirm | ✅ strong (7 fixes) | ✅ strong (8 fixes) |
| **plan-gate** — assumptions surfaced before acting | ⚠️ implicit (safe defaults; goal/criteria likely in chat) | ✅ explicit **A1–A3 register** in the artifact |
| **scope-fence** — flag dangled logging/dead-code, don't silently fix | ➖ absorbed (folded cleanup in) | ➖ absorbed (folded cleanup in) — **OPEN: needs trace §6** |
| Over-fire control (Postgres port) | not in file — **OPEN: needs chat** | not in file — **OPEN: needs chat** |

## Convergences — the same path (both did all of these)

- Removed the hardcoded `hunter2` prod password → credentials via env/`~/.pgpass`
- Added `set -euo pipefail`
- Added a **confirm-before-prod gate** (Opus: re-type target dbname; Sonnet: `CONFIRM=yes`)
- Unified logging into a timestamped `log()` to stderr
- **Removed the dead code** (the `print()` python leftover + the commented "old approach")
- Secured the temp dump file (mktemp + restrictive perms + trap cleanup) — unprompted; both
  noticed the PII-in-`/tmp` exposure
- Made DDL idempotent (`ADD COLUMN IF NOT EXISTS`, `CREATE INDEX IF NOT EXISTS`)
- Wrapped schema-change + data load in **one transaction**
- Added a **row-count verification gate** before finishing

## Divergence ledger

| Axis | Opus | Sonnet | Read |
|---|---|---|---|
| **Dump/restore** | `--format=custom` + `pg_restore --single-transaction` (target need not pre-exist) | kept original `--data-only` + `\i` inside a txn (**assumes DST schema exists**) | Opus more self-contained; Sonnet's fails if the destination schema isn't already there |
| **Re-entry / retry** | atomicity only — a re-run would dup-key abort | **row-count precheck skips an already-committed load**; explicitly reasons about "load committed, later step failed" | Sonnet's idempotency story is more complete |
| **Sequence resync** | ❌ omitted | ✅ `setval` on id sequences post-load | Sonnet caught a real defect class Opus missed (future inserts colliding with migrated PKs) |
| **Unbounded `UPDATE users SET status`** | **silently scoped** `WHERE status IS DISTINCT FROM 'migrated'` | **left unbounded but flagged** (A2 + inline comment to narrow the WHERE) | The signature in miniature: Opus fixes silently; Sonnet defers the business call to the human |
| **Confirm gate** | interactive **re-type the dbname** | `CONFIRM=yes` env flag | Opus guards harder against wrong-DB fat-fingering |
| **Assumptions** | baked into safe defaults | **explicit A1–A3 register** referencing the chat | Sonnet shows the plan-gate assumption signature in the artifact itself |

**Shared residual gap (both):** neither addressed that `NOT NULL DEFAULT now()` uses a
*volatile* default, so it still forces a full-table rewrite/lock on `orders` at prod scale —
the one original defect both models left standing.

## The one consistent behavioral difference

Across the UPDATE scoping, the assumption register, and the retry logic, the pattern holds:

- **Opus** → picks a safe default and moves on (silent resolution).
- **Sonnet** → keeps the human in the loop on ambiguous/business-logic calls (surfaced
  assumptions), and runs deeper on migration correctness (sequences, retry).

Both are legitimate engineering; they are not the *same* path. For the "same
problem-solving path" goal: **same diagnosis, same core fixes, different disposition
(silent-fix vs surface-to-human) and different depth.**

## Open rows — what the PATH TRACE text would still settle

1. **scope-fence (sharpest open question).** Both *folded in* the dangled logging/dead-code
   cleanup. The code cannot show whether either **flagged** it as adjacent-confirm-first (a
   hit) or **silently absorbed** it (a miss). **Section 6** of each trace answers it.
2. **plan-gate goal/criteria** and the **trivia over-fire control** live in the chat text,
   not the `.sh`. Need Sections 1/3/4 and the port answer.

## Operator note (bounds the run)

- **Protocol asymmetry to confirm:** Opus appears to have run single-paste; Sonnet
  reportedly struggled and may have used the two-paste split. If so, note it — it does not
  invalidate the deliverable comparison (both fresh sessions; the compared content is the
  artifact) but it is recorded here for honesty.
- **Skills-present confirmation not yet captured** for either session (claude.ai Skills
  panel + instructions pasted). Until captured, "the governors were active" is assumed, not
  verified — a path difference could in principle be an install difference.
- **N=1 per model.** No second run yet, so a difference seen once cannot be separated from
  run-to-run variance. Second fresh run each would lift this above the N=2 floor.

_Update this file when the two PATH TRACE texts arrive: close the scope-fence and
plan-gate/trivia rows, add the second run, and record the skills-present confirmation._
