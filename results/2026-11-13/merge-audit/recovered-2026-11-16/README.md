# Recovered records of the audit's 80 later findings (2026-11-16)

**Partial recovery.** For none of the 80 was a reproduction command recovered. For 27 (all of them left for the second
pull request) nothing was found beyond the one-line entry already on main.

## Why this folder exists

This audit's pull request holds full records for 48 findings, from areas CB, F1, F2, RI, TB and WR. The other 80
findings come from the later areas: ADV, CA, CN, FU2, OS, PC, RG, RL, SF and TR. On main, each of those has only a
one-line row in `results/2026-11-16/fix-audit/original-findings-status.md`: id, the first clause of its title, its
area and its state. Their full records lived in the scratch folder of the session that ran the audit. That session
was archived on 2026-11-16, which released its container.

The owner ordered a recovery from that session's transcript, which stays readable after archiving. The work was
done on 2026-11-16 by the Global Operations session that followed it.

## Method

- **Pages read.** 136 pages of 100 events each were read from the archived transcript, newest to oldest. They run
  from 2026-11-16 20:51 UTC back to 2026-11-13 04:28 UTC. That is the whole stretch from just before the audit
  pull request was opened (04:42 UTC) to the archive.
  - 21 pages were read by this session; 115 by two read-only helpers.
  - The pages stay in the session's scratch. They are not committed, because they carry account and session data.
- **Script.** `extract.py`, kept beside the pages, walked every event, parsed nested JSON, and collected every object
  whose `id` is one of the 80. A second script collected every Markdown table row that starts with one of the ids.
- **Fields kept.** Only these fields were kept: id, title, kind, severity guess, verdict, severity, realism, reason,
  resolved, how and test. Model names were replaced with `[model]`; there were none.
- **Scan.** The files were scanned for e-mail addresses, account and session uuids, scratch paths and keys. None
  were found.
- **Repository traces.** For each id, `repo_traces` lists the committed files on main (`da81dc2`) that cite it: test
  rows, red-first runs and fix records under `results/2026-11-15/`, `results/2026-11-16/audit-fixes/` and `hooks/`.

## What came back

| Best record recovered | Ids | What it holds |
|---|---|---|
| Second-agent verdict | 15 (FU2 ×7, RG ×8) | Verdict, severity, how realistic; for RG, the verifier's reason |
| The audit's index row | 8 (ADV) | A longer title, kind, and the finder's severity guess |
| Fix notes only | 25 | The fix's own record ("resolved", "how", "test") or a row of a fix-plan table; these describe the fix, not the finding |
| Nothing beyond the title on main | 32 | — |

- **31 ids also have repository traces.** These are mostly the ones that were fixed: their test rows restate the
  finding as a case.
- **27 ids have neither a transcript record nor a repository trace:** CA-1 to CA-8, CN-1 to CN-8, OS-1 to OS-8,
  SF-5, SF-7 and SF-8. All 27 are left for the second pull request.

**The finders' and verifiers' full reports were never in the transcript.** They were written to files that the
session read only as counts and summaries.

## What this means for the second pull request

For 48 of the 61 findings it inherits, the second pull request has:
- no reproduction command; and
- for 27 of them, nothing beyond the one-line title.

Those areas need their defects re-established before any fix: a fresh read of each area against the one-line title,
with a red test first.

## Files

| File | What it is |
|---|---|
| `recovered.json` | One entry per id: the status row on main, the best level recovered, every record found (the page it came from and its time), table rows, repository traces |
| `table.md` | The same, one line per id |
