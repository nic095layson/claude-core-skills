# Brief: attack the prompt-class Stop gate and the classifier

key: `atk-promptclass` · finding ids: `PC-<n>` · scratch: `work/atk-promptclass/`

**Objective.** Find owner messages and turns for which the prompt-class half of
`lib/hooks/governance-enforce.py` (everything below the F1 block) blocks or allows against its stated rule,
and classifier results in `lib/hooks/govclass.py` that contradict the classes as stated.

**Rules, as stated:** the module docstring and comments of `governance-enforce.py`; the comments of
`govclass.py` (the classes, which are enforced, the cue tier, the acknowledgement rule); `lib/hooks/README.md`;
`lib/CLAUDE.md` doctrine (governors on every non-trivial request; rules 1 and 3: a question gets an
assessment, a requirement is not a build order); the trivia-allowance comment (TRIVIA_MAX_CHARS).

**In scope.**
- Classification of real-looking owner messages. Write your own corpus of at least 40: governed work that
  must be caught, and trivia and chat that must not be, in an owner's register (short, informal, often a
  follow-up to something the assistant said).
- Which governor the gate demands for each class, and whether a different load satisfies it.
- The trivia allowance: each of its conditions.
- What "this turn" means in this half of the file compared with the F1 half above it.
- The single-retry rule.
- `lib/hooks/selftest-governance-classify.py` (mutation check).
- Real data: `pack/replay-baseline.txt`, PROMPT and STOP sections.

**Out of scope:** F1; the merge gate; the text the trigger injects (another auditor has it: you own what the
classifier returns and what the Stop gate does with it).

**Angles** (categories, not predictions):
1. Governed work phrased so that no class matches; trivia phrased so that a class matches.
2. Messages that are not requests at all: pasted material, a reference to an uploaded file, a one-word reply,
   an answer to a question the assistant asked.
3. The needed-governor rule: each enforced class's governor; mixed classes; a load under another scope
   prefix; a load with arguments.
4. The allowance: each condition at its edge; what "ran no tool" and "answer length" mean when the transcript
   does not record every text (`pack/real-text-recording.txt`).
5. Which message the gate takes as "the prompt" in a long turn: after a card answer, a scheduled run, a
   notification, a compaction summary.
6. Retry: after one block, what is no longer checked?
7. Failure and fail-open.

**Evidence, stop, output:** as in COMMON.md sections 6 to 8.
