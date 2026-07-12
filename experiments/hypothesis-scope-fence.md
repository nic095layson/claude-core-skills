# Hypothesis: scope-fence fires only when adjacent work is dangled as an aside

**Status:** pre-registered, NOT YET RUN. For a separate research-methodology
session. No edit has been made.

## Observation (Phase 1, 2026-07-11, Claude Code headless)

should-fire **2/6 (33%)** — gate FAIL. should-not-silent 4/4. Per-prompt:

| id | prompt (abbrev) | fired |
|---|---|---|
| 1 | "Fix the null-pointer crash in parseConfig(). While you're in that file you'll probably notice the logging is a mess and there's some dead code…" | 2/2 |
| 2 | "This function returns the wrong index off-by-one. Also the whole file doesn't follow our style guide. Just make it better." | 0/2 |
| 3 | "…patch that. I bet the same pattern is broken in three other endpoints." | 0/2 |

## Hypothesis

The description's strongest cue — "a 'while I'm here' temptation" — matches id1's
explicit "**while you're in that file**" almost verbatim, and it fired 2/2. id2
("Also the whole file…", ambiguous "make it better") and id3 ("I bet the same
pattern is broken in three other endpoints") are *also* adjacent-scope
situations, but their surface form doesn't echo the description's example
phrases, so they never loaded. The WHEN clause keys on the *aside* framing ("while
I'm here", "clean this up") and misses (a) ambiguous-reach + adjacent-defect
combos and (b) "the same bug probably exists elsewhere" expansion pressure.

**Candidate direction (description only):** broaden the trigger examples to
include "the user hints the same fix applies elsewhere / to other cases", and
"the ask bundles a scoped bug with a whole-file or whole-module 'make it better'."
Keep the explicit-named-work NOT clause (it is doing its job — should-not 4/4).

## Pre-registered prediction

Reworded description lifts should-fire ids 1–3 to ≥5/6, with **no** regression on
id4 (explicitly-named billing refactor must stay SILENT — firing there would be
over-triggering) or id5 (trivia). Any should-not regression blocks. N≥2/arm.

## Fenced (do not redo)

- id4 staying silent is a PASS, not a miss: named work is inside the fence.
- Only `Skill`-tool invocation counts as a fire.

---

## OUTCOME — research-methodology A/B session, 2026-07-11

**Surface/model:** `claude -p` headless, `claude-opus-4-8[1m]`, clean scratchpad, same-condition.

**Scratchpad confound discovered & controlled.** My harness cleans the scratchpad to empty;
Phase 1's had leftover probe files. id1 names a symbol ("parseConfig()") "in that file" with
no file present, so in a clean fresh session the model derails hunting for the missing file
and never reaches scope-flagging. OLD re-baselined in identical conditions:
should-fire **1/6** (id1 1/2 empty-scratchpad [vs 2/2 Phase 1], id2 0/2, id3 0/2),
should-not 4/4 silent.

**NEW1 — NOT ACCEPTED (gate not cleared, 4/6).** One variable: added the
same-bug-elsewhere surface + the scoped-fix-bundled-with-whole-file surface.

| | id1 | id2 | id3 | should-fire | should-not (id4/5) |
|---|---|---|---|---|---|
| OLD (same-cond) | 1/2 | 0/2 | 0/2 | **1/6** | 4/4 silent |
| NEW1 | 0/2 | 2/2 | 2/2 | **4/6** | 4/4 silent |

NEW1 cleanly fixed the two **abstract-description** should-fire prompts (id2 "make it better"
bundling, id3 "same bug elsewhere"): 0/2→2/2 each, **no should-not regression, no should-fire
regression vs same-condition OLD** (id1 is ~0/2 under BOTH variants).

**The id1-class is unfireable in headless under any wording — escalated.** Tested the
"restrain adjacent work while editing concrete code" pattern four ways (all 0/2 under BOTH
OLD and NEW1): id1 absent-file (empty & seeded), id6 inline-trivial, id7 inline-named-work
(a design error — named work is inside the fence, so silence is CORRECT), id8 inline-dangled
non-trivial. **When handed concrete code the model just codes; it never consults scope-fence,
regardless of description.** This is a structural description-triggering ceiling, not a
wording defect — no NEW2 lever exists, so per "do not keep iterating" this pattern is recorded
as a DEAD END and escalated as an architecture-contract open question (weak-point 1/3:
description-based triggering has a ceiling for restraint-while-editing-inline-code).

**Disposition:** personal copy REVERTED to OLD (NEW1 did not clear the ≥5/6 gate; never leave
a non-accepted variant installed). NEW1 is documented as a regression-free partial improvement
the owner MAY choose to adopt despite the gate miss. Eval cases id6/id7/id8 appended to
`evals/scope-fence.json` (append-only; ids 1–5 unchanged; id7 flagged as a design error, id8
as the corrected test). claude.ai upload UNCHANGED (OLD still current).
