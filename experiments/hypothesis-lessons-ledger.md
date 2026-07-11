# Hypothesis: lessons-ledger fires on "burned two hours" but not on quieter diagnosis phrasings

**Status:** pre-registered, NOT YET RUN. For a separate research-methodology
session. No edit has been made.

## Observation (Phase 1, 2026-07-11, Claude Code headless)

should-fire **2/6 (33%)** — gate FAIL. should-not-silent 4/4. Per-prompt:

| id | prompt (abbrev) | fired |
|---|---|---|
| 1 | "We just **burned two hours** chasing a bug — staging config had DEBUG=true, silently swallowed all errors. Fixed now, moving on." | 2/2 |
| 2 | "Finally cracked it: the deploy kept failing because the Dockerfile was caching a stale lockfile. Clearing the cache fixed it. Anyway, done." | 0/2 |
| 3 | "That intermittent CI test failure took me all afternoon — race condition in the fixture setup. Fixed with a lock." | 0/2 |

## Hypothesis

id1 fired 2/2 — it names an explicit **duration cost** ("burned two hours") that
maps directly onto the description's recording rule ("a diagnosis cost real
time"). id2 ("Finally cracked it… Anyway, done") and id3 ("took me all
afternoon") are the *same class* of costly diagnosis, but the model didn't map
"all afternoon" / "finally cracked it after a failing deploy" to the ledger's
append trigger. The description leads with CONSULT framing ("was this tried?",
"has this doc lied before?") and buries the APPEND trigger; the append cue may be
too tied to an explicit numeric time cost.

**Candidate direction (description only):** surface the APPEND trigger earlier and
make it fire on qualitative markers of a hard-won diagnosis ("finally figured
out", "turned out to be", "took all day", "kept failing until"), not only an
explicit hour count. Keep the do-not-record-successes NOT clause (should-not 4/4).

## Pre-registered prediction

Reworded description lifts should-fire ids 1–3 to ≥5/6, no regression on id4
("build passed first try" — routine success, must stay SILENT) or id5 (bash
trivia). Any should-not regression blocks. N≥2/arm.

## Fenced (do not redo)

- id4 SILENT is a PASS: recording a routine success would be the padded-ledger
  failure the skill warns against.
- Only `Skill`-tool invocation counts.
