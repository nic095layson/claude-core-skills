# Trigger-eval results — `red-team` candidate, first measurement (2026-10-19)

Pre-registered in `experiments/hypothesis-2026-10-19-red-team.md` (committed 2026-10-19 with the skill,
before any run). This file was created with the method section below BEFORE the first run; the results
sections were appended after, from `grade.py` over the committed transcripts.

## Method and environment (held constant, recorded before the runs)

- Surface: Claude Code headless (`claude -p`, CLI 2.1.303), `--output-format stream-json --verbose`,
  `--max-turns 6`, `--allowedTools "Skill,Read,Glob,Grep"` (read-only: the prompts name artifacts that do
  not exist, and the measurement is the Skill invocation), 900 s timeout, fresh session per run, cwd an empty
  `work/` folder outside every repository (a session cannot read its own output log — 2026-10-13 confound),
  the account plugin `core-governance@synced` disabled per run (no governance hook fires), the three project
  environment variables unset. Driver: `drivers/run_one.sh`.
- Skill under test: `~/.claude/skills/red-team/SKILL.md`, a byte copy of the branch's
  `.claude/skills/red-team/SKILL.md` (description 997 chars). Registration confirmed in a one-turn probe
  session before any eval run: 49 skills listed by the init event, `red-team` among them. The account-synced
  roster (governors, brand-standard, document skills and the rest) rides along constant in every run.
- Prompts: `evals/red-team.json` ids 1–6, verbatim, N=2 per prompt per model.
- Models (plan-gate A1, stated before the run): primary `claude-fable-5-1` (the owner's current session
  model); the gate verdict is read on it. Replicate `claude-opus-5-5`, N=2, recorded as rates, not gate-bearing.
- FIRED := a `Skill` tool_use whose `skill` ends with `red-team` in the transcript (`grade.py`). Other skills
  invoked are recorded. A run whose result subtype is neither `success` nor `error_max_turns` is a non-run
  (INC-2026-08-26-01) and is listed, not graded; it is rerun once.
- Gate (hypothesis): ids 1–3 fire in ≥5 of 6 runs; ids 4–5 silent in 4 of 4. The evals file's `_grading.gate`
  reads ≥3/4 silent; both readings are printed, the hypothesis governs the verdict (flagged in the PR).
- Transcripts: `transcripts/<model>-id<N>-r<R>.jsonl`, verbatim. Grading output: `grading-<model>.txt`,
  `grading-<model>.json`.

## Results

(appended after the runs)
