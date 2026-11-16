# What the auditors' files still flag after this unit (2026-11-16)

The files of both outside reads were run on the hooks of commit ed8ef13 (before) and on this tree (after); every line
that changed is in `auditors-before-after.txt`, each finding's run on the fixed tree in `repro-on-fixed.txt`. Below,
every line still marked "XX" or "MISMATCH" after the change, with one line of why. "Was XX before" means the line did
not change.

## Each finding's own file: nothing left

DM-1 `bbF.py`: 0 of 18 (before: 14 XX). DM-2 `dm2_retract.py`: "passed after a retraction: 0 of 18" (before: 18 of
18). DM-3 `dm3_condition.py`: "granted now: 0 of 22" (before: 22 of 22). DM-5, DM-6, DM-7, DM-8: no XX left. DS-1
`sim.py`: at most two F1 blocks in eight stops in all three modes, and "empty all": F1 2, receipt 1, prompt-class 1,
then let go (before: F1 8 and receipt 4, never let go). DS-2 `lcases.py`: "0 differ" (before: L1 and L1b). DS-5:
`sim.py input pc` and `input rc` unchanged (once each; the table now pins it).

## D4 by design: a wordier order, or a message typed mid-turn, now gets a card (the owner's decision)

| file | lines | the owner's words (examples) |
|---|---|---|
| `dm4_honest.py` (DM-4) | DM4-07, 09, 10, 11, 12, 13, 14, 18, 20, 21 (merge), 26, 27, 30 (push to main) | "Merge #34 because the checks passed.", "Merge #34 and let me know when it's done.", "Next steps:\n- merge #34 ...", "Squash and merge #34.", "Merge #34, it's been reviewed.", "Push straight to main, no PR needed." |
| `bbA.py` HO (honest orders) | HO06, 08, 09, 11, 15, 18, 20, 21, 22, 23, 24, 27, 28, 29, 30, 31, 32, 33, 34, 36 | "Merge #34 — the audit is clean.", "OK merge #34 and then update the README.", "Alright, let's merge #34." ("alright" is no lead-in word), "The audit is done, merge #34.", "Since CI passed, merge #34.", "Merge #34 so we can move on." |
| `bbA.py` NB (mid-turn remarks after "Merge #34.") | NB01 to NB13 | "Thanks!", "Sounds good.", "Ping me when it's done.", "Yes.", "Don't forget to merge #34.", "No need to ask again, just merge #34." |
| `bbB.py` CY (yes on a merge question) | CY03, 07, 08, 12, 16, 17 | "Merge #34 and upload the plugin?", "Merge #34 without waiting for the audit?", "Ready to merge #34?", "Merge #34? The audit passed." (the last sentence is not the question), "Merge #34 now, then report back?" |
| `bbB.py` PH (typed push orders) | PH03, 08, 09, 12, 13 | "Push the fix to main and then tell me.", "Push it to main, then upload the plugin.", "Push to main — the guard passed." |
| `bb7.py` | X01 (was ok), X05 (was XX) | mid-turn "thanks"; mid-turn "wait, not #141" (the whole word ends, #34 included) |
| `bbC.py` | C06 (was XX) | mid-turn "Also merge #34 in the deck." (rule C names the remedy too) |
| `dm9_cpu.py` (DM-9) | DM9-paste-then-order (was XX: gate-error) | the 71,691-character paste with the order as its last line: a message over 4,000 characters is not read (now `merge-word` in 0.10 s, not `gate-error` after 8 s). The paste followed by a card answered yes is allowed (`DM9-paste-then-card-yes`: ok). The in-process CPU lines at the head of that file time the module of the audited tree, not this one. |

## Unchanged by this unit (were XX before; stated limits or other units' defaults)

| file | lines | why |
|---|---|---|
| `bbD.py` | WR13, WR14 | printf / echo -e with a `\x65` escape: only `\n` and `\t` are decoded (a limit) |
| `bbD.py` | WR28 | an edit in place whose replacement text hides the merge words in quotes (`m''erge`): the file is unknown and the text screens miss the words (a limit) |
| `bbD.py` | DR03 | a script over 256 KB is not read (stated limit) |
| `bbD.py` | DR20 | `bash -o noexec FILE`: the file is read and denied though nothing runs (a rare false block, stated by the auditor as such) |
| `bbD.py` | DR34, DR36 | `pushd sub && bash x.sh`, `env -C sub bash x.sh`: the directory is unknown, so the file is not read (stated limit: a file named relative to a directory the gate does not know) |
| `bbD.py` | UW19, UW20 | `find ... -exec bash {} \;`: the script's name is filled in by find (now a stated limit in the README) |
| `bbD.py` | UW27, UW28, UW29 | an honest text that cannot be parsed and holds `git`, `push` and `main` is denied by the crude screen (stated: "crude on purpose") |
| `bbD.py` | RB20 | `gh api --raw-field query=@FILE` keeps "@FILE" as text: read as a body that cannot be read (fails closed; pre-existing) |
| `bbD.py` | RB25, RB26 | curl `-T FILE` and `--data-urlencode key@FILE` bodies are not read (pre-existing; outside the findings of this unit) |
| `bbH.py` | H-newline, H-dash, H-bad-utf8, H-nul-in-text, H-deep-nesting | script names with ANSI-C quoting, a leading dash after `--`, invalid UTF-8, a NUL byte, 30 nested `bash -c` (rare; the second read's MORE line) |
| `bb7.py` | Z08, Z12 | an input whose tool name or command is a list, not a string (pre-existing) |
| `bbC.py` | C08, C15, C16 | rule C (`BARE_NUMBER_ONE_REPOSITORY`): the second merge of a bare number in a call whose repository reads differently costs one card (a default; stated) |
| `repro_am7.py` (first read) | typed-number-other-repo, card-number-other-repo | rule C: the gate cannot know which repository the owner meant when the FIRST merge goes to another one (stated) |
| `repro_am_sched.py` (first read) | python-c | a merge through `python3 -c` (stated limit) |
| `bb14.py` (first read) | RD01 | a body the gate cannot read on the GraphQL path fails closed (pre-existing) |
| `repro_am4.py` (first read) | the five `-M03`, `-M05`, `-M06`, `-M12` lines (`exit2`) | a run of the auditor's own broken copies, which the scratch copy of the file does not have; the lines on this tree (`-fixed`) are ok |
| `bbx.py` (DS-3) | R1c, R1d, R1k, R1k2 | a denial in a wording outside the leads and without `toolDenialKind` counts as an act (stated limit, README; no lead was added, as the brief says) |
