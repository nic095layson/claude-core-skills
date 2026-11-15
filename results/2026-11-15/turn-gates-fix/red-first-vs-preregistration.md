# Red first: the test table on the merged hooks, against the pre-registration (2026-11-15)

What was run: `python3 hooks/selftest-turn-gates.py --hooks <the merged hooks, commit 1ce99d5>`, on 2026-11-15,
before any of the three hook files was changed. The full output is `red-on-merged.txt` in this folder. The
table is `hooks/selftest-turn-gates.py` as it stands at this commit; its fixtures are built by
`hooks/selftest_rows.py`.

The pre-registration is `experiments/hypothesis-2026-11-15-turn-gates-cases.md` (prediction 2: 188 RED rows).
RED = the merged hooks give another verdict than the wanted one (the case prints FAIL). pin = the same verdict.

## Counts

| table | cases | RED, pre-registered | RED, measured | pin, pre-registered | pin, measured |
|---|---|---|---|---|---|
| 1 (the 254 cases of the first design) | 254 | 145 | 146 | 109 | 108 |
| 2 (30 cases of the second design) | 30 | 25 | 26 | 5 | 4 |
| 3 (new cases) | 30 | 18, and 1 marked "new" | 20 | 11 | 10 |
| tables 1 to 3 | 314 | 188, and 1 "new" | 192 | 125 | 122 |
| O (cases of the earlier fixture, not pre-registered) | 20 | - | 0 | - | 20 |
| whole table | 334 | - | 192 | - | 142 |

Prediction 2 said 188 RED rows. Measured: 192. The four rows that make the difference are listed below; each
is a mark that moved, none is a wanted verdict that changed. No case ended with a runner error.

Every name, every wanted verdict and (for table 1) every findings tag of the pre-registration is in the table,
exactly and in the same order: checked by a script that parses the pre-registration and the table's `--list`
output (314 names, 0 mismatches).

## Every case whose mark differs from the pre-registration

| case | table | pre-registered mark | measured | merged verdict, recorded then | merged verdict now | reason |
|---|---|---|---|---|---|---|
| `M14-free-text-answer-merge-it` | 1 | pin | RED | allow | deny | The fixture is rebuilt as the specification orders (6.1): a card answered with free text now comes back in the program's second answer form ("The user answered: ..."). The merged hooks look only for the words of the first form, so they no longer see the answer. The wanted verdict (allow) is unchanged |
| `m_d1_card_free_text_refusal` | 2 | pin | RED | deny, no code | deny, no code | The merged verdict is the same as recorded. The wanted verdict carries a code, `deny[merge-word]`, and the table requires a code in brackets to be in the denial text. The merged hooks print no code, so the case fails on them. The pre-registered mark compared the kind of verdict only |
| `J04c-deadline-stop` | 3 | pin (predicted, not run) | RED | allow (predicted) | block:F1 | The prediction assumed the slow record reader would be reached. The merged Stop hook reads the record with its own lines and never calls the shared reader, so the replaced reader does not run there. The fixture is an owner turn with a commit and no governor (the same record as `X05c`), so that a hook which does read the record would block; the merged hook does, at once. With a record that holds nothing to block the mark would be a pin, and the case would show nothing about the deadline |
| `J17-span-equals-stretch` | 3 | new | RED | no such interface | no span output | Not a move in substance: the pre-registration marks the case "new" because the merged hooks have no `span` command line. The case fails on them, as expected, and is counted with the RED rows here |

## Merged verdicts that read differently from the recorded ones, with the same mark

| case | recorded | now | why |
|---|---|---|---|
| `W01-matcher` | 12 classified names are not selected (read from the pattern's text) | 20 of 38 classified names not selected; 6 read-only names selected | The table checks every leaf under two server prefixes (`mcp__github__`, `mcp__other__`): 4 built-in names and 8 leaves under 2 prefixes = 20. The same 12 distinct names. The 6 read-only names are selected because the merged pattern is a search, not a whole-name match |
| `J04a-deadline-merge-tool` | the hook is cancelled at the wired 10 seconds and the merge proceeds | no answer within 9 seconds | The runner stops waiting after 9 seconds; the merged hook was still inside the slow reader |
| table 2, the four cases recorded as `deny[-]` and marked RED | deny, no code | deny | The same verdict; the table prints a code only when the wanted verdict has one |

For table 1 the comparison was made by script: in 253 of 254 cases the merged verdict equals the recorded one
word for word; the one that differs is `M14` above.

## What this run does not show

- It says nothing about the fixed hooks: none exists at this commit.
- The 20 cases named `O..` are pins by construction: each carries a case of the earlier fixture
  (`old-selftest-mapping.md`) with its old verdict.
- `J04b-deadline-edit` is a pin that waits out the slow reader (20 seconds) on hooks without a deadline: it
  shows the direction (allow, exit status 0), not the time. Only `J04a` carries the time limit.

## Cases added after the pre-registration

Added on 2026-11-15, after the run above. The table now holds 349 cases: the 314 pre-registered ones, unchanged in name and
wanted verdict, and the 35 below. `red-on-merged.txt` was made again at the end, with the same command, on the grown table:
**349 cases, 145 pass, 204 fail** on the merged hooks. The verdict of every one of the 347 cases of the run before it is the same,
word for word (compared by script). The rows are in the order of the table: `J16b`, the 14 cases added last, then the `O..` cases.

| case | wanted verdict | verdict of the merged hooks | why it is in the table |
|---|---|---|---|
| `J16b-stale-ledger-note-is-not-counted` | allow | allow (pin) | added while the hooks were rebuilt, as the twin of `J16`: a helper's note that is older than the first row of the stretch is not counted, although it names more rows than the record now holds (the time stamp places a note, not the row count) |
| `X01c-payload-not-json-push-main` | deny [gate-error] | allow (RED) | the failure paths of the pre-tool hook did not know a push to a default branch (review of the rebuilt hook, 2026-11-15; decision D3 puts it in the same class as a merge). Written first: on the rebuilt hooks as they stood the verdict was `allow`; it is the wanted one since the crude screen of the failure paths knows such a push (`CRUDE_PUSH_WORDS`) |
| `X04c-shared-module-missing-push-main` | deny [gate-error] | allow (RED) | the failure paths of the pre-tool hook did not know a push to a default branch (review of the rebuilt hook, 2026-11-15; decision D3 puts it in the same class as a merge). Written first: on the rebuilt hooks as they stood the verdict was `allow`; it is the wanted one since the crude screen of the failure paths knows such a push (`CRUDE_PUSH_WORDS`) |
| `X04d-shared-module-missing-push-branch` | allow | allow (pin) | control of the same change: on a failure path a push to another branch is still let through. On the rebuilt hooks before the change: `allow` |
| `X04e-shared-module-missing-push-all` | deny [gate-error] | allow (RED) | the failure paths of the pre-tool hook did not know a push to a default branch (review of the rebuilt hook, 2026-11-15; decision D3 puts it in the same class as a merge). Written first: on the rebuilt hooks as they stood the verdict was `allow`; it is the wanted one since the crude screen of the failure paths knows such a push (`CRUDE_PUSH_WORDS`) |
| `X04f-shared-module-missing-push-mirror` | deny [gate-error] | allow (RED) | the failure paths of the pre-tool hook did not know a push to a default branch (review of the rebuilt hook, 2026-11-15; decision D3 puts it in the same class as a merge). Written first: on the rebuilt hooks as they stood the verdict was `allow`; it is the wanted one since the crude screen of the failure paths knows such a push (`CRUDE_PUSH_WORDS`) |
| `X05e-error-while-classifying-push-main` | deny [gate-error] | allow (RED) | the failure paths of the pre-tool hook did not know a push to a default branch (review of the rebuilt hook, 2026-11-15; decision D3 puts it in the same class as a merge). Written first: on the rebuilt hooks as they stood the verdict was `allow`; it is the wanted one since the crude screen of the failure paths knows such a push (`CRUDE_PUSH_WORDS`) |
| `X05f-error-while-classifying-push-branch` | allow | allow (pin) | control of the same change: on a failure path a push to another branch is still let through. On the rebuilt hooks before the change: `allow` |
| `J04d-deadline-while-classifying-push-main` | deny [gate-error] within 9 seconds | allow in 0.0 seconds (RED) | the failure paths of the pre-tool hook did not know a push to a default branch (review of the rebuilt hook, 2026-11-15; decision D3 puts it in the same class as a merge). Written first: on the rebuilt hooks as they stood the verdict was `allow in 8.0 seconds`; it is the wanted one since the crude screen of the failure paths knows such a push (`CRUDE_PUSH_WORDS`) |
| `S17-card-inside-run-then-owner-message` | deny [merge-word] | deny:scheduled[-] (RED) | a case the break list showed to be missing: with the rule removed (break `SC05`: a card answered inside a scheduled run grants) every other case still passed. Rule G14 of the specification: such a card grants nothing, also after the owner writes |
| `M06b-click-merge-nothing-on-one-pr-card` | deny [merge-word] | allow (RED) | a case the break list showed to be missing (break `CD11`: a chosen option that refuses is read as an order). Rule G9: a refusing option grants nothing, here on a card that names exactly one pull request, where the option would otherwise take the question's number |
| `M19b-structured-answer-to-question-never-asked` | deny [merge-word] | allow (RED) | a case the break list showed to be missing (break `CD05`): `M19` gives the answer as text; this one gives it in the structured field of the result row, where an answer to a question the card did not ask must be dropped as well |
| `T30b-order-then-wake-with-no-stop-row` | deny [no-owner-word] | allow (RED) | a case the break list showed to be weak (break `RW16`: a wake row does not end the word): the only case that caught it was the restart notice (`T32`). Decision D2: work started by a wake-up starts with no word, also in a record that holds no stop row before the wake |
| `X06a-merge-gate-keeps-its-own-list-merge` | deny [merge-word] | the Stop gate's list was found 0 times (RED) | the merge gate looked only at calls whose act was on the Stop gate's list of counted acts, so narrowing that list (one of the owner's switches) would have switched the gate off for those calls (found by the builder of the break list, 2026-11-15). These cases run a copy of the hooks whose Stop list holds commits only. On the rebuilt hooks before the change: `allow` |
| `X06b-merge-gate-keeps-its-own-list-push-main` | deny [default-branch] | the Stop gate's list was found 0 times (RED) | the merge gate looked only at calls whose act was on the Stop gate's list of counted acts, so narrowing that list (one of the owner's switches) would have switched the gate off for those calls (found by the builder of the break list, 2026-11-15). These cases run a copy of the hooks whose Stop list holds commits only. On the rebuilt hooks before the change: `allow` |
| `O01-plan-gate-without-adversarial-verify` | block:F1 | block:F1 (pin) | carries a case of the earlier fixture (44 cases, 2026-10-29) that no pre-registered case carries, with its old verdict (`old-selftest-mapping.md`) |
| `O02-plan-gate-before-verify-after` | allow | allow (pin) | carries a case of the earlier fixture (44 cases, 2026-10-29) that no pre-registered case carries, with its old verdict (`old-selftest-mapping.md`) |
| `O03-synced-copy-skill-names-count` | allow | allow (pin) | carries a case of the earlier fixture (44 cases, 2026-10-29) that no pre-registered case carries, with its old verdict (`old-selftest-mapping.md`) |
| `O04-trivia-no-tools` | allow | allow (pin) | carries a case of the earlier fixture (44 cases, 2026-10-29) that no pre-registered case carries, with its old verdict (`old-selftest-mapping.md`) |
| `O05-read-only-git` | allow | allow (pin) | carries a case of the earlier fixture (44 cases, 2026-10-29) that no pre-registered case carries, with its old verdict (`old-selftest-mapping.md`) |
| `O06-outward-act-before-the-owners-latest-message` | allow | allow (pin) | carries a case of the earlier fixture (44 cases, 2026-10-29) that no pre-registered case carries, with its old verdict (`old-selftest-mapping.md`) |
| `O07-task-notification-row-is-not-the-owner` | block:F1 | block:F1 (pin) | carries a case of the earlier fixture (44 cases, 2026-10-29) that no pre-registered case carries, with its old verdict (`old-selftest-mapping.md`) |
| `O08-github-notification-is-no-boundary` | block:F1 | block:F1 (pin) | carries a case of the earlier fixture (44 cases, 2026-10-29) that no pre-registered case carries, with its old verdict (`old-selftest-mapping.md`) |
| `O09-read-without-a-header-is-no-boundary` | block:F1 | block:F1 (pin) | carries a case of the earlier fixture (44 cases, 2026-10-29) that no pre-registered case carries, with its old verdict (`old-selftest-mapping.md`) |
| `O10-branch-creation-after-load-no-plan` | advise | advise (pin) | carries a case of the earlier fixture (44 cases, 2026-10-29) that no pre-registered case carries, with its old verdict (`old-selftest-mapping.md`) |
| `O11-plan-shown-before-a-later-load` | advise | advise (pin) | carries a case of the earlier fixture (44 cases, 2026-10-29) that no pre-registered case carries, with its old verdict (`old-selftest-mapping.md`) |
| `O12-scratch-write-after-load` | allow | allow (pin) | carries a case of the earlier fixture (44 cases, 2026-10-29) that no pre-registered case carries, with its old verdict (`old-selftest-mapping.md`) |
| `O13-advisory-once-per-load` | advise,allow | advise,allow (pin) | carries a case of the earlier fixture (44 cases, 2026-10-29) that no pre-registered case carries, with its old verdict (`old-selftest-mapping.md`) |
| `O14-stop-payload-not-json` | allow | allow (pin) | carries a case of the earlier fixture (44 cases, 2026-10-29) that no pre-registered case carries, with its old verdict (`old-selftest-mapping.md`) |
| `O15-recommended-list-without-a-card` | reminder | reminder (pin) | carries a case of the earlier fixture (44 cases, 2026-10-29) that no pre-registered case carries, with its old verdict (`old-selftest-mapping.md`) |
| `O16-recommended-list-with-a-card` | silent | silent (pin) | carries a case of the earlier fixture (44 cases, 2026-10-29) that no pre-registered case carries, with its old verdict (`old-selftest-mapping.md`) |
| `O17-recommended-only-in-prose` | silent | silent (pin) | carries a case of the earlier fixture (44 cases, 2026-10-29) that no pre-registered case carries, with its old verdict (`old-selftest-mapping.md`) |
| `O18-list-without-recommended` | silent | silent (pin) | carries a case of the earlier fixture (44 cases, 2026-10-29) that no pre-registered case carries, with its old verdict (`old-selftest-mapping.md`) |
| `O19-recommended-bullet-without-a-card` | reminder | reminder (pin) | carries a case of the earlier fixture (44 cases, 2026-10-29) that no pre-registered case carries, with its old verdict (`old-selftest-mapping.md`) |
| `O20-reminder-beside-the-governance-cue` | reminder with the governance cue | reminder with the governance cue (pin) | carries a case of the earlier fixture (44 cases, 2026-10-29) that no pre-registered case carries, with its old verdict (`old-selftest-mapping.md`) |

Of these 33, 10 are RED on the merged hooks and 23 are pins (the 20 `O..` cases by construction, the two controls, and `J16b`).
None of them is a pre-registered case: predictions 1 and 2 are read on the 314 names of tables 1 to 3, as before.
The four cases that came from the break list pass on the rebuilt hooks without any change to the hooks: each pins a rule the code
already kept and no case tested.
