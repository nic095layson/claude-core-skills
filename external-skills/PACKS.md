# Capability packs — install runbooks (2026-07-13)

Packs adopted by tier but **not vendored** — too large, or license-restricted.
Each installs on demand and uninstalls after the season of work. Commands
verified against the packs' own repos on 2026-07-13; re-check before relying
(upstreams move).

## MUST ADD

### Anthropic official document skills (docx, pdf, pptx, xlsx)
- **Why:** Claude Code has zero Office-document capability; these are the
  production-grade pipelines (OOXML unpack-edit-repack + validation,
  tracked changes, PDF forms, xlsx recalc). claude.ai already ships them
  natively — this install is for the Claude Code surface only.
- **License:** © Anthropic, all rights reserved (governed by your Anthropic
  terms). **Never vendor into this repo.**
- **Install (Claude Code):**
  ```
  /plugin marketplace add anthropics/skills
  /plugin install document-skills@anthropic-agent-skills
  ```
- **Skip** the `example-skills` plugin from the same marketplace
  (web-artifacts-builder / internal-comms / webapp-testing overlap built-ins
  and brand-standard).

## HIGHLY RECOMMEND

### Trail of Bits security skills (75 skills)
- **Why:** the definitive security pack — differential-review, fp-check,
  CodeQL/Semgrep orchestration, variant analysis, fuzzing, constant-time
  audits. Evaluated at HEAD `cfe5d7b` (2026-06-30).
- **License:** CC BY-SA 4.0 — **plugin-only; never copy its text into this
  repo** (ShareAlike would attach to derivatives).
- **Install (Claude Code):**
  ```
  /plugin marketplace add trailofbits/skills
  ```
  then `/plugin install <name>@trailofbits-skills` per skill group needed
  (start with `differential-review` and `fp-check`).

## NICE TO HAVE — install when the domain becomes real

| Pack | Trigger to install | Install | License / caution |
|---|---|---|---|
| K-Dense-AI/claude-scientific-skills (149 skills) | science/bio/chem/data work appears | clone + project-scope only the needed skill dirs | MIT |
| jeffallan/claude-skills (66 stack packs) | deep work in a specific stack (the postgres-pro references are the standout) | clone + cherry-pick the one stack dir | MIT |
| hashicorp/agent-skills | first Terraform/Packer task | `/plugin marketplace add hashicorp/agent-skills` | MPL-2.0 |
| product-on-purpose/pm-skills (68 skills) | sustained PM lifecycle work | clone + cherry-pick | Apache-2.0 |
| santifer/career-ops | active job-search campaign | clone, project-scope; **brand-standard overrides its voice/typography assets — its voice-dna.md, fonts/, cv templates must not be used for David-named output** | MIT |
| daxaur/openpaw | personal-ops automation **on a local Mac only** (useless in cloud sessions) | follow repo README | MIT |
| avifenesh/agnix (432-rule config linter) | this repo grows hooks/MCP/plugin configs worth linting | `cargo install agnix-cli` + its skill | MIT/Apache-2.0 |
| sanjay3290/ai-skills — postgres/notebooklm/elevenlabs slices ONLY | those specific tools enter use | clone + cherry-pick those dirs | Apache-2.0. **Never use its Google Workspace block: OAuth routes through a third party's cloud function with a hardcoded client ID (gmail/scripts/auth.py), and Gmail/Drive/Calendar connectors already cover it.** |

## Explicitly rejected (do not revisit without new evidence)

- ComposioHQ/awesome-claude-skills collection — etiquette-prose class that
  measurement retired (live-state-truth standard).
- superpowers: brainstorming, executing-plans, dispatching-parallel-agents,
  requesting-code-review, using-superpowers, verification-before-completion —
  owned by plan-gate / adversarial-verify / platform built-ins.
- fable-loop — restates plan-gate + adversarial-verify over built-in
  orchestration.
- BehiSecc/awesome-claude-skills — a bookmark, not a dependency; re-scan
  quarterly (full ~170-entry catalog with URLs:
  `results/2026-07-13/external-skill-analysis/analysis-result.json`).
