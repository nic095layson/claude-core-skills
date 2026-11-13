# PR #34 as merged (title and body, read live from GitHub 2026-11-12)

Title: QA loop: upstream the scheduled-run fix, standing hook registry, outcome metric, weekly review, council
State: merged 2026-11-12T21:35:59Z; base bfedb3e; head 18289f3; merge commit 1ce99d5; 38 files, +1347 -5; 3 commits.

## Body (verbatim)

This PR builds the seven proposals from the system-wide QA audit of 2026-11-12 (`results/2026-11-12/qa-loop/AUDIT.md`; ledger INC-2026-11-12-01), which the owner approved as P1–P7.

| # | Change | Evidence |
|---|---|---|
| P1 | A scheduled run is a turn of its own and never merges. Built in the kit on 2026-11-04 and upstreamed here unchanged; plugin 0.1.5. | The kit's fixture fails 3 cases on main (41/44) and passes 44/44 after |
| P5 | `redteam/` is now a standing registry of every hand-set value in `hooks/` (33 entries). The guard fails on drift. | The 2026-10-19 one-off failed against the live hooks: 6 drifted, 15 unregistered. A constant changed by one makes the guard FAIL |
| P3 | `corrections_rate.py` reports wrong statements to the owner per ISO week, split by who caught them. A convention line and a log template go with it. | On the kit's real log: 7 rows in one week, 2 owner-caught |
| P4 | `weekly_review.sh` is a read-only evidence pack for a weekly run that proposes and never merges. | It prints three sections and leaves the tree unchanged (test) |
| P7 | `stale_rules.py` lists rules still marked unmeasured after 60 days. | 20 today |
| P6 | The `council` skill comes in from the owner's account, body verbatim, plus an "outside read" rule and house sections. | Lint PASS; trigger eval fired 6/6 and stayed silent 4/4 |
| P2 | Account packages for independent-audit, red-team and council will be built from main after merge. | — |

**Checks**
- Pre-registered in `111fc60`; outcome appended to the hypothesis file.
- Guard PASS before and after.
- 8 new tests in `test_qa_loop.py`; the existing 17 still pass.
- Classifier fixture 45/45.

**Not measured**
- Whether the weekly run's proposals are useful.
- Whether a Council verdict beats an undeliberated answer.

**Follow-ups**
- Companion PR syncs the deck. The kit already carries these hooks byte-identical.
- After merge, the owner uploads plugin 0.1.5 and three skill packages.
- The weekly task is created only on the owner's word.

Do not merge without David's word.

# What the author told the owner in chat when reporting the work (claims to check like any other)

1. "The kit's test file goes from 41/44 to 44/44 on library code."
2. "The old 10/19 registry failed against today's hooks: 6 values changed, 15 unregistered. Changing one threshold by 1 now fails the guard."
3. "On the kit's real log: 7 this week, 2 caught through you."
4. "Prints its three sections and changes nothing (tested)."
5. "20 rules still untested after 60 days, oldest 124 days."
6. "Council copied into the library word for word, plus one rule ... Live test, 10 fresh sessions: loaded 6/6 when asked, stayed silent 4/4, including 'city council'."
7. "Guard passes before and after, and in a fresh clone; 10 new tests pass; existing tests unchanged."
8. "The registry leaves 23 thresholds marked 'hand-set, never calibrated'."
9. About the weekly task: "It never merges (the new hook enforces that), and it switches itself off after 3 runs in a row with nothing you merge."
10. "Until you upload 0.1.5, sessions with several repos attached run plugin 0.1.4, which treats a scheduled run as part of your previous turn."
11. Account packages: "each matches main" (the three .skill files and the .plugin file in sent/).
