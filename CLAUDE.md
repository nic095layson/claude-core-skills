# claude-core-skills

A governance library. The skills under `.claude/skills/` auto-load in this repo.

**Read `README.md` for what each skill is** — this file deliberately does not list
them. A doc that enumerates the tree goes stale the moment the tree changes, and
this repo has an incident about exactly that (`.claude/LESSONS.md` INC-11).

## Before you edit anything here

| Editing… | Gate |
|---|---|
| A governor's SKILL.md | `architecture-contract` (invariants) first, then `skill-authoring` |
| A `description:` field | That is the **trigger surface**. `research-methodology` — pre-register, A/B, N=2 floor |
| Anything, before you commit | `bash .claude/skills/diagnostics-and-tooling/scripts/guard_essentials.sh` |

The guard asserts what the 2026-08-11 audit established as essential: every skill
lints, every governor mechanism is present, GAUNTLET and the receipt law survive
in the paste block, no duplicate ledger keys, and **no unacknowledged deletions**.
Run it before AND after any substantial change — a before-run is what makes the
after-run mean anything.

## Conventions

- **Evidence** → `results/<YYYY-MM-DD>/<topic>/`. Raw artifacts commit beside the
  report, never summarized away.
- **Experiments** → `experiments/hypothesis-<date>-<slug>.md`, written *before*
  any run.
- **Incidents** → `.claude/LESSONS.md`. New keys are `INC-YYYY-MM-DD-nn`; the
  older integer keys stay valid via the concordance at the top of that file.
  **Never renumber an existing entry** — other files cite them.
- **Volatile facts carry dates.** An undated "the copies agree" is a defect.
- **Deletions** are declared in `.guard-acknowledged-deletions` or the guard fails.

## Two things worth knowing before you trust a check

1. **A failing check earns the same scrutiny as a failing artifact.** On
   2026-08-12 a link checker reported 25 dangling references (all false), a grep
   reported two clauses missing (both present), and the guard reported no
   deletions while three sat staged. Each was the checker, not the repo. This is
   `adversarial-verify` rule 9, and it was written from a *different* project's
   pixel detector months earlier.
2. **A settings box is live state; this repo is not a record of it.** The
   claude.ai instructions block and the account-synced skills can silently
   diverge from what is here. Diff against what is actually deployed, not against
   a branch.

## Surfaces

Claude Code has a hook layer (`hooks/`); **claude.ai does not**. Anything relying
on mechanical enforcement is Claude Code only. On claude.ai the carrier is
`instructions/claude-ai-custom-instructions.md`, which must be re-pasted by the
owner to take effect — merging it here changes nothing on that surface.
