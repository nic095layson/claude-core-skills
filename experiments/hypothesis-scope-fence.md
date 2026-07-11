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
