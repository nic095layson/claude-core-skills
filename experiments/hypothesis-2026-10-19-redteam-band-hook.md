# Hypothesis — the band reminder hook makes a model-derived headline carry its structural band (2026-10-19)

Pre-registered per research-methodology BEFORE any A/B run. Status: **REGISTERED, NOT RUN.** The hook
(`hooks/redteam-band-reminder.sh`) exists and pipe-tests 7/7 (`hooks/selftest-redteam-band-reminder.sh`,
red-first: 0/7 before the hook, `results/2026-10-19/red-team-hook/`); its behavioral effect is unmeasured.

## Background

The red-team skill's rule 3 ("two error bars or none") comes from the kit post-mortem of 2026-10-19: a
report quoted a title share as ±0.4 where one hand-set simulator constant moved it by +3.4 / −2.3. A skill
can instruct but not compel (architecture-contract weak-point 3); the moment the lesson class shows
description-based triggering missing is when the session is already writing the report. The hook is the
same lever as `plan-gate-first-write-reminder.sh`: an advisory PreToolUse injection, once per session,
never a block (a hook cannot tell a modelled figure from a measured one, so a block would violate
invariant 5).

## The mechanism under test

PreToolUse on Write | Edit | NotebookEdit. Fires when the content being written contains a figure with a
sampling error (`±` or `+/-` between two numbers) and no band word (FRAGILE, SENSITIVE, ROBUST,
"structural band"). Injects one line: quote the last sweep's band beside the figure, or say the model has
no hand-set constants, or proceed if the figure is measured from data. Sentinel per session id.

## Hypotheses and pre-registered predictions

**H1 (fires where it should matter).** Prompts that ask for a written report quoting a figure from a
described model with a named hand-set constant (3 prompts, authored before the run, in
`evals/red-team-band-hook.json` when written): with the hook wired, the written report carries a band
sentence or an explicit "no band available / uncalibrated" statement in ≥5/6 runs; without the hook,
≤3/6. The reminder's own text ("a figure measured from data: proceed") is the control surface.

**H2 (no ceremony where it should not).** Prompts whose written figure is a measured count or a data
percentage with no ± (2 prompts) and prompts that write prose with no figure at all (1 prompt): zero
reminders injected in 6/6 runs (the regex is the gate; a regex false positive is a FAIL against H2
regardless of what the model then did), and no band language added to the written file.

**Adoption rule.** H1 confirmed and H2 clean → the hook may be wired into the project enforcement pack
(`.claude/settings.json`, once PR 24 lands) and the plugin twin (version bump, owner re-upload). Any H2
regression blocks (invariant 3). H1 refuted with H2 clean → the hook stays in `hooks/` as an owner
candidate with install steps, not wired.

## Method (committed)

Headless A/B per house law: fresh `claude -p` sessions, arms = hook wired in a scratch project's
`.claude/settings.json` vs the same project without it, N=2 per prompt per arm then N=3 where a cell lands
within one run of its threshold, cwd isolated, `~/.claude/skills` identical across arms, prompts
byte-identical, FIRED := a `hookSpecificOutput` with the reminder text in the transcript; the H1 signature
graded from the written file, not the chat. Transcripts kept verbatim under
`results/<date>/red-team-band-hook-ab/`.

## What is recorded today (not the A/B)

- Pipe tests 7/7 after the hook (0/7 before).
- One live negative run, hook wired, conversational prompt that writes a note with no figure: expected no
  reminder in the transcript. One live positive run, hook wired, a prompt that writes a ± figure from a
  described model: expected one reminder. N=1 each; existence checks, not rates.

## Provenance

Authored 2026-10-19 with the red-team toolkit (ledger INC-2026-10-19-01; kit after-reports
`after-report-2026-10-19-draft-postmortem.md`, `after-report-2026-10-19-redteam-standing.md`). Derives
from `experiments/hypothesis-2026-08-03-hook-enforcement.md` (the reminder-hook A/B shape) and
hooks/README.md's doctrine on advisory versus blocking hooks.
