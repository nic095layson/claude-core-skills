# Phase 0 baseline — RESULT (2026-07-15)

**Pre-registration:** `phase0-baseline-PREREG.md` (committed before any run).
**Surface:** Claude Code headless (`claude -p`, v2.1.210). **Model:**
`claude-opus-4-8` (the incident model). **N=3 per prompt, 9 runs.**

## The number that did not exist before

| prompt (uncued) | governor `Skill` fires | result |
|---|---|---|
| `u1_rivian` (verbatim incident prompt) | **0/3** | analysis delivered in prose, no load |
| `u2_analysis` (different analysis-advice phrasing) | **0/3** | same |
| `s1_canary` ("15% of 80") | **0/3** (correct — silent) | "12" |

**Governors auto-fire 0/9 on the uncued analysis class.** Adversarially verified:
raw grep finds **zero** `"name":"Skill"` tool_use and zero governor-named tool_use
across all nine transcripts — the 0/9 is real, not a grading artifact.

## What this establishes (per the pre-registered decision rule)

**The invocation gap is reproducible on Claude Code — it is NOT
claude.ai-instruction-specific.** The skill *descriptions* alone do not fire on an
analysis/advice prompt, on the same surface and model where the campaign's cued
should-fire gates PASS (plan-gate 9/9, adversarial-verify 6/6 on their *cued*
prompt sets). So:

- The gate was passed on **cued** prompts; the analysis class is **uncued** and
  sits outside what the current descriptions catch. This is the "coverage gap, not
  regression" framing, now measured — not asserted.
- **Plan Phase 1 (widen the descriptions) is justified**, and it helps both
  surfaces (descriptions drive triggering everywhere).
- **Plan Phase 2 (the Claude Code hook) has a real gap to close** — there is
  something for a mechanical trigger to fix here.

The behavioral echo of INC-8 is exact: in every u1/u2 run the model applied the
*principles* in prose ("good analysis means not overselling it," refuted the
date-is-knowable premise, refused to invent figures) while invoking **no**
governor — spirit-compliance without the procedure, the incident's signature.

## Caveats (report faithfully)

1. **Web-blocked confound.** The environment's network policy denied WebSearch/
   WebFetch, so the analysis runs could not pull live data (the claude.ai incident
   *did*). This degraded the *content* but not the measured variable: governor
   invocation was 0 regardless, and the prose-governance-without-load behavior
   matched the incident. If anything it strengthens the finding (even a degraded
   attempt never reaches for the governor).
2. **Surface is Claude Code, not claude.ai.** This measures description
   auto-triggering; it does not inject the claude.ai custom-instruction pointers
   (INC-3: surfaces diverge). A low rate here indicts the descriptions; the full
   claude.ai condition (descriptions + instruction pointers) is a later contrast.
3. **Condition = 3 governors amid a realistic skill set.** The isolated project
   provided the 3 governors at project scope, but the `claude` install also
   injected its built-in skills (deep-research, dataviz, …; confirmed in the
   `init` line). More realistic than "3 governors alone," and the governors were
   confirmed registered/available — but the context was not governor-only.
4. **N=3, single model, baseline read.** Catches a gross pattern (0/9 is
   unambiguous); recorded as a rate, dated. Not change acceptance — any wording
   edit still goes through research-methodology R1/R2. Sonnet is a cheap add if a
   future read is ambiguous; this one is not.

## Artifacts

Transcripts: `phase0_baseline/transcripts/*.jsonl` (kept for spot-check).
Runner: `scratchpad/phase0_run.py`. Prompts + FIRED definition: PREREG.
Operational note: `--dangerously-skip-permissions` is refused under root in this
environment; runs use default headless permissions (which auto-decline
prompt-requiring tools like WebSearch — the source of caveat 1).
