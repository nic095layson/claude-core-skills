# Corrections log

Statements a session made to the owner that the records later showed to be wrong, each with how it was
caught and the check that would have prevented it. Append-only: a row is never edited or removed. A session
adds a row in the same pull request as its next change. `corrections_rate.py` turns this file into a weekly
rate; the weekly review reads it.

Rows 1 to 8 of 2026-11-12 cover the 21 failing rows of `results/2026-11-13/merge-audit/findings/AUDIT-TABLE.md`
(row numbers in brackets). Rows 9 to 12 come from the other auditors and from the run itself.

| Date | What was said | What the records showed | How it was caught | The check that prevents it |
|---|---|---|---|---|
| 2026-11-12 | "It never merges (the new hook enforces that)", of the weekly task; the same in pull request 34 and two READMEs | The task's session ran plugin 0.1.4, which has no scheduled-run rule. On 0.1.5 the hook stops two spellings of a merge; three other routes pass. [4, 43, 62, 65] | Outside auditors (WR-1, WR-2, F2-6, CB-1) | Test a claim about a gate on the copy that is installed where it runs, and name the version |
| 2026-11-12 | "Every hand-set value in hooks/ is registered, and the guard fails on an unregistered or changed one" | The registry check compares against a hand-written list of 33 names. Five of six changes to unlisted values pass the guard. [8, 49, 52, 63, 67, 69] | Outside auditor (CB-2) | Change one unlisted value and run the guard before writing "every" |
| 2026-11-12 | "6 values changed, 15 unregistered", of the old registry against the live hooks | A re-run gives 13 unregistered. The committed record shows none, because it was made with the old reader. [10, 33, 56, 70] | Outside auditor (CB-3) | Take a count from the committed record, never from memory |
| 2026-11-12 | "20 rules still untested after 60 days, oldest 124 days" | 20 marker lines are 13 items. The 124-day one is a sentence about a hardening idea, not a rule. [16, 36] | The session's own later check, then an outside auditor (CB-4) | Open the listed items before naming their unit |
| 2026-11-12 | "8 new tests", in the body of pull request 34 | The merged file has 10. [23] | Outside auditors (the weekly verifier, CB-5) | Read the pull request text against the final head before the merge card |
| 2026-11-12 | The trigger eval and the test run were presented as recorded evidence | The eval's raw outputs were not committed. The "green" test record is the 8-test output with a bare "OK" appended. [76, 77] | Outside auditor (CB-6) | Capture each record by running at the final head; commit raw outputs with model names removed |
| 2026-11-12 | "The kit fixed a library hook on 2026-11-03" | The kit's commit is dated 2026-11-04. [55] | Outside auditor (CB-7) | Read the commit's date, not the date in its message |
| 2026-11-12 | The merge cited doctrine rule 6 (no model names in pushed work) as followed | All three commits of the merge name the model in their trailer. [81] | Outside auditor (CB-8) | Read the commit messages for a model name before pushing |
| 2026-11-12 | The weekly run is "a scheduled, read-only session" | Its first step stashes, switches and hard-resets three live checkouts; its sixth pushes a branch and opens a pull request | Outside auditor (WR-4), confirmed by a second agent | Read the stored prompt's commands before describing what the run does |
| 2026-11-12 | "It switches itself off after 3 runs in a row with nothing you merge" | The stored rule counts pull requests, exempts ones that were touched, and never fires when runs fail before the sixth step | Outside auditor (WR-3), confirmed by a second agent | Work the stored rule through three histories before describing it |
| 2026-11-12 | "Prints its three sections and changes nothing (tested)" | The test passes when the pack is empty. The script leaves three bytecode files in the library | Outside auditor (WR-7), confirmed by a second agent | Break the script on purpose and see the test fail before citing the test |
| 2026-11-12 | The audit would take "about 2 to 3 hours" | Two usage windows bought six finished agent runs; the audit ran into the next day | The run itself | Check the account's usage limit before estimating a multi-agent run |
