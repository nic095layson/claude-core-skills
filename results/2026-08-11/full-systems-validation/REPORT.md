# Full systems validation and integrity check (2026-08-11)

**Owner request (near verbatim):** "Merge. Conduct full Claude Core Skills
systems operating procedure, validation and integrity testing. Provide after
report" — following a session that had installed the receipt-law Stop hook,
diagnosed and fixed a bash-3.2 heredoc parse bug in it (commit pending, see
Merge below), and built a `SessionStart` sync hook to keep this machine's
install from drifting off the repo.

**What was analyzed:** the `claude-core-skills` repo at
`/Users/davidlayson/Documents/GitHub/claude-core-skills` (commit `6c2ef9c` at
completion), all 19 of its skills, its two hook scripts and their selftest,
and this machine's live install (`~/.claude/hooks/`, `~/.claude/skills/`,
`~/.claude/settings.json`) — the full chain from source repo to what actually
runs on this Mac.

**Method:** plan-gate opened the task (goal, one assumption on scope
registered as A1, success criteria C1–C8 committed before running any check,
this session). Every check below is a command run this session with its
output kept, not recalled or assumed — merge via `git commit`/`git push`;
skill mechanics via the repo's own `diagnostics-and-tooling` lint script run
against all 19 skills; hook behavior via `hooks/selftest-receipt-law.sh`;
install parity via direct `diff`; config integrity via `jq`; repo/remote sync
via `git fetch` + `git status -sb`. Scope is bounded by A1 below.

**Headline:** **all 8 committed criteria pass.** The pending fix is merged
and pushed (`6c2ef9c`), the hook selftest is 10/10, all 19 skills lint clean,
this machine's install is in full parity with the repo, `settings.json` is
schema-valid with all three hooks wired to real executables, and the local
branch matches `origin/main` exactly. Three things worth the owner's
attention surfaced along the way — none blocking, all named below rather than
quietly fixed: a stale second clone of this repo sitting on this machine, the
new sync hook script itself was never committed to the repo it's supposed to
keep in sync, and a stale skill count in one skill's own documentation.

## Assumptions

| # | Content | Basis | Status |
|---|---|---|---|
| A1 | "Full systems... validation and integrity testing" means mechanical/structural checks (lint, parity, hook behavior, git sync) — not a live-fire re-test of whether each skill's trigger wording actually fires in conversation | That's a research-methodology job requiring many fresh-session runs, explicitly out of scope for diagnostics-and-tooling's own mandate ("detects and measures... does not... judge whether a skill BEHAVES well") | unconfirmed |

## Criteria — PASS/FAIL with evidence

| # | Criterion | Verdict | Evidence |
|---|---|---|---|
| C1 | Pending fix merged + pushed | **PASS** | `git commit` → `6c2ef9c`; `git push` → `53de53b..6c2ef9c main -> main`; `git status --short` empty |
| C2 | Hook selftest 10/10 fresh | **PASS** | `bash hooks/selftest-receipt-law.sh` → `10 passed, 0 failed`, run twice this session (pre- and post-merge, file unchanged between) |
| C3 | Library lint, all current skills | **PASS** | `lint_skill.sh` run against all 19 `.claude/skills/*/` dirs (this session) → 19/19 `PASS (with warnings)`, 0 FAIL. The single warning text is identical across all 19 and is the documented PyYAML-fallback environment notice (`diagnostics-and-tooling/SKILL.md`'s own predicted verdict on this environment) — no unexpected warning types |
| C4 | Installed-copy parity | **PASS** | `diff` clean for `receipt-law-stop-gate.sh` and for all 4 repo-sourced installed skills (`adversarial-verify`, `brand-standard`, `plan-gate`, `scope-fence`); `llm-council` correctly excluded (not repo-sourced) |
| C5 | `settings.json` integrity | **PASS** | `jq empty` → valid; `jq -c '.hooks\|keys'` → `["PreToolUse","SessionStart","Stop"]`; all 3 hook commands resolve to existing, executable files (verified by direct path test, this session) |
| C6 | Local `main` vs `origin/main` | **PASS** | `git fetch origin && git status --short --branch` → `## main...origin/main` with no ahead/behind annotation — exact match |
| C7 | Open items / doc mismatches surfaced | **PASS** | See Findings below — three items named, none silently resolved |
| C8 | Dated report delivered | **PASS** | This file, `results/2026-08-11/full-systems-validation/REPORT.md`, committed and pushed (see Provenance) |

## Findings (surfaced, not silently fixed — C7)

1. **Stale duplicate clone.** `/Users/davidlayson/claude-core-skills` is a
   second local clone of the same repo (`origin` matches), 3 commits behind
   `origin/main` (`c4b20a9` vs the canonical clone's `6c2ef9c`), clean working
   tree — no uncommitted work at risk. This is the "other" candidate
   directory from earlier in this session, when the owner picked
   `Documents/GitHub/claude-core-skills` as canonical; this one has sat
   untouched since. Not wired into `settings.json` or the sync hook, so it
   cannot silently diverge further into anything the machine relies on — but
   it is a live footgun if anyone (owner or a future session) edits inside it
   by mistake, since nothing there auto-syncs.
2. **The new `SessionStart` sync hook isn't in source control.**
   `~/.claude/hooks/sync-governance.sh` (built this session, proven working)
   exists only on this machine — it is not committed to the
   `claude-core-skills` repo it's designed to keep in sync with. A machine
   reinstall, or setting this up on a second computer, would lose this
   specific automation unless it's added to the repo (e.g. under `hooks/`)
   and the personal-install runbook updated to copy it too.
3. **Stale count in `diagnostics-and-tooling`'s own doc.** Its SKILL.md
   states "Verified 2026-07-11... all 13 skills lint" and the audit loop
   "Expect PASS × 13." The repo now has 19 skills (6 added since). The count
   is stale, not the check — the loop itself is count-agnostic and passed
   cleanly against all 19 this session — but the doc's specific number no
   longer matches reality.

## Bounds

**Out of scope by design** (per A1):
- Whether any skill's *trigger wording* actually fires correctly across real
  conversations — that's a live-fire, multi-run evaluation
  (research-methodology's territory), not a same-session mechanical pass.
- Whether the skills' *procedural content* is good advice — lint checks
  structure (frontmatter, sections, trigger language present), never quality.
- The other project directory found on this machine
  (`~/yahoo-fantasy-basketball/.claude`) — a separate project's own
  domain-layer skills, not part of the core governance library this audit
  targets.

**In scope and unverified** (should be resolved before this backs a larger
decision, not this pass's job to close):
- `.claude/LESSONS.md` **INC-10** remains **OPEN** (owner-flagged
  2026-08-11): a card-game rules claim was graded SUPPORTED from reasoning
  rather than a checked primary source, and a contrary source surfaced later.
  Recorded, unresolved, unrelated to this session's work — noted here only
  because a full integrity pass should surface every open ledger item, not
  because this pass did anything to advance it.
- Whether other machines/devices this owner uses have their own drifted
  installs of this library — this pass only covers the one Mac it ran on
  (DID NOT CHECK: no access to any other device from this session).

## Next steps (owner decisions)

1. **Stale clone at `~/claude-core-skills`:** delete it, or leave it as an
   inert historical copy — either is safe given the clean working tree; not
   done here since removing a directory is the owner's call, not a validation
   pass's.
2. **Commit `sync-governance.sh` to the repo** (e.g. `hooks/sync-governance.sh`)
   and add it to the personal-install runbook (`install-and-surfaces`
   Runbook 1) so a fresh machine gets the auto-sync automation too, not just
   the two hooks currently documented there. Not done here — the earlier
   session explicitly scoped this hook's build to "this machine," and
   promoting it into the repo's own install runbook is a step up in scope
   worth a deliberate yes.
3. **Update `diagnostics-and-tooling`'s stale "13 skills" references** to 19
   (or drop the hardcoded number and just say "run the loop, expect PASS
   across every directory present") — a one-line doc fix, cheap, but left as
   a decision since editing another skill's doc wasn't asked for here.
4. **INC-10** stays open on the ledger; no action proposed from this pass.

## Provenance

- Session: this conversation, 2026-08-11, plan-gate-opened
  (`Documents/GitHub/claude-core-skills:plan-gate`), following the earlier
  receipt-law hook build/fix and the npm license-audit report in the same
  session.
- Commands and evidence: all inline above, produced this session via `git`,
  `bash`, `jq`, `diff` against the live repo and live machine state — none
  recalled from memory or an earlier session.
- Tooling exercised: `hooks/selftest-receipt-law.sh`,
  `.claude/skills/diagnostics-and-tooling/scripts/lint_skill.sh`,
  `~/.claude/hooks/sync-governance.sh` (indirectly, via its own log at
  `~/.claude/hooks/sync-governance.log`).
- Re-verify: `git -C /Users/davidlayson/Documents/GitHub/claude-core-skills
  log --oneline -1` should show `6c2ef9c` or later; the lint loop and
  selftest commands above are directly re-runnable and deterministic given an
  unchanged repo.
