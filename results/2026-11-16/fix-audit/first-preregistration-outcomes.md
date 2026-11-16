# The first pre-registration, prediction by prediction, at ed8ef13 (2026-11-16)

**Of its 16 predictions, 2 are met, 4 missed, 3 cannot be measured and 7 belong to units the owner moved to a second
pull request.** Of the 94 recorded breaks of G7, 35 are now caught by a named break, 41 belong to those units and
18 could not be placed.

`experiments/hypothesis-2026-11-14-gate-fixes.md` (committed 2026-11-14, before any change) made 12 predictions
G1 to G12 and 4 overall predictions, and ends: "A prediction that misses is reported as a miss." The evidence of
this pull request reported only against the second pre-registration
(`experiments/hypothesis-2026-11-15-turn-gates-cases.md`). The outside audit found this gap (finding AC-2). This file
closes it.

## How each outcome was read

| outcome | meaning |
|---|---|
| MET | every part of the prediction holds; the file or command that shows it is named |
| MISSED | a part did not happen as predicted; what happened instead is said |
| NOT MEASURED | a part cannot be measured on what exists; why is said |
| DEFERRED | a part belongs to a unit the owner moved to a second pull request (card of 2026-11-16, about 03:35 UTC: "Ship built part first"); the unit is named |

A prediction with several parts takes the weakest outcome among them, in this order: MISSED, NOT MEASURED, DEFERRED,
MET. Each part is described in its row.

"Outside auditor" means the fresh auditors of the outside audit of this pull request, who re-ran the reproductions
of the findings named in their regression lists at c3c8615 (quoted below by their status words). "Builder" means
the agents that made the fix. Three commits followed the outside audit (077c860, 7a5f978, ed8ef13). At ed8ef13 the
break list, run for this file (`python3 hooks/selftest-mutations.py`, 6 min 52 s), gives
`== 462 breaks: 462 caught, 0 survived, 0 stale; control: 0 failing of 1062 cases ==`; the control line is the
whole test table passing. The replay lines below come from the audit pack's replay tool, run for this file on the
hooks at ed8ef13 (`replay_real.py --hooks hooks --what all`, verdicts only).

## The predictions

| # | what it predicted (in short, in its own words) | outcome | evidence |
|---|---|---|---|
| G1 | Turn model rebuilt. "Each reproduction of TB-1 to TB-7, F2-4, F2-7, PC-1, RI-3, RI-5 prints the verdict its rule requires on the fixed hooks. The new tests for them fail on 1ce99d5 (run recorded) and pass on the fix" | **MET** | Outside auditors: TB-1, TB-2, TB-4, F2-4, F2-7, RI-3, RI-5 "fixed"; TB-3 "fixed" for the merge part (its Stop part is in the builder's table only: F17, F18, F19a); TB-5 "fixed: 14/14"; TB-7 and PC-1 "FIXED"; TB-6 denied "as D2 decides" (an owner decision of 2026-11-13). Red then green: `results/2026-11-15/turn-gates-fix/red-on-merged.txt` (349 cases, 204 fail on 1ce99d5) and `pass-on-fixed.txt` |
| G2 | Merge gate per D1 to D3. "Each reproduction of F2-1 to F2-8, RI-1, RI-2, RI-4, RI-7, WR-1, WR-2, SF-3 prints the rule's verdict. The honest merges of F2-8 that are refused today are allowed" | **MISSED** | Second sentence: of F2-8's 12 cases only c and g are allowed; the other 10 are still refused, each by an owner decision (D1, D2, Q1 and the 2026-11-15 answer on a card inside a scheduled run; outside merge auditor). D1 to D3 date from 2026-11-13, a day before the prediction, so as written it contradicted them. First sentence: F2-1 to F2-4, F2-7, RI-1, RI-2, RI-4, RI-7, WR-2 "fixed"; F2-5 "fixed for routes 1-3 and 5-8", route 4 a stated limit; SF-3 "FIXED in the wiring"; F2-6 and WR-1 wait for the owner's upload of plugin 0.1.6 (`results/2026-11-16/surfaces-fix/after-the-merge.md`) |
| G3 | Stop gate. "Each reproduction of F1-1 to F1-8, RI-6, RI-8 prints the rule's verdict. On the replay of the real session record the five false blocks of 2026-11-13 are gone" | **NOT MEASURED** | Second sentence: the replay record ends before 2026-11-13. Its last stop is 2026-11-12T21:36 (replay run for this file; `results/2026-11-15/receipt-gate-fix/replay-vs-baseline.md` gives the span 2026-10-21 to 2026-11-12), and no evidence file names the five blocks. First sentence: F1-1 to F1-6, F1-8, RI-6, RI-8 "FIXED" by the outside Stop auditor (F1-4 with two stated limits); F1-7 by the builder only: its 9 recorded changes are named by breaks CL01, CL02, CL04, CL05, CL06, CL26, ST07, ST08 and ST01, all caught at ed8ef13 |
| G4 | Prompt-class gate, classifier, prompt trigger, decision-cards reminder: "Each reproduction of PC-1 to PC-8 and TR-1 to TR-8 prints the rule's verdict, or the finding is listed as deferred with its reason" | **DEFERRED** (prompt side) | Re-run here: PC-1, PC-5 "FIXED"; PC-4 "D3 and D5b fixed" (case D2 changed by Q3); PC-6 "F1 half fixed"; PC-8 changed by Q5. PC-2, PC-3, TR-1 to TR-8 and the classifier part of PC-7 wait for the second pull request. The pull request names the unit, not each finding with its reason, as the "or" part asks |
| G5 | Receipt gate on the same turn; contractions matched. "Each reproduction of RL-1 to RL-8 and TB-5 prints the rule's verdict" | **MISSED** | Three reproduction cases do not print the rule's verdict: RL-6's Q01 and Q02 (a claim in a block quote or inline code) are still allowed, and RL-7's S05 (a scheduled run in a record with no stop row) still blocks. The outside receipt auditor reports them; `hooks/README.md` states Q01 and Q02 as a deliberate exemption. Everything else holds: RL-1 to RL-5, TB-5 and FU2-9 "fixed"; RL-6 "R 12/12 fixed"; RL-7 "6 as wanted"; RL-8 by the builder only: breaks RC02 to RC15 name all 11 surviving changes, all caught at ed8ef13 |
| G6 | Advisory hooks, first-write reminders, compaction protocol, plugin wrapper: "Each reproduction of ADV-1 to ADV-8, SF-5, SF-8 prints the rule's verdict, or the finding is listed as deferred" | **DEFERRED** (registry rest, advisory hooks and guard gaps) | ADV-4 "FIXED" (outside Stop auditor); ADV-1 is a stated limit (break AD02: the advisory says the record does not keep every message). ADV-2, ADV-3, ADV-5 to ADV-8, SF-5 and SF-8 wait for the second pull request |
| G7 | The tests pin the rules; the list of breaks is a standing check the guard runs. 94 recorded breaks pass today; "After the fix: 0 of the 94 pass. A break shown to change no behaviour is listed with the reason and not counted as caught" | **NOT MEASURED** | Standing check: the guard runs the break list (`results/2026-11-16/audit-fixes/receipt-gate/guard-after.txt`, line "every deliberate break ... is caught by the table"). The 94: 35 caught by a break named for them, 41 in deferred units, 18 not placed (table below). Whether any of the 94 was listed as changing no behaviour was not found in the evidence |
| G8 | The registry reads the hand-set values from the hook code. "Each reproduction of RG-1 to RG-8 prints the rule's verdict; the 16 unlisted changes of RG-1 all fail the registry check" | **NOT MEASURED** | The 16 changes of RG-1 were made on the old hooks and were not made again on the rebuilt ones. Holds: `redteam/live.py` reads the four gate modules whole (lines 27-28), and an unregistered word in one of them fails the check (`results/2026-11-15/receipt-gate-fix/registry-proof.txt`); RG-1 to RG-3 by the builder only. Deferred: RG-4 to RG-8 and the values outside those four modules (registry rest). The outside claims auditor noted that a hand-set value of the test runner (`HOOK_WAIT_SECONDS` in `hooks/selftest-turn-gates.py`) can change with the check still passing |
| G9 | Wiring, install runbook, parity checks, plugin version. "Each reproduction of SF-1 to SF-8 prints the rule's verdict; a project installed by the runbook to the letter runs every hook its settings call" | **DEFERRED** (SF-5, SF-8: registry rest, advisory hooks and guard gaps; SF-7: no unit named) | Second sentence MET: `results/2026-11-16/surfaces-fix/raw/runbook4-green.txt` (step 4 PASS), re-run by the outside claims auditor ("step 4 PASS"). SF-2, SF-4, SF-6 by the builder only (`results/2026-11-16/surfaces-fix/README.md`); SF-3 "FIXED in the wiring" (outside Stop auditor); SF-1 waits for the plugin upload. Not done here: SF-5, SF-7, SF-8, and SF-2's wrapper case W11 (it needs the wrapper's rule) |
| G10 | Weekly task: a new stored prompt and `weekly_review.sh`; the task is NOT re-enabled. "Each reproduction of WR-1 to WR-8 prints the rule's verdict; the three live checkouts are byte-identical before and after a dry run" | **DEFERRED** (weekly task prompt) | WR-2 "fixed" (outside merge auditor); WR-1 waits for the plugin upload; WR-3 to WR-8 and the dry run wait for the second pull request. Whether the task is still paused was not checked here (that needs the scheduling tools) |
| G11 | Outcome scripts and their tests. "Each reproduction of OS-1 to OS-8 prints the rule's verdict, or the finding is listed as deferred" | **DEFERRED** (outcome scripts) | No OS finding is in any regression list of this pull request |
| G12 | Documents and claims. "The 21 failed rows of the first claims audit, re-graded against the corrected text, pass; the second claims audit's rows likewise" | **DEFERRED** (documents and claims) | No re-grading was done in this pull request |
| 1 | Red first: "every MUST finding has a test that fails on 1ce99d5 and passes on the fix; both runs are recorded" | **DEFERRED** (the five units) | For the findings of this pull request the red and green runs are recorded: `results/2026-11-15/turn-gates-fix/red-on-merged.txt` and `pass-on-fixed.txt`, `results/2026-11-15/receipt-gate-fix/red-on-start.txt` and `pass-on-fixed.txt`, `results/2026-11-16/surfaces-fix/raw/` (red files), and `red-on-start.txt` / `table-after.txt` in each folder of `results/2026-11-16/audit-fixes/`. MUST findings of the deferred units have no test yet. F2-6, WR-1 and SF-1 cannot fail red in this repository (the old plugin runs on the account) |
| 2 | "`guard_essentials.sh` passes before ... and after. Every existing selftest still passes; an existing test that had to change is listed with the reason" | **MET** | Before: PASS on 1ce99d5 (recorded in the pre-registration, 2026-11-14 05:19Z). After, at ed8ef13: `results/2026-11-16/audit-fixes/receipt-gate/guard-after.txt` ends `== RESULT: PASS ==`. The old 44-case turn-gate fixture was replaced; each case's fate and the reason for each changed verdict is in `results/2026-11-15/turn-gates-fix/old-selftest-mapping.md` (20 + 4 + 20 = 44) |
| 3 | No new false block: "on the replay of the real session record, nothing the merged hooks allowed becomes a block or a denial, except where a finding names it as wrongly allowed; each exception is listed by finding id" | **MISSED** | Replay at ed8ef13, against the merged hooks: before a tool call 3 merge denials (the merged hooks had 1, a false one, now gone): two at 2026-10-21T23:25 tied to decision D1, not to a finding; one in the turn from 2026-11-12T21:23, tied to no finding (the replay judges a push with no branch named against today's checkout: `results/2026-11-15/turn-gates-fix/replay-vs-baseline.md`). Receipt gate: 2 of 26 stops blocked (2026-10-28T23:02, 2026-11-02T22:41) where the merged gate blocked none, tied to no finding id (`replay-vs-baseline.md` of the receipt gate: bare claims by the rule's words; the `RECEIPT_SCOPE` default is open for the owner). The other Stop gate adds no block (`BLOCK:F1` 2 to 1, prompt-class 1 to 1) |
| 4 | "An outside audit (fresh auditors, then a second agent on each finding) runs on the fix before the merge card. Its findings are reported whatever they are" | **MISSED** | It ran for four areas (claims, merge gate, receipt gate, Stop gate), each with a second agent's verdicts, and the three commits after it report what it found. The fifth area (wiring, plugin, runbook, registry, guard) was read by no outside auditor: the owner chose that on the card of 2026-11-16, about 15:36 UTC, and it is listed as open. No merge card had been shown at ed8ef13 |

Totals: **MET 2** (G1, 2) · **MISSED 4** (G2, G5, 3, 4) · **NOT MEASURED 3** (G3, G7, G8) · **DEFERRED 7** (G4, G6,
G9, G10, G11, G12, 1). 16 in all.

## G7: the 94 recorded breaks

The 94 and their split by finding are the pre-registration's own (G7 row): 9 (TB-8), 9 (F1-7), 11 of 13 (RL-8),
11 (PC-7), 15 of 16 (ADV-6), 16 of 16 on the registry check (RG-1), 20 of 20 (OS-3), 3 (SF-4). The names of the
breaks inside each group come from each finding's recorded output in the audit's findings file; for PC-7, whose
recorded output is cut short, from that auditor's full output (M1 to M10 and M12; M11 is a benign variant the
auditor did not count). A break counts as caught when a break in `hooks/selftest-mutations.py` names it in its
origin (for example `TB-8 M2`) and that break is caught at ed8ef13.

| finding | recorded | caught now, by | deferred (unit) | not placed |
|---|---|---|---|---|
| TB-8 | 9 | 7: M1 (WD19), M2 (RW01, RW02), M3 (RW22), M4 (SC01), M5 (RW19, RW20), M6 (CD02), M10 (RW18) | 0 | 2: M8 and M9 change the OLD receipt gate's own turn start. The specification routes them to the receipt gate's work (`results/2026-11-15/turn-gates-fix/CORE-SPEC.md`, section 6.3: "not in these files"); the rebuilt receipt gate uses the shared turn model, and no break names them |
| F1-7 | 9 | 9: M1a (CL01), M1b (CL02), M1c (CL04), M2 (CL05), M3 (CL06), M4 (CL26), M5 (ST07), M6 (ST08), M7 (ST01) | 0 | 0 |
| RL-8 | 11 | 11: M02 to M12 (RC02, RC03, RC04, RC05 to RC07, RC09, RC10, RC11, RC12, RC13, RC14, RC15), re-made on the rebuilt gate | 0 | 0 |
| PC-7 | 11 | 5: M1 (PC01), M3 (PC02, RW23), M4 (RW01), M5 (PC03); M2 (the allowance widened from 400 to 590 characters) through PS21 and PS22, which break the same value | 6: M6, M7, M8, M9, M10, M12, the classifier's patterns, markers and cue floor (prompt side) | 0 |
| SF-4 | 3 | 3: M3 (WI12, WI13), M4 (WI14, WI15), M5 (WI11) | 0 | 0 |
| ADV-6 | 15 | 0 | 15: the advisory, the reminders and the compaction hook (registry rest, advisory hooks and guard gaps). No break names ADV-6 | 0 |
| RG-1 | 16 | 0 | 0 | 16: made on the old hooks; no break or case names them, and they were not made again on the rebuilt files. Some fall in files that are deferred (classifier, reminders), some in the rebuilt gate modules; not counted one by one |
| OS-3 | 20 | 0 | 20 (outcome scripts) | 0 |
| **all** | **94** | **35** | **41** | **18** |

So "0 of the 94 pass" holds for the 35 that are caught. It is not established for the 18 not placed, and it waits
for the second pull request for the other 41.

Prediction 3's own words say that "each exception is listed by finding id"; the replay evidence of this pull request
lists them by decision or by explanation instead, which is part of why row 3 reads MISSED.
