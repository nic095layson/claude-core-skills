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

---

## OUTCOME — research-methodology A/B session, 2026-07-11

**Surface/model:** `claude -p` headless, `claude-opus-4-8[1m]`, personal-scope install,
fresh session per run, clean scratchpad. Same as Phase 1.

**H1 (prompt-design confound) — REFUTED.** Appended inline-artifact should-fire cases
(ids 6/7/8: the data-export fn, SQL migration, dedupe script embedded IN the prompt).
Ran **OLD** against them: **0/6** — the description does NOT load even when there IS an
artifact to verify. Every run the base model reviewed the code well (found CSV-escaping,
lock/rewrite, null-crash bugs) *without loading the skill*. So the Phase-1 0/6 was not
merely the missing-artifact confound; the description genuinely under-fired.

**H2 (description defect) — CONFIRMED and FIXED. ACCEPTED (NEW1).** One variable
(description only): added the user-handoff trigger surface — "Load it ALSO when the user
hands you something they made and asks you to check it — confirm it's correct /
double-check before prod / is this right? / ready to ship? / sound right?". Result:

| | should-fire (id6/7/8) | should-not-silent (id4/5) |
|---|---|---|
| OLD | **0/6** | 4/4 |
| NEW1 | **6/6** (2/2 each) | 4/4 (2/2 each) |

Gate ≥5/6 cleared; no should-not regression. Landed to repo + personal (byte-identical).
Eval cases 6/7/8 appended to `evals/adversarial-verify.json` (append-only; ids 1–5 unchanged).
claude.ai upload now STALE — needs re-upload by owner.

**Length-compliance follow-up (2026-07-11):** description trimmed to 969 chars; ACCEPTED trim holds gate 6/6. Now ≤1024 (was over). Full A/B: `experiments/hypothesis-2026-07-11-length-compliance.md`.
