# Brief: attack the turn boundary

key: `atk-turnboundary` · finding ids: `TB-<n>` · scratch: `work/atk-turnboundary/`

**Objective.** Every gate judges "this turn". Find real or plausible transcripts in which the code's idea of
where the turn starts, and of what happened in it, differs from the stated rule, and show what each gate
then gets wrong.

**Rules, as stated:** the docstrings and comments of `lib/hooks/turngate.py` (owner_index, scheduled_index,
turn_start, events); the comments in `lib/hooks/governance-enforce.py` about which user rows are not the
owner's request; `lib/plugin/core-governance/README.md` section "0.1.5";
`kit/after-report-2026-11-04-turn-gate-scheduled.md` (the scheduled-run rule and its fixtures S1-S5);
`lib/CLAUDE.md` doctrine ("Governor text already in context from an earlier task or from a compaction does
not count as loaded"; the "After a compaction" paragraph).

**In scope.** In `turngate.py`: load, owner_index, scheduled_index, turn_start, events. The second copy of
"which row is the owner's message" inside `governance-enforce.py` (the prompt-class half), and whatever the
receipt gate and the trigger use: do all the hooks agree on the turn? The S cases of the selftest.

**Out of scope:** the decision each gate makes once the turn is fixed (other auditors), except to show the
consequence of a boundary error.

**Your main input** is `pack/real-row-shapes.md`: the kinds of row a real transcript of this session
contains. For EVERY kind listed there, decide from the stated rule what it should be (starts a turn / part
of the current turn / part of no turn; the owner's word / not the owner's word) and test what the code does
with it. Then list row kinds the catalog does not contain but the harness can plausibly write (the catalog
covers one session), test those, and label them "plausible, not observed".

**Angles** (categories, not predictions):
1. Things the owner did that should start a new turn or carry their word, and do not.
2. Rows the owner did not write that start a turn or are read as their word.
3. What survives across the boundary that should not (loads, approvals), and what is lost that should not be.
4. Scheduled runs: several notifications in one read; a scheduled run followed by ordinary work; a read that
   mentions a scheduled task without delivering one; the first thing after a run.
5. The file itself: this session's transcript file restarts at a compaction boundary
   (`pack/tools/replay_real.py`, docstring); a transcript with no owner message at all; tool calls made by a
   helper agent (which transcript does a hook receive then? if the pack cannot settle it, say so).
6. For each boundary error, name the gate it breaks and the direction (allows / blocks), with a run of that
   gate (`mk.run_stop`, `mk.run_pre`, `mk.run_receipt`, `mk.run_trigger`).

**Evidence, stop, output:** as in COMMON.md sections 6 to 8.
