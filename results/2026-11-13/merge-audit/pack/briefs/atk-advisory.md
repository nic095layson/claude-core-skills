# Brief: attack the advisory hooks and the compaction protocol

key: `atk-advisory` · finding ids: `ADV-<n>` · scratch: `work/atk-advisory/`

**Objective.** Decide, with tests, whether each advisory hook fires when its rule says it should and stays
silent when it should not, and whether an advisory that "never blocks" can in practice mislead, flood, or go
permanently silent.

**Targets.**
- The F3 "plan shown" advisory in `lib/hooks/turn-gates-pretool.py` (with `turngate.py`: what counts as a
  write, the plan marker, the once-only sentinel)
- `lib/hooks/plan-gate-first-write-reminder.sh`, `lib/hooks/scope-fence-reminder.sh` (and `selftest-reminders.sh`)
- `lib/hooks/session-doctrine.sh` (SessionStart on compact|resume: the post-compaction protocol)
- `lib/hooks/ledger-recount-reminder.sh`, `lib/hooks/redteam-band-reminder.sh` (and its selftest): what are
  they, and are they wired anywhere?

**Rules, as stated:** `lib/hooks/README.md` (the status notes at the top and each hook's own section); the
docstring of `turn-gates-pretool.py` (F3) and the Outcome section of
`lib/experiments/hypothesis-2026-10-29-turn-gates.md` (why F3 is advisory); `lib/CLAUDE.md` doctrine: the
"Communication" paragraph (a required plan is shown before acting as one compact table), the "After a
compaction" paragraph, the "Enforcement" paragraph.

**Out of scope:** F1, the merge gate, where a turn starts.

**Angles** (categories, not predictions):
1. Fires / does not fire: for each hook, the smallest input on each side of its rule.
2. Once-only state: what keys each hook's "already reminded" memory? When does a reminder that should repeat
   stay silent, or one that should be silent repeat? Across a compaction, a resume, a new day, two sessions
   on one machine, a temp directory that is cleaned or cannot be written?
3. Real data: `pack/replay-baseline.txt` shows the plan-shown advisory on 78 of 92 real write calls, and
   `pack/real-text-recording.txt` shows which assistant texts the transcript recorded. What does the advisory
   actually measure?
4. Which file locations are exempt from the write test, and is that the right set?
5. The text each hook injects: is it true, and does it ask for something the doctrine forbids or that cannot
   be done (in an unattended run, or in a helper agent)?
6. Failure: a hook that errors, times out (the timeouts are in the wiring files) or prints malformed output.

**Evidence, stop, output:** as in COMMON.md sections 6 to 8.
