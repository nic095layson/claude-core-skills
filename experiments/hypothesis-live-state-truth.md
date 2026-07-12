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

---

## OUTCOME — research-methodology A/B session, 2026-07-11

**Surface/model:** `claude -p` headless, `claude-opus-4-8[1m]`, clean scratchpad, N=3.
OLD re-baselined in these conditions **exactly reproduced Phase 1**: should-fire **6/9
(67%)** (id1 0/3, id2 3/3, id3 3/3), should-not 6/6 silent. (No scratchpad confound here —
these prompts reference external prod systems, not absent local files.)

**NEW1 — ACCEPTED.** One variable (description only): added the live-confirmation trigger
surface alongside "is X set up?" — "OR any request to confirm/verify something about the
running environment right now — confirm the service is up and reachable / check we're
really on version Y / is it actually running at the moment? — where the honest answer
requires probing the live system, not reading a doc".

| | id1 | id2 | id3 | should-fire | should-not-silent (id4/5) |
|---|---|---|---|---|---|
| OLD | 0/3 | 3/3 | 3/3 | **6/9 (67%)** | 6/6 |
| NEW1 | 3/3 | 3/3 | 3/3 | **9/9 (100%)** | 6/6 |

id1 (the sole 0/3 — "confirm the service is up and reachable right now") lifted to 3/3;
no regression on id2/id3 or on the concept-question NOT clause (id4 TCP/UDP, id5 foreign-key
stayed 3/3 silent). Gate ≥8/9 cleared. Landed to repo + personal (byte-identical).
claude.ai upload now STALE — needs re-upload by owner.
