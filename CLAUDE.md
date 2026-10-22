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

Cloud sessions have no `~/.claude/CLAUDE.md` and no user settings; this repository
carries its own doctrine and its own enforcement (`.claude/settings.json` wires
`hooks/`). The block below is a verbatim copy of
`instructions/project-doctrine-block.md`; the guard fails if the two drift.

---- BEGIN BLOCK ----

## Operating doctrine (every session, every surface)

The core governors run on every non-trivial request here — **plan-gate** before the
first consequential action, **scope-fence** during the work, **adversarial-verify**
before delivering — and they are **loaded with the Skill tool, never applied from
memory**. Governor text already in context from an earlier task or from a compaction
does not count as loaded. Source of truth: `nic095layson/claude-core-skills`.

Four rules this project binds every session to, in addition to the governors:

1. **A question gets an assessment, not a fix.** When the owner asks whether something
   is right, or disagrees with a result, the deliverable is the assessment. A fix,
   candidate, rewrite, or dry run — even in scratch — waits until the owner asks for it.
2. **Method parameters are stated before the run.** Any data window, sample, cutoff,
   era, or baseline an analysis runs on is named to the owner in one line before the run
   that uses it, with its basis. A parameter inherited from a file's extent or a script's
   default is an assumption, not a choice.
3. **A stated requirement is not a build order.** "X is critical" says what the work
   must respect; it authorizes nothing new.
4. **Decisions come as options.** When there is a decision for the owner to make, offer
   2–4 options, each with a brief plain-language explanation, the recommended one listed
   first and marked "(Recommended)". Where the surface has clickable choices (Claude Code:
   the AskUserQuestion tool, with a preview card when comparing options helps), use them;
   otherwise a numbered list. Not for trivial choices or ones with an obvious default (state
   the default in one line), and never in an unattended run, where nobody is there to click:
   record the open decision in the report instead.

After a compaction: list the owner's open objections in one line before continuing;
a result the owner disputed stays disputed; reload the governors before the next
consequential action.

Enforcement: this repository's `.claude/settings.json` wires the governance hooks
(prompt trigger, Stop gate, first-write reminders, compaction protocol). They run in
Claude Code sessions that start inside this one repository, on the web included. A
cloud session with several repositories attached reads only plugin keys from each
repository's settings, not hooks (Claude Code settings documentation, read 2026-10-13);
there, this file and the plugin route carry the doctrine.

---- END BLOCK ----
