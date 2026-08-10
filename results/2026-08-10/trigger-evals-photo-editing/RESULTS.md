# photo-editing trigger evals — RESULTS (2026-08-10)

**Verdict: GATE PASS, clean sweep — 8/8 should-fire runs fired, 6/6
should-not runs stayed silent** (committed gate: ≥7/8 fire, ≥5/6 silent).
Every fire run also showed the full behavioral signature; no over-fire
anywhere.

## Protocol (as pre-committed in `evals/photo-editing.json`, 2026-08-10)

- 7 prompts (ids 1–4 should-fire, 5–7 should-not) × 2 runs = 14 fresh
  headless sessions: `claude -p --model claude-sonnet-5 --output-format
  stream-json --max-turns 12`, project scope (repo root at commit
  `4c2a49e`, photo-editing live in `.claude/skills/`).
- FIRED := the photo-editing Skill tool invoked in the transcript
  (mechanically graded; grader + raw output committed beside this file).
- Fixtures seeded once per the eval file's spec (`fixtures/sample-padded.png`,
  `sample-photo.png`, `sample-logo.png`), present and byte-stable for ALL
  runs (INC-2: state held fixed).
- **Method deviation, recorded:** runs used `--allowedTools "Bash Read Write
  Edit Glob Grep Skill"`. A first attempt under the default permission mode
  stalled on Bash approval prompts mid-procedure (transcripts discarded, all
  14 re-run under identical conditions). The graded signal (Skill
  invocation) is upstream of tool permissions; the flag exists so the
  behavioral corroboration could execute.

## Per-run grid (from `grading-output.txt`)

| id | expect | r1 | r2 | inspect-script ran | new file created |
|---|---|---|---|---|---|
| 1 crop padding | FIRE | FIRED | FIRED | both | both |
| 2 resize 1200×630 JPG | FIRE | FIRED | FIRED | both | both |
| 3 rotate 90° | FIRE | FIRED | FIRED | both | both |
| 4 RGBA→JPG convert | FIRE | FIRED | FIRED | both | both |
| 5 JPEG-vs-PNG question | SILENT | silent | silent | — | — |
| 6 poster generation | SILENT | silent | silent | — | — |
| 7 bar chart | SILENT | silent | silent | — | — |

## Corroboration beyond the gate

- **The three laws held inside the eval runs.** After all 8 edit runs, the
  seeded originals were byte-identical to a deterministic regeneration
  (md5 compare) — no session overwrote an original; outputs appeared as new
  descriptively-named files (`sample-padded-cropped-300x200.png`,
  `sample-photo-1200x630.jpg`, …). Fire runs ran `inspect_image.py` BEFORE
  editing and re-verified after.
- **Silent runs did the right other thing:** id6 engaged the poster as a
  design/generation task (no photo-editing load); id7 built a chart
  artifact (no photo-editing load); id5 answered directly.

## Bounds

- One surface (Claude Code headless, this cloud container), one model
  (`claude-sonnet-5`), N=2 per prompt — rates are rates, not "always".
  claude.ai triggering and cross-model behavior untested. Behavioral value
  vs no-skill baseline not isolated (no without-skill arm in this protocol;
  the 2026-08-03 candidates carry the same bound).
- Grader is mechanical (tool_use scan); transcripts committed for re-grade.

## Provenance

Run 2026-08-10 by the adoption session (owner decision A), same day as
authoring. Raw transcripts in `transcripts/` (14 files), grader output in
`grading-output.txt`. Re-grade: rerun the committed grader over
`transcripts/`. Register: `evals/model-capability-register.md` row 13.
