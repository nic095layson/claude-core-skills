# The surfaces fix: wiring, plugin 0.1.6, the install runbook, the copies (2026-11-16)

**The built part (merge gate, Stop gate, receipt gate) can now be installed without bricking a session, its
wiring is tested, and the plugin and the two other repositories are ready. Nothing is uploaded or synced.**

| finding | what was wrong | resolved by | proof (red, then green) |
|---|---|---|---|
| SF-2 (high) | a project installed by Runbook 4 to the letter lacked `turn-gates-pretool.py`: python3 exits 2, every Bash, Edit and Write call denied; step 4 still passed | both wiring files: each command runs its script only when the file is there, except the merge tools' own group (bare command: a missing script denies the merge). Runbook 4: generated file list, step 4 runs the wiring cases | `raw/runbook4-red.txt`, `raw/runbook4-green.txt`, `raw/missing-script-runs.txt`, `raw/red-W-on-start-wiring.txt` (W03, W04 red) |
| SF-4 (medium) | the guard passed with the merge gate cut off from the PR tools or the receipt gate unwired | table "W" (W01 widened, W02 to W06), which the guard runs; 22 new breaks (WI05 to WI26) and WI01 to WI04 re-targeted | `raw/red-W-auditor-mutations.txt` (the auditor's M3, M4, M5 and N1, N2, N3, N6 each caught), `raw/sf4-sf6-guard-mutations.txt` |
| SF-6 (low) | the guard's parity list was typed and missed a file; the wrapper selftest had no case for "the project wires other hooks, not this one" | the guard computes the list from the folders and requires every file the wiring runs, imports or tests; wrapper selftest case 10 | `raw/guard-section9-red-green.txt`, `raw/wrapper-selftest-red-green.txt`, `raw/sf6-wrapper-mutation.txt` |
| F2-6, WR-1, SF-1 (high) | the weekly task's session runs the account's plugin 0.1.4, which lets a scheduled run merge | plugin 0.1.6 holds the rebuilt gates (`claude plugin validate --strict` passes: `raw/plugin-validate.txt`). **Only the owner's upload closes these** | `after-the-merge.md` |

Other files: `other-repositories.md` (what the sync changes in the kit and the deck, their selftests, the
unattended command forms with their verdicts); `raw/*-sync-*.txt` (the sync script's output in each clone);
`tools/` (the scripts that made the raw files; they take their folders as arguments). Each raw file starts with
its command. `<tree>`, `<kit>`, `<deck>`, `<work>` and `<scratch>` stand for the folders the runs used.

Not measured: a live session on any surface; the stored prompts as they are on the account today.
