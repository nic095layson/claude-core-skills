# Phase 2b — RESULT: Stop-hook enforcement WORKS — governed loads 3/3, zero over-fire, zero confabulation (2026-07-15)

**Pre-registration:** `experiments/hypothesis-2026-07-15-governance-enforce-stophook.md`
(committed before any run). **Surface:** Claude Code headless. **Model:**
`claude-opus-4-8`. **Variable:** two hooks (UserPromptSubmit load-only trigger +
Stop enforcer) absent vs wired. N=3.

## Result — adversarial-verify `Skill` loads, OFF vs ENFORCE

| id | class | OFF | ENFORCE | confab | verdict |
|---|---|---|---|---|---|
| SF1 | **verbatim Rivian incident prompt** (web-blocked) | 0/3 | **3/3** | 0 | ✅ **0→3/3** |
| SF2 | Nvidia forecast (web-blocked) | 0/3 | **3/3** | 0 | ✅ 0→3/3 |
| SF3 | REST→GraphQL analysis | 0/3 | **3/3** | 0 | ✅ |
| REG1 | inline "check before prod" | 3/3 | 3/3 | 0 | ✅ held |
| SN1 | "15% of 80" | 0/3 | 0/3 | 0 | ✅ silent |
| SN2 | "tacos or pizza" | 0/3 | 0/3 | 0 | ✅ silent |

**PASSES the pre-registered decision rule on every clause:** every governed case
loads adversarial-verify ≥2/3 (all **3/3**), both should-not stay 0/3 (no
over-fire), confabulation = 0. Raw-grep confirmed `"skill":"adversarial-verify"`
3/3 in each SF/REG case.

**The headline:** SF1 — the *verbatim prompt* that started this whole
investigation, where claude.ai Opus applied governance "in spirit" without loading
— now loads adversarial-verify **every single time (3/3)**, even on a web-derailed
degraded turn. This is the "each and every time" the owner asked for, achieved on
Claude Code.

## Mechanism verified (not just the outcome)

Adversarial spot-check of SF1 clean runs: the sequence is `web attempts (no load) →
GOV-ENFORCE block → LOAD:adversarial-verify`. The model would have shipped without
loading (OFF proves it: 0/3); the **Stop hook blocked the turn and forced the load
on retry**. The enforcement did the work — the up-front nudge alone did not (the
model went to web first, skipped the load, and only loaded after the block). Two
design choices proven necessary:
- **Enforce, don't request** (INC-9 fix): the load-only inject asks for no receipt,
  so there is nothing to confabulate — 0 confabulations vs 4 in Phase 2. The Stop
  hook checks the *observable load*, not a self-reported ✓.
- **Classifier gate = anti-ceremony**: SN1/SN2 classified not-governed → no inject,
  Stop hook allows immediately → silent. No ceremony on trivia.

## Critical methodology note — the first (contaminated) ENFORCE run was a harness bug

The initial ENFORCE run (concurrency 4) scored SF1/SF2 at 1/3 and looked like a
partial failure. **That was a test-harness contamination, not an enforcement
failure.** Root cause (INC-10): the nested `claude -p` processes inherited
`CLAUDE_CODE_SESSION_ID` from the parent session, so all 36 runs shared **one**
session transcript; under concurrency the Stop hook read a transcript jumbled by
other in-flight runs and mis-decided whether to block. Fix: strip the inherited
session env vars so each nested run gets its own session id + transcript; re-run
gave a clean 3/3. **This bug is specific to the concurrent nested-run test harness
— a real single-user Claude Code session has exactly one transcript, so the hook
works correctly in production.** Caught by distrusting a smooth-looking partial
result and reading the internal transcript (which showed the block DID force loads).

## Caveats (faithful)

- N=3, single model (Opus), single surface (Claude Code headless). Strong, clean
  separation (0/3 → 3/3), but a rate on N=3, recorded as such.
- **Classifier coverage is the ceiling now.** Enforcement only fires on prompts the
  keyword classifier flags as governed; a governed prompt with novel phrasing that
  dodges the keywords gets no enforcement (a false negative). The classifier is a
  first cut — widening/replacing it (or an LLM classifier) is the next refinement.
- **Single-retry (loop-safe).** The Stop hook blocks once (`stop_hook_active`); a
  model that refused on the single retry would escape. Here it complied 3/3.
- **Claude Code only.** claude.ai has no hook layer — this enforcement cannot exist
  there (the INC-8 surface remains prose-only; unchanged).
- The web-block confound from Phase 2 is now *resolved*: enforcement forced loads
  even on web-derailed turns, so the SF1/SF2 issue was never the prompt class.

## Artifacts

`results/2026-07-15/phase2b_enforce_ab/`: clean transcripts (`transcripts_clean/`),
the contaminated first run (`transcripts/`, retained as the INC-10 evidence),
runners, both frozen hooks. Shipped to `hooks/` with install + caveats.
