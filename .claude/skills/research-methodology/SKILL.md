---
name: research-methodology
description: >-
  How a hunch about wording or behavior becomes an accepted change to this library
  — hypothesis with exact quoted text and pre-registered predictions, one variable
  per experiment, fresh-session A/B runs, the N=2 evidence floor, and the
  any-regression-blocks rule. Load when you catch yourself thinking "I bet
  rewording this description would fix X", "let me just tweak it and see", "did my
  edit actually make the skill better?", or "is one good run enough evidence?" —
  i.e., BEFORE editing any SKILL.md on a hypothesis, and AFTER an experimental run
  when deciding whether the outcome counts. Do NOT load for diagnosing a live
  breakage (debugging-playbook), authoring structure (skill-authoring), whether the
  change is architecturally allowed (architecture-contract), or running the
  mechanical lint (diagnostics-and-tooling) — this skill only turns hypotheses
  into evidence and routes the result.
---

# Research Methodology

The "code" in a skill library is prose that a model interprets,
nondeterministically, at runtime. So "I changed the wording and it looked better
once" is the dominant failure mode of skill development — it is how prose
libraries rot. This discipline separates a **result** (something you can act on)
from an **anecdote** (something that happened once).

## Terms (defined once)

- **Hunch** — an untested belief that a specific change will change behavior.
- **Variant** — one version under test: OLD (current tree) or NEW (your edit).
  Exactly two per experiment.
- **Run** — one test prompt sent to one *fresh* session with one variant
  installed.
- **Pre-registration** — the predicted outcome for every case, written down and
  saved to a dated file BEFORE any run. A prediction written after seeing output
  is worthless, and next week only the file's timestamp proves the order.

## Step 0 — is this a research question?

| You are thinking… | Go to |
|---|---|
| "It's broken / won't trigger / fires on everything" | debugging-playbook — diagnose, don't experiment |
| "Would this change violate the design?" | architecture-contract — check invariants BEFORE investing |
| "Was this tried before?" | lessons-ledger |
| "I think wording W causes behavior B, and W′ would cause B′" | **Stay here** |

## Step 1 — write the hypothesis (before touching anything)

One sentence, three mandatory parts. If you cannot fill all three, you have a
mood, not a hypothesis:

```
Changing [EXACT QUOTED TEXT in <skill>/SKILL.md]
to [EXACT NEW TEXT]
will [SPECIFIC BEHAVIOR CHANGE],
predicted per test case: [case-by-case, including "unchanged"].
```

Rules, each with its reason:

- **Quote the real current text** — verify with
  `grep -n "fragment" .claude/skills/<name>/SKILL.md` first. If grep returns
  nothing, the hypothesis targets text that does not exist.
- **One variable.** One contiguous change per experiment; description AND body
  is two experiments — you cannot attribute the effect otherwise.
- **Pre-register every case, not just the target.** Predictions for the cases
  expected to be *unchanged* are the regression net.
- **Save it to a dated file** (`hypothesis-YYYY-MM-DD-<slug>.md`) before any run.

## Step 2 — the A/B protocol

Anything in context can confound, and identical inputs can produce different
outputs. Design around both:

| Rule | Why |
|---|---|
| Same prompts, verbatim, both variants | Rephrasing is a second variable |
| Fresh session per run — no prior turns | Prior turns pre-trigger skills and steer output |
| One variant installed at a time; verify which is live before each run (grep a variant-unique fragment in the installed copy) | "Stale copy" is a known trap — debugging-playbook §4 |
| Both variants in the same sitting, same surface, same model | Model/date drift is uncontrollable; minimize the window |
| Pass criteria written before running | Grading by vibes after seeing output is how anecdotes get promoted |
| Record verbatim output, not your summary | You will unconsciously round output toward your prediction |

### The evidence bar

- **R1 — N=2 floor:** every case, at least 2 runs per variant (3 preferred for
  gating decisions), each in a fresh session. One run of a nondeterministic
  system cannot distinguish "the wording did this" from "the dice did this."
- **R2 — any regression blocks:** if ANY run of ANY case regresses under NEW, the
  change is blocked as-is. No averaging, no "3 of 4 passed" — a 50% failure rate
  on a previously-solid case is a real behavior change.
- **R3 — flaky target is inconclusive:** NEW passing the target only sometimes is
  "inconclusive", not "accepted". Strengthen the wording or raise N; do not ship
  a coin flip.
- **Known limitation, stated plainly:** N=2 catches gross regressions, not subtle
  rate shifts. It is a floor chosen so the protocol gets followed by hand; raise
  N when tooling makes runs cheap (governance-adoption-campaign, Phase 3).

## Step 3 — result vs anecdote

| | Anecdote (notes at most) | Result (may ship) |
|---|---|---|
| Prediction | After seeing output, or never | Pre-registered, dated file |
| Prompts | Paraphrased, varied | Verbatim, identical across variants |
| Sessions | Reused, carried history | Fresh per run |
| Runs | 1 per case | ≥2 per case per variant |
| Grading | "Looked better" | Pass/fail against written criteria, verbatim outputs kept |
| Scope | Only the hoped-for case | Every case, so regressions are visible |

An anecdote is a fine way to *generate* a hypothesis. It is never sufficient to
*accept* one.

## Step 4 — record the outcome, pass or fail

- **Confirmed → accepted:** land the edit; cite the experiment file in the
  commit; note the finding in the nearest skill's Provenance section, dated.
- **Failed:** append to **lessons-ledger** as a dead end (`DEAD-n`, status
  ABANDONED), so nobody re-runs it blind.
- **Case gap found** (the experiment needed a test case that didn't exist): add
  the case per skill-authoring step 5, regardless of the hunch's outcome.

## When NOT to use this skill

- Live breakage → **debugging-playbook**. Structure/style of the edit →
  **skill-authoring**. Design legality → **architecture-contract**. Mechanical
  checks → **diagnostics-and-tooling**. General verification of any deliverable
  (not an A/B on wording) → **adversarial-verify**.

## Provenance and maintenance

Generalized 2026-07-11 from `nic095layson/claude` (commit `df6e198`)
`research-methodology`: the hypothesis format, one-variable rule,
pre-registration discipline, A/B protocol table, R1/R2/R3 bar, and
result-vs-anecdote table carry over near-verbatim; repo-specific recording
locations are remapped to this library's (Step 4). That repo's honesty table
("almost none of this is established practice") applies here too: as of
2026-07-11 **zero experiments have been run against this library** — the
methodology is inherited doctrine, followed because the alternative is vibes.

Re-verify: experiment records — `ls hypothesis-*.md` in the scratch/records
area (absence = still zero). Update when: the first experiment lands (replace
the zero-experiments line, dated), or tooling changes the practical floor in R1.
