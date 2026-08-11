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
- **Gap provenance** — every unknown that reaches a deliverable carries one of
  three states, stated rather than implied: `NOT-ATTEMPTED` (no attempt was made
  — always a decision, never a limit), `ATTEMPTED-FAILED` (an attempt was made
  and failed; name the attempt and the failure mode), `UNVERIFIABLE` (no
  accessible source exists; name what was searched and why it cannot resolve).
  Only the last two are limits. A bare "unconfirmed" collapses all three, which
  is how a choice passes as a limit — invisible to the reader *and* to this pass.
- **Load-bearing gap** — an unknown whose resolution either way would change a
  conclusion, recommendation, or verdict in the deliverable.

## The pass — run all six, in order

### 1. Grade against the committed criteria

Take the success criteria from plan-gate and grade the deliverable row by row,
PASS/FAIL, with the evidence beside each verdict. Grade each item in isolation
before forming an overall opinion — an early PASS glow contaminates later rows.
No criteria on file → write them first from the original request, then grade.

**The grade is binary.** A criterion that is neither cleanly PASS nor FAIL is a
FAIL with a reason, not a passing shade of one. If you find yourself writing
PARTIAL, MIXED, or MOSTLY, you have written FAIL and softened the word: say what
is missing and route it through Step 6 before any ship decision. An invented
middle grade reads as passing to everyone including you, which is precisely how
a criterion can be marked "not fully met" and shipped in the same breath.

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

### 6. The gap audit

Steps 1–5 test what the deliverable *claims*. This step tests what it left
unexamined. A gap asserts nothing, so Steps 2–5 cannot see it at all, and Step 1
sees it only when a criterion happens to be worded about coverage — here,
detection is systematic instead of incidental.

List every unknown, hedge, "unconfirmed", "couldn't verify", "likely",
"probably", and TBD in the deliverable. Give each its gap provenance, then apply
the **load-bearing test**: would the conclusion, recommendation, or verdict
change if this unknown resolved the other way?

| | Not load-bearing | Load-bearing |
|---|---|---|
| `NOT-ATTEMPTED` | Label it and ship | **Resolve it now, or withdraw the conclusion it supports.** Shipping is not an option. |
| `ATTEMPTED-FAILED` | Label with the failure mode | Label, and state what the conclusion becomes under each resolution |
| `UNVERIFIABLE` | Label it and ship | Label, and mark the conclusion `candidate` |

A cheap `NOT-ATTEMPTED` gap under a load-bearing conclusion is the failure this
step exists to catch: one tool call was the whole distance between an honest
deliverable and a wrong one. Note the direction of the rule — it makes an honest
`UNVERIFIABLE` *cheaper* to state, not harder. A real limit, named with what was
searched, ships.

## Acceptance rule

Deliver only when: every committed criterion passes with evidence (a PARTIAL is
not a pass), the refutation attempt found nothing unaddressed, no regression
appeared in any check, and no load-bearing gap remains `NOT-ATTEMPTED`. A
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
**Gaps** — <n>: <n> not-attempted / <n> attempted-failed / <n> unverifiable ·
             load-bearing: <resolved | conclusion withdrawn | candidate>
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
   full table; skipping refutation entirely is the only wrong size. Step 6 sizes
   the same way: one line on a small deliverable, and absent entirely from a
   conversational answer with no unknowns in it.
6. **A claim of inability needs a receipt** — "couldn't verify", "unable to
   confirm", "not available", "no data exists" and their variants may be written
   only when the same sentence names what was attempted and how it failed. With
   no attempt to cite, the honest phrasing is **"did not check"** — and if the
   item is load-bearing, "did not check" is not a deliverable state. Reason: the
   reader cannot tell a limit from a choice, so the writer must. A budget
   decision dressed as an epistemic one is INFERENCE-as-EVIDENCE wearing a
   different hat, and worse in one way — nobody argues with a stated limit, so it
   also disables the reader's ability to correct it.
7. **Aggregates are built from records, never from recall** — any count, tally,
   classification, or comparison table of external facts is assembled from a
   written record produced this session: tool output, a file, a command result.
   Recall may generate candidate rows; it may never populate a published one.
   Reason: a recalled row and a verified row look identical in the finished
   table, so the reader cannot apply their own discount to the weak ones.

## When NOT to use this skill

- Work not yet started or mid-planning → **plan-gate**.
- Checking documentation/config claims against the live system → **live-state-truth**.
- The verification surfaced an out-of-scope problem → flag it via **scope-fence**,
  do not fix it here.
- The verification surfaced a ~15-minute-plus diagnosis, drift, or dead end →
  record it in **lessons-ledger**.
- Purely conversational answers with no artifact — proportionality: a quick
  self-check, not this protocol. No gap audit either: Step 6 audits unknowns in a
  deliverable, and a conversational answer with no unknowns has nothing to audit.

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

Re-verify lineage: `gh api repos/nic095layson/claude/contents/.claude/skills --jq '.[].name'`
— expect `validation-and-evals`, `logic-tree`, `claude-council`, `failure-archaeology`.

**Appended 2026-08-11** — `.claude/LESSONS.md` INC-9 (labeled "INC-2" in the
owner's report; that number was taken). New: gap provenance + load-bearing gap
(Terms), the binary-grade rule (§1), **Step 6**, the load-bearing-gap condition
(Acceptance + delivery shape), rules 6–7. Nothing deleted or renumbered. Driving
evidence: a report shipped 8 of 26 items unverified under "couldn't verify" with
no lookup attempted, and *this pass certified it* — §1 graded the coverage
criterion PARTIAL and delivery proceeded. The defect was therefore not an
invisible gap but a noticed gap with no consequence, which is why §1 and the
Acceptance rule changed and not only Step 6. Rule 7 comes from the same tally,
which classified a minion as a spell from recall. Status: **cued mechanism
CONFIRMED** (4/4 vs 0/2), proportionality guard **no regression** (2/2),
**uncued value UNMEASURED** — `results/2026-08-11/gap-provenance-guards/`,
pre-registered in `experiments/hypothesis-2026-08-11-gap-provenance.md`.
Descriptions untouched, so trigger rates are unaffected by construction.
