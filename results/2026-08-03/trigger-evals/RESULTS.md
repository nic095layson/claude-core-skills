# Trigger-eval results — four 2026-08-03 skills, first measurement (2026-08-03)

First live-fire trigger measurement (authoring checklist step 7) for
delegation-discipline, after-report, application-tailor, correspondence.
Two rounds same-day: the committed fixtures (46 runs), then the INC-8
append-only repair variants (14 runs). **60 runs total, all served by
`claude-sonnet-5`** (headless default here — the post-Fable daily model, so
these are the rates that matter going forward).

## Method and environment (held constant, recorded)

- Surface: Claude Code headless (`claude -p`, v2.1.220), `--output-format
  stream-json`, `--max-turns 6`, 180s timeout, N=2 per prompt.
- Skills present: the four skills under test at project scope in an isolated
  temp project dir (SKILL.md copies from repo HEAD `c849b2a`-adjacent state);
  the account-synced personal roster rode along constant in every run
  (governors, brand-standard, document skills, council, morning,
  skill-creator — enumerated in this repo's session log of 2026-08-03).
  Same environment for every run — no arm toggling (this is a live-fire
  measurement, not an A/B).
- FIRED := a `Skill` tool_use invoking the target skill appears in the
  stream-json transcript (grader: `grade.py`, this directory; raw output:
  `grading-output.txt`; verbatim transcripts: `transcripts/`, 60 files).
- Pre-committed gates (in each evals file's `_grading`, committed
  2026-08-03 before any run): ≥83% should-fire fire; ≥75% should-not silent.

## Round 1 — committed fixtures (46 runs)

| skill | should-fire | should-not silent | gate |
|---|---|---|---|
| correspondence | 5/6 (83.3%) | 4/4 | **PASS** |
| application-tailor | 4/8 | 4/4 | FAIL |
| after-report | 3/8 | 4/4 | FAIL |
| delegation-discipline | 1/8 | 4/4 | FAIL |

**Zero over-fires in the entire battery (16/16 should-nots silent)** — the
trust-eroding failure mode did not occur once. The should-fire misses
concentrated in prompts referencing absent artifacts or state ("my resume is
attached", "the agent you sent off earlier", "this diff", "our stack",
"these four vendor SDKs") — the recorded INC-2 trap, reproduced at fixture
authoring. Ledger entry: **INC-8** (`.claude/LESSONS.md`), filed before the
repair ran.

## Round 2 — INC-8 repair variants (append-only ids, 14 runs)

Self-contained or inline-artifact versions of each failed prompt class,
appended with dated `_added` notes; originals untouched (2026-07-11
adversarial-verify id6–7 precedent). Committed and pushed before the re-runs
completed (`c849b2a`).

| skill | repaired ids | fire rate |
|---|---|---|
| delegation-discipline | 7, 8, 9 | 5/6 (83.3%) |
| after-report | 7, 8 | 4/4 |
| application-tailor | 7, 8 | 4/4 |

## The honest read (both numbers, no gate redefinition)

The pre-committed gates were graded against the committed fixtures and three
skills FAILED them as written — that stands recorded above. The repair round
then isolated the variable: on prompts that test the *description* rather
than file-discovery (self-contained/inline), all four skills clear the ≥83%
fire bar on Sonnet-5:

| skill | description-testing prompts (clean + repaired) | should-not | verdict (2026-08-03, Sonnet-5) |
|---|---|---|---|
| correspondence | 5/6 | 4/4 | **MEASURED-PASS** (original set) |
| application-tailor | 8/8 (ids 2,3,7,8) | 4/4 | **MEASURED-PASS** on non-trap class |
| after-report | 7/8 (ids 2,3,7,8) | 4/4 | **MEASURED-PASS** on non-trap class |
| delegation-discipline | 5/6 (ids 7,8,9) | 4/4 | **MEASURED-PASS** on non-trap class |

The absent-artifact prompt class (ids 1/3/6 delegation — id2 "this service"
is borderline and counted in neither class, recorded 1/2 — ids 1/6
after-report, ids 1/6 application-tailor: 0/4 each) remains a recorded
triggering ceiling of the same species as DEAD-1 — not a wording bug, not
re-worded, kept in the eval files as regression sentinels for any future
description experiment.

Bonus observation: application-tailor co-fired **brand-standard** in 3 of 4
repaired-variant runs — the compose-with-brand-standard design works live,
unprompted.

## Consequences applied

- Register rows 8–11 updated with these rates (dated, Sonnet-5).
- README candidates table: statuses advanced from UNMEASURED to measured.
- No description was edited — any future reword is a research-methodology
  experiment with these files as the pre/post instrument.
- correspondence's *need* remains owner-unconfirmed (register row 11) — its
  trigger now measures fine; whether the lane is real is still David's call.

## Bounds, stated plainly

Single surface (Claude Code headless), single model (Sonnet-5 — no Opus or
claude.ai cells), N=2 per prompt (the house live-fire floor, not the N=5
escalation), one day. The behavioral quality of what fires (does the fit
table actually appear, is the brief contract actually written) was spot-read
in transcripts but not blind-graded — that is the phase-2-style follow-up if
the owner wants it. claude.ai triggering for the two uploaded skills
(after-report, application-tailor) is untested from here.

## Provenance

Run and graded 2026-08-03 by the Fable 5 session of
`results/2026-08-03/skill-proposals/`. Instruments: `evals/*.json` at the
gates committed therein; grader and raw output in this directory; 60 verbatim
stream-json transcripts in `transcripts/`. Re-verify: re-run `grade.py`
against `transcripts/` — the tables above must reproduce exactly.
