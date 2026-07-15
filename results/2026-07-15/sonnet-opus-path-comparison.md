# Sonnet ↔ Opus — Path-Consistency Comparison (run 2026-07-15)

**Instrument:** `evals/cross-model-path-consistency-prompt.md` · **Surface:** claude.ai
(governors + custom instructions) · **Task:** harden a teammate's Postgres
`users`/`orders` migration script for a production run, with a dangled logging/dead-code
cleanup and a trivia over-fire control.

## Plain-language summary (ELI5, for the human)

Two mechanics handed the same rickety car and told "make it road-safe." Both found the same
real faults, both refused to call it road-safe yet, and both ignored the cosmetic scratches
you pointed at while fixing the one part that was actually broken. The only steady
difference: **Opus quietly picks the safe option and drives on; Sonnet leaves the fuzzy calls
for you to decide and checks a couple of extra corners.** Same road, same repairs — Opus
drives, Sonnet asks for directions at the fuzzy turns. (Neat proof it's real: each model was
asked where *another* model might choose differently, and each correctly predicted the exact
spot where the other actually did.)

**Method note:** the full logical procedure behind this run — so a future session can rerun
and improve it — is written up in
[`../../evals/cross-model-path-consistency-METHOD.md`](../../evals/cross-model-path-consistency-METHOD.md).

## Status of this record

**Complete.** Captured: both models' **deliverables** (hardened scripts — the trace's
Section 8 artifact) and both models' **PATH TRACE §4–7** (pasted back 2026-07-15). §0–3 of
the traces (run header, task classification, skills-engaged table, step-by-step path) were
not captured; the plan-gate / adversarial-verify / scope-fence signatures below are read
from §4–7 plus the artifacts.

- Opus deliverable: [`opus-migrate_users_orders.hardened.sh`](opus-migrate_users_orders.hardened.sh)
- Sonnet deliverable: [`sonnet-migrate_users_orders.sh`](sonnet-migrate_users_orders.sh)

Deliverable claims are verified line-by-line against those files. §4–7 are **self-reported**
(each model tagged its own items OBSERVED/INFERRED); where self-report and artifact diverge,
the reconciliation note says so.

## Bottom line

**The two models take substantially the same path, with one consistent, characterizable
difference.** Same diagnosis, same core fixes, same scope reasoning, same verdict, same
over-fire behavior. Where they differ is **disposition on ambiguous business-logic calls**
(Opus silently picks the safe default; Sonnet preserves original behavior and flags it) and
**depth/mechanism** (Sonnet adds sequence resync + an explicit re-run precheck and keeps
`--data-only`; Opus uses a self-contained custom-format dump/restore). Both models'
own §7 divergence self-flags independently named these same split points — a sign the
instrument is capturing real reasoning, not noise.

**Note on method:** the deliverable-only read (before §4–7 arrived) got the scope-fence row
**wrong** — the rewritten scripts *look* like the cleanup was silently absorbed, but §6 shows
both models consciously **flagged** it. The trace was necessary; the artifact alone misled.

## Signature-hit matrix

| Signature | Opus | Sonnet | Same? |
|---|---|---|---|
| **adversarial-verify** — exercise the artifact, refute with evidence, don't affirm | ✅ ran `bash -n` + shellcheck + runtime probe; **12** defects; **no-ship** | ✅ ran `bash -n` + shellcheck; **~9** defects; **no-ship** | ✅ yes |
| **plan-gate** — success criteria set | ✅ **SC1–SC7** | ✅ **C1–C6** (≈1:1 with Opus) | ✅ yes |
| **plan-gate** — assumptions surfaced | ⚠️ in prose (schema/FK/version uncertainties in §7) | ✅ explicit **A1–A3 register** in the artifact | ~ close |
| **scope-fence** — flag dangled cleanup, fix only what breaks the task | ✅ logging + dead-code **flagged-only**; `print()` fixed as in-scope bug | ✅ logging + dead-code **flagged-only**; `print()` fixed as in-scope bug | ✅ **identical reasoning** |
| **over-fire control** (Postgres port) | ✅ PASS — "5432" direct, no ceremony | ✅ PASS — "5432" direct, kept separate | ✅ yes |

## Convergences — the same path

**Diagnosis (both, with evidence):** both ran static checks and caught that the script
**does not even parse** (`bash -n` + shellcheck fail at the `print()` line), and both noted
this **contradicts "ran fine on my laptop."** That is `adversarial-verify` working as
intended — exercising the artifact, not affirming it.

**Core fixes (both):** removed the hardcoded `hunter2` prod password → env/`~/.pgpass` ·
`set -euo pipefail` · a **confirm-before-prod gate** · idempotent DDL (`IF NOT EXISTS`) ·
schema-change + load in **one transaction** · secured the temp dump (restrictive perms +
trap cleanup — unprompted) · a **row-count verification gate before the status flip**.

**Success criteria (both):** Opus SC1–SC7 and Sonnet C1–C6 map almost one-to-one (no
credentials in file, fail-stop, idempotent re-run, dest==source before flip, no plaintext
dump survives, the broken `print()` must not ship).

**Scope reasoning (both, identical):** logging → flagged-only; commented "old approach"
block → flagged-only; `print()` line → **fixed as an in-scope bug** because it breaks the
script, *not* as cleanup. Both explicitly separated "parse-breaking bug (in-scope)" from
"cosmetic cleanup (out-of-scope, flag it)." Both self-flagged the `print()` call as the
point where a *stricter* scope reading would leave it in place (Sonnet logged it at "Medium
confidence").

**Verdict (both):** no-ship as posted → ship-with-changes for the delivered rewrite.

**Over-fire control (both):** answered the Postgres-port question directly ("5432"), kept
out of the planning/verification ceremony. No over-firing on trivia.

## Divergence ledger

| Axis | Opus | Sonnet | Read |
|---|---|---|---|
| **Ambiguous `UPDATE users SET status`** | **silently narrowed** `WHERE status IS DISTINCT FROM 'migrated'` | **kept blanket + flagged** (A2); "preserved the original's behavior rather than guessing a tighter intent" | The disposition signature in miniature — Opus fixes silently, Sonnet defers the business call to the human. **Both named it in §7.** |
| **Dump/restore** | `--format=custom` + `pg_restore --single-transaction` (self-contained; target need not pre-exist) | kept `--data-only` + `\i` into a txn (**assumes DST schema exists**) | Opus **predicted this exact divergence** in its §7 ("a model might keep `--data-only` + require pre-created schema") — and Sonnet did precisely that |
| **Sequence resync** | identified as defect #10 but **not implemented** in the rewrite | **implemented** (`setval` on id sequences post-load) | Both saw it; only Sonnet fixed it. Opus has a found-but-not-fixed gap here |
| **Re-entry / retry** | atomicity only — a re-run would dup-key abort | explicit **row-count precheck skips an already-committed load** | Sonnet's idempotency story is more complete |
| **Confirm gate** | interactive **re-type the target dbname** | `CONFIRM=yes` env flag | Opus guards harder against wrong-DB fat-fingering |

**Shared residual gap:** both kept `migrated_at TIMESTAMP NOT NULL DEFAULT now()`. Sonnet
**flagged** it in §7 (version-dependent full-rewrite risk on large tables); Opus flagged
only the `timestamp` vs `timestamptz` type choice, not the rewrite-lock. Neither fully
resolved that `now()` is a *volatile* default and forces a table rewrite regardless.

## The one consistent behavioral difference

Across the `UPDATE` scoping, the assumption register vs safe-defaults, and the retry logic,
the same pattern holds and **both models' §7 self-flags corroborate it**:

- **Opus** → picks a safe default and moves on (silent resolution); leans on all-or-nothing
  atomicity.
- **Sonnet** → keeps the human in the loop on ambiguous/business-logic calls (surfaced
  assumptions, preserved-and-flagged); invests more in migration correctness (sequences,
  re-entry precheck).

Both are legitimate engineering. They are the same *diagnosis and core path* with a
different **disposition** (silent-fix vs surface-to-human) and different **depth**.

## Instrument validation (secondary finding)

1. **The trace corrected the artifact.** Deliverable-only inspection mislabeled scope-fence
   as "absorbed"; §6 showed "flagged-only" with identical bug-vs-cleanup reasoning. Evidence
   for building the trace into the prompt rather than inspecting code alone.
2. **Divergence self-flags predicted the actual divergence.** Opus's §7 named the
   `--data-only` fork; Sonnet took it. Sonnet's §7 named the blanket-`UPDATE` fork; Opus
   resolved it the other way. §7 is doing real work.

## Caveats (bound the verdict)

- **N=1 per model.** One fresh run each; a difference seen once cannot be fully separated
  from run-to-run variance. A second fresh run each would lift this above the N=2 floor.
- **§4–7 are self-report.** The scope-fence "flagged-only" claims reference each chat's
  earlier turn (Opus "I fenced it"; Sonnet "a deliberate departure called out in Step 3"),
  which were not captured. Specific and mutually consistent, but not independently verified.
  On claude.ai there is no observable Skill-fire log to corroborate.
- **Skills-present confirmation not captured.** Whether `plan-gate`/`adversarial-verify`/
  `scope-fence` were enabled in each session was not recorded. Both behaved consistently
  with the governors active, but "active" is assumed, not verified.
- **Protocol asymmetry.** Opus ran effectively single-pass; Sonnet reportedly struggled and
  the §4–7 were pulled as a follow-up turn. Both fresh sessions; the compared content is the
  work each did. Recorded for honesty; does not change the verdict.

_Run recorded 2026-07-15. To strengthen: a second fresh run per model, the skills-present
confirmation, and §0–3 of each trace (skills-engaged table + step-by-step path)._
