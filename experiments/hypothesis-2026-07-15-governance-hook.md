# Hypothesis — a UserPromptSubmit governance hook fires the governor where wording can't

**Pre-registered 2026-07-15, BEFORE any A/B run.** Motivated by DEAD-3: the
description lever cannot fire adversarial-verify on the produce-an-analysis class
(SF1/SF2 flat 0/3 even quoting the incident verbatim). Plan Phase 2 — the
mechanical lever. Feasibility already confirmed this session: a project-scope
`UserPromptSubmit` hook fires in headless `claude -p` and its `additionalContext`
reaches the model (sentinel test: model echoed the injected token).

## The mechanism under test (the NEW "variant" is a hook, not wording)

`.claude/hooks/governance-trigger.py` (frozen for this run;
`results/2026-07-15/phase2_hook_ab/governance-trigger.py`): a `UserPromptSubmit`
hook that classifies the prompt (keyword/pattern) and, for governed-class work,
injects this `additionalContext`:

> Governance auto-trigger (from your operating rules): this request is classified
> as governed work (<governor(s)>). BEFORE you produce the answer, load
> <governor(s)> with the Skill tool and follow the procedure it defines; then end
> your reply with a one-line governance receipt. If on inspection this is genuinely
> trivial, say so in one line and skip — do not manufacture ceremony.

Classifier gating (deterministic pipe-test, pre-committed): SF1/SF2/SF3 →
adversarial-verify; REG1 → adversarial-verify (+plan-gate, migration); SN1/SN2 →
**silent** (no injection — the anti-ceremony gate is in the classifier itself).

## Arms & cases — HOOK-OFF vs HOOK-ON, same 6 prompts, N=3, fresh session each

Same prompt set as Phase 1 (`hypothesis-2026-07-15-advverify-analysis-trigger.md`).
Both arms install the same 3 governors (current shipped descriptions — Phase 1
proved the description doesn't move this class, so it is held fixed). The ONLY
variable is the hook (absent vs wired in `.claude/settings.json`).

FIRED = observed `adversarial-verify` `Skill` tool_use in the stream-json
transcript (the target governor; any-governor also recorded). Receipt presence is
recorded but is NOT the pass criterion — a real Skill load is (INC-5: don't grade a
governor from a self-reported line).

| id | class | HOOK-OFF pred | HOOK-ON pred |
|---|---|---|---|
| SF1 | Rivian incident prompt | 0/3 (baseline) | **≥2/3 loads adv-verify** |
| SF2 | Nvidia forecast | 0/3 | **≥2/3 loads** |
| SF3 | REST→GraphQL analysis | 0–1/3 | **≥2/3 loads** |
| REG1 | inline "check before prod" | 3/3 | ≥2/3 (no regression) |
| SN1 | "15% of 80" | 0/3 silent | **0/3 silent** (hook doesn't inject) |
| SN2 | "tacos or pizza" | 0/3 silent | **0/3 silent** (hook doesn't inject) |

## Decision rule (committed, research-methodology R1/R2/R3 + anti-ceremony)

- **ACCEPT the hook** iff under HOOK-ON: every SF loads adversarial-verify ≥2/3
  (target), REG1 ≥2/3 (no regression), AND both SN stay 0/3 (no over-fire — at
  the classifier OR the model level). Any single regression/over-fire blocks (R2).
- **R3:** an SF at exactly 1/3 under HOOK-ON = inconclusive → strengthen the
  injected text or raise N; do not ship a coin flip.
- **Veracity check (INC-5):** any run where the model emits a receipt ✓ for
  adversarial-verify but no Skill load is observed is flagged as a confabulated
  receipt — recorded, and counts as NOT-fired for the target.
- **FAIL → do not ship the hook**; record why (a hook that injects but doesn't
  cause a load would be a deeper finding: even mechanical injection can't force a
  load → escalate to a Stop-hook that blocks on a missing receipt, plan Phase 2b).

## Protocol / integrity

- Same 6 prompts verbatim both arms; fresh `claude -p` per run; same sitting,
  surface (Claude Code headless), model (`claude-opus-4-8`).
- Isolated out-of-repo `RUNROOT`; the hook is wired at **project scope**
  (`RUNROOT/.claude/settings.json`) — no `~/.claude` mutation (INC-4 safe).
- HOOK-OFF arm: settings.json absent. HOOK-ON arm: settings.json present. Verify
  per arm by checking the file's presence/content before the arm runs.
- Web tools network-blocked (as in Phase 0/1); does not affect the Skill-load
  measure; SF3/REG1/SN need no web.
- Verbatim transcripts kept. This is change-acceptance → R2 governs.
