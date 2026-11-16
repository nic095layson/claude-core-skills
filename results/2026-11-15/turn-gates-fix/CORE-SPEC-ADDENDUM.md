# CORE-SPEC addendum 1 (2026-11-15): the owner's answer to Q4 changes one default

Read `CORE-SPEC.md` first. This file overrides it where they differ. Source: `FIX/OWNER-DECISIONS.md`, the table
"Six policy answers". Five of the six answers keep the specification as written. Q4 does not.

## The change

`COMPACTION_VOIDS_LOADS = True` (the specification built False). `WAKE_TURN_INHERITS_LOADS = True` is unchanged.

The owner's words on the card: "Matches your doctrine: after a compaction the Stop gate wants the governors
reloaded before a commit or push. A notification wake-up that continues your turn keeps the earlier loads."

## The rule, replacing row S15 of table 1.3

For the outward-action rule, a compaction boundary (a `system` row `compact_boundary`, event COMPACT) inside the
governance turn voids the governor loads made before it, for every counted outward act that comes after it:

- For a counted outward act at row r: let c be the latest COMPACT row before r inside the governance turn (the
  start of the governance turn when there is none). plan-gate must be loaded after c and before r.
- adversarial-verify must be loaded after the latest COMPACT row that precedes the LAST counted outward act of
  the part being judged (anywhere after it, before or after the act, as today).
- Acts made before the first compaction of the turn are judged on the loads made before that compaction, exactly
  as the specification says for a turn without a compaction.
- A compaction that comes after the last outward act voids nothing for this rule: the doctrine asks for a reload
  "before the next consequential action", and there is none.
- A scheduled run and a wake are unchanged (S10, S11). The merge word is unchanged: a compaction does not end the
  window (table 1.2: "a compaction: nothing: the grant stays").
- The prompt-class rule (table 1.4, P4 and P9) is unchanged: a governor loaded anywhere in the governance turn
  counts for it. Say so in `hooks/README.md`.
- The block reason names the cause in plain words when this is the miss: the governors were loaded before a
  compaction and must be loaded again.

## Tests this changes

- `F15-loads-before-compaction-count-by-default`: wanted verdict becomes **block:F1** (it was allow). Rename it
  `F15-loads-before-compaction-do-not-count`.
- New, written first (red on the merged hooks only where marked):
  - `J19-reload-after-compaction-allows`: owner message, plan-gate, a compaction, plan-gate again,
    adversarial-verify, commit, push, stop: **allow** (pin).
  - `J20-compaction-after-last-act`: owner message, plan-gate, adversarial-verify, commit, push, a compaction,
    a closing text, stop: **allow** (pin: nothing consequential follows the compaction).
  - `J21-verify-before-compaction-only`: owner message, plan-gate, adversarial-verify, a compaction, plan-gate,
    commit, stop: **block:F1**, missing adversarial-verify (merged hooks: allow).
  - `J22-act-before-and-after`: owner message, plan-gate, adversarial-verify, commit, a compaction, push with no
    reload: **block:F1** (merged hooks: allow).
- One deliberate break for the list of 6.3: `COMPACTION_VOIDS_LOADS` set to False must be caught by the renamed
  F15, by J21 and by J22.
- `T24-compaction-midturn-keeps-order` is unchanged (the merge word survives a compaction).

## Replay prediction

Not run. The pre-registered prediction "Stop: 25 of 26 equal to the baseline" was made with the old default. With
this change a real stop whose turn committed or pushed after a compaction without reloading would turn into a
block. The implementer runs the replay and lists every such stop; each is a real miss against the doctrine, not a
false block.
