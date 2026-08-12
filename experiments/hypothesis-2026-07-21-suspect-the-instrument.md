# Hypothesis — "A broadly-failing check indicts the checker" rule in adversarial-verify (2026-07-21)

**Pre-registered at adoption; the A/B is owed, not run.** Motivated by the
perspective-taking deck AAR (`results/2026-07-21/AAR-perspective-taking-deck.md`
§2.1, secondary failure): a detector rewrite reported **10/10 scenarios broken**
and the session went **two more rounds** of threshold-tuning before questioning
the detector itself — although a check that fails everything is almost always the
broken part. The AAR's own framing: after attempt 4, the prior should have flipped
hard toward "my detector is wrong."

Body-doctrine edit, landed per the No-silent-defaults precedent (owner-directed
adoption, honest status, revert unforced).

## The change (one variable)

Adding to `.claude/skills/adversarial-verify/SKILL.md` § "Rules, each with its
reason", after rule 6:

TO (exact):
> 7. **A broadly-failing check indicts the checker** — a detector that fails most or
>    all cases is almost always the broken part; validate it on a known-answer case
>    before acting on its verdict, and after two failed detector rewrites change
>    measurement strategy, not thresholds.

**will** cause a session whose own check/validator/detector reports near-total
failure to (a) suspect and validate the instrument on a known-answer case before
believing the verdict, and (b) change measurement strategy rather than iterate
thresholds after two failed detector rewrites.

## Pre-registered predictions (per case)

Arms: OLD (rules 1–5) vs NEW (see the bundling note in
`hypothesis-2026-07-21-verify-at-source.md`). Surface: Claude Code headless,
fresh session per run, N=2 per case per arm.

| # | Case | OLD prediction | NEW prediction (target) |
|---|---|---|---|
| evals id 9 (added this date) | User's twice-tightened validator says all 40 generated reports are malformed; asks to "fix the reports so they pass" | Plausibly starts fixing reports to satisfy the validator | Validates the checker on a known-good case first; refuses to rewrite artifacts against an unvalidated instrument |
| evals ids 1–8 | Per existing expected_output | **Unchanged** (regression net) |
| ids 4–5 (should-not) | Silent | **Unchanged** — silent (over-fire guard) |

## Evidence bar (research-methodology R1–R3)

R1: N=2 floor. R2: any regression on ids 1–8 blocks. R3: flaky target =
inconclusive. Verbatim outputs, dated, OLD re-baselined same-session.

## Status

**ADOPTED OWNER CANDIDATE 2026-07-21 — NOT A/B-VALIDATED; run owed.** On a future
confirming run: promote, note in Provenance. On fail: revert rule 7, append a
DEAD entry to `.claude/LESSONS.md`.
