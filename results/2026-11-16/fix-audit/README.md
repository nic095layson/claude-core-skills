# Outside reads of the fix (2026-11-16)

This folder is the record of the two outside reads of this pull request and of what was done with each finding.
The owner ordered them: the fix of the merge audit (pull request 35) is merged only after an outside audit, and on
2026-11-16 the owner chose a second read of every rule changed after the first one.

## Method

- **Readers.** Each area was read by a fresh agent that had not built the fix and had not seen the builder's
  reasoning (an "auditor"), followed at once by a second fresh agent that re-ran each finding from its reproduction
  and gave a verdict (CONFIRMED, UNCLEAR, REFUTED) and a severity. Both ran on a model other than the one that built
  the first part of the fix ("session model B"). They wrote only to scratch folders and had no GitHub, scheduling
  or mail tools.
- **What each auditor did.** Regression first (the earlier findings of its area, re-run against the fixed hooks),
  then black-box cases written from the owner's decisions and the stated rules before reading the code, then the
  code, then deliberate breaks of each new rule to see whether a test case catches them. Every finding carries a
  reproduction command and the output it printed.
- **Round 1** read the pull request at commit `c3c8615`, four areas: the merge gate, the Stop gate, the receipt gate,
  and what the pull request says about itself.
- **Round 2** read the changes made after round 1: the merge gate and the Stop gate at `7a5f978`, the receipt gate at
  `ed8ef13`.
- **Not read by any outside auditor** (the owner's choice of 2026-11-16, about 15:36 UTC, to keep the cost in
  bounds): the wiring files, the plugin package, the install runbook, the registry of hand-set values and the guard.
  The builder's own evidence for that area is in `results/2026-11-16/surfaces-fix/`.

## What is here

| file | what it holds |
|---|---|
| `findings-table.md` | every finding of both rounds, and two the builder found while reviewing (OW-1, OW-2): the second agent's verdict and severity, the state it is in now and where that was done |
| `raw/find-<area>.json`, `raw/verify-<area>.json` | each auditor's and each second agent's full report (scratch paths replaced by PACK, WORK, FIXED, SCRATCH) |
| `original-findings-status.md` | where each of the merge audit's 128 findings stands, built from the records |
| `first-preregistration-outcomes.md` | each prediction of `experiments/hypothesis-2026-11-14-gate-fixes.md` with its outcome |
| `timing.py`, `timing-at-<commit>.txt` | the run-time measurement of every gated hook on a 48 MB record, and its output |

The fixes themselves, with their red-first runs, are in `results/2026-11-16/audit-fixes/` (one folder per fix
unit).

## Totals

| round | areas | findings | confirmed by the second agent | unclear | high · medium · low (second agent) |
|---|---|---|---|---|---|
| 1 (`c3c8615`) | merge gate, Stop gate, receipt gate, the pull request's claims | 29 | 22 | 7 | 5 · 10 · 14 |
| 2 (`7a5f978`, `ed8ef13`) | the merge-gate, Stop-gate and receipt-gate changes made after round 1 | 25 | 22 | 3 | 2 · 12 · 11 |
| the builder's own review | OW-1 (round 1), OW-2 (round 2) | 2 | - | - | - |

State of all 56 at commit `008f04c` and this record (`findings-table.md` has one row each): fixed 34 · fixed in part,
the rest a stated limit 4 · changed by the owner's decision D4 4 · a default the owner decides on the merge card 4 ·
a stated limit 2 · a document corrected or added 8. No finding of either round is open without a state.

## What the reads taught (stated plainly)

- Both rounds found the same weakness in the merge gate: a typed order was read through lists of words, and every
  list leaked in both directions (orders for later that granted; honest orders that were refused). The owner then
  decided (D4, 2026-11-16): a typed message counts only when its order is plain and comes last; anything wordier
  gets a card. The grant side is now an allowlist; a miss costs one card, never a wrong merge.
- Three of round 2's findings were holes the builder's own fixes of round 1 opened (an endless Stop block, a
  table headed "Claim" exempting every row, a passive "by + noun" exempting any sentence); a fourth (a bracket after
  the pull requests) the builder found in its own design while reviewing round 2's fixes. A fix of a gate is itself
  a change that needs an outside read.
- The receipt gate's rules on natural language behave the same way. Its fixes keep the default on the side of
  judging the text, with short allowlists for exemptions, and its README lists what is still blocked wrongly.
