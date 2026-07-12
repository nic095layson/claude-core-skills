# v1 — CONFOUNDED, SUPERSEDED (do not cite)

These are the first Phase 2 execution(s), run with cwd **inside this repo**, whose
`.claude/skills/` ships the governors at **project scope**. The "without-library"
arm therefore still loaded all five governors — e.g. `phase2_scored.json` records
plan-gate's `without` runs as `final_present: true, skill_fired: true`, which is the
project-scope leak, not a real base-model behavior. The blind-grade artifacts here
(`traces/`, `verdicts.json`, `phase2_scored.json`) graded that contaminated data and
their without-arm numbers are invalid.

- `transcripts/`, `transcripts_run2_confounded/` — two confounded in-repo runs.
- `rundirs_in_repo/` — the in-repo working dirs that caused the leak.
- `*.log` — run logs from those attempts.

**The valid, corrected results are in `../transcripts_v2/` and `../RESULTS-PHASE2.md`**,
run with cwd outside the repo & `~/.claude` (without-arm fired 0/20). Retained only as
evidence of the methodology correction (see `.claude/LESSONS.md`, project-scope-leak
incident).
