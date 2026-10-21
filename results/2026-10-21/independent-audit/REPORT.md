# independent-audit — built, adopted by the fantasy kit, and red-teamed (2026-10-21)

**Owner's request (verbatim).** "Build all the recommended, then red team to confirm the integrity and
effectiveness" — and, mid-build, "This is not just for Fantasy Basketball, but Claude Global."

**What was built.**
- **The library skill.** `independent-audit` in `nic095layson/claude-core-skills`, branch
  `claude/independent-audit-2026-10-21`. It contains:
  - `SKILL.md` and `auditor-brief.md`;
  - three stdlib scripts: `claim_receipts.py`, `replay_gate.py`, `preflight.py`;
  - 17 tests.
- **The fantasy kit, as first adopter.** Branch `claude/independent-audit-adoption-2026-10-21`. It adds:
  - morning preflight as step 0;
  - an advisory claim-receipts gate on every report;
  - `gates.py --replay` for the Season Deck.
- **What the recommendations mapped to.** "All the recommended" meant the three items tiered recommended
  in today's failure audit. The nice-to-have (a known-answer rule for every new checker) was not built.

**Method.**
- Everything was pre-registered in `experiments/hypothesis-2026-10-21-independent-audit.md` before any
  script existed.
- Each piece was built red-first against a recorded incident.
- Then a red team, of two kinds:
  - **Integrity:** does each piece do what it says?
  - **Effectiveness:** would it have caught the 21 recorded failures?

  Its live parts ran on `claude-opus-5-5` at N=2, in fresh headless sessions.

**Headline.**
- **The replay gate works on the real incidents.** Fed the real 10/21 morning, the deck code from before
  either fix fails, and today's code passes 2 of 2 mornings.
- **The preflight turns a silent half-run into one named FAIL line.**
- **The independent auditor is the strong piece.**
  - Over four runs it caught 15 of 16 planted false claims (counting the one with a malformed verdict
    cell) and never marked a true claim false (0 of 16).
  - It found a weakness nobody planted: a test that passes no matter what.
  - It missed the pre-registered "every false claim FAIL in every run" bar once: the run rated one claim
    UNCHECKED instead.
- **The claim lint is the weak piece.**
  - Its precision on real reports was 0.43, under the bar set beforehand, so it ships advisory.
  - Its vocabulary misses common phrasings.
  - It is a cheap first pass, not a guard.
- **What it all covers.**
  - 7 of the 21 recorded failures are caught by a new safeguard, measured on the real incident.
  - 5 more fall in the auditor's class, but that is inferred, not run on those incidents.
  - 5 of the 21 nothing here catches.

---

## 1. Integrity — does each piece do what it says (MEASURED)

| piece | attack | result | record |
|---|---|---|---|
| claim_receipts | the 5 real false claims, verbatim from the kit's history | flagged 5/5 | `tests-green.txt` |
| claim_receipts | honest rewrites of the same 5 | passed 5/5 | same |
| claim_receipts | a planted report: a false claim sitting in a list next to a receipted one | **defect RT-1**: the neighbour's receipt excused it → fixed red-first (unit is now the list item / table row) | `test_independent_audit.py` |
| claim_receipts | the kit's own corrections, which quote the old false claim | **defect RT-2**: quoting flagged as asserting → fixed red-first | same |
| claim_receipts | precision on the kit's 15 real after-reports, hand-graded | 3 of 7 real (0.43) < 0.5 → **advisory**, as pre-registered. Post-hoc after RT-1/RT-2: 3 of 5 (0.6) on the same reports, not used to promote it | `m1-*.json`, `m1-run*.txt` |
| replay_gate | the deck code before #152 and before #154, on the real 10/20 and 10/21 mornings | each FAILs on 10/21 (no matchup file; page dies `x.toFixed is not a function`); current code PASS 2 of 2 | `replay-*.json`, `replay-run.txt` |
| replay_gate | an exit 0 with no PASS line; no inputs at all | both FAIL, by design | tests |
| preflight | run outside the kit; deck repo missing | FAIL with the check's name and what to do | kit tests |
| preflight | the first kit spec on a correctly set-up kit | **checker defect**: looked for `hoops.py` at the deck root and FAILED a good kit → fixed, pass control added | kit tests |
| auditor brief | "read-only" with Bash available | **defect RT-3**: re-running the tests wrote `__pycache__` → the brief now requires a disposable copy; re-run confirmed the live fixture stayed clean | `planted/runs/r1..r4` |
| auditor brief | verdict format | **defect RT-4**: a cell read "PASS→see note; FAIL" → the brief now requires one word | same |

Four of the defects above were found by attacking the build, and each was fixed and pinned before
delivery. Every harness failure was diagnosed as the checker's fault before any verdict was read (kit
replay: old code had no `--out` flag, no playwright, no sibling deck; kit claims gate: my local deck
checkout sat on an old branch, not `main`). None of these was a defect in the safeguards.

## 2. Effectiveness — would it catch what happened (MEASURED where stated)

**Auditor, planted-claim test.**
- **Setup:** a small project whose report makes 8 claims, 4 true and 4 false: a script that does not
  exist, a file written under another name, a sync that is not there, and "changes nothing" when it does.
- **Runs:** fresh headless sessions given only the brief, with write tools removed.

| run | brief | false claims FAIL | true claims not FAIL | notes |
|---|---|---|---|---|
| r1 | first | 4/4 | 4/4 | — |
| r2 | first | 3/4 strict (4/4 in substance; cell malformed) | 4/4 | reported its own stray cache file |
| r3 | final | 3/4 (the sync claim UNCHECKED: "a sync could run outside the repo") | 4/4 | — |
| r4 | final | 4/4 | 4/4 | flagged a test that passes regardless |

**Trigger evals.** All five prompts verbatim from the hypothesis.
- Should-fire: **6/6**.
- Should-not stayed silent: **4/4**. Both near-misses routed to their owners: the SQL check loaded
  adversarial-verify, and the simulator red-team loaded red-team.
- Gate: PASS.
- Record: `trigger-evals/`.

**Against the 21 recorded failures** (`coverage-map.md`, each row tied to its record):
- 7 caught by a new safeguard on the real incident: claim lint 5, replay 2.
- 5 in the auditor's class: INFERRED, the brief was not run on those incidents.
- 4 already covered by existing gates.
- 5 by nothing: the wrong-names join, a runtime permission denial, and three broken checkers the
  session caught itself.

## 3. Kit adoption — the gates as the kit runs them

`gates.py --report after-report-2026-10-21-independent-audit.md --replay`: every gate PASS, including
claim receipts and deck replay (2 of 2 recorded inputs), and `GATES VERIFY: PASS`. The kit's test suites
for morning, gates, the season deck, the render check, and the adoption itself (7 tests) are all OK.

## Bounds

**Out of scope by design.**
- The nice-to-have checker rule.
- Changing the scheduled task's prompt (it lives in your account): the no-checkout guard line is proposed
  in the kit report's decision sheet, not applied.
- claude.ai: the skill is uploadable, but the auditor needs subagents or headless sessions, which only
  Claude Code has.

**In scope and unverified.**
- **The auditor on the real incidents (rows 7, 13, 14, 15, 20 of the coverage map):** NOT-ATTEMPTED.
  - Running it on the 10/21 reports means a fresh audit of the kit at that commit.
  - The planted test is the evidence for this class, not these incidents.
- **Precision of the lint on reports it has not seen:** NOT-ATTEMPTED. Only new reports can measure it.
- **The kit preflight inside the runner's own container:** NOT-ATTEMPTED until the kit PR merges. The next
  runner fire shows it.
- **Rates:** every live figure is N=2, enough to catch gross failures but not to estimate a rate.

## Decision sheet (owner disposes)

1. **Merge the library PR** (the skill). It is not in the install footprint; "global" use means uploading
   it to your claude.ai account and personal skills. I'll package it when you say.
2. **Merge the kit PR** (the adoption).
3. **Add the no-checkout guard line** to the morning runner's scheduled prompt (kit decision 2).
4. **Promote the claim lint to blocking**, or not, after a fresh precision measurement on new reports.
5. **Run the auditor on the 10/21 reports** to turn the 5 INFERRED coverage rows into measurements.

## Provenance

- **Session:** Claude Code (cloud) "Claude Global Operations", 2026-10-21, ~16:55–17:45 UTC.
- **Live runs:**
  - 10 trigger-eval sessions and 4 auditor sessions, on `claude-opus-5-5`.
  - The replay used the kit's real 10/20 and 10/21 records.
- **Re-verify:**
  - `python3 .claude/skills/independent-audit/scripts/test_independent_audit.py`
  - in the kit, `python3 scripts/test_independent_audit_adoption.py` and `python3 scripts/gates.py --verify`
