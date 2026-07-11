# Phase 1 Trigger Evals — Results (2026-07-11)

**Campaign:** governance-adoption-campaign, Phase 1 (the A2 test).
**Surface measured:** Claude Code **headless** (`claude -p`), personal-scope
install (`~/.claude/skills/`), fresh session per run, run from a scratchpad
**outside this repo** so only the five personal governors load.
**Model:** `claude-opus-4-8` (as reported by each session's init event).

## How "fired" was measured (committed before running)

FIRED := the governor's **`Skill` tool was invoked** in that run's stream-json
transcript (a `tool_use` with `name: "Skill"`, `skill: "<governor>"`) — a direct
observation of the transcript, not an introspective "would you have loaded it?".
SILENT := no such invocation. In a fresh session the only path to a governor's
guidance is the `Skill` tool, so the invocation is necessary and sufficient for
"the governor fired." The behavioral signature (gate block, scope flag, etc.) was
recorded as corroboration; it is not the primary gate because base-model caution
can mimic it without the skill loading (see confounds).

Raw transcripts: `*.jsonl` in this directory (one per run,
`<gov>__id<n>__r<k>.jsonl`). Machine summaries: `_summary_runs2.json`,
`_summary_lst_r3.json`. Detection was cross-checked with an independent raw grep
(9 FIRE transcripts, matching the parser exactly).

## Per-prompt firing (fires / runs)

| governor | id1 (SF) | id2 (SF) | id3 (SF) | id4 (SN) | id5 (SN) |
|---|---|---|---|---|---|
| plan-gate | 1/2 | 0/2 | 0/2 | 0/2 | 0/2 |
| scope-fence | 2/2 | 0/2 | 0/2 | 0/2 | 0/2 |
| adversarial-verify | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 |
| lessons-ledger | 2/2 | 0/2 | 0/2 | 0/2 | 0/2 |
| live-state-truth | 0/3 | 3/3 | 3/3 | 0/3 | 0/3 |

SF = should-fire, SN = should-not-fire near-miss. live-state-truth escalated to 3
runs/prompt per the campaign's "within one run of its gate" rule (it was at 4/6).

## Rates table (recorded as rates, per the measurement-bar doctrine)

| governor | should-fire | should-not-silent | **gate** |
|---|---|---|---|
| plan-gate | **1/6 (17%)** | 4/4 (100%) | **FAIL** |
| scope-fence | **2/6 (33%)** | 4/4 (100%) | **FAIL** |
| adversarial-verify | **0/6 (0%)** | 4/4 (100%) | **FAIL** |
| lessons-ledger | **2/6 (33%)** | 4/4 (100%) | **FAIL** |
| live-state-truth | **6/9 (67%)** | 6/6 (100%) | **FAIL** |

Gate = ≥5/6 (≥83%) should-fire fire **and** ≥3/4 (≥75%) should-not stay silent.

**Phase 1 verdict: FAIL for all five governors on this surface.** Every governor
passes the should-not-silent bar (they never over-fired, and no adjacent governor
ever co-fired — zero boundary defects). Every governor fails the should-fire bar:
none triggers reliably on realistic phrasings that don't name it. This is the
founding-incident class (silent non-triggering) the campaign exists to kill,
observed directly.

## The key pattern: triggering is phrasing-deterministic, not noisy

Firing is **bimodal per prompt** — a phrasing fires either every run (2/2, 3/3)
or never (0/2, 0/3). The only split result in 34 should-fire runs was plan-gate
id1 (1/2). So run-to-run stochasticity is small; **the phrasing of the request
determines whether the description matches.** Some phrasings hit the WHEN clause
reliably (scope-fence's "you'll probably notice… while you're in that file";
lessons-ledger's "burned two hours chasing a bug"; live-state-truth's "is Redis
set up correctly", "are we actually on 14 in prod?"). Others never do (JWT
refactor, CI/CD setup, "confirm the service is up"). This is exactly the
signal a description-rewording pass needs — logged per governor in
`experiments/hypothesis-*.md`.

## Confounds and limitations (stated plainly, per adversarial-verify)

1. **Surface is headless only.** Interactive Claude Code and claude.ai are
   untested. The headless-artifact worry (would `-p` suppress auto-triggering
   everywhere?) is **refuted** — auto-triggering demonstrably occurs in headless
   (live-state-truth 6/9, others nonzero), and it varies by description, so this
   is a real per-description measurement. But headless may still under-trigger
   relative to interactive; the A2 update is scoped to "Claude Code headless,
   dated," not "all surfaces." (assumption A-h1, unconfirmed.)

2. **adversarial-verify's 0/6 is prompt-confounded.** All three should-fire
   prompts imply an artifact ("here's my SQL migration", "here it is") that does
   **not exist** in the fresh scratchpad. The model spent its turn discovering the
   file was missing (and, notably, refused to fabricate a review — behaviorally
   aligned with the skill, without loading it) rather than engaging the verify
   flow. Its 0/6 must be read as "0/6 **under this prompt design**"; the fix to
   test next is embedding the artifact inline, before concluding the description
   is at fault. Recorded in `experiments/hypothesis-adversarial-verify.md`.

3. **FIRED = Skill-tool load, not prose signature.** A governor that changes
   behavior *without* loading (organic plan-gate-shaped caution was observed on
   plan-gate id1 r2 and elsewhere) counts as SILENT. This is correct for a
   *trigger* eval — A2 is specifically "does the description load the skill" — but
   it means these rates measure triggering, not the base model's latent caution.
   Whether firing *changes* behavior beyond the base model is Phase 2's question.

## Disposition

No descriptions were edited this session (per instruction and
research-methodology: baseline measurement is not change acceptance). Each
under-firing governor has a pre-registered rewording hypothesis in
`experiments/` for a separate research-methodology session to run as a proper
before/after A/B.
