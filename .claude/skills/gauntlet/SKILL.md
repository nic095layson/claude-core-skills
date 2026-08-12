---
name: gauntlet
description: >-
  The owner's named end-to-end governance run — plan-gate before acting, the work,
  adversarial-verify before delivering, reported in after-report shape. Load
  whenever a message contains GAUNTLET in any casing: "run gauntlet", "gauntlet
  this", "gauntlet report", "run the gauntlet on this deck", "why didn't you run
  Gauntlet?" — and treat the word as an explicit order to run the full sequence no
  matter how simple the task looks. Load it also when the full process is asked for
  by description: "run the whole process", "do the full governance pass". Do NOT
  load on a trivial or casual message even when the word appears — say in one line
  that it was skipped and why. Do NOT load to run a single governor: plan-gate,
  adversarial-verify and after-report own their own triggers, and this skill only
  sequences them.
---

# Gauntlet

**GAUNTLET is a sequence, not a new law.** Every rule it applies lives in a
governor that already exists; this skill's only job is to make the owner's word
mean something reproducible, so that "run Gauntlet" loads the same three skills
in the same order every time instead of producing whatever shape the session
improvises.

Why it exists as a named skill: the word was validated on claude.ai in 2026-07
(on-command 3/3, skips trivia 3/3) while living **only** in the custom-instructions
box. Instructions can be overwritten by the next paste, and were — a later block
authored from a base that never carried the definition replaced it, and the word
silently stopped meaning anything. A skill is discoverable in the catalog and
survives an instructions rewrite. Both carriers are wanted; this is the durable one.

## Terms (defined once)

- **The sequence** — plan-gate → work → adversarial-verify → after-report shape.
- **Named firing** — ending the delivery by stating which governors actually
  loaded. Not a receipt of *compliance* (a claim of loading is confabulable and
  was measured doing exactly that); a statement of *what happened*, checkable
  against the session.

## The procedure

### 1. Triage first — the word does not defeat proportionality

If the message is trivial or casual, say so in one line and answer. "GAUNTLET:
skipped, this is a one-line factual question" is correct compliance, not a
failure. Convening the sequence to compute 15% of 80 is a hard FAIL of this
skill (architecture-contract invariant 5).

### 2. Load plan-gate and pass its gate

Actually load it — applying its principle from memory is the skip this exists to
catch. Goal, knowns/unknowns, assumptions, success criteria, phased plan. Its
§2 convert-cheap-unknowns law is the one most often skipped mid-task: settle what
a tool call can settle **before** planning around it, and if you stop converting
for cost, say so.

### 3. Do the work

Inside the fence the prompt drew. Adjacent problems get flagged in one line, not
fixed (scope-fence). If the work is external-facing in the owner's name, load
brand-standard too.

### 4. Load adversarial-verify and run its pass

All six steps, proportional to the deliverable. Step 6's gap audit is not
optional on anything carrying a tally, a classification, or a recommendation —
that is the exact shape that failed before.

### 5. Report in after-report shape

Method up front, evidence dated, EVIDENCE vs INFERENCE marked, bounds split into
out-of-scope-by-design versus in-scope-and-unverified, next steps left as owner
decisions.

### 6. Name what fired

End with the governors that actually loaded this run. If one that should have
fired did not, say that — an honest "adversarial-verify did not load" is worth
more than a confident list.

## Output format

```
**GAUNTLET — <task>**
**Goal** — one falsifiable sentence.  **Assumptions** — A1, A2… (omit if empty)
**Success criteria** — the checkable definition of done.
<the work>
**Criteria** — C1: PASS (evidence) · C2: FAIL (output shown)   [binary; PARTIAL is FAIL]
**Refutation** — attacks tried, what they found
**Gaps** — <n>: not-attempted / attempted-failed / unverifiable · load-bearing: <disposition>
**Bounds** — out of scope by design | in scope and unverified
**Status** — delivered | candidate | open
**Fired** — plan-gate · adversarial-verify · <others, or "none — and why">
```

## Rules, each with its reason

1. **The word overrides your own read of the task** — if the owner typed
   GAUNTLET on something you judged simple, run it anyway (bar triage). The
   request is evidence your read may be wrong.
2. **Load, do not recall** — a governor applied from memory is the failure mode
   this sequence was built after. The skills are short; load them.
3. **Triage still wins on trivia** — over-firing on casual messages is what kills
   governance skills, and no keyword is worth that.
4. **Name what fired, honestly** — a stated list that is wrong is worse than no
   list, because it manufactures confidence. Never claim a load you did not make.
5. **This skill adds no law** — if it ever seems to conflict with a governor, the
   governor wins and the conflict is a defect to report.

## When NOT to use this skill

- Trivial, casual, or creative messages → answer directly, even if the word appears.
- One governor is what's wanted → **plan-gate** / **adversarial-verify** /
  **after-report** / **scope-fence** directly; this skill only sequences them.
- Verifying an artifact the owner handed over, with no work to do first →
  **adversarial-verify** alone.
- Deciding whether adjacent work is in scope → **scope-fence**.

## Volatile facts (dated)

- Authored 2026-08-12; **UNMEASURED as a skill** — the trigger evals in
  `evals/gauntlet.json` are authored, not run. *candidate*
- The word's prior validation was as instructions text, not as a skill: on-command
  3/3, trivia-skip 3/3, always-on ~83% with 0/3 over-fire (2026-07-16, claude.ai
  proxy, Opus, N=3). Those rates do **not** transfer to this skill's triggering.
  *verified, but for a different carrier*

## Provenance and maintenance

Authored 2026-08-12 at the owner's request, after `.claude/LESSONS.md` INC-11
found that the validated GAUNTLET definition had been silently dropped from the
instructions block: it was developed and confirmed on branch
`claude/rivian-stock-analysis-h5y46x` (2026-07-16, commits `b731746`, `f63a656`,
`01f6788`, `f679404`) which was **never merged to main**, so the 2026-08-03 block
— authored from main, and diff-clean against it — carried no trace of the word and
overwrote it in the live settings box on paste. The sequence and the "load, do not
recall" rule restate that branch's INC-8 finding (governors applied "in spirit",
never loaded). No law here is new; every step delegates to its governor.

Re-verify: the governors it sequences exist —
`ls .claude/skills/{plan-gate,adversarial-verify,after-report}/SKILL.md`.
Update when: a governor in the sequence is retired or renamed, the owner changes
the trigger word (it is arbitrary — any distinctive token works if the definition
names it), or the trigger evals run and the candidate status resolves.
