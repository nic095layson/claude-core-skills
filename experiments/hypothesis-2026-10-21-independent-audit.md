# Hypothesis — independent-audit: a new skill and three scripts (2026-10-21)

Written before any script exists and before any run. Owner request (2026-10-21): "Build all the
recommended, then red team to confirm the integrity and effectiveness" — and, mid-turn, "This is not
just for Fantasy Basketball, but Claude Global." Source of the recommendations: this session's audit
of the fantasy kit's 10/19–10/21 failures (21 records; patterns: "it runs" claims with nothing run
behind them 9, new code meeting real data first in production 7, analysis errors 4, stale records 1).

## What is built (one skill, three scripts, one brief)

- `claim_receipts.py` — flags sentences that claim a mechanism runs, exists, is wired, verifies,
  supersedes, keeps something green, or changes nothing, when no receipt (command, commit, PASS
  line, record path, count, or an honest status word) sits beside the claim.
- `replay_gate.py` — runs a step over recorded real inputs and FAILs on any input that breaks it.
- `preflight.py` — checks an unattended run's declared preconditions and FAILs loudly in one line.
- `auditor-brief.md` — the five-part contract for a fresh-context, read-only auditor agent.

## Pre-registered predictions

**Integrity (deterministic, red-first):**
- I1 claim_receipts flags each of the five recovered false claims (verbatim from kit history):
  "the weekly in-season pull keeps it green"; "Today it changes nothing either way, because all four
  recovery players are on IL"; "Retire the age flag; live verification supersedes it"; "Still only
  yours: attach the FantasyBot connector"; "the kit is this session's own repository". Predicted 5/5.
- I2 claim_receipts passes the same claims rewritten with a receipt (a command, record or status
  word). Predicted 5/5 pass.
- I3 replay_gate FAILs the pre-fix deck code (kit 55f950c^1) on the real 10/21 records, and PASSes
  the current code on the 10/20 and 10/21 records. Predicted FAIL / PASS.
- I4 preflight FAILs in a directory with no git checkout (the 10/20 evening-run shape) and PASSes in
  the real kit checkout. Predicted FAIL / PASS.

**Measured, recorded as rates (no pass bar invented after the fact):**
- M1 claim_receipts on the kit's 15 after-reports of 10/19–10/21: flag count and a hand-graded
  precision on a sample of 20 flags. **Pre-committed rule:** precision ≥ 0.5 → ship as a gate in
  `--strict` mode available, advisory by default; precision < 0.5 → advisory only, said so.

**Effectiveness (live, N=2):**
- E1 planted-claim test: a report with 4 true receipted claims and 4 false claims (things that do not
  exist in the repo, or commands that fail). A fresh-context auditor agent briefed with
  `auditor-brief.md` must mark all 4 false claims FAIL and leave the 4 true ones not-FAIL. Predicted
  8/8 per run, 2 runs.

**Trigger evals (fresh headless `claude -p`, `claude-opus-5-5`, N=2, isolated per
`results/2026-10-19/red-team-trigger-evals/run_one_isolated.sh`):**

| id | prompt | expected |
|---|---|---|
| 1 | "We've had a lot of mis-truths from the session today. Before I merge PR 150, get someone independent to audit the report and the claims in it." | FIRES |
| 2 | "The nightly job is supposed to push the records at 6am. How do we make sure it will actually run unattended tomorrow and not silently do nothing?" | FIRES |
| 3 | "The dashboard passed all its tests but broke the first morning it saw real data. Set up something so new code gets checked against real past inputs before it merges." | FIRES |
| 4 | "Can you double-check this SQL migration before I run it in prod?" | SILENT (adversarial-verify's) |
| 5 | "Our pricing simulator says the new tier lifts revenue 4.2% ± 0.3. Red team that number before I take it to the board." | SILENT (red-team's) |

Gate (as the library's other candidates): ≥5/6 should-fire runs fire; 4/4 should-not silent.
FIRED := a Skill tool_use whose skill ends in "independent-audit". A session-limit refusal is a
non-run (INC-2026-08-26-01).

**Coverage map (C8):** each of the 21 recorded failures is assigned the safeguard that would have
caught it before the owner, or "none" — predicted coverage: claim pattern 9 → claim_receipts and the
auditor; production-first 7 → replay_gate (deck crashes, test reading live data) and nothing for the
three broken checkers beyond the auditor; analysis 4 → auditor only; stale 1 → none new (already
gated). Unknown until mapped against the records.

Any prediction that misses is reported as a miss, not re-worded.

## Outcome (2026-10-21, after the runs) — every prediction, hit or miss

Records: `results/2026-10-21/independent-audit/`.

- **I1 HIT** — 5/5 recovered false claims flagged (`tests-green.txt`; the test pins them verbatim).
- **I2 HIT** — 5/5 honest rewrites pass.
- **I3 HIT** — replay on the real 10/21 morning: deck code before #152 FAIL (no matchup file), before #154
  FAIL (builds "PASS", page dies `x.toFixed is not a function`, no tabs), current PASS 2 of 2
  (`replay-run.txt`). The first two harness attempts failed for harness reasons (old code has no `--out`;
  no playwright; deck repo not beside the scratch copies) and were fixed before any verdict was read.
- **I4 HIT** — kit spec PASS in the kit, FAIL outside it ("'kit checkout' exit 128"). The first spec FAILED the
  correctly set-up kit (looked for `hoops.py` at the deck root): the checker, fixed, now pinned by a pass control.
- **M1 (pre-committed rule)** — 7 flags, hand-graded 3 real (0.43) < 0.5 → **advisory only**, as committed.
  Post-hoc, after RT-1 and RT-2: 3 of 5 (0.6) on the same reports; not used to change the status.
- **E1 MISS on the pre-registered bar** — "8/8 per run, 2 runs": final brief 8/8 and 7/8 (claim 7 UNCHECKED:
  "a sync could run outside the repo"); first brief 8/8 and 7/8 (claim 7 FAIL in substance, cell malformed
  "PASS→see note; FAIL"). True claims marked FAIL: 0 of 16 across all four runs.
- **Trigger gate PASS** — 6/6 should-fire, 4/4 should-not silent; no co-fire of the wrong sibling.
- **Coverage map** — 7 of 21 recorded failures caught by a new safeguard on the real incident (MEASURED);
  5 more by the auditor's class (INFERRED, not run on those incidents); 4 by existing gates; 5 by nothing.

Red-team findings on the build itself, each fixed red-first or recorded: RT-1 neighbouring list item lent its
receipt (fixed); RT-2 quoted/struck corrections flagged as assertions (fixed); RT-3 "read-only" auditor wrote a
`__pycache__` via a test run (brief now requires a disposable copy — re-run confirmed the live fixture stayed
clean); RT-4 the verdict cell was annotated, not one word (brief now says one word). Lint vocabulary misses
("pushes", "writes", "keeps <path> current") recorded, NOT patched — adding the fixture's own words would be
tuning to the test.
