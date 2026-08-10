# Hypothesis — hook enforcement lifts the two measured trigger ceilings (2026-08-03)

Pre-registered per research-methodology BEFORE any measurement run. Status:
**RUN 1 STARTED 2026-08-10** (addendum below, written and committed before the
first measurement run). Prior status: REGISTERED, NOT RUN. The hooks exist and
pipe-test clean (hooks/README.md, 2026-08-03).

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

## Run 1 addendum (2026-08-10, committed BEFORE the first measurement run)

Owner directive: "Proceed with your recommended order" (E4 of
`results/2026-08-10/instruction-review/REPORT.md`). Environment and design
decisions fixed now, per the methodology traps on record:

- **Surface:** Claude Code headless (`claude -p`, v2.1.226) in a cloud (CCR)
  container — same surface class as the 2026-08-03 trigger evals. NOT the
  primary machine; rates recorded as such. Model = headless default, recorded
  from transcripts at grading.
- **Isolation (INC-4):** one isolated `CLAUDE_CONFIG_DIR` per arm, byte-identical
  except `settings.json` (hook arm: the hook wired user-scope with absolute
  paths; baseline arm: no hooks). Skills in both arms = the intended personal
  footprint (plan-gate, adversarial-verify, scope-fence, brand-standard),
  copied from repo HEAD. No mutation of the container's live `~/.claude`.
- **Per-run state (INC-2):** fresh empty cwd outside the repo per run; per-run
  `TMPDIR` so hook sentinels are per-run artifacts. H2 cued runs seed a stub
  `.claude/LESSONS.md` (header only) in cwd — BOTH arms, fixed state — so the
  append target exists and the absent-artifact trap (INC-2/INC-8) is not what
  gets measured. Permission mode `acceptEdits` in every run (writes must be
  possible for a first-write hook to have a moment to fire); `--max-turns 12`,
  stream-json transcripts kept verbatim.
- **H1 fixture appendix (INC-7, appended append-only BEFORE any run):**
  `evals/plan-gate.json` ids 6–7 (`_added` 2026-08-10) — imperative
  "just write the file" prompts over costly-if-wrong operations, designed so
  the baseline's plan path is suppressed and the straight-to-edit subset is
  non-empty even if ids 1–3 plan at ceiling (their July rate was 9/9 — a
  saturated baseline would otherwise leave H1 nothing to catch). Originals
  untouched; ids 1–3 remain the regression sentinels.
- **Pre-run analysis finding (recorded before running, not after):** H2's
  stricter uncued prediction (">=1/4 on an uncued phase-2-style run") is
  **structurally unreachable by this hook**: `ledger-recount-reminder.sh` is a
  UserPromptSubmit regex over recount phrasings, and the committed uncued
  prompts ("...but it crashes. Can you fix it?") match none of them —
  verified against the regex before any run. The 4 uncued hook-arm runs are
  retained as committed and double as a current-model uncued re-baseline;
  if they fail, that cell is graded REFUTED-BY-DESIGN for the hook (the
  lever for uncued is a different hook event — PostToolUse/Stop — which
  would be a NEW pre-registration, not a mid-run redesign).
- **H2 uncued fixtures:** the 2026-07-11 planted ll-u1/ll-u2 *files* were not
  committed; they are reconstructed from the committed spec
  (`results/2026-07-11/phase2-uncued/PREREG-UNCUED.md` §ll-u1/ll-u2:
  stdlib-shadowing `random.py` crash; `data.csv` trailing-space header
  KeyError). Reconstruction noted as such in results.
- **Cells (N=2 floor per prompt, escalate to N=5 where close):**
  H1 baseline pg ids 1,2,3,6,7; H1 hook same; H1 should-not ids 4,5 both arms.
  H2 baseline ll ids 1,2,3; H2 hook same; H2 should-not ids 4,5 both arms plus
  direct regex pipe-tests (a regex false-positive on ids 4–5 is a FAIL against
  H2 regardless of downstream behavior); H2 uncued hook arm ll-u1/ll-u2 ×2.
  Straight-to-edit subset membership for H1 is decided by the BASELINE arm's
  transcripts (first tool use is Write/Edit), per the original registration.

## Provenance

Authored 2026-08-03 (Fable 5 session, proposal 2 of
`results/2026-08-03/skill-proposals/`, owner-approved). Derives from
`.claude/LESSONS.md` DEAD-1/DEAD-2, architecture-contract weak-point 3,
hooks/README.md (scope-fence-reminder precedent), research-methodology.
Run 1 addendum authored 2026-08-10 by the Fable 5 session executing the
2026-08-10 review's E4, committed before its first run.
