# The 44 cases of the earlier turn-gate fixture, and where each one went (2026-11-15)

`hooks/selftest-turn-gates.py` as merged at commit 1ce99d5 held 44 cases (16 Stop, 18 pre-tool, 6 on the card
reminder of the prompt hook, 4 others; counted from that file, and its own last line reads "44 passed" on the
merged hooks). The file is replaced by the test table. Each old case is either carried by a case of the table
with the same verdict, or its verdict was changed by a decision, or nothing carried it and it got a case of its
own, named `O..`. Old verdict words: block = the Stop gate blocks; deny = the pre-tool hook denies.

In numbers: 20 carried by a pre-registered case with the same verdict; 4 with a verdict that a decision
changed; 20 carried by a new `O..` case with the same verdict. 20 + 4 + 20 = 44. All 20 `O..` cases pass on the
merged hooks (`red-on-merged.txt`), as cases of the old fixture must.

D1, D2, D3 are the owner's three answers on the merge gate (2026-11-13). "Specification" is the rebuild's
specification, committed with this evidence when the rebuild lands.

## Stop gate (16)

| # | old case | old verdict | now |
|---|---|---|---|
| 1 | "Continue" then a commit, no governor | block | `F01-ungoverned-commit`, block:F1 |
| 2 | "re-pasted instructions complete" then a pull request by tool, no governor | block | `F24c-create-pull-request`, block:F1 |
| 3 | plan-gate loaded only after the push | block | `F31-plan-gate-after-first-act`, block:F1 |
| 4 | a merge with plan-gate but no adversarial-verify | block | new: `O01-plan-gate-without-adversarial-verify`, block:F1 |
| 5 | plan-gate before the push, adversarial-verify after | allow | new: `O02-plan-gate-before-verify-after`, allow |
| 6 | plan-gate, adversarial-verify, then commit and push | allow | `F30-verify-then-commit-and-push`, allow |
| 7 | skill names with a prefix count as loads | allow | new: `O03-synced-copy-skill-names-count`, allow |
| 8 | an edit only, no outward action | allow | `F32-edit-only-turn`, allow |
| 9 | a trivial question, no tool | allow | new: `O04-trivia-no-tools`, allow |
| 10 | read-only git commands | allow | new: `O05-read-only-git`, allow |
| 11 | an outward action before the owner's latest message does not count | allow | new: `O06-outward-act-before-the-owners-latest-message`, allow (rebuilt with the stop row a real record has between the two turns) |
| 12 | a task notification after the owner's message is not the owner | block | new: `O07-task-notification-row-is-not-the-owner`, block:F1 |
| 13 | S1: the owner's turn pushes before plan-gate; a scheduled run then loads both, in a file with no stop row | allow | **verdict changed** to block:F1: `F19c-legacy-owner-push-then-scheduled-run-loads-both`. Specification 2.3 and 6.1: in a file without any stop row nothing counts as judged, so the owner's ungoverned push is still open at this stop (finding FU2-3). The same file with the stop row a real record has is `J11a-run-after-owner-miss-with-stop-row`, allow |
| 14 | S2: a governed owner turn, then a scheduled run that commits with no governor | block | `F16a-scheduled-run-ungoverned-commit` and `F16c-legacy-scheduled-run-ungoverned`, block:F1 |
| 15 | S3: a GitHub notification is no boundary; the ungoverned commit before it still counts | block | new: `O08-github-notification-is-no-boundary`, block:F1 |
| 16 | S4: a notification read without a scheduled header is no boundary | block | new: `O09-read-without-a-header-is-no-boundary`, block:F1 |

## Pre-tool hook (18)

| # | old case | old verdict | now |
|---|---|---|---|
| 17 | "I've uploaded, proceed", the assistant's note before it calls the pull request mergeable | deny | `T03-yes-after-offer`, deny |
| 18 | "Proceed with recommendations and merge." | allow | **verdict changed** to deny, by D1: an order without the pull request number authorizes nothing. `T02-merge-it-no-number` |
| 19 | a click on "Merge all three" on a card that names no number | allow | **verdict changed** to deny, by D1 (a): the card must name the pull request. `M22-legacy-click-no-number-anywhere` |
| 20 | "Proceed with 1 and 2" after the assistant wrote 'Say "merge #29 and #156"', merging #29 | allow | **verdict changed** to deny, by D1: the assistant's own text grants nothing (specification 1.2, row G13). `T03-yes-after-offer` |
| 21 | the same, merging #31, which the assistant's text did not name | deny | `T03-yes-after-offer`, deny |
| 22 | "mergeable" in the assistant's text is not the word "merge" | deny | `T03-yes-after-offer`, deny (the assistant's text no longer counts at all) |
| 23 | the command-line merge on "ok" | deny | `R04a-gh-number-last`, deny |
| 24 | "Do not merge yet" | deny | `T07-do-not-merge-until-i-say-merge` and `T08-you-cant-merge-yet`, deny |
| 25 | "don't merge #26, merge #27", merging #27 | allow | `T05c-dont-merge-26-comma-merge-27`, allow |
| 26 | a click on "Wait" where only the question says merge | deny | `M04-click-wait-after-offer`, deny |
| 27 | `git merge origin/main` is a branch sync, not a merge of a pull request | allow | `N08-git-merge-origin-main`, allow |
| 28 | plan-gate loaded, no plan text, a branch is created | advise | new: `O10-branch-creation-after-load-no-plan`, advise |
| 29 | plan-gate loaded, the plan table shown | allow | `A07-plan-shown`, allow |
| 30 | a plan shown before a later plan-gate load does not count | advise | new: `O11-plan-shown-before-a-later-load`, advise |
| 31 | no plan-gate in the turn, an Edit | allow | `A08-no-load-no-ceremony`, allow |
| 32 | plan-gate loaded, a write under the scratch directory | allow | new: `O12-scratch-write-after-load`, allow |
| 33 | plan-gate loaded, a read-only shell command | allow | `A02a-readonly-grep-mention`, allow |
| 34 | S5: a scheduled run never merges; the owner's earlier "merge" does not carry into it | deny | `S13-legacy-scheduled-fixture` and `S01-scheduled-merge-tool`, deny:scheduled |

## The card reminder of the prompt hook (6)

These run `hooks/governance-trigger.py`, which the rebuild's three files do not include. They are carried so
that replacing the file drops no check.

| # | old case | old verdict | now |
|---|---|---|---|
| 35 | D1: a numbered "(Recommended)" list and no card | reminder | new: `O15-recommended-list-without-a-card`, reminder |
| 36 | D2: the same list, but a card was shown | silent | new: `O16-recommended-list-with-a-card`, silent |
| 37 | D3: "(Recommended)" only in prose | silent | new: `O17-recommended-only-in-prose`, silent |
| 38 | D4: a list without "(Recommended)" | silent | new: `O18-list-without-recommended`, silent |
| 39 | D5: a bullet "(Recommended)" and no card | reminder | new: `O19-recommended-bullet-without-a-card`, reminder |
| 40 | D6: the reminder is added beside the governance cue, not in its place | both | new: `O20-reminder-beside-the-governance-cue`, reminder with the governance cue |

## Others (4)

| # | old case | old verdict | now |
|---|---|---|---|
| 41 | the advisory is given once per plan-gate load: the second write of the same session passes | advise, then allow | new: `O13-advisory-once-per-load`, advise,allow |
| 42 | the retry flag is set and the record shows no block | allow | `F13c-retry-flag-without-any-block-on-record`, allow |
| 43 | the pre-tool hook's input is not JSON | allow, exit status 0 | `X01b-payload-not-json-plain`, allow |
| 44 | the Stop hook's input is not JSON | allow, exit status 0 | new: `O14-stop-payload-not-json`, allow |

## How the `O..` fixtures differ from the old ones

The old fixture built rows by hand: no `origin`, no ids that pair a result to its call, no stop rows. The `O..`
cases are rebuilt with `hooks/selftest_rows.py` in the row shapes of a real record: the owner's rows carry
`origin`, every result is paired to its call, and a stop row sits where a real record has one (cases 11 and 35
to 40). The situation and the verdict of each are the old ones.
