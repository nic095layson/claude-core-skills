# The "product output" skill — survey and proposal (2026-08-10)

> **Addendum, same day:** the owner clarified that "product output" meant
> **image generation, particularly photo editing** — the re-scope this
> report's bounds anticipated (assumption A1). The image-focused survey and
> proposal live in [`../image-output-skill/REPORT.md`](../image-output-skill/REPORT.md).
> This report stands as general context; its decision sheet remains
> owner-gated and unexecuted.

**Owner request (near verbatim):** "research what is the most powerful and
best product output skill.md — propose to me what is the cleanest and most
legit for you to implement here."

**What was analyzed:** the external skill ecosystem's strongest
output/deliverable-producing skills (primary sources fetched 2026-08-10:
`github.com/anthropics/skills`, Anthropic's skill-authoring best-practices at
`platform.claude.com`, `github.com/obra/superpowers`,
`github.com/pbakaus/impeccable`; marketplace rankings treated as leads only),
against this library's 18 skills and this account's live install footprint
(`ls /root/.claude/skills`, this session).

**Method:** plan-gate opened the task (goal, A1, success criteria committed
before authoring); after-report's claim-check applied to every external claim
(blogs = leads, primary sources fetched and quoted); the coverage gap was
verified mechanically (grep over all When-NOT sections and skill bodies);
the proposed draft was linted (`lint_skill.sh` → PASS, zero warnings, two
runs) and the full deliverable set was adversarially graded against the
pre-committed criteria before delivery — the pass caught and fixed three
self-consistency defects (eval-gate counts, a premature path claim, this
method line's own ordering claim). Proposals only — nothing was installed.

**Headline:** the "most powerful product output skills" in the ecosystem are
Anthropic's own document skills (docx/pptx/xlsx/pdf) — and this account
already has them installed, so there is nothing to buy there. What no skill
here or elsewhere in the footprint owns is the **finish line**: choosing the
right format, composing the applicable standards, running a
validate-fix-repeat pass, and handing over a real dated file instead of a
chat blob. The cleanest, most house-legit implementation is a thin
fresh-authored router/checklist skill, `product-output` (draft attached,
lints PASS, evals authored, UNMEASURED) — adoption gated on the owner and on
trigger measurement, per house law.

---

## 1. The survey — what "best product output skill" means out there

| Candidate | What it is | Verdict for this library |
|---|---|---|
| Anthropic document skills (`anthropics/skills`: docx, pptx, xlsx, pdf) | The production-grade skills behind Claude's real file outputs; 167.3k★, source-available | **ALREADY OWNED** — installed in this account's personal scope |
| Anthropic authoring doctrine (validator loop, template pattern, examples pattern) | The published patterns that make output skills powerful | **FOLD-DON'T-ADD** — ideas folded into the proposal; no text vendored |
| `obra/superpowers` (269.8k★, MIT) | A full development *methodology* (brainstorming → plans → review) | **NOT NEEDED** — process ground the governors already own; consistent with passing on external process libraries (2026-07-13, 2026-08-03) |
| `pbakaus/impeccable` (57.4k★, Apache 2.0) | Frontend design-quality system; `/impeccable polish` = "final pass … shipping readiness" | **NOT NEEDED** as a dependency — frontend-only, overlaps installed frontend-design + brand-standard; its polish framing *corroborates* the finish-line gap |
| Marketplace "best skills" lists (Taskade, Composio, Firecrawl, claudeskills.info …) | Blog rankings | **LEADS ONLY** — but they converge on the same story: document skills + methodology + design |

Evidence for the load-bearing rows:

- **Anthropic document skills exist and are the flagship output skills.**
  EVIDENCE: `github.com/anthropics/skills` (fetched 2026-08-10) lists
  `skills/docx`, `skills/pdf`, `skills/pptx`, `skills/xlsx` as
  "source-available document creation & editing skills"; repo at 167.3k★ /
  19.9k forks, with `spec/` and `template/` directories.
- **They are already installed here.** EVIDENCE: `ls /root/.claude/skills`
  (this session, 2026-08-10) → `docx`, `pptx`, `xlsx`, `pdf`,
  `frontend-design`, `pdf-extract` present alongside the governors and
  standards. Per-environment fact; re-enumerate live on other surfaces.
- **The doctrine that makes output skills powerful is published.** EVIDENCE:
  Anthropic best-practices (platform.claude.com, fetched 2026-08-10) —
  feedback loops: "Run validator → fix errors → repeat … This pattern greatly
  improves output quality"; template pattern ("templates beat prose");
  examples pattern ("Examples convey the desired style and level of detail to
  Claude more clearly than descriptions alone"); eval-first development
  ("Create evaluations BEFORE writing extensive documentation").
- **Star counts** are as displayed on fetch date (2026-08-10); GitHub renders
  rounded figures. Superpowers 269.8k★ / impeccable 57.4k★. EVIDENCE (that
  the pages so state), not a quality measurement.

Demotion conditions (per the report contract): ALREADY OWNED would demote if
the installed copies turn out to be stale or absent on the owner's primary
surfaces (check: `ls ~/.claude/skills` there). NOT NEEDED for superpowers /
impeccable would flip if the owner's work mix shifts toward greenfield
frontend shipping or if a governor is retired leaving process ground bare.

## 2. The gap — what nothing owns (and how that was verified)

Mechanical check (grep over all 18 skills, 2026-08-10):

- `adversarial-verify` owns **grading** the deliverable ("grade it against the
  success criteria", "Report faithfully — the delivery contract") — not
  format choice or packaging. EVIDENCE: its body, lines 44/51/97.
- `brand-standard` owns **voice/look** in David's name; `after-report` owns
  one genre's **content contract** (analysis reports); the document skills
  own **mechanics** per format.
- `application-tailor` already routes its one lane's finish line ("hand …
  file output to the document skills" — its description). No skill claims
  the general question: *which format, which standards compose, and what does
  a proper handover look like?*

INFERENCE (stated plainly): the gap is **coverage-inferred, not
failure-measured** — `.claude/LESSONS.md` records no incident of a fumbled
delivery. The house founding rule is that a skill earns its place only where
disciplined and default behavior *measurably* differ; whether that difference
exists at the finish line is exactly what the attached eval set would measure
before adoption.

## 3. The proposal — `product-output`, authored fresh in house style

Draft: [`draft/product-output/SKILL.md`](draft/product-output/SKILL.md) —
lints **PASS, zero skill-content warnings**
(`bash .claude/skills/diagnostics-and-tooling/scripts/lint_skill.sh …`,
2026-08-10); description 998 chars (≤1000 house target under the verified
1024 platform cap); 147 lines (house governor range 100–170).
Trigger cases: [`draft/evals/product-output.json`](draft/evals/product-output.json)
— 5 should-fire + 3 should-not, self-contained prompts per INC-2/INC-8,
grading block committed 2026-08-10, **NOT YET RUN**.

What it is: a thin finish-line standard — classify the deliverable → route to
the owning skills (a five-row table; composition, never duplication) → fix
the shape with a template/example → validate-fix-repeat → verify
(adversarial-verify owns the grading) → hand over a real dated file with a
3–6 line delivery manifest ending in a "not checked" line. Anti-ceremony
valve: chat answers, code edits, and drafts are not deliverables; small
deliverables get a two-line manifest.

Why this shape is the cleanest and most legit here:

- **It adds only the unowned step.** Every other layer routes to its owner —
  no restated rules to drift (architecture-contract Decision 2's corollary,
  applied at the delivery layer).
- **It is authored fresh, ideas-only.** House precedent: every external
  candidate this library evaluated was passed on in favor of fresh authoring
  (2026-07-13, 2026-08-03); the validator-loop/template/examples patterns are
  folded as ideas with provenance, no vendored text.
- **It respects the trigger lessons.** DEAD-1 taught not to bet on
  auto-triggering for process skills; the description leans on explicit
  deliverable phrasings ("ship it", "final version", "export as docx"), and
  the skill is equally usable invoked by name. Adoption as anything more than
  a project skill waits on measured trigger rates.
- **It is UNMEASURED and says so.** Volatile-facts section dates every claim;
  the eval set exists before any adoption decision (invariant 2:
  pre-commitment ordering).

## 4. Bounds — what this analysis did NOT cover

- Single-pass survey, US-only search; niche or unlisted skills may exist that
  no fetched source names. The four fetched repos/docs are the primary
  sources; everything else was treated as leads.
- "Product output skill" was interpreted per assumption **A1** as *a skill
  governing the final deliverable a session hands over*. The survey supported
  A1 (the ecosystem's "output" skills are exactly document/design/delivery
  skills), but if the owner meant a specific artifact by that name, this
  report re-scopes.
- No trigger or behavioral evals ran in this session — the draft's value is
  argued, not measured. The 2026-08-03 candidates' history shows survey-clean
  drafts can still need INC-8-style repairs once runs happen.
- Chat history from other sessions is not visible; "no recorded delivery
  failure" means the repo's ledger records none.
- Install-footprint facts are for this cloud session's environment; the
  owner's Mac and claude.ai surfaces were not enumerated (install-and-surfaces
  law: capabilities don't travel).

## 5. Decision sheet (owner calls — nothing below was executed)

| # | Option | Cost | When it pays off |
|---|---|---|---|
| A | **Adopt `product-output` as a candidate**: move draft → `.claude/skills/product-output/`, evals → `evals/`, README row; run the 60-run trigger protocol from `results/2026-08-03/trigger-evals/` | one move + one eval session | every deliverable handover, if measurement confirms the gap |
| B | Fold the validator-loop + examples doctrine into `skill-authoring` as a body edit | a gated wording pass (research-methodology) | every future skill authored |
| C | Do nothing | zero | the pieces (document skills + standards + verify) already exist; the gap stays coverage-inferred |

Recommended: **A**, with B flagged as adjacent work (scope-fence: it was
noticed, not asked for — it needs its own gate). A and C are both honest
calls; what would settle it is the eval run A includes.

## 6. Provenance

Produced 2026-08-10 by the Claude Code cloud session on branch
`claude/product-output-skill-research-jt42nu` (owner-requested research).
Sources, all fetched 2026-08-10: `github.com/anthropics/skills`,
`platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices`,
`github.com/obra/superpowers`, `github.com/pbakaus/impeccable`; leads:
Taskade / Composio / Firecrawl / claudeskills.info rankings (not relied on).
Local evidence: `ls /root/.claude/skills`, grep over `.claude/skills/*/SKILL.md`,
`lint_skill.sh` output, `.claude/LESSONS.md`. Re-verify volatile claims by
re-fetching the four primary sources and re-listing the live skills
directory. No skill, eval, hook, or config was installed by this report —
draft and proposals only.
