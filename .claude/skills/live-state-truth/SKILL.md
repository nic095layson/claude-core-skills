---
name: live-state-truth
description: >-
  The doctrine that live state outranks every description of it — check the running
  system, the actual file, the real API, the current page, and never assert from
  documentation, memory, or "nobody touched it". Load this whenever you are about to
  state a fact about an environment you did not verify THIS session: what a config
  contains, whether a service is up, what version is installed, what an account can
  see, whether two copies match, what a repo's layout is, what an app supports.
  Load it before planning around any doc's claim, before answering "is X set up?",
  and whenever docs and observed behavior disagree. Do NOT load for judging whether
  finished work is GOOD (adversarial-verify — this skill proves states, not
  quality), for planning (plan-gate), or for recording a discovered drift's history
  (lessons-ledger — this skill detects, that one chronicles).
---

# Live-State-Truth

One law with two halves: **a document is a claim about the past; the live system
is the fact of the present. When they disagree, the system is right and the
document is a defect.** Docs, comments, READMEs, memories, and your own training
knowledge all describe how things were at some earlier moment — every one of them
rots silently, and none of them errors when it rots. The only statement you can
stand behind is one you verified this session, and the skill below is the
discipline of doing that cheaply.

## Terms (defined once)

- **Live state** — what a command, read, or observation returns right now:
  the file's bytes, the process list, the API response, the screenshot.
- **Drift** — two things that are supposed to agree no longer do (doc vs system,
  copy vs copy, artifact vs source). Nothing "broke", but the record lies until
  reconciled.
- **Volatile fact** — any true statement that a future action can silently make
  false. Volatile facts carry a date or they carry nothing.

## The doctrine: measure instead of eyeball

Eyeballing fails silently: two files that "look the same" can differ by a
trailing newline; a config that "looks fine" can miss the one key that matters.
House table — wrong way vs right way:

| Question | Wrong way | Right way |
|---|---|---|
| Are two copies the same? | Open both, skim | `diff a b` (silence = identical) or compare hashes |
| Is the output under the limit? | "Looks short" | `wc -w` / `wc -c` on the artifact |
| Does the config parse? | It has the right shape, ship it | Parse it with the real parser |
| Is the service healthy? | "It was running earlier" | Hit the endpoint / check the process now |
| Did the artifact drift from source? | "Nobody touched it" | Rebuild-and-diff, or hash both |
| What changed between versions? | Guess from dates | `diff -u` — the diff names the lines |
| Is X installed / available / connected? | Memory of the setup | `command -v X` / list the live integrations |

**When a check matters, script it once and rerun the script** — a script applies
the same criteria every time; a fresh pair of eyes does not. When you state a
system fact anywhere ("the copies agree", "the body is 814 words"), it should be
the output of a command, ideally date-stamped.

## The procedure

1. **Before asserting, ask: did I observe this, THIS session?** If not, it is a
   hypothesis. Either verify it now (usually one tool call) or label it
   explicitly ("per the README, unverified").
2. **Prefer the cheapest live check that settles the question.** `ls` beats
   reading the docs about layout; running `--version` beats the changelog;
   one screenshot beats remembering what an app can do.
3. **Date-stamp volatile facts** when you write them anywhere durable
   ("parity HOLDS as of 2026-07-11") — and treat a found date-stamp as an
   expiration notice, not a guarantee: rerun the check rather than trusting the
   line.
4. **On disagreement, the system wins.** Plan against observed behavior. Then
   treat the stale doc as a live defect: fix it if it is in scope, flag it via
   scope-fence if not, and record the drift per lessons-ledger either way —
   a drift you silently route around bites the next reader.
5. **Verify registration, not just content.** The costliest failure class this
   law comes from: an artifact that is perfectly correct but invisible to the
   system that should load it — right file, wrong directory, zero error output.
   After installing/deploying/configuring anything, confirm the system actually
   *sees* it (it loads, it fires, it appears in the list), not merely that the
   file exists.

## Environment boundaries — a special case of the law

Capabilities do not travel between environments; verify per surface. An
authorization, tool, or install that exists in one context (an account's cloud
integration, one machine's credentials, one repo's config) proves nothing about
the neighboring context. Recorded instance (this repo's ledger,
`.claude/LESSONS.md` INC-1, 2026-07-11): a GitHub authorization
granted to a cloud session was assumed live in a local session — the local
machine had no credentials at all, and every "can you just pull it?" assumption
failed until the local state was checked and set up. Before saying "I have access
to X" or "X is configured", check *here*, not somewhere X was once true.

## When NOT to use this skill

- Judging quality of finished work (correctness of logic, fitness of a design)
  → **adversarial-verify**. This skill proves what IS; that one judges what was
  MADE.
- Structuring a task before starting → **plan-gate** (which calls this skill for
  its "convert cheap unknowns into facts" step).
- The live check surfaced a problem outside the current task → **scope-fence**.
- Writing down the history of a detected drift → **lessons-ledger** (detection
  here, chronicle there).

## Provenance and maintenance

Generalized 2026-07-11 from `nic095layson/claude` (commit `df6e198`, 2026-07-10):
`diagnostics-and-tooling` (the measure-instead-of-eyeball doctrine and its table,
script-once-rerun corollary, date-stamped volatile facts — carried nearly
verbatim), `change-control` Gate D ("the doc must agree with the tree, not with
history"), `failure-archaeology` (the drift definition; INC-1 — the
correct-file-wrong-directory silent failure behind procedure rule 5; DRIFT-1 —
the stale README behind the doctrine). That repo keeps its own scripts; this
library ships a generalized copy of `lint_skill.sh` under
`diagnostics-and-tooling/scripts/` (its `check_release_parity.sh` deliberately
stays behind — see diagnostics-and-tooling's Provenance).

Re-verify lineage: `gh api repos/nic095layson/claude/contents/.claude/skills --jq '.[].name'`
— expect `diagnostics-and-tooling`, `change-control`, `failure-archaeology`.
