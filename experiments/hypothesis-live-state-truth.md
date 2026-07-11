# Hypothesis: live-state-truth fires on "is X set up / are we actually on Y" but not on "confirm the service is up"

**Status:** pre-registered, NOT YET RUN. For a separate research-methodology
session. No edit has been made.

## Observation (Phase 1, 2026-07-11, Claude Code headless; escalated to 3 runs)

should-fire **6/9 (67%)** — gate FAIL (needs ≥8/9 for ≥83%). should-not-silent
6/6. Best-performing governor, but still under the bar. Per-prompt:

| id | prompt (abbrev) | fired |
|---|---|---|
| 1 | "Our README says the API listens on port 8080. Can you **confirm the service is actually up and reachable** right now?" | 0/3 |
| 2 | "**Is Redis set up correctly** in our production environment at the moment?" | 3/3 |
| 3 | "The docs claim we're running Postgres 14. **Are we actually on 14 in prod?**" | 3/3 |

## Hypothesis

The description's literal cues — "before answering **'is X set up?'**", "whenever
docs and observed behavior disagree", "whether a service is up" — map cleanly onto
id2 ("is Redis set up correctly") and id3 (docs-vs-reality), which fired 3/3 each.
id1 asks to "**confirm the service is up and reachable**" — semantically identical
to "whether a service is up" in the description, yet it fired 0/3. The likely
difference: id1 reads as a **connectivity/ops check** ("reachable right now") that
the model treats as a straightforward task to just attempt, rather than a
doc-vs-live truth claim; the description's "never assert from documentation" frame
didn't engage because the user isn't asserting — they're asking to test.

**Candidate direction (description only):** add the "confirm / verify that
<something the environment does> right now" surface to the WHEN list, alongside
"is X set up?", so live-reachability/confirmation requests trigger the same
live-check discipline. Keep the concept-question NOT clause (should-not 6/6).

## Pre-registered prediction

Reworded description lifts id1 to ≥2/3 (bringing the governor to ≥8/9 overall),
with no regression on id2/id3 (must stay ≥3/3-class) and no regression on id4
(TCP/UDP concept) or id5 (foreign-key concept) — both must stay SILENT. Any
should-not regression blocks. N≥3/prompt given the tight margin.

## Fenced (do not redo)

- This is the closest governor to passing; it is still a FAIL at 6/9 and must be
  recorded as 67%, never rounded to "fires reliably."
- Only `Skill`-tool invocation counts as a fire.
