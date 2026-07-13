---
name: architecture-contract
description: >-
  The load-bearing design decisions of this governance library, each with its
  rationale, the invariants any edit must preserve, and the known-weak points
  stated plainly. Load BEFORE editing any governor's SKILL.md, adding or merging
  skills, changing what gets personally installed, or whenever you ask "why five
  separate governors?", "why not one big skill or a CLAUDE.md blob?", "what would
  break if I reworded this law?", or "which repo wins when rules conflict?". Do NOT
  load for authoring mechanics (skill-authoring), concept definitions
  (domain-reference), or whether an edit is in scope at all (scope-fence) — this
  skill answers "why is it built this way and what must stay true".
---

# Architecture Contract

What this library is: **the general form of the operational laws first written,
repo-scoped, in `nic095layson/claude`** — extracted 2026-07-11 on the owner's
instruction that those laws were always meant to govern Claude holistically, not
one project. Every decision below is load-bearing; edit against them knowingly or
not at all.

## Decision 1 — Five separate governors, not one mega-skill

**Rationale.** Triggering is per-description: a session verifying finished work
needs adversarial-verify's body, not 1000 lines of everything. Separate skills
load the right law at the right moment, keep each description sharp (a mega-skill's
description must say "always", which triggers never or always), and let each
governor evolve under its own eval set.
**Rejected alternative:** one `agent-discipline` skill — fenced off because its
trigger would be unfalsifiable and its body would defeat progressive disclosure.

## Decision 2 — Governors are project-agnostic; instances win locally

**The precedence law:** when working inside a project that carries its own
instance of a law (e.g. `failure-archaeology` as the lessons-ledger of
`nic095layson/claude`, its `change-control` gates as the scope-fence there), **the
project instance takes precedence in that project**; the governor supplies the law
where no instance exists.
**Rationale.** Instances encode verified local facts (paths, gates, incident
history) the governor must not duplicate — duplication is drift waiting to happen.
**Corollary:** no repo-specific fact may live in a governor's procedure. Lineage
sections may cite the source repo as history; procedure text may not depend on it.

## Decision 3 — Descriptions carry the whole trigger; every skill carries a NOT clause

Inherited from the source repo's hardest-won lesson class: a governance skill that
under-triggers is dead weight, and one that over-triggers erodes trust in the whole
library. Every description here states WHEN, quotes situations, and names where
near-miss cases go.

## Decision 4 — Anti-ceremony is a first-class law, not a caveat

Every governor contains a triage or proportionality rule (plan-gate's triage,
adversarial-verify's proportional pass, scope-fence's margin test, lessons-ledger's
no-padding rule). **Rationale:** the observed failure mode of governance systems is
not absence but bloat — rituals applied to trivia until the user disables the
library. The source repo pinned this with an eval (its case 3: "Council: what's 15%
of 80?" must skip ceremony and answer 12); this library inherits the doctrine as an
invariant.

## Decision 5 — Activation footprint: install the active governors personally; the eight support skills load per-project

**Rationale.** Every installed description sits in every session's context
(domain-reference, consequence 2). The governors govern all work and earn that
cost; the support skills (authoring, debugging, campaign, this contract) matter
only when working ON the library or on skills, which happens inside this repo where
they auto-load as project skills.
**Status:** assumption A3 in domain-reference — owner-adjustable, not doctrine.
**Amended 2026-07-11 by Decision 7:** the active set is three (plan-gate,
adversarial-verify, scope-fence).

## Decision 6 — Laws carry lineage

Every governor ends with a Provenance section naming its source-repo cousins and
which laws carried over. **Rationale:** the owner's explicit requirement at
extraction ("ensure that no operational prowess or laws are lost") is only
auditable if each skill declares what it carried; an unattributed law cannot be
checked against its origin.

## Decision 7 — Retirement of live-state-truth and lessons-ledger (2026-07-11, owner-decided)

The owner retired both governors from all installs (personal `~/.claude/skills/`
and claude.ai uploads) on the campaign's evidence: live-state-truth
RETIRE-CONFIRMED (zero behavioral delta in all eight cells, cued + uncued, Opus +
Sonnet — base models check live state natively); lessons-ledger inert (0/16
uncued firing, weak cued value against built-in memory — earns its cost in no
test, though its uncued verdict is formally INCONCLUSIVE, see weak-point 5).

**What survives retirement:** the doctrines remain true and citable — the
measure-instead-of-eyeball table, the drift definitions, the recording rule, the
`.claude/LESSONS.md` project-ledger convention all stay in force as *practice*,
carried by base-model behavior, platform memory features, and the remaining
skills' references. Only the always-in-context *skills* were retired, because
measurement showed the context cost buys no behavior change.

**Reversibility:** both SKILL.md files remain in this repo, marked RETIRED, with
their full eval history. Reinstate = copy back to `~/.claude/skills/` and re-run
the discriminating tests on the then-current models — base-model behavior is a
volatile fact; a future model class that stops checking live state re-opens this
decision.

**Deferred cleanup (flagged, not silently done):** the three active governors'
descriptions and bodies still contain NOT-clause pointers to the retired pair.
Harmless while retired (a routing pointer to an absent skill is a no-op), but the
next gated wording pass should reword them; that edit goes through
research-methodology like any other.

## Decision 8 — Capability skills are a third class, project-scoped by default (2026-07-13, owner-directed)

Six capability skills (frontend-design, pdf, docx, pptx, xlsx, mcp-builder)
added on the owner's request — runbooks for producing artifacts, not governors
and not library-support skills. Footprint within Decision 5's taxonomy:
**project-scoped by default**; promoting any of them to the personal install is
a separate owner call recorded here when made. claude.ai uploads are selective
(conflict audit 2026-07-13, `results/2026-07-13/`): frontend-design yes; pdf
conditional under a renamed package (name-collision with the surface's built-in
pdf skill); docx/pptx/xlsx/mcp-builder no — claude.ai's built-in document skills
own that surface, and duplicating them pays permanent context for shipped
capability (Decision 4's anti-bloat law applied to uploads).
**Deferred to gated wording passes** (flagged, not silently done): adding
workbooks/spreadsheets to brand-standard's artifact enumeration, and an
mcp-builder phrase in skill-authoring's description NOT clause — their body
When-NOT sections carry the routing meanwhile (2026-07-13).

## The invariants — what any edit must preserve

| # | Invariant | Breaking it looks like |
|---|---|---|
| 1 | Evidence definitions stay strict: no entry/claim without command output, path, diff, or dated observation | "Everyone knows" creeping into ledger entries or verification reports |
| 2 | Pre-commitment ordering: criteria/predictions/hypotheses written BEFORE acting/checking/running | Reordering plan-gate or adversarial-verify steps so grading follows results |
| 3 | Any-regression-blocks acceptance | "3 of 4 runs passed, shipping it" |
| 4 | Flag-don't-fix for adjacent work; approval is per-scope | "While I was here I also…" in a delivery |
| 5 | No ceremony on trivia (Decision 4) | A planning ritual on a one-step ask; a ledger padded with routine successes |
| 6 | Recording-rule thresholds (15-minute rule; drift-even-if-fixed; dead-ends-labeled-abandoned) | Softening "MUST append" to "consider appending" |
| 7 | Live state outranks records; volatile facts carry dates | Undated "the copies agree" anywhere in the library |
| 8 | Placement law: skills live at `.claude/skills/<name>/SKILL.md`, `name:` = directory | Any other layout — it fails silently (source incident `6dc366f`) |

An edit that relaxes an invariant is not an edit, it is a redesign — bring it here
first, and it needs the owner.

Scope note on invariant 3: it governs **accepting a change** (before/after,
OLD vs NEW). Baseline **measurement** of a stochastic system may use rate
thresholds (governance-adoption-campaign's gates) — measured rates get recorded
as rates, dated, never rounded up to "always".

## Known-weak points (stated plainly, as of 2026-07-11)

1. **Trigger reliability is unmeasured** (A2). The descriptions follow the house
   rules, but zero trigger evals have run. governance-adoption-campaign owns this;
   until it closes, treat "the governors fire when needed" as a candidate, not a
   fact.
2. **Governor boundaries overlap at the edges.** Verify-vs-detect
   (adversarial-verify vs live-state-truth) and detect-vs-record (live-state-truth
   vs lessons-ledger) are principled but will produce double-loads in practice.
   Acceptable cost; watch for genuine contradictions and record them in the ledger.
3. **Enforcement is voluntary at the skill layer.** A skill can instruct but not
   compel; a session can ignore a governor silently. The counters today are
   trigger quality (weak-point 1) and the owner noticing ungoverned behavior.
   Mechanical enforcement does exist one layer down on some surfaces — Claude
   Code hooks in `settings.json` can block or intercept tool calls — but this
   library deliberately ships as prose-only; wiring governors into hooks is a
   **candidate** hardening path, unexplored as of 2026-07-11.
4. **The five-way decomposition is unproven in use** (A1). If real sessions show
   two governors always co-firing or one never firing, merge or split — through
   this contract.
5. **Two governors flunk the context-cost review — owner decision pending** (routed
   here by governance-adoption-campaign Phase 2). Measured behavioral value of
   **live-state-truth** and **lessons-ledger**, across cued + uncued prompts and
   both model classes (Opus `claude-opus-4-8`, Sonnet `claude-sonnet-5`), fresh
   headless A/B, blind-graded, dated 2026-07-11:

   | governor | cued with·without (Opus / Sonnet) | uncued with·without (Opus / Sonnet) | verdict |
   |---|---|---|---|
   | live-state-truth | 4/4·4/4 / 4/4·4/4 | 4/4·4/4 / 4/4·4/4 | **RETIRE-CONFIRMED** (recommendation) |
   | lessons-ledger | 4/4·2/4 / 3/4·4/4 | 0/4·0/4 / 0/4·0/4 | **INCONCLUSIVE** (uncued) |

   **live-state-truth → RETIRE-CONFIRMED (recommended to owner, not yet executed).**
   No behavioral delta in any of the eight cells: the base model reads the real
   source (server.js/.nvmrc/package.json) and catches a doc's false port/version
   **even uncued**, cued or not, on both models. Privileging live state over a doc
   is baseline model behavior here, not governor-supplied. Removal is an owner call
   through this contract; the measurement supports it.
   **lessons-ledger → INCONCLUSIVE uncued.** With 0/4 and without 0/4 on both
   models: the governor **did not fire** on a self-encountered live failure (0/16
   uncued fires), and the base model did not spontaneously record the quick "fix and
   move on" bugs either — so the uncued test could not discriminate. Two honest
   readings, both kept: (a) the planted bugs were fixed fast (one self-hinted by the
   Python runtime) so neither arm judged them ledger-worthy — a prompt-design ceiling;
   (b) the deeper issue is that lessons-ledger doesn't trigger uncued, so it cannot act
   even when a lesson exists. Its cued value is also weak (Phase 2 partial; Sonnet
   without ≥ with, via the built-in memory feature). Not a RETIRE by the committed
   rule, but no evidence it earns its cost. Overlaps weak-point 2 (detect-vs-record)
   and the built-in memory feature. Evidence: `results/2026-07-11/phase2-uncued/`
   (`RESULTS-UNCUED.md`), `results/2026-07-11/phase2-sonnet/`, `results/2026-07-11/phase2/`.

## When NOT to use this skill

- Mechanics of writing/editing a skill → **skill-authoring**.
- What a skill even is → **domain-reference**.
- Whether your current edit is in scope → **scope-fence**.
- Proving a proposed redesign is better → **research-methodology** (hypothesis
  first), then here for the invariant check.

## Provenance and maintenance

Authored 2026-07-11 at extraction from `nic095layson/claude` (commit `df6e198`);
Decisions 3, 4, and the placement invariant generalize that repo's
`architecture-contract`, `skill-authoring`, and INC-1. Decisions 1, 2, 5, 6 are
this library's own, made this date, owner-instructed ("break out the skills into a
separate repo for all of your operations", "no operational prowess or laws lost").

Re-verify: invariant 8 — `ls .claude/skills/*/SKILL.md` at this repo root; source
lineage — `gh api repos/nic095layson/claude/contents/.claude/skills --jq '.[].name'`.
Update when: any register row in domain-reference settles (fold the answer in), a
weak point closes (say so, dated), or practice overturns a decision (record the
old decision as fenced, per lessons-ledger).
