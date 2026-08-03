# Hypothesis — hook enforcement lifts the two measured trigger ceilings (2026-08-03)

Pre-registered per research-methodology BEFORE any measurement run. Status:
**REGISTERED, NOT RUN.** The hooks exist and pipe-test clean (hooks/README.md,
2026-08-03); their behavioral effect is unmeasured.

## Background (the ceilings, as recorded)

- DEAD-1: scope-fence's inline-code should-fire class fired 0/2 under both OLD
  and NEW wording across 4 framings — "a triggering ceiling, not a wording
  bug." plan-gate shares the mechanism class (hands-on model does not consult
  governance skills mid-work); its first-write moment is the analogous gap.
- DEAD-2: lessons-ledger append-on-diagnosis plateaued at 78–80% should-fire
  under two honest rewords (NEW2: 12/15), 0/16 uncued in phase-2. Recorded
  candidate next lever: "mechanical enforcement (hooks), not wording."

## Hypotheses and pre-registered predictions

**H1 (plan-gate hook).** With `plan-gate-first-write-reminder.sh` active, a
non-trivial coding prompt that goes straight to editing (plan-gate's
evals/plan-gate.json should-fire set, restricted to prompts where the baseline
arm's first tool use is a write) will produce a written goal/criteria/plan
before or at the first edit in ≥5/6 runs, versus the no-hook arm's baseline
(to be re-measured same-day, same prompts, same model — prediction: baseline
≤3/6 on the straight-to-edit subset). Should-not prediction: on
evals/plan-gate.json's trivial prompts (id 4–5 class), the hook arm adds NO
planning ceremony in ≥3/4 runs — the reminder text's own triage line is the
control surface being tested.

**H2 (ledger hook).** With `ledger-recount-reminder.sh` active, the
evals/lessons-ledger.json should-fire recounts produce an actual ledger append
(or explicit offer with the entry drafted) in ≥5/6 runs versus the recorded
~80% wording ceiling — and, the stricter test, ≥1/4 on an uncued phase-2-style
run where baseline was 0/16. Should-not prediction: non-recount prompts
(evals ids 4–5 class) trigger zero reminders and zero appends in 4/4 runs
(the regex, not the model, is the gate — a regex false-positive is a FAIL
recorded against H2 regardless of downstream behavior).

## Method (committed)

Headless A/B per house law: fresh `claude -p` sessions, arms = hook wired
in settings vs not, N=2 floor per cell then escalate to N=5 where the read is
close (the DEAD-2 lesson: small-N optimism), `~/.claude/skills` locked and
identical across arms (INC-4), scratchpad state fixed (INC-2), cwd isolated,
prompts byte-identical from the committed evals files, FIRED operationalized
as in each evals `_grading` block plus the H1/H2 behavioral signatures above,
transcripts kept verbatim. Any should-not regression blocks adoption
(invariant 3). Grade cells in isolation before any overall verdict.

## Outcomes routing

- Confirmed → hooks graduate from UNMEASURED to measured in
  `evals/model-capability-register.md` (rows 2–4) and hooks/README.md gains
  the dated live verdict; wording of the reminder strings becomes gated text
  (edits re-run this A/B).
- Refuted or regression → hook reverted from settings, entry appended to
  `.claude/LESSONS.md` (DEAD-n), scripts retained in hooks/ marked as such.
- Inconclusive → recorded as INC-n; hooks may stay as owner candidates only if
  zero should-not regressions were observed (the no-silent-defaults precedent,
  2026-07-15).

## Provenance

Authored 2026-08-03 (Fable 5 session, proposal 2 of
`results/2026-08-03/skill-proposals/`, owner-approved). Derives from
`.claude/LESSONS.md` DEAD-1/DEAD-2, architecture-contract weak-point 3,
hooks/README.md (scope-fence-reminder precedent), research-methodology.
