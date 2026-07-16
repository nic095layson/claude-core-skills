# Hypothesis — an explicit in-prompt cue fires the governor where nothing automatic does (claude.ai lever)

**Pre-registered 2026-07-16, BEFORE any run.** Owner's idea: since no automatic
lever fires the governor on the uncued analysis class on claude.ai (DEAD-3, INC-8,
INC-11), what if the USER appends an explicit cue to the prompt? That converts an
*uncued* prompt (governors don't fire) into a *cued* one (positive control: cued
prompts fire 2/2; acceptance tests passed on cued phrasings).

## Variable = the cue appended to the prompt (one variable)

claude.ai proxy: 3 governors installed + current (post-revert) instructions via
`--append-system-prompt`, all arms identical except the appended cue. Model
`claude-opus-4-8`, N=3, fresh session per run (session env cleared, INC-10).
FIRED = adversarial-verify `Skill` load in the run's stream-json.

| arm | prompt = Rivian incident prompt + … | prediction |
|---|---|---|
| R_uncued | (nothing appended) | 0/3 (reproduce the gap) |
| R_cue_generic | " Run the skills process for this task." | **≥2/3** (owner's phrasing) — uncertain: "skills process" is generic |
| R_cue_named | " Before you answer, use your adversarial-verify skill on this." | **3/3** (names the governor = strongest cue) |

## Decision rule
- If R_cue_* loads ≥2/3 while R_uncued ~0/3 → the in-prompt cue is a real,
  deployable claude.ai lever (user-held, not automatic). Report which phrasing
  works (generic vs named).
- If even the named cue doesn't load → deeper problem than cueing; record it.
- Report rates, dated; N=3.
