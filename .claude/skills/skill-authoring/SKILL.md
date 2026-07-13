---
name: skill-authoring
description: >-
  How to author a NEW skill in this house style — for this library or any
  project — or restructure an existing one — naming rules, the description-as-trigger contract (WHEN /
  quoted phrases / NOT clause), body structure (purpose, procedure, output format,
  rules, edge cases), the required house sections (date-stamped volatile facts,
  When-NOT, Provenance), and the end-to-end checklist from "choose scope" to
  "verified live". Use when you hear "write a new skill", "add a governor", "author
  a SKILL.md", "how should the description be worded", or "what sections does a
  skill need". Do NOT use for what a skill even is (domain-reference), diagnosing a
  misbehaving skill (debugging-playbook), install/packaging mechanics
  (install-and-surfaces), proving a wording change helped (research-methodology),
  or whether the change preserves the library's design (architecture-contract).
---

# Skill Authoring

Every axis you set when authoring a skill in this library, and the checklist for
shipping one. Audience: a mid-level engineer or Sonnet-class model who has never
authored a skill (concepts live in domain-reference — read that first if needed).

## Axis 1: `name` and placement

- kebab-case; says what the skill is FOR, not how it works (`plan-gate`, not
  `pre-task-checklist-protocol`). A reader must route correctly from the name alone.
- `name:` in frontmatter equals the directory basename exactly.
- Placement IS correctness: `.claude/skills/<name>/SKILL.md`, nowhere else — a
  perfect file elsewhere fails silently (invariant 8; source incident `6dc366f`).

## Axis 2: `description` — the trigger contract

The single highest-leverage text you will write. Three jobs; skipping any one
makes the skill misroute:

1. **State WHEN to fire** — the situation in plain terms, not just keywords, so
   the model can match by situation.
2. **Quote concrete trigger phrasings** — several literal wordings a user or
   session state would present.
3. **State when NOT to fire** — the nearest look-alike situations, each pointing
   to the sibling skill that owns it. The NOT clause is the part authors omit
   most, and its absence is how near-miss prompts over-fire.

House rules: **write the description before the body** (if you cannot say when it
fires, the scope is wrong — stop); no marketing language (routing metadata, not a
pitch); lean pushy on WHEN for governance skills (skills under-trigger by default)
and lean strict on NOT (the anti-ceremony invariant pushes back). Size class:
**the platform spec caps `description` at 1024 characters (verified 2026-07-11) —
this is a hard limit; a longer description is rejected on upload to claude.ai
(Claude Code headless was observed to tolerate up to ~1322 chars, but do not rely
on it).** Author to **≤1000 chars** to keep margin under the cap. This library's
descriptions measure 100–165 words (mean ~128, 2026-07-11) — aim for the low end;
every installed description is permanent context, so each word must earn its
routing value. (An earlier 60–120 target proved unrealistic for three-job
descriptions; changing existing descriptions to chase a number is a gated wording
edit, not a cleanup — but trimming to satisfy the 1024 cap still requires
re-running the eval set, since a shorter description is a new variant:
2026-07-11 all five governors were trimmed ≤1000 and re-passed, see
`experiments/hypothesis-2026-07-11-length-compliance.md`.)

## Axis 3: body structure, in order

| Part | Requirement |
|---|---|
| Purpose paragraph | 1–2 paragraphs: what this is, WHY it exists (the failure it prevents), what the reader sees. The why is not decoration — a model that understands the reason applies the rule beyond its examples. |
| Terms | Define every term once, up front, if the skill uses any word in a specific sense. |
| Procedure | Numbered steps, imperative runbook voice, copy-pasteable commands where commands exist. |
| Output format | If the skill's product has a required shape, show it in a fenced template — templates beat prose descriptions of templates. |
| Rules | The non-negotiables as a short list, **each with its reason**. A bare MUST teaches compliance; a reasoned rule teaches judgment. |
| Edge cases / proportionality | Where the procedure bends or is skipped — every governance skill needs its anti-ceremony valve here (invariant 5). |

Length: what the content honestly needs, no padding — governors here run
roughly 100–170 total lines (measured 2026-07-11; count includes frontmatter).

## Axis 4: required house sections

1. **Date-stamped volatile facts**, with the three confidence labels used
   consistently: *verified* (you ran it), *assumption* (numbered, in the
   domain-reference register), *candidate* (unproven idea). No oversell.
2. **"When NOT to use this skill"** — near the end, naming sibling skills. The
   library's boundary map is load-bearing; two skills claiming one question is a
   routing bug.
3. **"Provenance and maintenance"** — last section: what the skill derives from,
   one-line re-verification commands for volatile claims, and the conditions that
   should prompt an update. For governors, lineage to the source-repo cousin is
   mandatory (architecture-contract, Decision 6).

## The checklist — new skill, end to end

| # | Step |
|---|---|
| 1 | **Choose scope.** One skill answers one question. Check the boundary map (all When-NOT sections); if an existing skill owns the question, extend it instead of competing. |
| 2 | **Check the contract.** New governor, merge, or split → architecture-contract first (Decision 1/2, invariants). |
| 3 | **Write the description** — all three jobs — before any body text. |
| 4 | **Draft the body** per Axis 3 + Axis 4. |
| 5 | **Write trigger cases before polishing:** ≥3 should-fire prompts and ≥2 should-not-fire near-misses, with expected behavior each. Polishing before cases exist means editing toward prose you like, with no way to tell whether an edit helped (the source repo's hardest live problem, inherited). |
| 6 | **Lint:** `bash .claude/skills/diagnostics-and-tooling/scripts/lint_skill.sh .claude/skills/<name>` — expect PASS with zero skill-content warnings (the environment-level PyYAML WARN, printed on machines without PyYAML, is exempt — see diagnostics-and-tooling). The script does NOT check the NOT clause; verify that by eye. |
| 7 | **Live-fire per surface:** fresh session, skill in the loaded list, fires on a should-fire prompt, stays silent on a should-not. Never skip the negative case — a skill that fires on everything is worse than one that never fires. |
| 8 | **Gate the change:** behavioral edits to an existing skill go through research-methodology (pre-registered before/after); update the README inventory (a doc that describes the tree is re-checked when the tree changes). |

## Common authoring mistakes

- Trigger logic in the body (dead text — body loads after the match).
- Vague description ("helps with quality") — matches nothing reliably, everything
  occasionally.
- No NOT clause — the over-fire class.
- Prose instead of an output-format block.
- Repo-specific facts in a governor's procedure (violates Decision 2's corollary).
- Polishing before trigger cases exist (step 5's rationale).

## When NOT to use this skill

- Giving Claude new callable tools (wrap an API, database, or service as tools)
  → **mcp-builder** — a skill teaches a workflow; an MCP server exposes tools.
  Decide which artifact class the ask needs before authoring anything.
- Concepts (what is a trigger/frontmatter/.skill) → **domain-reference**.
- A finished skill misbehaves → **debugging-playbook**.
- Packaging/installing/verifying per surface → **install-and-surfaces**.
- Whether the design change is allowed → **architecture-contract**.
- Proving a wording hunch → **research-methodology**.

## Provenance and maintenance

Generalized 2026-07-11 from `nic095layson/claude` (commit `df6e198`)
`skill-authoring` (the axes, the three-job description contract, the checklist
spine, the mistakes list — carried with repo-specific steps replaced by this
library's) and `docs-and-writing` (house style: terms-once, tables over prose
walls, imperative voice). That repo's checklist remains the instance for changes
inside it.

Re-verify: lint script present — `ls .claude/skills/diagnostics-and-tooling/scripts/`;
boundary map intact — `grep -l "When NOT to use" .claude/skills/*/SKILL.md` (expect
one hit per skill directory — 20 as of 2026-07-13). Update when: the lint script's checks change, a house rule is overturned
by practice, or the platform adds frontmatter fields (via domain-reference first).
