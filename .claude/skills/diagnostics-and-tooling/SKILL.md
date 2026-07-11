---
name: diagnostics-and-tooling
description: >-
  The runnable mechanical checks for this library — lint a skill directory
  (frontmatter valid, name matches directory, trigger language present, house
  sections in place) and audit the whole library in one loop. Load when you need a
  MECHANICAL check on artifacts: "lint this skill", "is the frontmatter valid",
  "does the name match the directory", "audit the library", "check every skill" —
  and before shipping any new or edited SKILL.md. Do NOT load for the
  measure-instead-of-eyeball doctrine itself (live-state-truth owns the doctrine;
  this skill ships its tools), for judging whether a skill BEHAVES well
  (research-methodology + live-fire tests), or for fixing what the checks find
  (skill-authoring / debugging-playbook) — this skill detects and measures, it does
  not fix or grade behavior.
---

# Diagnostics and Tooling

The tool rack for live-state-truth's doctrine: when a check matters, script it
once and rerun the script — a script applies the same criteria every time; a
fresh pair of eyes does not. Everything here is mechanical (exists, parses,
matches); nothing here judges whether a skill is *good*.

## Script: `scripts/lint_skill.sh`

Mechanical lint of one skill directory. Catches the mistakes that make a skill
silently fail to load or violate house style — by construction it catches the
founding incident class (name/placement, source incident `6dc366f`).

**Usage** (from this repo's root):

```bash
bash .claude/skills/diagnostics-and-tooling/scripts/lint_skill.sh .claude/skills/<name>
```

**Checks.** FAIL (exit 1): `SKILL.md` missing; frontmatter absent or unparseable;
`name` missing/empty; `description` missing/empty; `name` ≠ directory basename;
description contains no trigger language (a description that never says WHEN is a
defect, not a style nit); body under 50 words. WARN (exit 0): missing
`Provenance` section; missing `When NOT to use` section; PyYAML unavailable
(falls back to a built-in parser covering the house two-field frontmatter —
patched into this library's copy 2026-07-11 because a stock macOS `python3`
lacks PyYAML; install PyYAML for full YAML validation).

**Exit codes.** `0` PASS (warnings allowed) · `1` any FAIL · `2` usage error.

**What it does NOT check** — verify these by eye: the description's NOT clause;
repo-specific facts leaking into a governor's procedure (architecture-contract,
Decision 2); output-format blocks where the product has a required shape.

**Verified 2026-07-11 on this library:** all 13 skills PASS with 0 FAILs each;
the failure path was verified against a synthetic skill (wrong name, bare
description, 2-word body → 3 FAILs, exit 1).

## The library audit loop

```bash
for d in .claude/skills/*/; do
  bash .claude/skills/diagnostics-and-tooling/scripts/lint_skill.sh "$d" | tail -1
done
```

Run before any push and after any restructuring. Expect PASS × 13; any FAIL
blocks the push (scope-fence: fixing the failing skill is a blocking dependency
of shipping, hence in scope).

## Manual fallbacks (when the script is unavailable)

| Check | Command |
|---|---|
| Placement + inventory | `ls .claude/skills/*/SKILL.md` |
| Frontmatter shape | `head -4 <skill>/SKILL.md` — expect `---`, `name:`, `description:` opening |
| Name = directory | `grep '^name:' <skill>/SKILL.md` vs the directory basename |
| Copies identical | `diff a b` or `shasum -a 256 a b` — never skim |
| House sections | `grep -c 'When NOT to use\|Provenance' <skill>/SKILL.md` — expect 2 |

## When NOT to use this skill

- The doctrine behind these tools → **live-state-truth**.
- The check failed and you need to fix the skill → **skill-authoring** (structure)
  or **debugging-playbook** (behavior).
- Proving a wording change improved behavior → **research-methodology**.
- Installing or packaging what passed → **install-and-surfaces**.

## Provenance and maintenance

Script carried 2026-07-11 from `nic095layson/claude` (commit `df6e198`)
`diagnostics-and-tooling/scripts/lint_skill.sh`, with one change: the PyYAML
fallback parser (this library's environments include stock macOS python3 without
PyYAML — an instance of live-state-truth's environment-boundary rule). The
source repo's second script (`check_release_parity.sh`) is release-artifact
specific and stays there; this library's parity needs are covered by the manual
fallback table until it ships zipped artifacts.

Re-verify: `bash .claude/skills/diagnostics-and-tooling/scripts/lint_skill.sh
.claude/skills/plan-gate` — expect PASS; audit loop above — expect PASS × 13.
Update when: the script's checks change (keep this doc in sync — the script is
the source of truth), a new script lands in `scripts/`, or the library gains
zipped release artifacts (then port `check_release_parity.sh`).
