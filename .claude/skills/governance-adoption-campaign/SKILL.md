---
name: governance-adoption-campaign
description: >-
  The decision-gated campaign plan for this library's hardest live problem: the
  governors exist and lint clean, but NOTHING yet proves they trigger when they
  should, stay silent when they shouldn't, and change session behavior — across
  surfaces. Load when asked to "prove the governors work", "run the trigger
  evals", "measure the skills", "roll the library out", "is plan-gate actually
  firing?", or when planning any investment in this library's reliability. Do NOT
  load for a single wording experiment (research-methodology is the method; this
  is the campaign that sequences it), for install mechanics (install-and-surfaces),
  or for fixing an individual misfire (debugging-playbook).
---

# Governance-Adoption Campaign

**The problem, stated honestly (as of 2026-07-11):** this library was authored,
linted, and lineage-checked in one session — but assumption A2 (descriptions
trigger reliably) and A1 (the five-way decomposition matches real use) are
unconfirmed, and weak-point 3 (enforcement is voluntary) means the only lever is
trigger quality. Until this campaign closes, "Claude is governed by these skills"
is a **candidate**, not a fact.

Work the phases in order; each ends at a gate with an expected observation and a
branch rule. Do not skip gates — a campaign that skips its gates is the
ungoverned behavior this library exists to prevent.

## Phase 0 — Install and registration (prerequisite)

**Do:** Runbook 1 of install-and-surfaces (five governors, personal scope) on the
primary machine.
**Gate:** a fresh session outside this repo lists all five governors.
**Expect:** 5/5 listed. **If fewer:** debugging-playbook §1 (placement class);
do not proceed — every later phase measures a skill that must first exist.
**Status: OPEN as of authoring (2026-07-11).** The files-in-place half may
already be done — `ls ~/.claude/skills/` is the source of truth, and the
fresh-session listing is the half that counts.

## Phase 1 — Trigger evals (the A2 test)

**Do:** for each governor, write 3 should-fire prompts (realistic task phrasings,
NOT the skill's name — "help me build a migration script for X" must fire
plan-gate without the words "plan gate") and 2 should-not-fire near-misses
(trivia; adjacent-governor cases). 25 prompts total. Run each in a fresh session,
2 runs per prompt (R1 floor), record fired/silent.

**Gate:** per governor, ≥5/6 should-fire runs fire; ≥3/4 should-not runs stay
silent.
**Expect:** pass. **If a governor under-fires:** its description's WHEN is too
narrow or too abstract — description edit via research-methodology (one variable:
the description). **If it over-fires:** the NOT clause is weak — same route.
**If two governors co-fire constantly:** boundary defect — architecture-contract
weak-point 4, consider merging, but only with the owner.

## Phase 2 — Behavioral evals (does firing change anything?)

A governor that loads but doesn't alter behavior is decoration. For each
governor, one paired A/B (with-library vs without, same prompt, fresh sessions,
2 runs each): does plan-gate produce the gate block before action? Does
adversarial-verify produce criteria-graded delivery? Does scope-fence flag the
planted adjacent bug instead of fixing it? Does lessons-ledger append on a
planted >15-min diagnosis? Does live-state-truth check live state instead of
trusting the planted stale doc?

**Gate:** each governor shows its signature behavior in ≥3/4 with-library runs
and its absence is visible in without-library runs.
**Expect:** pass with visible deltas. **If a governor shows no delta:** body
defect, not trigger defect — the procedure isn't actionable enough; rewrite via
research-methodology. **If without-library runs ALSO show the behavior:** the
base model already does it; record the finding (ledger) and consider whether the
governor earns its context cost — take the answer to architecture-contract.

## Phase 3 — Ongoing measurement and ratchet

**Do:** save all Phase 1–2 prompts and criteria as the library's standing eval
set (in `evals/` at this repo's root, one JSON per governor: id, prompt,
expected_output, files[] — the schema inherited from the source repo). Every
behavioral edit thereafter runs before/after against them
(research-methodology). Raise N beyond 2 as tooling makes runs cheaper.
**Gate:** the eval set exists in-tree and the first gated edit has used it.
**Exit criteria for the whole campaign:** A1 and A2 in domain-reference's
register flip to verified-with-date; architecture-contract weak-points 1 and 4
close.

## Ranked solution menu (if resources are constrained)

1. **Phase 1 alone** — cheapest, kills the biggest risk (silent non-triggering,
   the founding-incident class). Do this even if nothing else happens.
2. Phases 1+2 on the two governors the owner leans on most (plan-gate,
   adversarial-verify), defer the rest.
3. The full campaign.

## Wrong paths, fenced off

- **Baking the governors into a CLAUDE.md blob "so they always apply".** Always-
  in-context prose has no triage valve — it applies to trivia too (invariant 5),
  costs context on every turn, and cannot be measured per-behavior. Rejected at
  design time (architecture-contract, Decision 1's rejected alternative).
- **Testing triggers by asking a session "would you have loaded plan-gate for
  this?"** Introspection is not observation; only fresh-session live fires count
  (validation doctrine inherited from the source repo).
- **Polishing descriptions before the eval prompts exist.** Editing toward prose
  you like, with no way to tell whether it helped — the exact rot this library's
  methodology exists to prevent (skill-authoring step 5).

## When NOT to use this skill

- One wording experiment → **research-methodology** (this campaign sequences
  many of them).
- Install steps themselves → **install-and-surfaces**.
- A specific observed misfire today → **debugging-playbook** §3/§8.
- Whether a campaign finding justifies redesign → **architecture-contract**.

## Provenance and maintenance

Authored 2026-07-11, generalizing the campaign form of `nic095layson/claude`
(commit `df6e198`) `eval-harness-campaign` (decision-gated phases, expected
observations with branch rules, ranked menu, fenced wrong paths) to this
library's hardest problem — which is adoption/triggering, not harness mechanics.
The eval schema in Phase 3 is that repo's, verified there 2026-07-10.

Re-verify: Phase 0 status — `ls ~/.claude/skills/` (expect the five governors);
campaign progress — `ls evals/` at this repo root (absence = Phase 3 not
started). Update when: any phase's gate is passed or failed (record the result
and date in-place), or a register row it targets flips status.
