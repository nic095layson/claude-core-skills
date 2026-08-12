# Hypothesis — "Verify at the source of truth" rule in adversarial-verify (2026-07-21)

**Pre-registered at adoption; the A/B is owed, not run.** Motivated by the
perspective-taking deck AAR (`results/2026-07-21/AAR-perspective-taking-deck.md`
§2.1): a claude.ai Opus session under the owner's governance stack spent five
successive pixel-analysis detectors (≈8–10 tool calls, the session's largest
reasoning block) inferring figure geometry from rendered PNGs — information the
session's own generator held exactly. Attempt 7 (instrument the generator to emit
bounding boxes) worked immediately and found all 5 real defects. The failure
class: *reverse-engineering your own output is a lossy proxy for facts you hold
upstream in exact form.*

This is a **body-doctrine** edit (a new rule with reason), not a description/
trigger edit. Landed per the No-silent-defaults precedent (2026-07-15): owner-
directed adoption, honest empirical status, revert unforced.

## The change (one variable)

Adding to `.claude/skills/adversarial-verify/SKILL.md` § "Rules, each with its
reason", after rule 5:

TO (exact):
> 6. **Verify at the source of truth** — when you built the thing being checked,
>    instrument the builder to report what it did rather than inferring it from its
>    output; reverse-engineering your own artifact is a lossy proxy for facts you
>    already hold exactly.

**will** cause a session that generated an artifact programmatically and needs to
verify a geometric/structural property to instrument the generator (or consult its
exact upstream data) **first**, instead of writing inference heuristics against the
rendered/serialized output.

## Pre-registered predictions (per case)

Arms: OLD (rules 1–5) vs NEW (rules 1–7, since rules 6 and 7 land together in the
tree, a clean single-variable run should test a 1–5+6 variant; noted as a protocol
cost of bundled adoption). Surface: Claude Code headless, fresh session per run,
N=2 per case per arm.

| # | Case | OLD prediction | NEW prediction (target) |
|---|---|---|---|
| evals id 10 (added this date) | Generator-placed figures; session is tuning a third pixel-threshold detector against rendered PNGs | Keeps tuning thresholds or writes detector #4 | Moves verification to the generator: emit placed geometry, check exactly |
| evals ids 1–8 | Fire/silent behavior per their existing expected_output | **Unchanged** (regression net) |
| ids 4–5 (should-not) | Silent | **Unchanged** — silent (over-fire guard) |

## Evidence bar (research-methodology R1–R3)

R1: N=2 floor per case per arm. R2: any regression on ids 1–8 blocks. R3: flaky
target = inconclusive, not accepted. Verbatim outputs, dated, OLD re-baselined
same-session.

## Status

**ADOPTED OWNER CANDIDATE 2026-07-21 — NOT A/B-VALIDATED; run owed.** The rule is
live in the tree with its status declared in the skill's Provenance. On a future
confirming run: promote, note in Provenance. On fail: revert rule 6, append a
DEAD entry to `.claude/LESSONS.md`.
