# Hypothesis: plan-gate under-fires on multi-step build/refactor phrasings

**Status:** pre-registered, NOT YET RUN. For a separate research-methodology
session. No edit has been made.

## Observation (Phase 1, 2026-07-11, Claude Code headless)

should-fire **1/6 (17%)** — gate FAIL. Per-prompt:

| id | prompt (abbrev) | fired |
|---|---|---|
| 1 | "build a migration script … move users and orders tables to a new database" | 1/2 |
| 2 | "refactor our authentication module to use JWTs … across the whole app. Where should we start?" | 0/2 |
| 3 | "Set up a CI/CD pipeline for our monorepo … deploys to staging on every merge" | 0/2 |

Silent runs produced plan-gate-*shaped* caution (dir check, FK assumption,
clarifying questions) **without loading the skill** — the base model plans a
little on its own but does not invoke the governor.

## Hypothesis

The description's WHEN list — "multi-step, touches state you did not create, has
unknowns that would change the approach, or would be costly to redo — including
'build X', 'fix Y', 'migrate Z', 'figure out why…', refactors, integrations" —
is **abstract**. The migration phrasing (id1) contains the literal cue "migrate"
and fired once; the refactor (id2) and CI/CD-integration (id3) phrasings match
only the *abstract* categories ("refactors, integrations") and never fired. The
model does not connect a concrete "refactor auth to JWT" or "set up a pipeline"
to the abstract word "refactors/integrations" strongly enough to load.

**Candidate direction (one variable = the description only):** make the WHEN
trigger on *concrete request surfaces*, not category nouns — e.g. add examples
phrased as tasks a user actually types ("set up / configure / wire up X",
"rewrite / migrate / convert Y to Z", "stand up a pipeline/service"). Keep the
NOT clause and body unchanged.

## Pre-registered prediction (to test in a research-methodology A/B)

Reworded description lifts should-fire on ids 1–3 to ≥5/6 across fresh sessions,
with **no** regression on the should-not near-misses (id4 "15% of 80", id5
one-line rename must stay 0/fire). Any should-not regression blocks the change
(R2 any-regression-blocks). N≥2 fresh runs/prompt, both arms.

## Fenced (do not redo)

- Do not grade by asking a session "would you have loaded plan-gate?" —
  introspection, fenced. Only fresh-session `Skill`-tool invocation counts.
- Do not treat the organic caution as a fire — it is base-model behavior, not the
  governor loading.

---

## OUTCOME — research-methodology A/B session, 2026-07-11

**Surface/model:** `claude -p` headless, `claude-opus-4-8[1m]`, clean scratchpad, same-condition.
OLD re-baselined in these conditions: should-fire **0/6** (id1 0/2, id2 0/2, id3 0/2),
should-not 4/4 silent.

**NEW1 (attempt 1) — FELL SHORT.** Replaced abstract category nouns ("refactors,
integrations") with concrete task surfaces ("build/set up/configure/wire up X",
"refactor/rewrite/migrate/convert Y to Z", "stand up a pipeline / set up CI/CD").
Result at N=3: id1 **1/3**, id2 **3/3**, id3 **3/3** = **7/9 (78%)** — fixed the two
targeted prompts (id2, id3) but id1 (data-migration script) stayed a coin flip; below the
≥83% gate.

**NEW2 (attempt 2) — ACCEPTED.** Kept NEW1's surfaces and added an anti-"just write the
script" clause (writing/running a migration, or moving data/tables between DBs, gates even
when it seems small — it touches real data). Result at N=3:

| | id1 | id2 | id3 | should-fire | should-not-silent |
|---|---|---|---|---|---|
| OLD | 0/2 | 0/2 | 0/2 | **0/6** | 4/4 |
| NEW2 | 3/3 | 3/3 | 3/3 | **9/9 (100%)** | 4/4 |

Gate ≥5/6 cleared (9/9); no should-not regression. Landed to repo + personal (byte-identical).
2 rewords used (budget). claude.ai upload now STALE — needs re-upload by owner.

**Length-compliance follow-up (2026-07-11):** description trimmed to 1000 chars; ACCEPTED trim holds gate 9/9. Now ≤1024 (was over). Full A/B: `experiments/hypothesis-2026-07-11-length-compliance.md`.
