# Hypothesis: adversarial-verify's 0/6 is a prompt-design confound, not (only) a description defect

**Status:** pre-registered, NOT YET RUN. For a separate research-methodology
session. No edit has been made. **This hypothesis must be tested BEFORE any
description edit** — the current evidence cannot yet blame the description.

## Observation (Phase 1, 2026-07-11, Claude Code headless)

should-fire **0/6 (0%)** — gate FAIL. should-not-silent 4/4. Per-prompt: id1 0/2,
id2 0/2, id3 0/2.

## The confound

All three should-fire prompts imply an artifact that is **absent** in the fresh
scratchpad:

- id1 "I've finished writing this data-export function … **here it is**" — no
  function was included.
- id2 "**Here's my SQL migration** …" — no SQL present.
- id3 "I wrote a script that dedupes … it worked on my one test file" — no script.

Inspection of id2 r1: the model ran `Bash` three times hunting for the file, then
said "**there's no SQL migration here to check … I don't want to invent a review
of something I can't see**" — behaviorally *aligned* with adversarial-verify's
honest-reporting law, but it never loaded the skill because there was nothing to
verify. The prompts under-power the test.

## Two hypotheses to separate (order matters)

**H1 (prompt design, test first):** with the artifact embedded inline in the
prompt, the same descriptions fire. If H1 holds, the eval prompts were the
problem, not the description — fix the eval set (post-registration, as a new
pre-registered set) and re-measure.

**H2 (description defect, only if H1 fails):** even with an inline artifact +
"confirm it's correct / ready to ship / double-check before prod", the
description does not load. Then the WHEN clause ("BEFORE delivering any
non-trivial product… whenever you are about to write 'done', 'fixed',
'verified'") may key on *the assistant's own* about-to-ship moment rather than a
*user handing over work to be checked*. Candidate direction: add the
user-facing trigger surface ("the user asks you to confirm / double-check /
sign off on something they made").

## Pre-registered prediction

Run H1 first: 3 new should-fire prompts identical in intent but with the artifact
inline, N≥2/arm. Predict ≥5/6 fire. If ≥5/6 → the description is fine; replace the
eval prompts. If <5/6 → proceed to H2 rewording A/B, ≥5/6 target, no should-not
regression (id4 rsync trivia, id5 haiku must stay SILENT).

## Fenced (do not redo)

- Do NOT conclude "adversarial-verify's description is broken" from the 0/6 — it
  is confounded and that conclusion is not yet earned.
- Only `Skill`-tool invocation counts as a fire; the honest "I won't fake a
  review" behavior is not a load.
