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

---

## OUTCOME — research-methodology A/B session, 2026-07-11

**Surface/model:** `claude -p` headless, `claude-opus-4-8[1m]`, clean scratchpad, same-condition.
OLD re-baselined in these conditions: should-fire **1/6 (17%)** (id1 0/2 [vs 2/2 Phase 1],
id2 0/2, id3 1/2), should-not 4/4 silent. (Cross-condition variance is real — id1, Phase 1's
strong firer, dropped to 0/2 here.)

**Both rewords improve dramatically but neither clears the ≥83% gate — DEAD END, escalated.**

- **NEW1** (surfaced APPEND trigger with qualitative hard-diagnosis markers — "finally
  figured it out / turned out to be / took all afternoon / kept failing until", not only a
  numeric hour count): N=3 → id1 2/3, id2 2/3, id3 3/3 = **7/9 (78%)**.
- **NEW2** (restructured to LEAD with the APPEND directive — the hypothesis noted CONSULT was
  burying it): N=3 gave 8/9 (89%), but a pre-committed N=5 escalation at the boundary gave
  id1 4/5, id2 3/5, id3 5/5 = **12/15 (80%)** — the 8/9 was small-sample optimism.

| | should-fire | should-not-silent |
|---|---|---|
| OLD (same-cond) | **1/6 (17%)** | 4/4 |
| NEW1 | **7/9 (78%)** | 4/4 |
| NEW2 | **12/15 (80%)** | 4/4 |

No should-not regression in either; both are large regression-free improvements (17%→80%),
but neither reaches ≥83%. **Failure mode:** residual run-to-run noise — the model often
responds conversationally or offers to log ("want me to jot a ledger entry?") *without*
invoking the Skill tool, even on clear costly-diagnosis recounts. 2 rewords used (budget
exhausted).

**Disposition:** personal copy REVERTED to OLD (neither cleared the gate). NEW2 documented as
an owner-adoptable regression-free improvement (17%→80%). Escalated as an architecture-contract
open question: description-based triggering appears to have a ~80% ceiling for the
append-on-diagnosis behavior (the model treats a finished debug story as conversation, not a
skill-load trigger). claude.ai upload UNCHANGED (OLD still current).
