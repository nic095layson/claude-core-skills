# In-prompt cue A/B — RESULT: the user-held lever WORKS on claude.ai (2026-07-16)

**Owner's idea:** since nothing *automatic* fires the governor on the uncued
analysis class on claude.ai, what if the user appends an explicit cue to the
prompt? **Pre-registration:** `experiments/hypothesis-2026-07-16-in-prompt-cue.md`.
**Surface:** claude.ai proxy (Claude Code headless, 3 governors + current
instructions via `--append-system-prompt`), Opus, N=3, one variable = the appended
cue. FIRED = real `Skill` load in the run's stream-json.

## Result

| arm | prompt = Rivian incident prompt + … | adversarial-verify | any governor |
|---|---|---|---|
| R_uncued | (nothing) | **0/3** | 1/3 (plan-gate once) |
| R_cue_generic | " Run the skills process for this task." | 1/3 | **3/3** (plan-gate 3/3) |
| R_cue_named | " Before you answer, use your adversarial-verify skill on this." | **3/3** | 3/3 |

Raw-grep confirmed 3 real `"skill":"adversarial-verify"` invocations in the
named-cue arm; 1 in the generic arm; 0 in uncued.

## Reading

1. **Uncued reproduces the gap** — 0/3 adversarial-verify (the incident, again).
2. **A generic cue reliably invokes governance** — "run the skills process" loaded a
   governor **3/3**, but the model chose **plan-gate** (the start-of-task governor)
   every time and reached adversarial-verify only 1/3. So a vague cue triggers *the
   machinery* but not necessarily *the governor you need*.
3. **Naming the skill is the reliable lever** — "use your adversarial-verify skill"
   loaded exactly it **3/3**. Explicit + named = deterministic on this evidence.

## Why this is consistent with everything else (and externally valid)

This does not contradict DEAD-3 / INC-8 / INC-11 — those measured **automatic**
firing on **uncued** prompts, which fails. This measures **user-cued** firing, which
succeeds — exactly as the earlier evidence predicted: cued prompts fired in the
positive control (2/2) and in the **real claude.ai** 7/7 acceptance (2026-07-12,
whose rows were all cued). So user-cued firing is already established on the true
surface; this A/B just shows it closes the *incident* prompt specifically, and that
naming beats a generic cue.

## The deployable answer for claude.ai (owner usage pattern)

**On claude.ai, the lever is in the user's hands.** For any analysis/answer you must
have vetted, append an explicit cue to your prompt — ideally **by name**:
> "…and before you answer, use your adversarial-verify skill on this."
> (or "run plan-gate first" for a build; "use scope-fence" to bound a change.)

- Reliable (3/3) when the skill is named; a generic "run the skills process" still
  invokes governance 3/3 but may pick the wrong governor.
- It is **not automatic** — you must remember to add it. That is the price of a
  surface with no hook layer. But it *works*, which no automatic prose lever does.
- On **Claude Code**, you don't need to remember — the Phase-2b Stop hook enforces
  the load for you (3/3, unprompted).

## Caveats (faithful)

- N=3, proxy surface. Mitigated by the real-claude.ai 7/7 cued acceptance corroborating
  cued firing on the true surface.
- The generic-cue → plan-gate result is a phrasing artifact (the cue reads as
  "plan this task"); different generic wordings may pick differently. Naming removes
  the ambiguity.
- Web tools were blocked (Rivian is web-dependent); did not affect the load measure
  (named cue fired 3/3 regardless).

Artifacts: `results/2026-07-16/in_prompt_cue_ab/` (9 transcripts, runner).
