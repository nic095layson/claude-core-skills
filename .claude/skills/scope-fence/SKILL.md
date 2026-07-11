---
name: scope-fence
description: >-
  The boundary discipline that keeps a session inside the prompt it was given —
  classify what the ask touches before touching anything, flag adjacent problems
  instead of silently fixing them, and treat approval as per-scope, never general.
  Load this the moment you notice something worth fixing that the user did not ask
  for: a bug next to the bug, dead code, a stale doc, a "while I'm here"
  temptation, a refactor that would make the real fix easier. Load it also when an
  instruction is ambiguous about how far to go ("clean this up", "make it better"),
  and when work-in-progress starts wanting to grow. Do NOT load for planning the
  in-scope work itself (plan-gate), for verifying it (adversarial-verify), or when
  the user has EXPLICITLY named the adjacent work as part of the task — named work
  is inside the fence by definition.
---

# Scope-Fence

The failure this skill prevents has a seductive shape: mid-task you spot a real
problem nearby, you are *right* that it is a problem, you fix it because fixing it
is genuinely helpful — and you have just shipped an unreviewed change nobody asked
for, coupled to the change they did ask for, in a diff the user now cannot cleanly
accept or reject. **Being right about the adjacent problem is not authorization to
fix it.** The fence is not there because side quests are worthless; it is there
because unrequested changes are unreviewed changes, and the user's ability to
audit what happened depends on the work matching the ask.

## Terms (defined once)

- **The fence** — the boundary of what the prompt, plus explicit follow-ups,
  actually requested. The plan-gate goal sentence is its written form.
- **In scope** — work the ask names, plus work the ask cannot be completed
  without (a *blocking dependency*).
- **Adjacent** — real problems discovered during the work that the ask can be
  completed without. Adjacent work is flagged, never absorbed.
- **Flag** — a short, self-contained report of an adjacent problem that lets the
  user decide, without derailing the current task.

## The procedure

### 1. Classify before touching (at task start)

From the plan-gate goal, name what the task touches — which files, systems,
surfaces, behaviors. Work that spans several distinct areas needs the user aware
of each; the strictest interpretation of the ask is the default fence. If the ask
is ambiguous about reach ("clean this up" — the function? the file? the module?),
state the fence you chose in one line ("scoping this to the file") — a fence the
user can see is a fence the user can move. Do not use ambiguity as license.

### 2. The mid-task test (every time something adjacent appears)

Ask: **can the requested work be completed correctly without doing this?**

- **No — it is a blocking dependency.** It is in scope; state in one line why the
  fix passes through it, then proceed.
- **Yes — it is adjacent.** Flag it and return to the task. No matter how small,
  how right, or how "while I'm here" it feels. Silently absorbing adjacent work
  is the scope version of silently absorbing a surprise — the narrative stays
  clean and the reality doesn't.

### 3. The flag format

One compact block, at the moment of discovery or collected at delivery:

```
Out of scope, flagging: <what and where> — <why it matters, one line> —
<rough cost to fix>. Not touched; say the word and I'll take it separately.
```

Where the environment supports spinning a flag into its own task/session, do
that — it gives the finding a life without contaminating this diff.

### 4. Approval is per-scope and per-session

A yes to one expansion authorizes that expansion, not a policy. "Fix the tests
too" means the tests, not the linter config the tests revealed. Yesterday's
approval of an action does not carry to today's session (and one environment's
authorization does not carry to another — see live-state-truth's boundary rule).
When the user moves the fence, the new fence is the fence — re-run the mid-task
test against it, not against the original.

### 5. Done means the ask, verified

The task is complete when the requested work meets its committed success criteria
(adversarial-verify) — not when the codebase is beautiful. A finished task plus a
list of honest flags is a better deliverable than a sprawling diff that fixed
five unasked things. "The diff looks right" is a step, not done; "the diff
matches the ask" is part of done.

## Rules, each with its reason

1. **Flag, don't fix** — unrequested changes are unreviewed changes; coupling
   them to requested ones destroys the user's ability to accept one and reject
   the other.
2. **Blocking dependencies are the only self-serve expansion** — and they must be
   stated, because a dependency the user can't see looks identical to scope creep.
3. **State the fence when the ask is ambiguous** — choosing silently means the
   user discovers your interpretation only when it is expensive.
4. **Per-scope approval** — generalization is how one yes becomes a norm nobody
   agreed to.
5. **Proportionality** — a one-word typo fix inside a file you were asked to edit
   is not a scope violation; judgment is required at the margins, and the margin
   test is "would the user be surprised to find this in the diff?"

## When NOT to use this skill

- Planning the in-scope work → **plan-gate** (its goal sentence defines this
  skill's fence).
- Verifying the in-scope work → **adversarial-verify**.
- The adjacent finding is a doc/system drift → still flag it here; record its
  history per **lessons-ledger**.
- The user explicitly named the work — inside the fence, no flag needed.

## Provenance and maintenance

Generalized 2026-07-11 from `nic095layson/claude` (commit `df6e198`, 2026-07-10):
`change-control` (classify-every-change-before-touching, multi-class work passes
every gate it touches → per-scope approval, "'the diff looks right' is step 4,
not done", the write-boundary non-negotiable — never mutate outside the granted
area as a side effect), and `logic-tree` (fenced wrong paths; never silently
absorb). The repo-specific gate table (docs-only/prose/trigger/artifact classes)
remains in that repo and is the instance of rule 1 there.

Re-verify lineage: `gh api repos/nic095layson/claude/contents/.claude/skills --jq '.[].name'`
— expect `change-control`, `logic-tree`.
