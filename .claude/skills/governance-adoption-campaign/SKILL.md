---
name: governance-adoption-campaign
description: >-
  The decision-gated campaign plan for this library's hardest live problem: the
  governors exist and lint clean (PASS ×13, 2026-07-11), but NOTHING yet proves
  they trigger when they should, stay silent when they shouldn't, and change
  session behavior — across surfaces. Load when asked to "prove the governors work", "run the trigger
  evals", "measure the skills", "roll the library out", "is plan-gate actually
  firing?", or when planning any investment in this library's reliability. Do NOT
  load for a single wording experiment (research-methodology is the method; this
  is the campaign that sequences it), for install mechanics (install-and-surfaces),
  or for fixing an individual misfire (debugging-playbook).
---

# Governance-Adoption Campaign

**The problem, stated honestly (as of 2026-07-11):** this library was authored,
linted, and lineage-checked in one session — but assumption A2 (descriptions
trigger reliably) and A1 (the five-way decomposition matches real use) are
unconfirmed, and weak-point 3 (enforcement is voluntary) means the only lever is
trigger quality. Until this campaign closes, "Claude is governed by these skills"
is a **candidate**, not a fact.

Work the phases in order; each ends at a gate with an expected observation and a
branch rule. Do not skip gates — a campaign that skips its gates is the
ungoverned behavior this library exists to prevent.

## Phase 0 — Install and registration (prerequisite)

**Do:** Runbook 1 of install-and-surfaces (five governors, personal scope) on the
primary machine.
**Gate:** a fresh session outside this repo lists all five governors.
**Expect:** 5/5 listed. **If fewer:** debugging-playbook §1 (placement class);
do not proceed — every later phase measures a skill that must first exist.
**Status: DONE for the primary machine, 2026-07-11** — the five governors were
copied to `~/.claude/skills/` and observed appearing in a live session's
available-skills list the same day (registration observed, not assumed).
claude.ai: files-uploaded 2026-07-11 (five spec-compliant .skill uploads
accepted by the validator, old versions removed first) — registration/firing
on that surface still unobserved; the 10-prompt smoke test is the check.
Other machines: OPEN. `ls ~/.claude/skills/` remains the
source of truth per machine.

**A distinction that keeps this campaign legal under the library's own laws:**
Phases 1–2 are **baseline measurement** of a stochastic system — they establish
what the current wording's trigger and behavior rates ARE, and their gates set
the bar for proceeding with rollout. They are NOT change acceptance: accepting an
*edit* stays under research-methodology R2 (any regression blocks, no averaging).
A governor passing Phase 1 at 5/6 is recorded as "fires at a measured ~83% on
this prompt set, dated", never promoted to "always fires" — and
architecture-contract invariant 3 ("no '3 of 4 passed, shipping it'") continues
to govern every before/after wording decision inside and after this campaign.

## Phase 1 — Trigger evals (the A2 test)

**Do:** for each governor, write 3 should-fire prompts (realistic task phrasings,
NOT the skill's name — "help me build a migration script for X" must fire
plan-gate without the words "plan gate") and 2 should-not-fire near-misses
(trivia; adjacent-governor cases). 25 prompts total. Run each in a fresh session,
2 runs per prompt (R1 floor; use 3 whenever a gate lands within one run of its
threshold), record fired/silent.

**Gate (measurement bar, per the distinction above):** per governor, ≥5/6
should-fire runs fire; ≥3/4 should-not runs stay silent. Record the actual rates
either way.
**Expect:** pass. **If a governor under-fires:** its description's WHEN is too
narrow or too abstract — description edit via research-methodology (one variable:
the description). **If it over-fires:** the NOT clause is weak — same route.
**If two governors co-fire constantly:** boundary defect — architecture-contract
weak-point 4, consider merging, but only with the owner.

**Status: RUN 2026-07-11 (Claude Code headless) — GATE FAILED for all five
governors.** Fresh-session `claude -p` runs, personal-scope install, FIRED
measured as an observed `Skill`-tool invocation in the stream-json transcript
(not introspection). should-fire trigger rates: plan-gate 1/6 (17%), scope-fence
2/6 (33%), adversarial-verify 0/6 (0%, prompt-confounded — its should-fire prompts
referenced artifacts absent from the fresh session), lessons-ledger 2/6 (33%),
live-state-truth 6/9 (67%, escalated to 3 runs as it landed within one run of the
gate). should-not-silent 100% for all (no over-fire; **zero co-fires** — no
boundary defect). The blanket-headless-artifact worry is refuted: auto-triggering
demonstrably occurs and varies by description. Triggering is phrasing-
deterministic (a phrasing fires every run or never). No descriptions were edited
(baseline measurement ≠ change acceptance); each under-firing governor has a
pre-registered rewording hypothesis in `experiments/hypothesis-<gov>.md` for a
research-methodology session. Full results + verbatim transcripts:
`results/2026-07-11/` (`RESULTS.md`). **Do not proceed to rollout on this
surface** until the rewordings are tested and the should-fire gate is met;
Phase 2 (behavioral) and other surfaces remain OPEN. A2 register row updated to
measured-with-date. eval set committed to `evals/` (Phase 3 artifact now exists).

**Status update 2026-07-11 (rewording A/B session, same model `claude-opus-4-8[1m]`,
same-condition OLD re-baselines via research-methodology):** the pre-registered
rewords were run. **3 of 5 gates now PASS** (were 0/5): **adversarial-verify 0/6→6/6,
plan-gate 0/6→9/9, live-state-truth 6/9→9/9** — all landed to repo + personal
(byte-identical). **2 still FAIL and were reverted to OLD:** scope-fence (NEW1 1/6→4/6 —
fixed the abstract-description prompts but the "restrain adjacent work while editing
concrete code" class is unfireable in headless under any wording) and lessons-ledger
(NEW1 78%, NEW2 80% — both large regression-free gains from 17% but under the ≥83% bar).
**Zero should-not regressions anywhere.** The two failures were escalated as an
architecture-contract open question: description-based triggering appears to have a
ceiling for triggers that require the model to pause mid-hands-on-work to consult a
governor; mechanical enforcement (hooks, weak-point 3) may be the only lever past it.
Rollout may proceed for the 3 accepted governors on this surface; scope-fence and
lessons-ledger remain gated. The 3 accepted governors' claude.ai `.skill` uploads are
now STALE (owner re-upload needed). Full A/B results + transcripts:
`results/2026-07-11/RESULTS-AB.md`.

**Status update 2 2026-07-11 (description-length compliance):** the platform caps
`description` at 1024 chars; the winning/adopted wordings exceeded it (plan-gate 1322,
lessons-ledger 1256, live-state-truth 1156, adversarial-verify 1144, scope-fence 1109).
All five were trimmed to ≤1000 (load-bearing surfaces + NOT clauses kept verbatim) and
re-run — **all held their rates, zero should-not regressions, zero co-fires**:
adversarial-verify 6/6, plan-gate 9/9, live-state-truth 9/9 (gates still PASS at the
shorter length); scope-fence and lessons-ledger adopted (owner decision) as better
wording while hooks are explored — gate stays FAIL, recorded as rates (scope-fence id1
0/2→3/5 flaky, lessons-ledger ~80%). Every governor description is now within the
claude.ai upload limit. Pre-registration + outcome:
`experiments/hypothesis-2026-07-11-length-compliance.md`.

## Phase 2 — Behavioral evals (does firing change anything?)

A governor that loads but doesn't alter behavior is decoration. For each
governor, two paired A/B prompts (with-library vs without, fresh sessions,
2 runs per prompt per arm — 4 with-library runs per governor): does plan-gate
produce the gate block before action? Does
adversarial-verify produce criteria-graded delivery? Does scope-fence flag the
planted adjacent bug instead of fixing it? Does lessons-ledger append on a
planted ~15-minute-plus diagnosis? Does live-state-truth check live state instead of
trusting the planted stale doc?

**Gate (measurement bar):** each governor shows its signature behavior in ≥3/4
with-library runs and its absence is visible in without-library runs. Record the
actual rates.
**Expect:** pass with visible deltas. **If a governor shows no delta:** body
defect, not trigger defect — the procedure isn't actionable enough; rewrite via
research-methodology. **If without-library runs ALSO show the behavior:** the
base model already does it; record the finding (ledger) and consider whether the
governor earns its context cost — take the answer to architecture-contract.

**Concurrency & isolation (mandatory — any phase whose arms mutate `~/.claude/skills/`):**
the "without" arm toggles the user's live, *global* governor install. **Only one
campaign run may do this at a time. Never run two campaign sessions against the same
machine's `~/.claude/skills/` concurrently** — two jobs swapping that shared dir empty
each other's installs mid-run and silently cross-contaminate both arms (2026-07-11: a
20/20-vs-5/20 with-arm firing gap for the same condition; `.claude/LESSONS.md` INC-4).
Before toggling: record a sha256 baseline, take a lockfile (or use an isolated
`CLAUDE_CONFIG_DIR`), restore under a trap, and verify byte-identical restoration. A
same-condition firing/behavior gap between two runs is a contamination smell — reconcile,
don't average.

**Status: RUN 2026-07-11 (Claude Code headless, `claude-opus-4-8[1m]`) — MIXED,
recorded honestly.** 40 paired A/B `claude -p` sessions (5 governors × 2 prompts ×
2 arms × 2 runs), signatures + without-predictions pre-registered and committed
before any run, each transcript graded in isolation. **Methodology correction
mid-run:** the first pass ran cwd *inside* this repo, so the repo's project-scope
`.claude/skills/` leaked all five governors into the "without" arm (plan-gate fired
there) — invalidated; re-run ("v2") with cwd outside the repo & `~/.claude`, where
the without-arm fired 0/20, confirming a true baseline. Governors moved out under a
trap-guarded script and restored **byte-identical** to a pre-recorded sha256 baseline
(without-arm state never left installed). **Behavioral results (with-lib / without-lib,
signature present):**
- **plan-gate 4/4 / 0/4 — GATE PASS, clean delta.** Full gate block with; questions +
  default script but no goal/criteria/phases without.
- **scope-fence 4/4 / 0/4 — GATE PASS, clean delta.** Fixes only the named bug and
  flags adjacent with; silently does the dangled cleanup ("also folded in the
  cleanups") without. **Notable:** failed the Phase-1 *trigger* gate yet passes the
  Phase-2 *behavioral* gate — fires 4/4 and behaves under the current trimmed wording.
- **adversarial-verify 4/4 / 0/4 (structured) — GATE PASS with caveat.** Criteria grid
  + named refutation with; the without arm is still a strong reviewer that catches the
  same bugs and says "not ready to ship" (0/4 *structured*, 4/4 *substantive*). The
  prompts cue review; the governor's marginal value here is discipline/structure, not
  bug-catching. Better future test: a should-verify-but-uncued prompt.
- **lessons-ledger 4/4 / 2/4 — GATE PARTIAL.** Structured ledger entry with; without,
  the base model records ~half the time via the **built-in Claude Code memory feature**
  (different format) and not at all the other half. Overlaps this governor's job →
  architecture-contract.
- **live-state-truth 4/4 / 4/4 — GATE FAIL (no delta).** The base model already probes
  live state and refuses the doc on these ("is it *actually* up right now") prompts.
  Fires but changes nothing observable → architecture-contract "earns its context
  cost?". Not spun as a pass.

All five FIRED 4/4 with and 0/4 without (clean trigger separation once cwd was fixed,
incl. scope-fence & lessons-ledger under the current wording). **2 clean behavioral
deltas, 1 structural, 2 base-model-already-does-it findings.** Full table, per-run
grades, verbatim transcripts, and the prompt-set limitation (3/5 signatures tested
with behavior-cueing prompts): `results/2026-07-11/phase2/` (`RESULTS-PHASE2.md`,
`PHASE2-GRADES.md`, `PHASE2-PREREG.md`, `transcripts_v2/`). Two operational incidents
(project-scope leak; concurrent-worker/summarized-context collision on
`~/.claude/skills`) recorded in `.claude/LESSONS.md`. **Route to
architecture-contract:** lessons-ledger (vs built-in memory) and live-state-truth (no
delta) earn a context-cost review; plan-gate and scope-fence are behaviorally
confirmed on this surface, dated. Other surfaces (interactive Claude Code, claude.ai)
remain OPEN.

**Reconciliation (2026-07-11):** this run collided with a second concurrent campaign
job (distinct job dirs — see INC-4). The clean out-of-repo dataset (`transcripts_v2/`,
without-arm fired 0/20) was **independently blind re-graded** (grader blind to arm) and
each verdict **adversarially verified** — cell-for-cell agreement on all 40 with the
in-situ grades; 0 verifier flips. The contaminated 5/20 with-arm was excluded from the
rates, retained as evidence. Authoritative reconciled summary crediting both runs:
`results/2026-07-11/phase2/RECONCILED-PHASE2.md`. Result unchanged: **plan-gate & scope-
fence PASS; adversarial-verify PASS (structured, substance caveat); lessons-ledger &
live-state-truth do not meet the clean gate → architecture-contract.**

**Cross-model discriminating test (Sonnet, 2026-07-11):** the two "base-model-already-
does-it" findings were re-run on `claude-sonnet-5` (both arms) to test the founding
premise that *smaller* models lack the native behavior — exact Phase 2 prompts/planted/
signatures reused, 16 fresh `claude -p` runs, cwd out-of-repo, lockfile held (isolated
`CLAUDE_CONFIG_DIR` rejected — breaks keychain auth here), restored byte-identical,
without-arm sentinel 0/8, blind-graded. **Hypothesis REFUTED for both.** Cross-model
signature rates (with · without): **live-state-truth** Opus 4/4·4/4, **Sonnet 4/4·4/4**
(no delta on either class); **lessons-ledger** Opus 4/4·2/4, **Sonnet 3/4·4/4** (partial
Opus delta does *not* reproduce — Sonnet base records *more* reliably via the built-in
memory feature; the one with-arm miss is the governor pausing for evidence under its
"no evidence, no entry" rule). Per the committed decision rule (without ≥3/4 →
RETIRE-CANDIDATE), **both → architecture-contract as owner decisions with the cross-model
table.** Bounding caveat carried forward: these prompts *cue* the behavior; the verdict is
"redundant on cued prompts across both model classes," not "worthless" — the uncued test
(governed behavior as the road not taken) remains the sharper outstanding measurement.
Full writeup + transcripts: `results/2026-07-11/phase2-sonnet/RESULTS-SONNET-DISCRIMINATING.md`.

## Phase 3 — Ongoing measurement and ratchet

**Do:** save all Phase 1–2 prompts and criteria as the library's standing eval
set: `evals/<governor>.json` at this repo's root, one JSON per governor, schema
by example (trigger case shown; behavioral cases put the signature behavior in
`expected_output`):

```json
{
  "skill_name": "plan-gate",
  "evals": [
    { "id": 1,
      "prompt": "help me build a migration script for our postgres schema",
      "expected_output": "FIRES: plan-gate loads; visible gate block (goal, knowns/unknowns, criteria, phased plan) precedes any file edit",
      "files": [] },
    { "id": 2,
      "prompt": "what's 15% of 80?",
      "expected_output": "SILENT: no governor loads; direct answer 12, no ceremony",
      "files": [] }
  ]
}
```

Every behavioral edit thereafter runs before/after against them
(research-methodology). Raise N beyond 2 as tooling makes runs cheaper.
**Gate:** the eval set exists in-tree and the first gated edit has used it.
**Exit criteria for the whole campaign:** A1 and A2 in domain-reference's
register flip from unconfirmed to **measured-with-date, with the observed rates
recorded** (not to an unqualified "verified" — see the Phase 1 distinction);
architecture-contract weak-points 1 and 4 close.

## Ranked solution menu (if resources are constrained)

1. **Phase 1 alone** — cheapest, kills the biggest risk (silent non-triggering,
   the founding-incident class). Do this even if nothing else happens.
2. Phases 1+2 on the two governors the owner leans on most (plan-gate,
   adversarial-verify), defer the rest.
3. The full campaign.

## Wrong paths, fenced off

- **Baking the governors into a CLAUDE.md blob "so they always apply".** Always-
  in-context prose has no triage valve — it applies to trivia too (invariant 5),
  costs context on every turn, and cannot be measured per-behavior. Rejected at
  design time (architecture-contract, Decision 1's rejected alternative).
- **Testing triggers by asking a session "would you have loaded plan-gate for
  this?"** Introspection is not observation; only fresh-session live fires count
  (validation doctrine inherited from the source repo).
- **Polishing descriptions before the eval prompts exist.** Editing toward prose
  you like, with no way to tell whether it helped — the exact rot this library's
  methodology exists to prevent (skill-authoring step 5).

## When NOT to use this skill

- One wording experiment → **research-methodology** (this campaign sequences
  many of them).
- Install steps themselves → **install-and-surfaces**.
- A specific observed misfire today → **debugging-playbook** §3/§8.
- Whether a campaign finding justifies redesign → **architecture-contract**.

## Provenance and maintenance

Authored 2026-07-11, generalizing the campaign form of `nic095layson/claude`
(commit `df6e198`) `eval-harness-campaign` (decision-gated phases, expected
observations with branch rules, ranked menu, fenced wrong paths) to this
library's hardest problem — which is adoption/triggering, not harness mechanics.
The eval schema in Phase 3 is that repo's, verified there 2026-07-10.

Re-verify: Phase 0 status — `ls ~/.claude/skills/` (expect the five governors);
campaign progress — `ls evals/` at this repo root (absence = Phase 3 not
started). Update when: any phase's gate is passed or failed (record the result
and date in-place), or a register row it targets flips status.
