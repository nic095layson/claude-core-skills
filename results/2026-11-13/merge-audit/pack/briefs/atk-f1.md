# Brief: attack the Stop gate's outward-action rule ("F1")

key: `atk-f1` · finding ids: `F1-<n>` · scratch: `work/atk-f1/`

**Objective.** Find inputs on which `lib/hooks/governance-enforce.py` decides F1 differently from the stated
rule: turns it should block and allows, turns it should allow and blocks, and ways it stops deciding at all.

**The rule, as stated** (read these yourself; quote the one you rely on):
- `lib/hooks/README.md` lines 11-20 (status 2026-10-29)
- `lib/experiments/hypothesis-2026-10-29-turn-gates.md`: the "What changes" table (row F1) and the "Outcome"
  section (the rule was narrowed there)
- the comment block above the F1 code in `lib/hooks/governance-enforce.py`
- `lib/CLAUDE.md`, "Operating doctrine" (what the governors are for; what counts as loaded)

**In scope.**
- The F1 block of `governance-enforce.py` and what it calls in `lib/hooks/turngate.py`: which tool calls count
  as an outward action, which Skill calls count as a governor load, the order test, the single-retry rule,
  error handling.
- The F1 cases of `lib/hooks/selftest-turn-gates.py`: do they pin the rule? (Mutation check, COMMON.md section 5.)
- The same code as shipped in `lib/plugin/core-governance/scripts` and as installed on the owner's account
  today (`account/plugin/core-governance/scripts`): same verdicts on your cases?

**Out of scope** (other auditors have them): where a turn starts (which rows count as the owner's message,
scheduled runs); the prompt-class half of the same file (below the F1 block); the merge-word gate; the
reminders.

**Angles to cover** (at least one test each; these are categories, not predictions):
1. An outward action the rule names, taken in a form the gate does not recognise.
2. Something the gate counts as outward that changes nothing outside the machine.
3. A governor "load" that should not count, and a real load that is not counted.
4. Order and repetition: several outward actions, loads between them, more than one stop in the same turn.
5. Timing: the gate runs when the assistant stops, after the action. What does a block actually prevent, and
   what do the documents say it prevents?
6. Broken or unusual input: an unreadable or very large transcript, missing fields, rows of unexpected shape,
   the helper module missing.
7. The real record: `pack/replay-baseline.txt` shows F1 blocks at two real stop points. Are those right?
   (`python3 PACK/pack/tools/replay_real.py --what stop`.)

**Evidence, stop, output:** as in COMMON.md sections 6 to 8.
