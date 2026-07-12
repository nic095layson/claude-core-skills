---
name: plan-gate
description: >-
  The gate between receiving a non-trivial task and taking the first action on it —
  write the goal, list unknowns and assumptions, set success criteria BEFORE acting,
  plan in phases. Load this at the START of any task that is multi-step or
  costly-if-wrong — including concrete requests a user actually types
  like "build / set up / configure / wire up X", "refactor / rewrite / migrate /
  convert Y to Z" (e.g. move auth to JWTs), "stand up a pipeline or service" / "set
  up CI/CD", "figure out why...", and anything the user will rely on. Load it even
  when the task LOOKS clear or feels like "just write the script" — writing or
  running a migration, or moving data or tables between databases, gates even when
  it seems small, because it touches real data and is costly to get wrong.
  Do NOT load for genuinely trivial one-step work (a factual question, a one-line
  read, a rename) — skip ceremony on trivia. Do NOT use it to verify finished work
  (adversarial-verify) or decide scope mid-task (scope-fence).
---

# Plan-Gate

One rule: **no consequential action before a written plan the user could audit.**
Jumping straight into coding or drafting feels fast, but unplanned work fails in a
specific, expensive way — it produces something correct-looking against a goal
nobody wrote down, and the rework costs more than the plan would have. Reasoning
that never predicts anything can never be wrong, and reasoning that can never be
wrong quietly drifts into fiction. The gate makes drift visible early, when it is
still cheap to correct.

## Terms (defined once)

- **Consequential action** — anything that edits state, produces a deliverable, or
  commits the session to an approach: writing files, running mutating commands,
  drafting the document. Reading, searching, and measuring are NOT consequential —
  they are how you pass the gate.
- **Assumption** — an unknown you cannot cheaply resolve, written down so it could
  be proven wrong, and carried forward by number (A1, A2, …).
- **Success criteria** — the checkable conditions that will mean "done", committed
  BEFORE work starts, so the finish line cannot quietly move to wherever you ended up.

## The triage rule (run this first, always)

- **Trivial** (one step, factual, or a pure preference call): answer or do it
  directly. No plan, no ceremony. Convening a planning ritual to compute 15% of 80
  is a hard FAIL of this skill, not compliance with it.
- **Non-trivial** (multiple steps, dependent results, unknowns that matter,
  costly-if-wrong): run the gate below, top to bottom, before the first
  consequential action.

When unsure which it is, it is non-trivial — misjudged triviality is cheap to
upgrade and expensive to discover later.

## The gate

### 1. State the goal so it could be failed

One sentence, concrete enough that a stranger could later judge PASS/FAIL against
it. "Improve the script" cannot be failed; "the script processes the 3 sample files
without error and outputs valid JSON" can. If you cannot write this sentence, you
do not understand the task yet — ask or investigate before proceeding, in that
order of cost.

### 2. Inventory: knowns vs unknowns

Separate what you KNOW from what you are GUESSING:

- **Verified facts** — things you checked this session (read, ran, measured, or
  the user stated). Note the basis for each.
- **Unknowns that matter** — things that would change your approach if they turned
  out differently.

**Convert cheap unknowns into facts first.** If a tool call (read, search, run,
measure) can settle an unknown in seconds, do that BEFORE planning around it.
Never deliberate about something you could simply look up — and never trust a doc
where you could check the live system (see live-state-truth).

### 3. Register the assumptions

Every unknown you cannot cheaply resolve becomes a numbered register row:

| Part | Meaning |
|---|---|
| Content | What you are assuming, stated so it could be proven wrong |
| Basis | Why this is the most defensible default (evidence, convention, cost of the alternative) |
| Status | `unconfirmed` until the user or evidence settles it |

Then **proceed on the register — do not stall.** Blocking on questions the user
may never answer is worse than acting on labeled defaults. But every conclusion
that depends on an assumption must say so ("assuming A2 …"), and when a row is
later corrected, re-derive only what depended on it.

### 4. Define success criteria — before acting

Write the conditions that will mean done: outputs that must exist, checks that
must pass, numbers that must land in range. Committed in advance, they are a
finish line; written afterward, they are a rationalization. Adversarial-verify
will grade the finished work against exactly these. Pre-committed criteria are
the only full-strength gate; adversarial-verify's fallback (criteria written from
the original request before looking at the result) salvages a degraded but still
honest grading — what cannot be salvaged is criteria written after seeing the
output.

### 5. Plan in phases with predicted outcomes

Number the phases. For each consequential phase write, BEFORE executing it:

- **Expected observation** — a concrete, checkable prediction ("the test count
  should be 12", "this search should return the config file").
- **Branch rule** — "if I see X instead, go to Y" for foreseeable failures.
  A plan with no branch rules is a hope, not a plan.
- **Fenced wrong paths** — approaches considered and rejected, with the reason,
  so nobody (including future-you) re-fights a settled battle.

Rank alternatives before committing: state the chosen approach and why it beats
the runner-up, one line each. During execution, compare expected vs actual at
each phase boundary — a surprise means your model of the problem is wrong; STOP
and re-diagnose rather than pushing a broken plan faster (the full
surprise-handling discipline lives in adversarial-verify).

## Output format

Present the gate's product compactly before starting work — adapt labels, keep it
short:

```
**Goal** — one falsifiable sentence.
**Knowns** — verified facts, with basis. / **Unknowns** — what could change the approach.
**Assumptions** — A1, A2… (content, basis, status). Omit if empty.
**Success criteria** — the checkable definition of done.
**Plan** — numbered phases, each with expected observation and branch rule.
```

For small-but-non-trivial tasks this can be five lines. Length is not rigor;
pre-commitment is.

## Rules, each with its reason

1. **The plan precedes the first consequential action** — a plan written after
   acting is a narrative, and narratives always fit.
2. **Predictions are concrete** — "should work" predicts nothing; a prediction you
   cannot check is decoration.
3. **If you cannot name what the task will change or produce, do not start** — the
   inability to predict is itself the finding; investigate or ask.
4. **No ceremony on trivia** — over-triggering this gate erodes the user's trust in
   it, and that erosion is what kills governance skills.

## When NOT to use this skill

- Trivial one-step tasks — answer directly (see the triage rule; skipping IS the
  protocol).
- Verifying finished work against the criteria → **adversarial-verify**.
- Deciding whether a newly discovered problem belongs in this task → **scope-fence**.
- Checking a doc's claim against reality before planning around it → **live-state-truth**.
- Recording that a plan's branch fired or an approach dead-ended → **lessons-ledger**.

## Provenance and maintenance

Generalized 2026-07-11 from `nic095layson/claude` (commit `df6e198`, 2026-07-10):
the `logic-tree` skill (triage gate, fact/guess inventory, assumption register,
gated phases, expected-vs-actual — carried here nearly verbatim), `change-control`
(classify-before-touch; "if you can't name an eval case that should move, question
why you're editing at all" → rule 3), and `research-methodology` (hypothesis
predicts outcomes before running). Repo-specific instances of these laws remain in
that repo and take precedence there.

Re-verify lineage: `gh api repos/nic095layson/claude/contents/.claude/skills --jq '.[].name'`
— expect `logic-tree`, `change-control`, `research-methodology` among the listing.
