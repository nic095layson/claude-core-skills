# Hypothesis — a sizing test and an emission rule make an honest gate distinguishable from a skipped one (2026-08-20)

Pre-registered per research-methodology BEFORE any measurement run. Status:
**REGISTERED; NOT RUN.**

**Framing, stated honestly.** research-methodology Step 0 routes "it's broken" to
debugging-playbook rather than to experimentation, and this is a diagnosed live
failure (`.claude/LESSONS.md` INC-2026-08-19-01, owner-reported 2026-08-19). The
patch is therefore an owner-directed repair and does not wait on an A/B for
adoption. This file exists so the repair is *falsifiable* rather than
aspirational, and so the two over-correction guards are graded against
predictions written before any run rather than after.

**One-variable note.** The house rule is one contiguous change per experiment.
This patch changes three things in `plan-gate` (sizing test, emission rule,
mandatory branch rules) plus one reporting change in `gauntlet`, so a positive
result says "the patch works", never "the sizing test works". Accepted
deliberately: D1 and D2 are independent defects that produced one visible
failure, and shipping them in separate gated slices would leave the emission hole
open for the duration. The consequence is recorded, not hidden.

## Background — what already existed and did not fire

`plan-gate` rule 1 already said the plan precedes the first consequential action,
and in the incident **it held**: the skill loaded as tool call #4, ahead of every
lookup. So the lever must not be a fifth restatement of rule 1. What was missing
was a rule about when the *reader* sees the gate — a property checkable from
outside the session, which rule 1 is not.

Likewise §"Output format" already allowed a five-line form. That allowance was
not wrong; its lack of a *condition* was. The edit adds a test that can fail,
not an exhortation to write more.

## The edits under test (exact text)

| # | File | OLD | NEW |
|---|---|---|---|
| 1 | plan-gate, Output format | "For small-but-non-trivial tasks this can be five lines." | "**The sizing test — the compressed form is earned, not chosen.** Five lines are permitted only when BOTH hold: … no source outside this session … AND … no more than two consequential actions." |
| 2 | plan-gate, Rules | *(4 rules; anti-ceremony was rule 4)* | new rule 4: "The gate's output is emitted as its own turn content before the first consequential action, never nested inside the finished deliverable"; anti-ceremony unchanged, renumbered to 5 |
| 3 | plan-gate §5 | "A plan with no branch rules is a hope, not a plan." | + "**Mandatory, not optional, for any phase whose expected observation depends on a source outside the session**" + the wiki-scope worked example |
| 4 | gauntlet §2 + Output format | named firing reports the load | + "**Named firing covers shape, not just load**" and the two reportable states; `**Fired**` line carries the distinction |

Descriptions are **byte-identical to `HEAD`** in both files (verified by
`git diff` restricted to the frontmatter block). Trigger rates are therefore
unaffected by construction, and this experiment measures output shape only.

## Pre-registered predictions, per case (`evals/plan-gate-emission.json`)

**H1 (the target — emission ordering).** On pg-emit-01, NEW emits a gate block at
a transcript index strictly before the first search tool call, 2/2. OLD is
predicted to produce the gate inside or immediately before the final answer in
≥1 of 2 — the founding case reproduced with different content.

**H2 (sizing).** On pg-emit-01 and pg-emit-02, the NEW gate block is FULL (goal +
knowns/unknowns + assumptions-or-explicit-none + criteria + numbered phases).
OLD is predicted to ship a 3-of-5 block in ≥1 of 2 — the exact shape recorded in
the incident. **This is the prediction most likely to be wrong**, because a
base model may produce a full block for its own reasons; a NEW pass that OLD also
passes is INCONCLUSIVE, not a win (INC-7's near-ceiling trap).

**H3 (branch rules on external dependence).** On pg-emit-02, NEW's §5 carries ≥1
branch rule naming absence, different scoping, or contradiction. OLD predicted to
carry expected observations without branch rules in ≥1 of 2.

**H4 (over-correction guard — trivia).** On pg-emit-03, NEW answers `5432` with
**zero** gate vocabulary, 2/2. Any goal/criteria/phases scaffolding on a one-line
factual question is a FAIL that blocks the whole patch (architecture-contract
invariant 5; plan-gate's own triage rule calls this a hard FAIL of the skill).
Predicted unchanged from OLD.

**H5 (over-correction guard — the earned compressed form).** On pg-emit-04, NEW
uses the compressed form or none at all, 2/2, and does **not** emit phases with
branch rules for a two-touch rename in one already-named file. This is the case
that proves P1 tightened the *condition* rather than simply demanding length.
A regression here blocks adoption exactly as H4's does.

**H6 (gauntlet shape reporting, corroboration only).** On pg-emit-02, NEW's
closing Fired line states which of the two states occurred, and that statement
**agrees with the mechanically graded ordering**. A Fired line claiming
pre-work emission on a run graded NOT-EMITTED is a confabulation of the
INC-13/INC-15 family and is a finding in its own right — record it, do not average
it away.

## Method (committed)

Headless `claude -p`, fresh session per run, cwd **outside** this repo and outside
`~/.claude` (INC-4: project-scope skills load from cwd ancestors and contaminate
arms). Arms built by copying `.claude/skills/` — OLD from `git show HEAD:`, NEW
from the working tree — into two isolated directories; before each run, grep a
variant-unique fragment (`the compressed form is earned`) to prove which variant
is live (debugging-playbook §4, stale-copy trap). Prompts byte-identical from
`evals/plan-gate-emission.json`. N=2 floor per cell (R1). Transcripts kept verbatim
under `results/2026-08-20/plan-gate-emission/`.

**Grading is mechanical and blind to self-report.** For each run record two
indices: first assistant text block containing a gate block, and first
consequential tool call (WebSearch, WebFetch, Write, Edit, side-effecting Bash).
EMITTED-PRE-WORK := the former is smaller. A delivery's own claim about whether it
emitted the gate is not evidence and is not scored — INC-13 and INC-15 both
measured requested receipts confabulating, and INC-15 got the free-receipt law
reverted for exactly this.

**Known confound, declared in advance.** `plan-gate` is a *retired-from-personal-
install* question no longer at issue here, but its uncued firing rate is not:
`results/2026-08-11` found the patched governors registered in every arm and
**fired in zero uncued runs**. If pg-emit-01 shows no `Skill` invocation in either
arm, the run measured base-model behavior with the patch inert — report it as such
and do **not** read a passing NEW as evidence for the patch. pg-emit-02 cues
GAUNTLET by name and is the case least exposed to this.

## Outcomes routing

- **Confirmed** → record the measured rates, dated, in
  `evals/model-capability-register.md`; fold them into both Provenance sections,
  replacing the UNMEASURED lines; flip INC-2026-08-19-01 to CLOSED with the rates.
- **Refuted** → the text stays (it is an owner-directed repair to a live defect)
  but both Provenance sections must say the repair did not measurably change
  shape, and the next lever is mechanical — a Claude Code hook that inspects turn
  ordering — not more wording. Note that claude.ai, the surface this incident
  occurred on, has **no hook layer**, so a mechanical lever there does not exist.
- **Regression on pg-emit-03 or pg-emit-04 → revert P1**, append a `DEAD-n` entry,
  and redesign. Ceremony on trivia is diffuse, permanent, and kills the whole
  library's credibility; it is a worse outcome than the incident being patched.

## Provenance

Authored 2026-08-20 by the fix session for `.claude/LESSONS.md` INC-2026-08-19-01.
Case shapes pg-emit-01…04 are the owner's §6 eval table from the incident report,
with prompts written here. Derives from research-methodology (pre-registration,
R1 N=2 floor, R2 any-regression-blocks), architecture-contract invariants 2, 3
and 5, and the ledger's INC-4 (arm isolation), INC-7 (near-ceiling baselines prove
nothing), INC-13/INC-15 (requested receipts confabulate — grade off the transcript).
