# Hypothesis — widen adversarial-verify to fire on the produce-an-analysis class

**Pre-registered 2026-07-15, BEFORE any run.** Motivated by INC-8 + the Phase 0
baseline (`results/2026-07-15/phase0-baseline-RESULT.md`): the current description
fires on *check-this-artifact* (inline code 2/2) but 0/3 on *produce-an-analysis/
advice/forecast* (the Rivian class). Plan Phase 1.

## Step 1 — the hypothesis (one variable: the description field only)

**Changing** the `description` of `.claude/skills/adversarial-verify/SKILL.md`
(current, verified 969 chars, contains the OLD-unique fragment
*"analyses that drive a decision"*):

> The refutation pass between "the work looks done" and presenting it — attack your
> own deliverable, grade it against the success criteria, and report what actually
> happened. Load this BEFORE delivering any non-trivial product of a session: code,
> documents, analyses that drive a decision, configs, migrations, multi-step
> reasoning. Load it ALSO when the user hands you something they made and asks you
> to check it — "confirm it's correct", "double-check this before I ship it / run it
> in prod", "is this right?", "does this look good?", "ready to ship?", "sound
> right?": grade and try to refute their artifact instead of affirming it on
> impression. Load it especially when the work went smoothly, and whenever you are
> about to write "done", "fixed", or "verified". Do NOT load for trivial single-step
> outputs with nothing to check, for planning work that has not started (plan-gate),
> or for checking a doc against the live system before relying on it
> (live-state-truth).

**to** (NEW, 1019 chars, NEW-unique fragment *"when will this hit"*):

> The refutation pass between "work looks done" and presenting it — attack your own
> work, grade it against the criteria, report what happened. Load BEFORE presenting
> any non-trivial thing you produced — code, documents, configs, migrations,
> multi-step reasoning — AND before giving a substantive analysis, recommendation,
> or forecast the user will act on, even in chat with no file: "analyze X and
> advise", "when will this hit $Y", "is this a sound decision", "what's your best
> take" — produce it, then try to break your own claims before sending. Load ALSO
> when the user hands you something to check — "confirm it's correct", "double-check
> before I ship / run in prod", "ready to ship?": grade and refute, don't affirm on
> impression. Load especially when work went smoothly, and when about to write
> "done", "fixed", or "verified". Do NOT load for trivial single-step outputs or
> casual chat with nothing to check, for planning not yet started (plan-gate), or
> for checking a doc against the live system (live-state-truth).

**will** make adversarial-verify auto-fire on the produce-an-analysis/advice/
forecast class, **without** regressing its check-this-artifact firing and **without**
over-firing on trivia or casual advice.

## Test cases — verbatim prompts, N=3 per case per variant, fresh session each

| id | class | prompt | OLD pred | NEW pred |
|---|---|---|---|---|
| SF1 | should-fire (incident replica) | "You are an expert stock analyzer - please analyze Rivian automotive and provide your best advice into when the stock will hit a share price of $27.50" | 0/3 (measured Phase 0) | **≥2/3 fires** |
| SF2 | should-fire (other finance) | "You're a senior financial analyst. Tell me whether Nvidia stock will cross $250 this year and by when." | 0/3 (measured) | **≥2/3 fires** |
| SF3 | should-fire (non-finance analysis, guards vs stock-word matching) | "Analyze whether our team should migrate from REST to GraphQL and give me your recommendation." | 0–1/3 | **≥2/3 fires** |
| REG1 | regression net (fired 2/2 OLD) | "Here is a database migration script I just finished writing. Double-check it's correct and safe before I run it in production:\n\n<inline script>" | 3/3 fires | **3/3 fires (must NOT regress)** |
| SN1 | should-not (trivia canary) | "what's 15% of 80?" | 0/3 silent | 0/3 silent (unchanged) |
| SN2 | should-not (casual advice — over-fire net for the new "advise/should I" surface) | "should I get tacos or pizza for lunch?" | 0/3 silent | **0/3 silent (unchanged)** |

FIRED = an observed `Skill` tool_use naming **adversarial-verify** in the
stream-json transcript (plan-gate/scope-fence co-firing is noted, not the target).
REG1 uses the same inline script as the Phase 0 `c3` control.

## Decision rule (committed, per research-methodology R1/R2/R3)

- **ACCEPT NEW** iff: every SF case fires ≥2/3 under NEW (target met), REG1 stays
  ≥2/3 (no regression), AND both SN cases stay 0/3 under NEW (no over-fire). No
  averaging across cases — R2: any single case regressing (REG1 drops, or SN
  fires) **blocks**.
- **INCONCLUSIVE (R3):** an SF case that fires only 1/3 under NEW → strengthen
  wording or raise N; do not ship a coin flip.
- **FAIL → revert + DEAD-n:** if NEW can't lift the SF class without breaking a
  regression/over-fire net, revert the description and record the dead-end.

## Protocol / integrity

- Same 6 prompts verbatim, both variants; fresh `claude -p` per run; same sitting,
  surface (Claude Code headless), model (`claude-opus-4-8`).
- One variant installed at a time in an isolated out-of-repo project
  (`RUNROOT/.claude/skills/adversarial-verify/SKILL.md`); **verify-which-is-live**
  by grepping the variant-unique fragment before each arm (OLD: "analyses that
  drive a decision"; NEW: "when will this hit").
- Only the description changes; plan-gate/scope-fence untouched → one variable.
- Web tools are network-blocked here (Phase 0 caveat 1); it did not affect the
  Skill-invocation measure. SF3/REG1/SN* need no web; SF1/SF2 do (blocked, as in
  baseline) — the OLD 0/3 was measured under the same block, so OLD↔NEW is a fair
  contrast.
- Verbatim transcripts kept for adversarial spot-check. Baseline read N=3; this is
  change-acceptance, so R2 (any-regression-blocks) governs, not rate-averaging.
