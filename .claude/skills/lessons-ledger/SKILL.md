---
name: lessons-ledger
description: >-
  The running log of mistakes, dead ends, and drifts — recorded as symptom → root
  cause → evidence → status so no session re-debugs a solved problem, re-walks a
  known dead end, or trusts a record that history proves stale. Load this in two
  directions: to CONSULT it before re-attempting anything that might have been
  tried before ("was this tried?", "did this break before?", "why does the doc
  disagree with reality?"), and to APPEND whenever the recording rule fires — a
  diagnosis cost real time, a doc of record was caught lying, an approach was
  abandoned, an artifact disagreed with its source. Load it at the END of any
  session that hit one of those, even if everything got fixed. Do NOT load it to
  diagnose a live problem from scratch (debugging is its own work; this is the
  archive), and do NOT record routine successes — a padded ledger is as useless as
  an empty one.
---

# Lessons-Ledger

An error made once is tuition; the same error made twice is a process failure.
Sessions end and context evaporates — the ledger is the only memory that
survives, and it only works if entries are written when the lesson is fresh and
consulted before the same ground is walked again. Its enemy is not laziness but
optimism: "I'll remember this" has never once been true across sessions.

## Terms (defined once)

- **Incident** — something broke or silently failed, was diagnosed, and was (or
  should have been) fixed. Has a before and after.
- **Drift** — two things that are supposed to agree no longer do (doc vs system,
  copy vs copy). Nothing "broke", but the record lies until reconciled.
- **Dead end** — an approach tried and abandoned, recorded so the next attempt
  doesn't walk into it. Labeled abandoned, never disguised as fixed.
- **Evidence** — a command output, file path + lines, diff, hash, or dated
  observation. **An entry without evidence is a rumor and does not belong in the
  ledger.**

## Where the ledger lives

Resolve in this order; write to the first that applies:

1. **The project's own ledger**, if one exists (e.g. a `failure-archaeology`
   skill or `LESSONS.md` in the repo) — the project instance always wins over the
   general one.
2. **`.claude/LESSONS.md` at the project root** — create it on first entry for
   any project you are working in.
3. **The persistent memory directory** (as a `feedback`- or `project`-type
   memory) — for lessons that are about how *you* work rather than about one
   project, or when no project filesystem exists.

Cross-cutting lessons may earn an entry in two places; link rather than duplicate
the content.

## The recording rule — when an entry MUST be added

Append when ANY of these is true:

1. **The 15-minute rule.** You spent more than ~15 minutes diagnosing why
   something "should work but doesn't" — regardless of how trivial the fix turned
   out to be. The diagnosis, not the fix, is the expensive thing being saved.
2. **A record was caught lying.** A doc of record, README, config comment, or
   memory contradicted the live system — record it as a DRIFT even if you fixed
   it in the same session, so the failure mode stays visible.
3. **An approach was abandoned.** Record the dead end and the reason, so the next
   author (human or model) does not re-fight a settled battle.
4. **An artifact disagreed with its source** — a build, package, or copy that
   should have matched and didn't.

Do NOT record: routine edits, first-try successes, or hypotheticals that never
bit anyone. **The ledger logs what happened, not what might.** Do not pad it —
and do not let real entries wait for a "better" write-up that never comes.

## Entry format

```
### <TYPE>-<n> — <one-line title>
- Date: <when discovered / when fixed>
- Symptom: what was observed, concretely.
- Root cause: why it actually happened (not the first theory — the confirmed one).
- Evidence: command output, path+lines, diff, hash. No evidence, no entry.
- Status: FIXED / OPEN / ABANDONED (dead ends are ABANDONED, not FIXED).
- Lesson: the one transferable sentence — what to check FIRST next time.
```

`TYPE` is `INC` (incident), `DRIFT`, or `DEAD` (dead end). Never renumber
existing entries — later references depend on them.

## The consulting rule — when to read it

- Before re-attempting anything that smells familiar or is listed as abandoned.
- Before trusting a doc that a ledger entry has ever flagged as drifted.
- At session start in a project whose ledger has OPEN entries — they are the
  standing traps.

A ledger nobody reads is a diary. The write is half the discipline; the read
before repeating history is the half that pays.

## Worked example (real, from this library's own history)

```
### INC-1 — Skill at repo root was never auto-loaded
- Date: discovered and fixed 2026-07-10.
- Symptom: SKILL.md at repo root; readable, syntactically perfect, silently
  never registered as a skill. No error anywhere.
- Root cause: skills are discovered only at .claude/skills/<name>/SKILL.md;
  root placement is not a discovery path.
- Evidence: commit 6dc366f — pure rename, 0 insertions, 0 deletions; the
  content was fine, only the location was wrong.
- Status: FIXED.
- Lesson: placement is part of correctness; when something "doesn't trigger",
  check the path FIRST, and verify registration, not just content.
```

Three days of a shipped-but-dead artifact, saved forever as six lines.

## When NOT to use this skill

- Diagnosing a live problem from scratch → **debugging-playbook** (which may
  route you here to check for prior art).
- Detecting whether a drift exists right now → **live-state-truth** (detection
  there, chronicle here).
- Deciding whether fixing a discovered problem is in scope → **scope-fence**
  (flag it there, record its history here).
- Recording preferences or user feedback unrelated to a failure — that is
  ordinary memory, not the ledger.

## Provenance and maintenance

Generalized 2026-07-11 from `nic095layson/claude` (commit `df6e198`, 2026-07-10):
`failure-archaeology` — the incident/drift/evidence definitions, the recording
rule (15-minute rule, drift-even-if-fixed, dead ends, artifact disagreement), the
no-padding doctrine, the symptom→root-cause→evidence→status format, and INC-1
(reproduced above) are carried nearly verbatim; only the repo-specific record and
watchlist stay behind. That skill remains the project ledger of that repo (see
"Where the ledger lives", rule 1).

Re-verify lineage: `gh api repos/nic095layson/claude/contents/.claude/skills --jq '.[].name'`
— expect `failure-archaeology` in the listing.
