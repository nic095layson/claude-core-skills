# claude-core-skills

A general-purpose governance library for Claude: five **governors** that shape how
any session plans, verifies, fact-checks, scopes, and learns — plus eight support
skills for maintaining and proving the library itself.

Extracted 2026-07-11 from [`nic095layson/claude`](https://github.com/nic095layson/claude)
(the claude-council skill library), whose operational laws were written repo-scoped
but intended to govern Claude holistically. This repo is the general form; that
repo keeps its project-specific instances, which **take precedence inside that
project** (see `architecture-contract`, Decision 2).

## The governors (three active, two retired)

| Skill | Governs | One-line law |
|---|---|---|
| [`plan-gate`](.claude/skills/plan-gate/SKILL.md) | Before acting | No consequential action before a written goal, assumption register, success criteria, and phased plan with predictions |
| [`adversarial-verify`](.claude/skills/adversarial-verify/SKILL.md) | Before delivering | Attack your own work, grade against pre-committed criteria, report faithfully — the author is the worst grader of their own work |
| [`live-state-truth`](.claude/skills/live-state-truth/SKILL.md) *(RETIRED 2026-07-11)* | Every factual claim | Live state outranks every description of it; measure instead of eyeball; capabilities don't travel between environments |
| [`scope-fence`](.claude/skills/scope-fence/SKILL.md) | During the work | The prompt defines the fence; adjacent problems get flagged, never silently fixed; approval is per-scope |
| [`lessons-ledger`](.claude/skills/lessons-ledger/SKILL.md) *(RETIRED 2026-07-11)* | After failure | Incidents, drifts, and dead ends get recorded as symptom → root cause → evidence → status, and consulted before re-attempts |

They compose over a task's lifecycle: plan-gate opens it, live-state-truth feeds
it facts, scope-fence bounds it, adversarial-verify closes it, lessons-ledger
remembers what it cost.

## The support skills

| Skill | Answers |
|---|---|
| `architecture-contract` | Why the library is shaped this way; the invariants any edit must preserve; known-weak points |
| `domain-reference` | What skills are, how triggering/discovery work, the glossary, the assumption register |
| `skill-authoring` | How to write a skill in this house style, end to end |
| `debugging-playbook` | Symptom → triage for skill and session failure modes |
| `diagnostics-and-tooling` | The mechanical checks — ships `scripts/lint_skill.sh` |
| `research-methodology` | How a wording hunch becomes an accepted change (pre-registration, N=2 floor, any-regression-blocks) |
| `install-and-surfaces` | Install/package/verify per surface; what does not carry between environments |
| `governance-adoption-campaign` | The decision-gated plan for proving the governors actually fire and change behavior |

## Install

**Claude Code, this repo:** nothing — project skills auto-load from
`.claude/skills/`.

**Claude Code, any machine (the intended footprint — governors only):**

```bash
for s in plan-gate adversarial-verify scope-fence; do
  mkdir -p ~/.claude/skills/$s && cp .claude/skills/$s/SKILL.md ~/.claude/skills/$s/
done
```

Then verify in a fresh session that the five appear in the skills list — files in
place is half an install; registration observed is the half that counts.

**claude.ai:** package each skill per `install-and-surfaces` Runbook 2 and upload
via Settings → Capabilities → Skills. The paired custom-instructions text (the
always-on trigger pointers + style rules) is versioned at
[`instructions/claude-ai-custom-instructions.md`](instructions/claude-ai-custom-instructions.md)
— the settings box and that file must never disagree.

## Lineage map (no laws lost)

| Governor here | Source instance in `nic095layson/claude` |
|---|---|
| plan-gate | `logic-tree` + `change-control` (classify-first) + `research-methodology` (hypothesis-first) |
| adversarial-verify | `validation-and-evals` + `logic-tree` (expected-vs-actual) + claude-council doctrine (Contrarian, honest verdicts) + `failure-archaeology` INC-1 (the behavioral-check law) |
| live-state-truth | `diagnostics-and-tooling` (measure-don't-eyeball) + `change-control` Gate D + `failure-archaeology` (drift, INC-1) |
| scope-fence | `change-control` (gates, per-class approval, write boundaries) + `logic-tree` (fenced paths) |
| lessons-ledger | `failure-archaeology` (recording rule, entry format, evidence bar) |

Each SKILL.md ends with a Provenance section naming exactly what carried over.
The source repo is **private** — the `gh api` re-verification one-liners in
those sections require owner access; everyone else should treat the lineage as
historical record.

## Status (as of 2026-07-11)

All 13 skills lint with zero FAILs (`diagnostics-and-tooling/scripts/lint_skill.sh`;
on PyYAML-less machines the verdict is `PASS (with warnings)` — the warning is
environmental, not skill content). Reviewed 2026-07-11 by three independent
reviewers (factual, doctrine, usability; blocking and important findings fixed
in-tree — see the fix commit). Trigger reliability and behavioral effect are
**unmeasured** —
assumption A2 in `domain-reference`; closing it is
`governance-adoption-campaign`'s job. Treat "the governors fire when needed" as a
candidate until that campaign's gates pass.
