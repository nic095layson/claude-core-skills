# Brief: attack the prompt trigger and the decision-cards reminder

key: `atk-trigger` · finding ids: `TR-<n>` · scratch: `work/atk-trigger/`

**Objective.** Find owner messages for which `lib/hooks/governance-trigger.py` injects the wrong advisory
text, none when its rule calls for one, or one when it should be silent; and decide whether the
decision-cards reminder can detect what it claims to detect.

**Rules, as stated:** `lib/hooks/README.md`: the status note of 2026-11-02 (decision-cards reminder) and the
trigger's own section; the docstring and comments of `governance-trigger.py` and `govclass.py` (auto-trigger,
cue tier, dispute note, requirement note, named-skill line); `lib/CLAUDE.md` doctrine rules 1, 3, 4 and 5.

**In scope.** Every kind of text the trigger can inject, and its condition; the "previous reply" lookup used
by the cards reminder (which rows, which text, which pattern); cases D1-D6 in
`lib/hooks/selftest-turn-gates.py` and the classifier selftest (mutation check); real data:
`pack/replay-baseline.txt` PROMPT section (17 real owner messages: 3 auto-trigger, 10 cue, 4 silent, cards
reminder 0) and `pack/real-text-recording.txt`.

**Out of scope:** what the Stop gate does with the classes (another auditor); the merge gate.

**Angles** (categories, not predictions):
1. Each injected line: the smallest message that triggers it, the nearest message that should and does not,
   the nearest that should not and does.
2. The cards reminder: the ways a decision is really put to an owner as text, and the ways a card is really
   used; a reply that used a card and also a text list; a reply the transcript did not record.
3. Rule 5 (a skill the owner names is used): which names and trigger words are recognised; near-misses; a
   word that names a skill in ordinary speech.
4. What the harness passes as "prompt" for things that are not typed messages (a slash command, a card
   answer, a scheduled run). If the pack cannot settle it, say so under `not_verified`.
5. The injected text itself: true? consistent with the doctrine? asking for something impossible in an
   unattended run?
6. Failure, size (a very long prompt), encoding.

**Evidence, stop, output:** as in COMMON.md sections 6 to 8.
