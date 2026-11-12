# Hypothesis — closing the integrity gaps and adding an outcome-driven improvement loop (2026-11-12)

Written before any change. Owner's clickable answer (2026-11-12) to the system-wide QA audit of the same day
(`results/2026-11-12/qa-loop/AUDIT.md`): build P1+P2+P5, P3+P4, P6+P7.

| id | change | prediction (checked how) |
|---|---|---|
| P1 | The kit's scheduled-run turn fix (kit `b040962` and later) becomes the library's `hooks/turngate.py`, `turn-gates-pretool.py`, `governance-enforce.py`, `selftest-turn-gates.py`; plugin 0.1.5; deck synced | The kit's fixture passes unchanged in the library (44/44); the cases added by the kit fail on library main; classifier fixture still 45/45; all three repos byte-identical on those files |
| P2 | `.skill` packages of independent-audit and red-team built from main for the owner's account | Each zip holds `<name>/SKILL.md` plus its scripts; SKILL.md identical to the repo copy |
| P5 | The hooks' constants registry moves to a standing `redteam/` at the repo root, re-read from today's live hook code, and the guard runs the registry check | On main the old registry is stale (≥6 live hand-set values unregistered: TRIVIA_MAX_CHARS, CUE_MIN_WORDS, RECEIPT_WINDOW, the merge-negation window, the plan marker, the outward-action patterns); after, `registry_check.py` passes and a deliberately changed constant makes the guard FAIL |
| P3 | `corrections_rate.py` (independent-audit/scripts) reads a project's corrections log and prints wrong statements per ISO week, split owner-caught / session-caught; convention line in this repo's CLAUDE.md (outside the doctrine block) and a template | On the kit's real log of 2026-11-12: 7 rows, one week, owner-caught 2, session-caught 5; an empty or missing log prints 0 and exits 0; a malformed row is counted as unparsed, never dropped silently |
| P4 | A weekly scheduled run (Mondays, fired into the library's operations session) executes `weekly_review.sh`: corrections rates, registry check, stale-rule list, then ONE fresh-context read-only auditor over the week's records, then one draft PR of proposals; never merges; stops itself after 3 consecutive runs whose PRs were not merged | `weekly_review.sh` runs read-only and exits 0 on today's repos, printing the three sections; the trigger is created only after the owner's merge word. Whether its proposals are useful: UNMEASURED until it has run |
| P6 | Council enters the library as a support skill: body verbatim from the account copy, description byte-identical, plus house sections and one added rule (a verdict the owner will rely on gets one independent-auditor read) | Lint PASS. Trigger eval, fresh headless sessions, N=2, session model B: should-fire ≥5/6 on three prompts ("council: should I …", "convene the council on …", "get the council's take …"), silent 4/4 on two near-misses ("what's the city council's role in zoning?", "double-check this migration before I run it") |
| P7 | `stale_rules.py` lists every UNMEASURED / candidate marker in skills and instructions older than 60 days by its nearest date | Runs on main and prints a dated list; a marker dated today is not listed; one dated 2026-08-03 is |

Not measured here, said in advance: behavioural effect of any wording; council's value (only its triggering);
P4's usefulness. A prediction that misses is reported as a miss.

## Outcome (2026-11-12, after the runs)

- **P1 HIT** — the kit's fixture: 41/44 on library main (S1, S2, S5 fail), 44/44 after; classifier 45/45.
- **P2** — packages built from main after merge (see the PR).
- **P5 HIT, and worse than predicted** — the old registry failed on live with 6 drifted values (predicted:
  unregistered ones only) and 15 unregistered (predicted: at least 6). After: 33 = 33 PASS; a constant
  changed by one makes the guard FAIL (`p5-guard-catches-drift.txt`).
- **P3 HIT** — the kit's log: 7 rows, one week, owner-caught 2 as predicted; session-caught 5
  as predicted. The fixture test's own regex was wrong (it expected "rows " where the output says "rows,");
  the test was corrected, the script was not.
- **P4** — `weekly_review.sh` exits 0, prints three sections, leaves the tree unchanged (test). The trigger
  is created only on the owner's merge word. Usefulness UNMEASURED.
- **P6 HIT** — should-fire 6/6, silent 4/4 (including "city council", which contains the keyword).
- **P7 HIT** — on main: 20 markers older than 60 days, 11 newer, 12 undated.

