# Hypothesis: `red-team` fires on model-attack requests and stays silent on deliverable-grading ones

**Status:** pre-registered, NOT YET RUN. Authored 2026-10-19 with the skill; no
trigger eval has been run on any surface. The skill is a **candidate**: not in the
install footprint, not always-on.

## Origin

`nic095layson/fantasy-basketball-2026-27`, after-report 2026-10-19 (draft
post-mortem): an engine audited for three months against its specification quoted
a title share as ±0.4 where a hand-set simulator constant moved it by +3.4 / −2.3.
The owner asked for a red-team check "with every task where applicable … in
fantasy basketball and my Claude operations as a whole". PR 1 built the standing
implementation in that kit (`scripts/redteam/`); this skill is PR 2, the general
form.

## Pre-registered prediction

On `evals/red-team.json` (6 prompts: ids 1, 2, 3, 6 should-fire; ids 4, 5
should-not), N≥2 per prompt on Claude Code headless: should-fire ≥5/6 of the
runs on ids 1–3 (the committed gate); should-not 4/4 silent on ids 4–5. The
NOT clause names adversarial-verify and live-state-truth by situation, so id 4
(deliverable grading) and id 5 (doc vs live state) are the over-fire risks; either
firing is a FAIL of this hypothesis and a description edit, not a body edit.

## Fenced (do not redo)

- The body is not the trigger surface; a trigger miss is fixed in `description:`
  only, under research-methodology (N=2 floor, pre-registered).
- The kit's tier thresholds (1 / 2 points) are not part of the skill's law; a
  project sets its own and states them before the sweep.
