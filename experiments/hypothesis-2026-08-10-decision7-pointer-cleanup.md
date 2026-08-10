# Hypothesis — removing the retired-skill pointer from adversarial-verify's description does not regress triggering (2026-08-10)

Pre-registered per research-methodology BEFORE any run. This is the
Decision-7 deferred cleanup (architecture-contract: "the next gated wording
pass should reword them"), scoped by the 2026-08-10 review's live
measurement: at the description level, only **adversarial-verify** still
routes to a retired skill. plan-gate and scope-fence descriptions are clean;
body references are not gated (bodies do not trigger) and are out of scope
for this experiment.

## The exact change (one variable)

OLD (final clause of `description`, quoted verbatim from repo HEAD):

> Do NOT load for trivial single-step outputs with nothing to check, for
> planning work that has not started (plan-gate), or for checking a doc
> against the live system before relying on it (live-state-truth).

NEW (identical except the final parenthetical — the dead pointer is replaced
by the direct instruction; the near-miss routing case itself is preserved per
Decision 3):

> Do NOT load for trivial single-step outputs with nothing to check, for
> planning work that has not started (plan-gate), or for checking a doc
> against the live system before relying on it — just check the live system.

No other character of the description changes. Side effect (predicted
benign-to-positive): the description shortens; INC-3's bonus finding was
that shorter descriptions fire more reliably.

## Pre-registered predictions

- P1 (no regression, blocking): NEW should-fire rate >= OLD should-fire rate
  on `evals/adversarial-verify.json` ids 1,2,3,6,7,8, same day, same model,
  same environment. Any should-fire cell where OLD fires 2/2 and NEW fires
  0/2 blocks adoption (any-regression-blocks, invariant 3).
- P2 (should-not, blocking): ids 4,5 stay silent 2/2 each in BOTH arms; any
  NEW over-fire blocks adoption regardless of should-fire gains.
- P3 (gate, informational): NEW clears the committed gate (>=5/6 fire on the
  description-testing prompt class) — expected, since OLD cleared 9/9 on
  Opus 2026-07-11; today's run re-baselines OLD on the current daily model
  (Sonnet-5 class) in the same cells, so the comparison is same-surface.

## Method (committed)

Headless A/B: fresh `claude -p` (v2.1.226, cloud container — same
environment as the hook-enforcement Run 1 executing today), isolated
`CLAUDE_CONFIG_DIR` per arm with the intended personal footprint (plan-gate,
adversarial-verify, scope-fence, brand-standard); arms differ ONLY in
adversarial-verify's SKILL.md description (OLD = repo HEAD; NEW = the text
above). Per-run empty cwd outside the repo, per-run TMPDIR, no hooks in
either arm, `--max-turns 12`, `--permission-mode acceptEdits`, stream-json
transcripts kept. N=2 per prompt per arm (the floor), escalate to N=5 on any
close read (DEAD-2 lesson). FIRED := Skill tool_use invoking
adversarial-verify, per the instrument's committed operationalization.
Runs start only after this file is committed.

## Outcomes routing

- P1+P2 hold → adopt NEW in the repo SKILL.md (Decision-7 cleanup executed);
  re-package for claude.ai per install-and-surfaces (upload is the owner's);
  update the instrument's `_grading` history and the register.
- Any regression → NEW discarded, entry appended to `.claude/LESSONS.md`,
  pointer cleanup stays deferred with the measured reason.
- Inconclusive (e.g. OLD at floor on this model — no headroom to compare) →
  recorded as such; adoption may still be an owner call on the no-regression
  evidence alone if P2 held.

## Provenance

Authored 2026-08-10 by the Fable 5 session executing E3 of
`results/2026-08-10/instruction-review/REPORT.md` (owner directive: "Proceed
with your recommended order"). Derives from architecture-contract Decision 7
(deferred cleanup), the 2026-08-10 review's pointer measurement, INC-3's
length finding, research-methodology.
