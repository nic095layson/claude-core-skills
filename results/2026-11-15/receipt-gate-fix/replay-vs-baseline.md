# The receipt gate on the real session record, against the baseline (2026-11-15)

    python3 <audit pack>/pack/tools/replay_real.py --hooks hooks --what stop

The audit's replay tool runs both Stop hooks at each of the 26 real stop points of one long session (a private
snapshot, 2026-10-21 to 2026-11-12) and prints verdicts only, never content. The baseline is the same tool's
output for the hooks as merged (commit 1ce99d5): the receipt gate allowed all 26. Run on the rebuilt gate after
the prose scan's changes; the record itself was not opened for this fix.

## Result

| | baseline (merged gate) | rebuilt gate |
|---|---|---|
| receipt gate: allow | 26 | 23 |
| receipt gate: block | 0 | 3 |
| the other Stop gate | as in `results/2026-11-15/turn-gates-fix/replay-vs-baseline.md` | the same 26 verdicts as there |

## Every stop whose receipt verdict differs

| stop | baseline | now | what is known without its text | right by the rule? |
|---|---|---|---|---|
| 2026-10-22T16:08 (the first of the two stops of that minute) | allow | block | while the gate was first built, a copy of it that printed categories only (family, position; no text) showed: a claim of the "could not + verb" family in an EARLIER text of the stretch, not in the final answer. The old gate read only the text after the last harness row (finding RL-7) | if that note was a real "could not ..." with no attempt in its sentence, yes: the rule has no exemption for a progress note. If a later lookup settled it, the answer would have had to say so. Not decidable without the text |
| 2026-10-28T23:02 | allow | block | the same copy showed: a claim of that family in the final answer, and a receipt word in a NEIGHBOURING sentence | by the rule's words ("the same sentence"), yes. With `RECEIPT_SCOPE = "neighbours"` this stop is allowed: it is the case the policy default is about |
| 2026-11-02T22:41 | allow | block | as the line above | as the line above |

What is NOT known: whether each of the three sentences is the assistant's own inability claim or one of the
readings the gate still gets wrong (the limits in `hooks/README.md`). The categories above were printed during
the first build; they were not printed again after the prose scan changed the grammar. The same three stops
block before and after that change, and no other stop does.

The gate was not tuned to the record: no rule, word or case of this fix was written from these three answers.
The earlier build blocked two more stops (both of 2026-11-02T22:43) through the family "X was not verified";
that family was switched off for a reason found in this repository's own reports
(`NOT_VERIFIED_IS_A_CLAIM`, a policy default), not for the record.

## The orchestrator's reading of the three answers (2026-11-16)

The orchestrator holds the record and read the three answers after the gate was finished (nothing in the gate
was changed afterwards). Without quoting them:

| stop | what the blocked sentence is | a receipt nearby? | by the rule's words |
|---|---|---|---|
| 2026-10-22T16:08 | a first-person "can't confirm" in an earlier note of the stretch, and a first-person "can't reach them from here" in the final answer | no attempt and no failure named in either sentence | bare claims |
| 2026-10-28T23:02 | a first-person "can't confirm" in the final answer, with a reason in free words in the same sentence | the next table row says why, and says "did not check" | a bare claim; allowed under `RECEIPT_SCOPE = "neighbours"` |
| 2026-11-02T22:41 | a first-person "one older item I can't confirm" in the opening sentence of the final answer | the detail follows in a table below | a bare claim; allowed under `RECEIPT_SCOPE = "neighbours"` only if the table row counts as the next sentence |

So none of the three is one of the readings the gate gets wrong: each is the assistant saying it cannot do
something without naming, in that sentence, what was tried and how it failed. Each would have cost one forced
continuation to add the receipt. Whether that is the behaviour the owner wants is the decision below.

## What the owner can do with this

Decide whether a receipt in the neighbouring sentence should count. Two of the three stops turn on that one
constant, `RECEIPT_SCOPE`.
