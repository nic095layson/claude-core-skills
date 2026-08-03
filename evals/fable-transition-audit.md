# Fable-transition audit — runbook (authored 2026-08-03, not yet run)

Purpose: when the model mix serving this account changes — Fable 5 leaving the
plan is the motivating event — re-measure which of this library's disciplines
the everyday models carry natively versus which only exist because a skill
supplies them, then route the verdicts through architecture-contract. The
contract already anticipates this moment: Decision 7 marks live-state-truth's
retirement reversible because "base-model behavior is a volatile fact; a future
model class that stops checking live state re-opens this decision." This
runbook is the procedure for that re-opening, generalized to every measured
calibration in the repo.

**Status: authored ahead of the event. Nothing below has been run on a
post-Fable mix.** Companion artifact: `model-capability-register.md` (same
directory) — the dated record this runbook feeds.

## When to run

- The account loses or gains a model class (Fable leaving; a Claude 6-class
  model arriving).
- A default-model change in daily surfaces (claude.ai default, Claude Code
  default).
- Observed governance regressions with no skill edit to explain them
  (debugging-playbook first to rule out install drift; then this audit).

Do NOT run for: minor version bumps with no observed behavior change, or a
single anecdote (one bad session is an anecdote; the register records rates).

## The audit, in order

Each step reuses machinery that already exists — this runbook sequences it,
it does not invent method. The methodology traps recorded in
`.claude/LESSONS.md` bind throughout: lock `~/.claude/skills` between arms
(INC-4 class), hold scratchpad state fixed (INC-2), isolate cwd, pre-register
before running (research-methodology).

1. **Snapshot the mix.** Record, dated: which models the account can reach per
   surface (`/model` in Code; claude.ai picker), which is default where, and
   the effort tiers available. This is the register's header row for the run.
2. **Re-run the retirement-class discriminating tests** on the new daily
   models. The instruments are in `results/2026-07-11/` and `evals/`:
   - live-state-truth 8-cell (cued + uncued, with + without skill): does the
     base model still check live state over docs unprompted? Gate: any cell
     where without-skill drops below with-skill re-opens Decision 7.
   - lessons-ledger uncued firing + cued value (phase2 design).
   - The no-silent-defaults A/B (`experiments/hypothesis-2026-07-15-no-silent-defaults.md`)
     — measured SATURATED on top-tier models; a weaker daily model is exactly
     the condition under which the candidate law could start earning its keep.
3. **Re-run the governor trigger evals** (`evals/plan-gate.json`,
   `evals/adversarial-verify.json`, `evals/scope-fence.json`) headless on the
   new daily model, same gates as committed in each file's `_grading` block.
   Known ceilings travel with their lessons: scope-fence's inline-code class
   (DEAD-1) and lessons-ledger's ~80% wording ceiling (DEAD-2) are triggering
   ceilings, not wording bugs — do not burn budget re-wording; the hook pack
   (`hooks/`) is the lever there.
4. **Behavioral-value spot checks** for the active governors: cued
   with/without on 2–3 tasks per governor (phase-2 design, blind-graded).
   The question is not "does it fire" but "does firing still change output" —
   a weaker base model may show LARGER deltas than the 2026-07-11 runs did;
   that is a finding worth recording, not just a pass.
5. **Write the register rows.** Every measured behavior gets a dated row in
   `model-capability-register.md`: carried-by, last-measured-on, verdict,
   re-open condition. Rates stay rates — never rounded to "always"
   (architecture-contract, invariant 3 scope note).
6. **Route the decisions.** Reinstate/retire/adjust calls go through
   architecture-contract (Decision 5/7 class, owner decides); wording changes
   through research-methodology; install changes through install-and-surfaces
   register-then-verify. This runbook produces evidence, not decisions.

## Budget guidance (assumption, dated 2026-08-03)

The 2026-07-11 campaign ran the full battery in roughly one working day across
two models. A transition audit re-running steps 2–4 on one new daily model
should land in the same envelope. If budget is short, priority order: step 2
(retirement reversals are the highest-stakes misses), then 3, then 4.

## Provenance and maintenance

Authored 2026-08-03 by the Fable 5 session that produced
`results/2026-08-03/skill-proposals/` (proposal 4), on owner approval of that
report. Derives from: architecture-contract Decision 7 (reversibility
condition — quoted above), the 2026-07-11 campaign instruments
(`results/2026-07-11/`, `evals/*.json`), lessons INC-2/INC-4/DEAD-1/DEAD-2,
and research-methodology's pre-registration law.

Re-verify before first use: instruments still present —
`ls evals/*.json results/2026-07-11/`; lessons still current —
`grep -c '^### ' .claude/LESSONS.md`. Update when: a run completes (link its
results dir here, dated), an instrument is superseded, or the register's
format changes.
