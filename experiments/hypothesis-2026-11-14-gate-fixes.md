# Hypothesis — fixing the defects the merge audit found in the governance gates (2026-11-14)

Written before any change and before any test run of the fix. The owner's words: card answer of 2026-11-13
("One fix PR, audited first"), three card answers of the same day on the merge gate (D1 to D3 below), and typed
on 2026-11-14: "I want these errors fixed and system to operate as robust and as intended as configured".

**What is being fixed.** The audit of the 2026-11-12 merge (`results/2026-11-13/merge-audit/`, draft pull request
35, not on main yet). On file when this was written (2026-11-14 05:20Z): 13 of 15 areas examined, 104 findings,
56 re-run by a second agent (52 CONFIRMED, 4 UNCLEAR, 0 REFUTED). Second checks for the other 48, the last two
areas and a completeness critic were still running; whatever they add joins the population below.

**The owner's decisions on the merge gate (2026-11-13).**
D1: a merge is authorized only by a click on a card that names the pull request, or by a typed order to merge
with its number; a bare "yes" or "proceed" no longer is. D2: the authorization covers only the pull requests
named and ends when the assistant stops; a later wake-up starts with none. D3: auto-merge and a direct push to a
default branch need the same word; in a scheduled run they are always denied.

**What this pull request must fix, fixed in advance.**

- MUST: every finding of kind false_allow, false_block, wrong_result or crash_or_fail_open rated medium or
  above by the second agent (or by the finder where no second agent has run); every test_gap; every overclaim
  (by changing the code or by correcting the claim).
- MAY DEFER, each with a written reason in the pull request: findings rated low; findings of kind ambiguity.
- A finding a second agent marked UNCLEAR, or any point where the stated rule is silent: the safest reading
  becomes the default behind one named constant, and the question goes to the owner.
- A finding a second agent REFUTES is not fixed; it is listed as refuted.

| id | change | prediction (checked how) |
|---|---|---|
| G1 | Turn model rebuilt on what the record itself says about each row: typed by the owner, sent by the owner mid-turn, a card answer paired to its own card, written by the harness, a scheduled notification inside a real notification read, or a helper agent's row. No owner message in the record means the gates fail closed for merges | Each reproduction of TB-1 to TB-7, F2-4, F2-7, PC-1, RI-3, RI-5 prints the verdict its rule requires on the fixed hooks. The new tests for them fail on 1ce99d5 (run recorded) and pass on the fix |
| G2 | Merge gate per D1 to D3: bound to the pull request number; a click counts only when paired with a real card; a refusal in any spelling is a refusal; every merge route is judged; a scheduled run is denied | Each reproduction of F2-1 to F2-8, RI-1, RI-2, RI-4, RI-7, WR-1, WR-2, SF-3 prints the rule's verdict. The honest merges of F2-8 that are refused today are allowed |
| G3 | Stop gate: a command counts when it runs the action, not when its text mentions it; outward actions of helper agents count; a Skill load that errored does not count; one block per miss; no bypass after another hook's block | Each reproduction of F1-1 to F1-8, RI-6, RI-8 prints the rule's verdict. On the replay of the real session record the five false blocks of 2026-11-13 are gone |
| G4 | Prompt-class gate, classifier, prompt trigger, decision-cards reminder | Each reproduction of PC-1 to PC-8 and TR-1 to TR-8 prints the rule's verdict, or the finding is listed as deferred with its reason |
| G5 | Receipt gate judged on the same turn as the other gates; contractions matched | Each reproduction of RL-1 to RL-8 and TB-5 prints the rule's verdict |
| G6 | Advisory hooks, first-write reminders, compaction protocol, plugin wrapper | Each reproduction of ADV-1 to ADV-8, SF-5, SF-8 prints the rule's verdict, or the finding is listed as deferred |
| G7 | The tests pin the rules. Every deliberate break an auditor made that passed becomes a test, and the list of breaks is kept as a standing check the guard runs | Recorded today as passing: 9 (TB-8), 9 (F1-7), 11 of 13 (RL-8), 11 (PC-7), 15 of 16 (ADV-6), 16 of 16 on the registry check (RG-1), 20 of 20 (OS-3), 3 (SF-4): 94 in all. After the fix: 0 of the 94 pass. A break shown to change no behaviour is listed with the reason and not counted as caught |
| G8 | The registry reads the hand-set values from the hook code, so a value it does not list fails the check | Each reproduction of RG-1 to RG-8 prints the rule's verdict; the 16 unlisted changes of RG-1 all fail the registry check |
| G9 | Wiring, install runbook, parity checks between the copies, plugin version raised | Each reproduction of SF-1 to SF-8 prints the rule's verdict; a project installed by the runbook to the letter runs every hook its settings call |
| G10 | Weekly task: a new stored prompt and `weekly_review.sh` that work on copies, run a preflight first and count runs in the stop rule. The task is NOT re-enabled by this pull request | Each reproduction of WR-1 to WR-8 prints the rule's verdict; the three live checkouts are byte-identical before and after a dry run |
| G11 | Outcome scripts (`corrections_rate.py`, `stale_rules.py`) and their tests | Each reproduction of OS-1 to OS-8 prints the rule's verdict, or the finding is listed as deferred |
| G12 | Documents and claims: the statements the claims audits failed are corrected; ledger entry; corrections log rows | The 21 failed rows of the first claims audit, re-graded against the corrected text, pass; the second claims audit's rows likewise |

**Overall predictions.**

1. Red first: every MUST finding has a test that fails on 1ce99d5 and passes on the fix; both runs are recorded.
2. `guard_essentials.sh` passes before (recorded 2026-11-14 05:19Z on 1ce99d5: PASS) and after. Every existing
   selftest still passes; an existing test that had to change is listed with the reason.
3. No new false block: on the replay of the real session record, nothing the merged hooks allowed becomes a
   block or a denial, except where a finding names it as wrongly allowed; each exception is listed by finding id.
4. An outside audit (fresh auditors, then a second agent on each finding) runs on the fix before the merge card.
   Its findings are reported whatever they are.

Not measured here, said in advance: behaviour in a live session beyond the replay; claude.ai, which has no
hooks; the owner's own computer; whether a plugin upload reaches a long-running session. A prediction that
misses is reported as a miss.
