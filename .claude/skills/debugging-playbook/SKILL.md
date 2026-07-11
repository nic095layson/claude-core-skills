---
name: debugging-playbook
description: >-
  Symptom-to-triage playbook for the recurring failure modes of Claude sessions and
  skills — load it the moment something is BROKEN and you need to know why. Use when
  a skill won't trigger or triggers too eagerly, an edit doesn't show up in a session
  ("stale copy"), a capability that worked elsewhere is missing here ("but I granted
  you access"), an installed artifact disagrees with its source, or behavior differs
  between surfaces (Claude Code vs claude.ai vs cloud). Do NOT use for checking
  whether a drift exists when nothing is broken (live-state-truth owns detection),
  for the historical record of past incidents (lessons-ledger), or for authoring
  fixes to a skill's wording (skill-authoring + research-methodology) — this skill
  routes from symptom to cause, then hands off.
---

# Debugging Playbook

Triage runbook for the failure modes of operating Claude across surfaces. Each row
is labeled honestly: **VERIFIED** — observed, with the evidence named; or
**ANTICIPATED** — a plausible failure of this design, prepared for in advance but
not yet seen. Do not read ANTICIPATED rows as history.

The meta-rule, from the incident that founded this playbook: **silent failures
outnumber loud ones.** A skill in the wrong directory, a stale upload, a missing
credential — none of these error; they just quietly don't exist. So triage starts
by verifying registration and freshness, not by reading content.

## Quick triage table

| # | Symptom | Likely cause | First command / check | Status |
|---|---|---|---|---|
| 1 | Skill won't trigger (Claude Code) | Not at a discovery path; broken frontmatter; name ≠ directory | `ls <repo>/.claude/skills/<name>/SKILL.md` and `~/.claude/skills/<name>/SKILL.md` | VERIFIED — nic095layson/claude commit `6dc366f`: three days at repo root, readable, never registered |
| 2 | Skill won't trigger (claude.ai) | `.skill` never uploaded, toggled off, stale, or mis-zipped | `unzip -l <name>.skill` — expect exactly `<name>/SKILL.md` | ANTICIPATED |
| 3 | Skill fires too eagerly | Description matches an unrelated sense of its keywords; missing NOT clause | Re-read the offending prompt against the description's trigger phrases | ANTICIPATED |
| 4 | Edit made, session shows old behavior | Wrong copy edited (tree vs personal vs uploaded), or session predates the edit | `diff` the copy the session actually loads against the copy you edited | ANTICIPATED |
| 5 | "But I granted you access" — capability missing | Authorization lives in a different environment than the session (cloud grant vs local credentials, per-machine keys, per-surface connectors) | Enumerate live capabilities HERE: `gh auth status`, `command -v <tool>`, list connected integrations | VERIFIED — 2026-07-11: claude.ai GitHub grant assumed live in a local session that had no credentials at all |
| 6 | Installed artifact disagrees with source | Nothing rebuilds artifacts on edit; hand-built copies rot | Hash or `diff` installed copy vs source | VERIFIED — nic095layson/claude DRIFT-1/DRIFT-2 (stale README; evals buried in a zip) |
| 7 | Doc says X, system does Y | Doc describes a past state | Check the live system; the doc is the defect | VERIFIED — same DRIFT-1 |
| 8 | Governance skill produces ceremony on trivia | Trigger description too broad; triage rule ignored | Compare prompt against the skill's triage rule; check the NOT clause | ANTICIPATED — the failure class the no-ceremony law exists for |

Run the first check, then work the numbered section.

## 1. Won't trigger, Claude Code — the placement class

Causes in order of frequency: (a) file not at `<repo>/.claude/skills/<name>/SKILL.md`
or `~/.claude/skills/<name>/SKILL.md` — anywhere else is invisible, with zero error;
(b) frontmatter missing/unparseable (must open and close with `---`, contain `name:`
and `description:`); (c) `name:` ≠ directory basename; (d) session started before
the file existed — restart fresh. Fix placement/frontmatter, then **verify
registration**: fresh session, skill appears in the loaded list, fires on a
canonical phrase. Run `diagnostics-and-tooling`'s `lint_skill.sh` instead of
eyeballing (a)–(c).

## 2. Won't trigger, claude.ai — the artifact class

claude.ai does not read any repo; the uploaded `.skill` is everything. Check the
toggle (Settings → Capabilities → Skills), then the zip structure (`unzip -l` —
exactly `<name>/SKILL.md`), then diff the uploaded artifact's SKILL.md against the
source. Rebuild and re-upload per install-and-surfaces if stale.

## 3 & 8. Trigger calibration — too eager, or ceremony on trivia

Confirm the prompt actually contains a trigger-phrase match. If it fired without
one, the description has drifted broad — that is a wording change, which is gated:
route through research-methodology (pre-registered A/B with should-fire AND
should-not-fire prompts, fresh session per run) before shipping a new description.
If the skill fired correctly but ran full ceremony on a trivial ask, the defect is
in the body's triage rule — same gated path.

## 4. Stale copy — the freshness class

Multiple copies of a skill can exist simultaneously: project tree, `~/.claude/skills`
personal install, claude.ai upload, and (for packaged libraries) the built artifact.
A session loads exactly one. Find which one, `diff` it against the copy you edited,
and reconcile. Editing the tree does nothing for a session running the personal
copy. After reconciling, restart the session — an already-running session keeps
what it loaded.

## 5. Capability mismatch — the environment class

Authorizations, credentials, tools, and connectors are **per-environment facts**
(live-state-truth's boundary rule). A grant on claude.ai lives on Anthropic's
servers and never reaches a local machine; local credentials never follow you to
cloud. Triage: enumerate what THIS session can actually see (`gh auth status`,
`command -v`, the live tool list), then set up the missing leg locally or move the
work to the surface that has the grant. Do not loop retrying the call that failed —
the capability is absent, not flaky.

## 6 & 7. Drift classes

Detection and measurement belong to live-state-truth (hash, diff, rebuild-compare).
This playbook's contribution is the routing rule: once confirmed, the LIVE state is
the truth to plan against, the stale copy is the defect to fix or flag
(scope-fence), and the drift gets a ledger entry (lessons-ledger) even if fixed on
the spot.

## After every diagnosis

If it took >15 minutes, revealed a lying record, or ended in an abandoned approach —
the lessons-ledger recording rule has fired; write the entry while the evidence is
open in front of you.

## When NOT to use this skill

- Nothing is broken; you're checking a fact or parity → **live-state-truth** /
  **diagnostics-and-tooling**.
- Looking up whether this failure happened before → **lessons-ledger**.
- Designing the fix to a trigger description → **skill-authoring** +
  **research-methodology**.
- Deciding if fixing a discovered adjacent problem is allowed → **scope-fence**.

## Provenance and maintenance

Generalized 2026-07-11 from `nic095layson/claude` (commit `df6e198`)
`debugging-playbook` — its triage-table form, VERIFIED/ANTICIPATED labeling, and
rows 1/4/6 carry over with the repo specifics removed. Row 5 is new, from this
library's own founding session (2026-07-11, the GitHub cloud-grant/local-credential
mismatch). Repo-specific rows (council phase-leak, verdict bloat, vote inflation)
remain in that repo's playbook.

Re-verify: row 1's incident — `gh api repos/nic095layson/claude/commits/6dc366f --jq '.commit.message'`.
Update when: a new failure mode is observed twice (one occurrence is a ledger
entry; two is a pattern that earns a row), or an ANTICIPATED row is observed
(relabel VERIFIED with the evidence).
