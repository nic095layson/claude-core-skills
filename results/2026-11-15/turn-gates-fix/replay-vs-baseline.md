# Replay of the real session record on the rebuilt hooks, against the baseline (2026-11-15)

What was run, by the orchestrator, after implementer 2's work: the audit's replay tool on a private snapshot of
one long session (1,562 rows, 2026-10-21 to 2026-11-12). The tool prints verdicts only, never content. The
baseline is the same tool's output for the merged hooks (commit 1ce99d5). Pre-registered prediction 3
(`experiments/hypothesis-2026-11-15-turn-gates-cases.md`) said what would differ.

## Result against prediction 3

| part | predicted | observed | verdict |
|---|---|---|---|
| Stop gate, 26 real stops | 25 equal; the second stop of 2026-10-21T23:26 turns from a block into an allow (finding F1-5) | exactly that: 25 equal, that one stop turns from `BLOCK:F1` into `allow` | as predicted |
| Prompt hook, 17 real owner messages | 17 equal | 17 equal | as predicted |
| Before a tool call: the two merges of the turn that began 2026-10-21T23:25 | both denied (a word that names no number; D1) | both denied, code `merge-word` (pull requests 29 and 156) | as predicted |
| Before a tool call: the baseline's one denial (a false one, finding RI-8, turn from 2026-10-28T23:16) | gone | gone | as predicted |
| Before a tool call: any other denial | none ("exactly two new denials") | **one more**: a shell call of 2026-11-12T21:34 that ends in a push with no branch named, code `default-branch` | **MISS as written**, explained below |
| The other 15 real merges | allowed | allowed (4 plain, 11 with the plan-shown advisory) | as predicted |

## The third denial is made by the replay, not by what happened

The rebuilt gate reads which branch a push with no branch named would go to from the checkout's `HEAD` file
(specification 3.1; no subprocess). The replay hands the hook a command of 2026-11-12 that first changes into the
library's checkout and then pushes. On 2026-11-12 that checkout was on the working branch of the day. Today the
same directory is on `main`, so the replayed call reads as a push to the default branch and is denied, as D3
orders for a real push to `main` without the owner's word for it.

Checked two ways:

- the same call with the directory replaced by a made-up checkout whose `HEAD` names that day's working branch:
  not denied (the plan-shown advisory, as for the other pushes of that turn);
- the design's reference prototype printed two denials on this record because its replay ran with the branch
  lookup switched off by an environment variable. The shipped code has no such switch, by design: nothing in the
  environment may change a verdict.

So the prediction's number (two) was right for what the session really did, and wrong for what this tool prints
today: three. A replay of a recorded command judges it against the file system as it is at replay time. That
limit belongs to the replay tool, and is stated here so that the next reader does not take the third line for a
false denial.

## Every line that differs from the baseline

Stop gate:

```
2026-10-21T23:26 | now: BLOCK:F1 -> allow                                  finding F1-5 (the earlier miss is not raised again)
totals: allow 23 -> 24, BLOCK:F1 2 -> 1, BLOCK:prompt-class 1 -> 1
```

Before a tool call, by owner turn (counts of calls; "write", "outward" and "merge" are the tool's own labels):

```
turn from 2026-10-21T23:25   merge: advisory x2 -> DENY x2                 D1: the word named no number
turn from 2026-10-22T16:01   write: allow x2 -> x3                         ADV-4: one more command is read as a write
turn from 2026-10-22T16:10   (not listed) -> write: allow x1               ADV-4
turn from 2026-10-28T22:56   write: advisory x1 -> x3                      ADV-4
turn from 2026-10-28T23:16   write: advisory x18 -> x24; outward: advisory x16 -> x14;
                             merge: DENY x1 -> gone                        RI-8: a search that mentioned the words is no merge
turn from 2026-11-02T21:59   write: advisory x1 -> x2                      ADV-4
turn from 2026-11-12T21:23   write: advisory x4 -> x16; outward: advisory x8 -> x7;
                             merge: (none) -> DENY x1                      the replay artifact described above
totals: merge DENY 1 -> 3; merge advisory 13 -> 11; merge allow 4 -> 4; write advisory 24 -> 45;
        write allow 2 -> 4; outward advisory 41 -> 38; outward allow 8 -> 8
```

The advisory counts were not predicted. They move because commands are now parsed: a redirection into a file, an
in-place edit and a file written through a shell tool count as writes, and a search that only mentions the words
no longer counts as an outward action.

## What the replay cannot test

The record holds no blocked stop followed by a merge, no message sent while the assistant worked, no scheduled
delivery and no outward call by a helper agent. Those rules are tested by the table only.
