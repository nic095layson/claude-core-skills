# Trigger-eval results — `red-team` candidate, first measurement (2026-10-19)

Pre-registered in `experiments/hypothesis-2026-10-19-red-team.md` (committed 2026-10-19 with the skill,
before any run). This file was created with the method section below BEFORE the first run; the results
sections were appended after, from `grade.py` over the committed transcripts.

## Method and environment (held constant, recorded before the runs)

- Surface: Claude Code headless (`claude -p`, CLI 2.1.303), `--output-format stream-json --verbose`,
  `--max-turns 6`, `--allowedTools "Skill,Read,Glob,Grep"`, 900 s timeout, one `claude -p` process per run,
  cwd an empty `work/` folder outside every repository, the account plugin `core-governance@synced` disabled
  per run (no governance hook fires), the three project environment variables unset. Driver:
  `drivers/run_one.sh`. **Correction after refutation (2026-10-19 18:10 UTC):** `--allowedTools`
  pre-approves tools, it does not remove the rest — the init events list Bash, Write and 38 more. Bash ran
  (directory listings, greps) in 23 of the 24 runs; three runs attempted a Write, each denied by the
  permission prompt; no file was written. The runs also inherited this container's session id (the three
  unset variables did not include `CLAUDE_CODE_SESSION_ID`), so a session could read sibling runs' folders
  and the prompt files through Read and Glob. Every fire is the first tool call, before any read, so the
  fire cells are unaffected; the silent cells carry this confound. **Replicate B** below closes it: Skill
  the only tool, every other tool disallowed, the session id unset (`drivers/run_one_isolated.sh`).
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

## Results (24 runs, 2026-10-19; wall-clock in `*.started.txt` / `*.finished.txt`)

Graded by `grade.py` over the committed transcripts; raw output `grading-<model>.txt`, machine-readable
`grading-<model>.json`. One grader bug was found and fixed before any grade was read: it crashed on a
transcript event whose `message` field is a string (the fix guards the type; no verdict logic changed).

| model | ids 1–3 fire | id 6 fire | ids 4–5 silent | gate (hypothesis: ≥5/6, 4/4) | gate (evals file: ≥5/6, ≥3/4) | cost |
|---|---|---|---|---|---|---|
| `claude-fable-5-1` (primary, gate-bearing) | **6/6** | 2/2 | **4/4** | **PASS** | PASS | $11.49 |
| `claude-opus-5-5` (replicate) | 6/6 | 2/2 | 4/4 | PASS | PASS | $2.24 |

- **Zero over-fires on both models.** On id 4 (a deliverable to check) Fable loaded adversarial-verify
  in both runs, exactly the routing the NOT clause names; Opus answered without a skill. On id 5 (a
  doc-versus-live-state question) both models ran directory listings and greps through Bash (executed:
  the tool was not pre-approved but ran under the session's permission mode) and never loaded a skill.
- **Every fire was the first tool call** (`corroboration.txt`: skill-call index 0 in all 16 fired runs).
- Corroboration, not grading: band or sweep vocabulary appears in the assistant text of **7** of the 16
  fired runs (`corroboration.txt`; an earlier version of this line said 8); the rest spent their turns
  reading for artifacts the prompts name and ended at the turn cap with little text. Four Fable runs ended
  `error_max_turns` after the fire; the fire stands, the signature does not. The `turns` column in
  `grading-*.txt` is the CLI's `num_turns` counter, not the `--max-turns` cap: every transcript holds at
  most 6 assistant messages, so the cap held.
- No run errored; no non-runs; no session-limit refusals (every result event is `success` or
  `error_max_turns`).
- Record completeness (after refutation): the prompt files the driver read are committed under
  `drivers/prompts/` and compared byte for byte to `evals/red-team.json` (`prompts-verification.txt`: equal);
  the registration probe is `probe-registration.jsonl`. The personal-scope copy at run time was the
  `742a640` SKILL.md (its description is identical to the current one); it was refreshed to the current body
  at 17:58 UTC, after the runs, for the acceptance check. The method section above is unchanged between the
  pre-run commit `b452621` and the results commit, which is the ordering evidence; `b452621`'s timestamp
  equals the first run's start to the second.

**Verdict against the pre-registration:** the hypothesis is **CONFIRMED** on Claude Code headless for both
models tested, N=2 per prompt. The candidate's description is unchanged; no wording experiment was needed.
Rates are rates: 6/6 on three prompts is not "always"; claude.ai triggering is not measured here.

## Replicate B (isolated driver) — INCOMPLETE, 2026-10-19 18:19 UTC

Launched to close replicate A's isolation confound (`drivers/run_one_isolated.sh`: Skill the only tool,
every other tool disallowed, the parent session id unset). The account's session limit hit during the
batch ("You've hit your session limit · resets 9:30pm (UTC)" — the success-shaped refusal of ledger
INC-2026-08-26-01; the first grader pass read 20 of them as silences before the detector was added to
`grade.py`). What stands: **4 Fable runs (ids 1 and 2, both runs each) fired `red-team` with Skill as the
only usable tool** before the cut — the transcripts hold the Skill call and a limit banner where the
answer would be; no other tool_use appears anywhere in the batch. The remaining 20 runs are non-runs
(6-line transcripts, $0). Transcripts committed as `transcripts/repB-*`; grading in `grading-repB-*`
counts 0 graded rows and 24 refusal-or-partial records by design. **The rerun is owed after the limit
resets**; until it lands, replicate A is the only complete measurement, its fire cells unconfounded
(first tool call) and its silent cells carrying the stated confound.

**What this does not show:** behavioral value (does loading the skill change what gets reported?) is
unmeasured; the prompts are description-testing phrasings that name the model and its constants, not the
uncued case where a session quotes a modelled figure without being asked to attack it. The hook in
`hooks/redteam-band-reminder.sh` is the lever for that case and has its own pre-registration
(`experiments/hypothesis-2026-10-19-redteam-band-hook.md`).
