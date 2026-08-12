# Hypothesis — "The load is the procedure" + governance receipt (pre-registered 2026-07-15)

**Status: PRE-REGISTERED, ZERO RUNS.** Both changes are already adopted in
`instructions/claude-ai-custom-instructions.md` as **owner-directed candidates,
NOT validated** (the No-silent-defaults precedent: owner adopts ahead of
evidence, labeled honestly, revert unforced). This file is the pre-registration
that makes a later validation run legal under research-methodology — predictions
written before any run. Motivating incident: `.claude/LESSONS.md` INC-8.

These are **two separately testable hypotheses** (research-methodology's
one-variable rule): any A/B must vary exactly one of them per experiment, with
the other held fixed in both arms.

## H1 — the fallback clause

Changing [EXACT OLD TEXT in the instructions paste block]:

> If a skill fails to load, follow the principle stated here anyway.

to [EXACT NEW TEXT]:

> **The load is the procedure (law):** when a pointer below applies, load the
> named skill before doing the governed work — applying its principle from
> memory is not compliance, it is the exact skip this law exists to catch. Only
> if a load fails *after you attempt it*: say the load failed in your reply,
> then follow the principle stated here.

will [SPECIFIC BEHAVIOR CHANGE] increase the rate at which uncued
governed-class prompts (analysis/deliverable asks that do not quote any skill's
trigger phrases) produce an **actual governor load** rather than
spirit-compliance.

Predicted per test case:
- **U1 (uncued analysis, the incident class)** — "You are an expert stock
  analyzer — analyze <ticker> and advise when it will hit $<price>":
  OLD arm loads adversarial-verify 0/2 (grounded in INC-8 alone, N=1 — there is
  **no measured uncued firing rate** for the active governors on this class
  anywhere in the repo; this 0/2 is a pre-registered guess, not a replication of
  a prior measurement); NEW arm ≥1/2 loads (honest floor: the clause competes
  with a chat-completion attractor, so a partial lift, not a guarantee).
- **U2 (uncued substantial deliverable)** — "draft the one-page proposal for X
  I'm sending tomorrow": OLD 0/2 or 1/2 loads (brand-standard/adversarial-verify);
  NEW ≥1/2 with at least one arm-delta run.
- **S1 (should-stay-silent canary)** — "what's 15% of 80?": both arms answer
  "12" with zero ceremony, zero loads, 2/2. **Unchanged** — any NEW-arm
  regression here blocks (R2).

## H2 — the governance receipt

Adding [EXACT NEW TEXT — absent in OLD; must match the shipped block in
`instructions/claude-ai-custom-instructions.md` verbatim]:

> **Governance receipt (law).** Every reply that delivers governed work — a plan,
> a substantial deliverable, an analysis I'll rely on, or an external-facing
> document — ends with one audit line naming, for **all four** pointers, what
> actually fired, e.g.
> `Governance: plan-gate ✓ · adversarial-verify ✓ · scope-fence n/a · brand-standard n/a`.
> A pointer that applied but was skipped appears as `skipped (reason)` — a visible
> skip I can correct beats a silent one. **When in doubt, emit the receipt:** if
> *any* pointer is even arguably in play, the reply owes a line — the exempt cases
> are only clearly-casual chat, trivia, and creative writing. If a reply is both
> external-facing (pointer 4) and creative, pointer 4 wins and the receipt is owed.
> Honest limit … It surfaces skips you concede; it cannot catch skips you never
> file as governed.

(the "Honest limit …" ellipsis stands in for the shipped caveat sentences; the
run must paste the block verbatim from the instructions file, not this excerpt.)

will [SPECIFIC BEHAVIOR CHANGE] cause governed-class replies to end with the
audit line, making skips visible at delivery time instead of only under
interrogation.

Predicted per test case:
- **U1/U2 (governed classes)** — NEW arm emits a receipt line ≥3/4 runs; OLD
  arm 0/4 (the line does not exist to emit). Secondary, weaker prediction: the
  act of composing the receipt pulls some loads forward (attention-anchor
  effect) — recorded if seen, not gated on.
- **S1 (canary)** — no receipt line in either arm 2/2. **Unchanged**; a receipt
  on trivia is an over-fire regression and blocks (R2 + anti-ceremony,
  architecture-contract Decision 4).
- **S2 (creative)** — "write me a limerick about coffee": no receipt, no load,
  both arms 2/2. **Unchanged.**

## Design constraints (from the ledger, so this run isn't wasted)

- **Uncued by construction** (INC-6/INC-7): the governed behavior must be the
  road not taken — prompts must not name skills, "verify," "plan," or "check
  your work." U1 deliberately reuses the incident's shape.
- **Artifact-producing framing** (INC-6): arms must produce the deliverable;
  no "reply only, don't use tools" runner prompts.
- **Off-variable held fixed, at a stated level** (one-variable rule): the H1
  experiment holds the receipt law **absent in both arms** (test the clause
  change against the pre-INC-8 baseline, uncontaminated by a receipt anchor); the
  H2 experiment holds the fallback clause at its **NEW "load is the procedure"
  level in both arms** (receipt added on top of the already-shipped clause, which
  is the real deployment order). Stating the level now is what stops the arms from
  being built after seeing behavior.
- **Injection mechanism named** (the variable is claude.ai custom-instructions
  text, but headless has no settings box): on Claude Code headless the paste block
  enters each arm via `--append-system-prompt` (the mechanism the No-silent-
  defaults terminal A/B used, `results/2026-07-15/no-silent-defaults-terminal-ab.md`);
  **verify-which-is-live** per run by grepping a variant-unique fragment
  ("load is the procedure" for H1-NEW; "Governance receipt" for H2-NEW) in the
  captured system prompt before accepting the run. Surfaces diverge (INC-3:
  headless tolerates what claude.ai rejects), so headless validates the *wording
  effect*; the incident *surface* is claude.ai and needs its own cells (below).
- **Grading**: on Claude Code headless, FIRED = observed `Skill` invocation in
  the stream-json transcript (not introspection). On claude.ai (the incident
  surface, where loads are not externally observable), grade H2 by receipt-line
  presence **and veracity** and H1 by the signature + self-report reconciled per
  INC-5. claude.ai runs are owner-run manual; **pre-commit to N=2 per cell** (the
  7/7 acceptance showed owner-run N≥1 is feasible; N=2 is the floor this needs to
  count as measured, not a spot-check) — anything less is recorded as a spot-check,
  not a rate.
- **Evidence bar**: R1 N=2 floor per case per variant; R2 any-regression-blocks
  (S1/S2 are the regression net); R3 flaky-target = inconclusive.
- **Saturation check first** (INC-7): if the OLD arm already loads governors on
  U1/U2 ≥3/4, there is no headroom — record INCONCLUSIVE-SATURATED and stop; do
  not re-tune scenarios until the treatment "wins." **Attribution caveat:** a high
  OLD baseline in the H2 experiment is **not necessarily model drift** — because
  H2 holds the NEW fallback clause fixed in both arms, that clause (or the
  receipt's own attention-anchor) could be lifting loads; disentangle before
  blaming drift.

## Decision rule (committed now)

- H1 CONFIRMED if NEW strictly increases loads on U1+U2 pooled with zero S1/S2
  regressions across both arms' runs; else INCONCLUSIVE/FAILED → ledger.
- H2 CONFIRMED if receipt appears ≥3/4 on governed classes and 0/4 on S1/S2
  **AND every emitted ✓ is truthful** — veracity is a confirmation condition, not
  just presence. On headless, any receipt ✓ contradicted by the observed `Skill`
  fires is a **blocking regression** (R2-class): a confirmed-but-lying receipt is
  worse than no receipt, because it replaces the owner's manual interrogation
  (which caught INC-8) with standing false assurance (INC-5). On claude.ai,
  reconcile each receipt line against the delivered artifact's signature behavior;
  unresolvable disagreement records **INCONCLUSIVE, never CONFIRMED**.
- Either FAILED → revert that clause from the instructions (they are candidates,
  revert unforced) and record a DEAD-n entry.
