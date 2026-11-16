# Recovered records of the audit's 80 later findings (2026-11-16)

**Partial recovery, corrected the same day.**
- **76 of the 80** have more than the one-line title on main:
  - 57 have the verifier's summary line (kind, severity, verdict, longer title);
  - 9 have the finder's record plus the command its verifier ran;
  - 10 have only an index row or fix notes.
- **For all 48 left for the second pull request**, at least the summary line is recovered (3 also have a command).
- **Nothing beyond the title:** PC-4, PC-5, PC-7, SF-3.
- **No finding's reproduction is runnable from here.** The commands name scripts in the audit session's scratch
  folder, which was released at the archive.

An earlier commit on this branch (`7c1f12f`) said "no reproduction command recovered" and "27 with nothing". That
was wrong: its extractor read whole JSON objects only, and missed the cut-off previews and the plain-text summary
tables that hold most of what is here.

## Why this folder exists

This audit's pull request holds full records for 48 findings, from areas CB, F1, F2, RI, TB and WR. The other 80
findings come from the later areas: ADV, CA, CN, FU2, OS, PC, RG, RL, SF and TR. On main, each of those had only a
one-line row in `results/2026-11-16/fix-audit/original-findings-status.md`: id, the first clause of its title, area
and state. Their full records lived in the scratch folder of the session that ran the audit. That session was
archived on 2026-11-16, which released its container.

The owner ordered a recovery from that session's transcript, which stays readable after archiving. The work was
done on 2026-11-16 by the Global Operations session that followed it.

## Method

- **Pages read.** 136 pages of 100 events each, newest to oldest, from 2026-11-16 20:51 UTC back to 2026-11-13
  04:28 UTC. That is the whole stretch from just before the audit pull request was opened (04:42 UTC) to the archive.
  - 21 pages were read by this session; 115 by two read-only helpers.
  - The pages stay in the session's scratch. They are not committed, because they carry account and session data.
- **Three extractors**, kept in the session's scratch:
  1. whole JSON objects whose `id` is one of the 80;
  2. cut-off JSON previews ("resultPreview" fields of workflow progress), read field by field up to the cut;
  3. plain-text summary tables: `ID  kind  severity  VERDICT  title`.
- **Fields kept.**
  - Finder: id, title, component, kind, rule quoted, severity guess.
  - Verifier: verdict, reproduced, severity, realism, reason, command run.
  - Fix records: resolved, how, test.
- **Scrubbing.** Workflow fields (model, tokens, labels) were dropped. Scratch paths became `SCRATCH/` and the old
  session's id was removed. A final scan found no e-mail address, uuid, `/tmp/` path or model name.
- **Limits of the extractors.**
  - A preview holds only the first object of each list, so it gives a full finder record for one finding per area at
    most.
  - The summary lines are the verifier's own table and are cut at 150 to 155 characters.
  - Prose mentions that fit none of the three forms were not extracted.
- **Repository traces.** For each id, `repo_traces` lists the committed files on main (`da81dc2`) that cite it:
  test rows, red-first runs and fix records under `results/2026-11-15/`, `results/2026-11-16/audit-fixes/` and
  `hooks/`. 31 of the 80 have at least one.

## What came back

| Best record recovered | Ids | Left for the 2nd PR |
|---|---|---|
| Finder record + verifier command | 9: ADV-1, CA-1, CN-1, FU2-6, OS-1, PC-1, RG-1, RL-1, SF-1 | 3 |
| Verifier's summary line | 57 | 45 |
| Index row or fix notes only | 10 | 0 |
| Nothing beyond the title on main | 4: PC-4, PC-5, PC-7, SF-3 | 0 |

TR-1 also has its verifier's command, though not its finder record. That makes 10 ids with a command.

## What this means for the second pull request

The second pull request inherits 48 of these findings. For each it has the defect's kind, severity, verdict and a
title cut at about 150 characters. For 3 of them it also has the full finder record and the verifier's command.

**No reproduction script survives.** A fix there should start by rebuilding the reproduction from the recovered text
as a red test, before changing code.

## Files

| File | What it is |
|---|---|
| `recovered.json` | One entry per id: the status row on main, the best level recovered, every record and summary line found (the page it came from and its time), fix-plan rows, repository traces |
| `table.md` | The same, one line per id |
