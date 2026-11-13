# Brief: attack the receipt-law Stop gate

key: `atk-receipt` · finding ids: `RL-<n>` · scratch: `work/atk-receipt/`

**Objective.** Find final answers on which `lib/hooks/receipt-law-stop-gate.sh` blocks an honest sentence or
passes a bare claim of inability, against the rule it enforces.

**The rule, as stated:** adversarial-verify rule 6 (`lib/.claude/skills/adversarial-verify/SKILL.md`, "A claim
of inability needs a receipt"); the owner's instruction text in
`lib/instructions/claude-ai-custom-instructions.md` (search "receipt"); the hook's own header comment;
`lib/hooks/README.md` (search "receipt").

**In scope.** The hook script (it embeds Python): its phrase list, what counts as a receipt and how near it
must be (RECEIPT_WINDOW), which text it examines (which message, which turn, how much of it), any
once-only or per-session state, retry behaviour; `lib/hooks/selftest-receipt-law.sh` (mutation check); real
data: `pack/replay-baseline.txt` (receipt column: 26 of 26 real stops allowed) and
`pack/real-text-recording.txt`.

**Out of scope:** the other Stop hook's rules; the merge gate.

**Angles** (categories, not predictions):
1. Claims of inability in natural wording that the phrase list misses; honest sentences it flags (negations,
   quotations, reported speech, code blocks, tables, a sentence ABOUT the rule, a question to the owner).
2. Receipts: text that satisfies the receipt test without being a receipt; a real receipt that fails the test
   (position, distance, format).
3. Which text: long answers, several texts in one turn, text before and after tool calls, an answer the
   transcript did not record.
4. The turn boundary this hook uses, compared with the other Stop hook: do they look at the same turn?
5. State and retry; failure, timeouts, missing tools (which interpreter and commands does the script need?).
6. A 26-of-26 allow rate on a long real session: is the gate quiet because the session was honest, or because
   it cannot see? Find a way to tell.

**Evidence, stop, output:** as in COMMON.md sections 6 to 8.
