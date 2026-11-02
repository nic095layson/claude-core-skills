# Hypothesis — decision cards: drop the default exemption, add an advisory reminder (2026-11-02)

Written before any change. Owner's clickable answer (2026-11-02): "Reword + advisory hook (Recommended)",
after an after-report from the Solo-Leveling-System session (cards at 8 of 13 decision points; the 5
misses were decisions with a stated default) and this session's check of it: the owner's own rule text
(claude.ai block, cloud doctrine rule 4, Mac doctrine) said "Not for trivial choices or obvious
defaults", which licensed the misses alongside the tool description and the autonomy guidance.

## Changes

| id | where | change |
|---|---|---|
| W | rule 4 in all three carriers + every CLAUDE.md block copy | A default is not an exemption: it goes first as "(Recommended)" on the card. Only a trivial yes/no follow-up is exempt; unattended runs still never ask. |
| H | `hooks/governance-trigger.py` (UserPromptSubmit, advisory) | When the previous assistant turn contains a list line (number or bullet) with "(Recommended)" and no AskUserQuestion call, add one context line telling the model to put the decision as a card if it is still open. Never blocks. |

## Predictions (fixture, `hooks/selftest-turn-gates.py`, red on main → green)

| case | previous turn | expected |
|---|---|---|
| D1 | "1. **Option A (Recommended)** … 2. Option B" and no card | reminder |
| D2 | same list, but an AskUserQuestion call in that turn | silent |
| D3 | "(Recommended)" only in running prose, no list line | silent |
| D4 | no "(Recommended)" anywhere | silent |
| D5 | bullet "- Keep advisory (Recommended)" and no card | reminder |
| D6 | the reminder is added alongside the existing governance cue, not instead of it | both present |

Live behaviour (whether the next turn then asks with a card) is NOT pre-registered as measured here:
it needs a two-turn headless run, which `claude -p` does not give without a resumed session; marked
UNMEASURED in the outcome. Wording: UNMEASURED.
