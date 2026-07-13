# Operating procedure (updated 2026-07-13)

The one-page workflow for running this library across surfaces. Concepts live
in `domain-reference`; install mechanics in `install-and-surfaces`; this page
is the order of operations.

## 1. The standing footprint (always-on, unchanged)

| Surface | What's installed | Source of truth |
|---|---|---|
| Claude Code, any machine | `plan-gate`, `adversarial-verify`, `scope-fence`, `brand-standard` in `~/.claude/skills/` | README §Install |
| claude.ai | the same four as `.skill` uploads + the custom-instructions paste block | `instructions/claude-ai-custom-instructions.md` (acceptance PASS 7/7, 2026-07-12) |
| This repo | all 14 core skills auto-load as project skills | `.claude/skills/` |

Nothing added 2026-07-13 changed this footprint. That is deliberate:
always-on additions require measured evidence they earn per-session context
cost (architecture-contract Decisions 5/7).

## 2. The on-demand layer (adopted 2026-07-13)

When a task needs a domain capability, install it for the season of work,
then remove it:

1. **Check the registry first:** `external-skills/README.md` (13 vendored
   skills) and `external-skills/PACKS.md` (plugin/checkout packs + the
   rejected list). Don't hand-roll a capability that's already adopted.
2. **Vendored skill →** `tools/install-external-skill.sh <name>`
   (personal) or `--target <project>/.claude/skills` (project-scoped), or
   `--package <name>` for a claude.ai `.skill` upload.
3. **Pack →** run its PACKS.md runbook (document-skills and Trail of Bits are
   the pre-approved defaults for documents and security work).
4. **Register-then-verify, always:** fresh session, skill visible in the
   list, one live-fire trigger. Files on disk prove nothing.
5. **Uninstall when done** — the strict-tiered footprint is a practice, not a
   one-time decision.

Standing task→capability map: Office documents on Code → document-skills
plugin · security review → Trail of Bits (fallback: vendored
`owasp-security`) · multi-agent plan execution → `subagent-driven-development`
(+ `writing-plans`) · stubborn bug → `systematic-debugging` · external-facing
prose sweep → `avoid-ai-writing` (+ `brand-standard`, which always wins on
voice) · feature work in a dev repo → `test-driven-development`
project-scoped · YouTube research → `youtube-transcript`.

## 3. Change governance (what stays gated)

- Core-skill wording/body edits: `research-methodology` (pre-registered
  hypothesis, fresh-session A/B, N=2 floor, any-regression-blocks) +
  `architecture-contract` invariant check. This includes the four
  fold-don't-add grafts from the 2026-07-13 report — approved as candidates,
  NOT yet executed.
- Vendored external skills: never edited in place; re-vendor at a newer
  upstream commit and update `PROVENANCE.md`.
- The claude.ai paste block: any change invalidates the 2026-07-12
  acceptance — re-run the 7-row protocol after edits.

## 4. Maintenance cadence

| When | What |
|---|---|
| After any core-skill edit | `diagnostics-and-tooling` lint + Runbook 3 stale-copy sweep (installed copies are forks) |
| Quarterly | Re-scan BehiSecc/awesome-claude-skills (catalog snapshot with URLs in `results/2026-07-13/external-skill-analysis/analysis-result.json`); re-check vendored commits against upstream HEADs |
| When a domain becomes real (IaC, science, PM, job search) | Its pre-evaluated pack is already tiered in PACKS.md — install, don't re-research |
| Open items | governance-adoption-campaign trigger evals (A2 still open); the four gated folds; re-paste of the 4-pointer instructions block if not yet done |
