# Merge audit of 2026-11-13: the record

**Status on 2026-11-13: the defects documented here are not fixed.** This record was published on the owner's
decision of that day, made after the session reported that the repository is public. The report is `REPORT.md`; everything else
is the raw material behind it.

| Path | What it holds |
|---|---|
| `REPORT.md` | The report: verdicts, the findings with duplicates merged, bounds, decisions |
| `findings/all-results.json` | The five auditors' 40 findings in full, and the second agent's 8 verdicts on the weekly task |
| `findings/claims-results.json`, `findings/AUDIT-TABLE.md` | The outside claims auditor: 81 statements, each PASS, FAIL or UNCHECKED |
| `findings/weekly-run-verdicts.json` | The verifier's verdicts, with its own reproductions |
| `auditors/<key>/` | Each auditor's reproduction scripts and synthetic fixtures (`fx/`) |
| `my-checks/` | The session's own checks: its suspicions written before any agent reported, its known answers, its re-run of all 48 reproductions (`rerun/`), and its second reproductions with inputs of its own |
| `pack/` | What the auditors were given: briefs, the turn-gate rules as stated, tools, the pull request text, the stored weekly prompt |
| `council-eval-raw/` | The ten council trigger-eval runs of 2026-11-12: prompts, driver, outputs, exit codes |

## What is not here, and why

- **The session transcript, and anything copied from it.** It is the owner's private record.
  `pack/tools/replay_real.py` replays it and prints verdicts only; `pack/replay-baseline.txt` is that output.
  Three pack files the briefs mention were derived from the transcript's rows and are left out:
  `real-row-shapes.md`, `real-text-recording.txt`, `timing.txt`.
- **The auditors' private checkouts, mutated hook copies and sandboxes.** Bulk; the scripts rebuild them.
- **Model names** are replaced by "[model name removed]" (doctrine rule 6). **Account and session ids** are
  replaced by "[id removed]".
- **From the council runs** only the user, assistant and result events are kept, without thinking blocks. The
  start-up event (it lists the account's plugins and their paths) and the usage events are dropped.
- **From `pack/session-tools.txt`** the mail, file and other connector tool names.

## Reading the scripts

The scripts hold absolute paths into the session's scratch folder (`/tmp/claude-0/...`). They are the record of
what ran, not a suite that runs from this repository. To run them again, rebuild the pack as
`pack/README.md` describes: a clone of the library at `1ce99d5`, the kit at `f6d49f5`, the deck at `c933f07`.

## Not finished on 2026-11-13

Nine areas had no auditor yet, and 32 of the 40 gate findings had no second agent. Both were running when this
record was committed; their results come as an addendum in this folder.
