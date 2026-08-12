# claude-core-skills

A general-purpose governance library for Claude: five **governors** that shape how
any session plans, verifies, fact-checks, scopes, and learns — plus eight support
skills for maintaining and proving the library itself, and one personal standard
(`brand-standard`) governing external-facing documents produced in David's name.

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

## The standards

| Skill | Answers |
|---|---|
| [`brand-standard`](.claude/skills/brand-standard/SKILL.md) | How anything published in David's name sounds and looks — voice/tone (evidence-derived), typography (Eurostile display / Poppins body), and the color system (Space Blue, Muted Space Blue, black + greys) with exact CMYK/RGB/HEX/Pantone/SW values. Loads before any external-facing document. |

## Candidates authored 2026-08-03 (unmeasured — not in the install footprint)

Authored by the Fable 5 session of `results/2026-08-03/skill-proposals/` on
owner approval; each lints PASS and registers as a project skill. **Trigger
evals ran same-day** (60 headless runs on Sonnet 5,
`results/2026-08-03/trigger-evals/`): zero over-fires anywhere; all four
clear the ≥83% fire bar on description-testing prompts (correspondence passed
its committed gate outright; the other three failed the naive aggregate via
the INC-8 fixture trap, repaired append-only and confirmed). Behavioral value
and claude.ai triggering remain unmeasured — empirical status lives in
`evals/model-capability-register.md` (rows 8–12); nothing here earns
always-on until Decision-5 review.

| Skill | Governs | Evals |
|---|---|---|
| [`delegation-discipline`](.claude/skills/delegation-discipline/SKILL.md) | Briefing, bounding, and verifying subagent/workflow work; the untrusted-content law | `evals/delegation-discipline.json` |
| [`after-report`](.claude/skills/after-report/SKILL.md) | The house analysis-report format + primary-source claim-check | `evals/after-report.json` |
| [`application-tailor`](.claude/skills/application-tailor/SKILL.md) | Job-application tailoring: evidence-only claims, never fabricate, fit verdict first | `evals/application-tailor.json` |
| [`correspondence`](.claude/skills/correspondence/SKILL.md) | Email in David's name: draft-never-send, quote-accurate, sensitive-send flags (need-unconfirmed) | `evals/correspondence.json` |

Companions shipped the same day: two mechanical trigger hooks
(`hooks/plan-gate-first-write-reminder.sh`, `hooks/ledger-recount-reminder.sh`
— pipe-tested, A/B pre-registered in
`experiments/hypothesis-2026-08-03-hook-enforcement.md`), the Fable-transition
audit runbook (`evals/fable-transition-audit.md`), and the model-capability
register (`evals/model-capability-register.md`).

## Adopted 2026-08-12 — `product-output`

Owner-approved from the 2026-08-10 draft (`results/2026-08-10/product-output-skill/`),
which sat unadopted for two days. The finish-line standard: when a session is
about to hand something over, a real dated **file** comes out — not a chat blob
where a file was asked for. It routes rather than formats: classify the
deliverable and audience, pick the format, call the owning skills, run the
validate-fix-repeat loop, deliver with a short manifest.

| Skill | Governs | Evals |
|---|---|---|
| [`product-output`](.claude/skills/product-output/SKILL.md) | The finish line: format choice, composition of standards, handover | `evals/product-output.json` |

**Empirical status: UNMEASURED.** Lints PASS; its eval set is authored and
**not run**. It is a coordinator — it owns no format mechanics, no voice, no
correctness grading — so its value depends entirely on whether "answered in chat
when a file was wanted" is a recurring annoyance. Project scope only; no
Decision-5 promotion.

## Retired 2026-08-12 — `photo-editing` removed

Adopted 2026-08-10 on decision A of the image-output survey, trigger-gated clean
(8/8 fire · 6/6 silent), and **removed 2026-08-12 at the owner's direction — no
longer wanted.** The skill and its eval set are deleted; the research that
produced it is **kept**, because deleting measured evidence and deleting a
capability are different acts:

- `results/2026-08-10/image-output-skill/` — the survey and the decision record
- `results/2026-08-10/trigger-evals-photo-editing/` — 14 transcripts and grades

Retirement rationale and what a future session should NOT re-derive are in
`.claude/LESSONS.md` (`DEAD-4`). This is a withdrawn capability, not a failed
one; the gate it passed still stands in the record.

## Install

**Claude Code, this repo:** nothing — project skills auto-load from
`.claude/skills/`.

**Claude Code, any machine (the intended footprint — governors plus the personal
brand standard):**

```bash
for s in plan-gate adversarial-verify scope-fence brand-standard; do
  mkdir -p ~/.claude/skills/$s && cp .claude/skills/$s/SKILL.md ~/.claude/skills/$s/
done
```

Then verify in a fresh session that they appear in the skills list — files in
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

## Status (as of 2026-08-11)

**2026-08-11 — INC-9 repair (the "unattempted verification" hole).** A chat
session shipped a tally and a recommendation built on eight of twenty-six items
it described as ones it "couldn't verify" but had never looked up — and the
adversarial-verify pass ran, graded the coverage criterion PARTIAL, and delivered
anyway. Patched: gap provenance (`NOT-ATTEMPTED` / `ATTEMPTED-FAILED` /
`UNVERIFIABLE`) defined once in `adversarial-verify` and referenced elsewhere,
the receipt law, a new **Step 6 gap audit** with the load-bearing test wired into
the Acceptance rule, aggregates-from-records, plan-gate's stop-the-conversion
rule, after-report's Bounds split, and the standing-principles line in
`instructions/` (**owner must re-paste that one**). Measured same day on
`claude-sonnet-5`: cued mechanism 4/4 vs 0/2 baseline, proportionality guard
2/2 no-regression, honest-limit control 8/8 no-regression, **uncued value
unmeasured** — full record and bounds in
[`results/2026-08-11/gap-provenance-guards/`](results/2026-08-11/gap-provenance-guards/RESULTS.md),
ledger entries `.claude/LESSONS.md` INC-9 and INC-10 (OPEN).

**2026-08-12 — INC-11: GAUNTLET restored as a skill.** A validated trigger word
went missing because the branch that carried it (`claude/rivian-stock-analysis-h5y46x`,
2026-07-16) was **never merged**; a later instructions block authored from `main`
was diff-clean against main, false against the live settings box, and overwrote it
on paste. GAUNTLET is now [`gauntlet`](.claude/skills/gauntlet/SKILL.md) — a skill
that sequences plan-gate → work → adversarial-verify → after-report — plus pointer 7
in the instructions. **That branch is still unmerged and carries 17 commits / 239
files**, including INC-8, DEAD-3, and a validated Stop-hook enforcement pair that
drove a governor 0/3 → 3/3. Owner decision outstanding; its ledger numbering
collides with `.claude/LESSONS.md` and must be reconciled on merge, not renumbered.

All 20 skills lint with zero FAILs (`diagnostics-and-tooling/scripts/lint_skill.sh`,
re-run 2026-08-11; the count read "18" here since 2026-08-10 and was one behind
the tree — corrected against a live `ls`, not by trusting the line). The lint now also enforces the 1024-char description limit
from INC-3, with a warning band above 1000 — no skill currently warns; the
longest description (plan-gate) sits exactly at the 1000 boundary, so a single
added word enters the band. On PyYAML-less machines the verdict is `PASS (with
warnings)`; that warning is environmental, not skill content. The original 13
skills were reviewed 2026-07-11 by three independent reviewers (factual,
doctrine, usability; blocking and important findings fixed in-tree).

Trigger reliability is **measured, not assumed** — assumption A2 in
`domain-reference` carries the full dated story. In short: plan-gate and
adversarial-verify passed their headless trigger gates after the 2026-07-11
reword/trim passes (9/9 and 6/6); scope-fence triggers ~60–67% by description
with a recorded inline-code ceiling (DEAD-1 — the `hooks/` pack is the lever
there); the four 2026-08-03 candidates cleared the fire bar on
description-testing prompts with zero over-fires anywhere
(`results/2026-08-03/trigger-evals/`). Behavioral value is measured for the
retired pair (Decision 7) and the governors (Phase 2), unmeasured for the
candidates. The dated record of what carries each discipline on which model is
[`evals/model-capability-register.md`](evals/model-capability-register.md);
open items are tracked in the 2026-08-10 review
(`results/2026-08-10/instruction-review/REPORT.md`).
