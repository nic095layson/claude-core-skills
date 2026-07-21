---
name: adversarial-verify
description: >-
  The refutation pass between "the work looks done" and presenting it — attack your
  own deliverable, grade it against the success criteria, and report what actually
  happened. Load this BEFORE delivering any non-trivial product of a session: code,
  documents, analyses that drive a decision, configs, migrations, multi-step
  reasoning. Load it ALSO when the user
  hands you something they made and asks you to check it — "confirm it's correct",
  "double-check this before I ship it / run it in prod", "is this right?", "does
  this look good?", "ready to ship?", "sound right?": grade and try to refute
  their artifact instead of affirming it on impression. Load it especially when the
  work went smoothly, and whenever
  you are about to write "done", "fixed", or "verified". Do NOT load
  for trivial single-step outputs with nothing to check, for planning work that has
  not started (plan-gate), or for checking a doc against the live system before
  relying on it (live-state-truth).
---

# Adversarial-Verify

The premise, and the reason this skill exists: **the author is the worst possible
grader of their own work — they see intent, not output.** Reading your own
deliverable and feeling good about it is impression, not evidence. This skill
forces a role switch: for one pass, you are not the author defending the work,
you are the adversary paid to break it. Logic failures surfaced here cost one
pass; the same failures surfaced by the user cost the work's credibility.

## Terms (defined once)

- **Evidence** — an observed behavior of the deliverable: a command run, an output
  checked, a number measured. In descending strength: fresh-context behavioral
  check → measured artifact check → author impression → "I read it and it looks
  right" (the last is not evidence at all).
- **Success criteria** — the pre-committed definition of done from plan-gate. If
  none exists, write criteria NOW, before looking at the result — criteria written
  after seeing the output are a rationalization.
- **Regression** — anything that worked before the change and no longer does.

## The pass — run all five, in order

### 1. Grade against the committed criteria

Take the success criteria from plan-gate and grade the deliverable row by row,
PASS/FAIL, with the evidence beside each verdict. Grade each item in isolation
before forming an overall opinion — an early PASS glow contaminates later rows.
No criteria on file → write them first from the original request, then grade.

### 2. Behavioral check, not inspection

If the deliverable can be exercised, exercise it — run the code, open the
document, execute the query, follow the instructions you wrote as if you knew
nothing. A recorded incident behind this law: a syntactically perfect file shipped
to the wrong directory failed silently for three days because nobody ran anything
— reading it could never have caught what running it caught immediately.
**One good run is an anecdote.** If a second run is cheap, run it twice —
agreement is evidence; a single run of a non-deterministic step is a coin you
have not flipped again.

### 3. The refutation attempt

Actively try to break it. Argue the opposite: "this is wrong because…" and see
what completes the sentence. Attack the weakest joints:

| Attack | Question |
|---|---|
| Edge inputs | What happens at empty, zero, huge, malformed, concurrent? |
| Hidden assumptions | Which register rows (A1, A2…) does this silently depend on? Say so in the delivery. |
| The unhappy path | Does every failure mode fail loudly? Silent failure is the worst outcome of all. |
| The stranger test | Could someone with no context use/run/read this and get the claimed result? |
| Regressions | What worked before that this change could have broken? Check it — changes have non-local effects, and "unrelated" regressions block acceptance. |

### 4. Self-consistency check

Claims must agree with each other and with the artifacts. Numbers quoted twice
must match; the summary must describe the same behavior the artifact exhibits;
names, paths, and counts stated in prose must be the ones that exist. Where a
claim can be checked mechanically, check it mechanically — `diff`, `wc`, a rerun
— never by eyeball (the measurement doctrine lives in live-state-truth).

### 5. Surprise handling

Any mismatch between expected and observed means your model of the work is wrong
somewhere. STOP. Re-diagnose before patching — a patch applied to a
misunderstanding compounds it. **Never silently absorb a surprise into the
narrative**; either the surprise invalidates the work (fix it) or it revises your
understanding (say so in the delivery, and record it per lessons-ledger if it
meets the recording rule).

## Acceptance rule

Deliver only when: every committed criterion passes with evidence, the refutation
attempt found nothing unaddressed, and no regression appeared in any check. A
deliverable that improves the target but breaks something adjacent is rejected,
not shipped with a caveat.

## Report faithfully — the delivery contract

The verification's product is an honest status, in the delivery itself:

- Tests fail → say so, with the output. A step was skipped → say that.
- Unproven parts stay labeled **candidate** or **open** no matter how elegant.
  No oversell.
- Conclusions resting on assumptions cite the row ("assuming A2…").
- **A clean-looking summary of messy work is a defect**, not a kindness.

Delivery shape (adapt labels; keep every section honest, omit only what's empty):

```
**Criteria** — C1: PASS (evidence) · C2: PASS (evidence) · C3: FAIL (output shown)
**Refutation** — attacks tried, what they found (or "nothing survived")
**Regressions** — none found in <checks actually run> / found: <which, output>
**Status** — delivered | candidate (unproven parts named) | open (assuming A2…)
```

## Rules, each with its reason

1. **Criteria before results** — the finish line must not move to wherever you
   landed.
2. **Exercise over inspect** — silent failures are invisible to reading.
3. **Two runs where cheap** — non-determinism makes single runs unreliable
   evidence. (This is the judgment-form for verifying deliverables; wording
   experiments on skills carry research-methodology's unconditional N=2 floor.)
4. **Any-regression-blocks** — "unrelated" breakage is how quality erodes one
   justified exception at a time.
5. **The pass is proportional** — a five-line fix gets a five-minute pass, not the
   full table; skipping refutation entirely is the only wrong size.
6. **Verify at the source of truth** — when you built the thing being checked,
   instrument the builder to report what it did rather than inferring it from its
   output; reverse-engineering your own artifact is a lossy proxy for facts you
   already hold exactly.
7. **A broadly-failing check indicts the checker** — a detector that fails most or
   all cases is almost always the broken part; validate it on a known-answer case
   before acting on its verdict, and after two failed detector rewrites change
   measurement strategy, not thresholds.

## When NOT to use this skill

- Work not yet started or mid-planning → **plan-gate**.
- Checking documentation/config claims against the live system → **live-state-truth**.
- The verification surfaced an out-of-scope problem → flag it via **scope-fence**,
  do not fix it here.
- The verification surfaced a ~15-minute-plus diagnosis, drift, or dead end →
  record it in **lessons-ledger**.
- Purely conversational answers with no artifact — proportionality: a quick
  self-check, not this protocol.

## Provenance and maintenance

Generalized 2026-07-11 from `nic095layson/claude` (commit `df6e198`, 2026-07-10):
`validation-and-evals` (evidence hierarchy §1; the two-runs doctrine — carried
here in its where-cheap judgment form, while research-methodology carries the
unconditional R1 floor for experiments; the
targeted-improves-AND-nothing-regresses acceptance rule §1/§7; author-as-worst-
grader and grade-in-isolation §8), `logic-tree` (expected-vs-actual, surprise →
STOP, truth labels, "clean-looking summary of messy work is a defect"), the
claude-council doctrine (the Contrarian's refutation move; honest reporting — no
inflated verdicts), and failure-archaeology INC-1 (the ran-nothing incident behind
the behavioral-check law). The repo-specific eval protocol (evals.json schema,
fresh-session trigger tests) remains in that repo and applies when editing skills
there.

Rules 6–7 added 2026-07-21 from the perspective-taking deck AAR
(`results/2026-07-21/AAR-perspective-taking-deck.md` §2.1: five pixel-heuristic
detectors produced zero verified information the generator could have reported
exactly, and a 10/10-failure verdict was believed over the artifact for two more
rewrites). Status: **adopted owner candidate, not yet A/B-validated** —
pre-registered in `experiments/hypothesis-2026-07-21-{verify-at-source,suspect-the-instrument}.md`.

Re-verify lineage: `gh api repos/nic095layson/claude/contents/.claude/skills --jq '.[].name'`
— expect `validation-and-evals`, `logic-tree`, `claude-council`, `failure-archaeology`.
