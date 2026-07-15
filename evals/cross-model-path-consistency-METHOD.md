# Cross-Model Path-Consistency Verification — Method & Procedure

**Audience: a future Claude session (or the owner) improving this system.** This is the
durable, logical procedure behind the cross-model verification the owner cares about —
"do two models follow the *same* skill-driven problem-solving and resolution path?" The
finding of any one run is disposable; **this procedure is the asset.** Do not let it rot
into "we pasted a prompt and it looked fine once."

- **Instrument (the prompt):** [`cross-model-path-consistency-prompt.md`](cross-model-path-consistency-prompt.md)
- **First run (worked example):** [`../results/2026-07-15/`](../results/2026-07-15/) —
  `sonnet-opus-path-comparison.md` + both deliverables.
- **Kin skills:** `governance-adoption-campaign` (sequences evals across surfaces),
  `research-methodology` (turns a wording hunch into evidence), `architecture-contract`
  (is a change legal), `adversarial-verify` (grade-and-refute discipline this method applies
  to its own output).

---

## 1. What this method is for (and is not)

**Is:** a *path-comparison* — given identical input and the same installed governors, do
model A and model B reach the answer the same way, and where do they diverge?

**Is not:** a cold *trigger* test (does a skill fire from a name-free prompt — that lives in
`evals/*.json` + `governance-adoption-campaign` Phase 1), and not a *behavioral* with/without
test (does the governor change anything — Phase 2). This is the third axis:
**cross-model consistency of the governed path.**

Keep the axes separate. A result here does not substitute for a trigger rate or a behavioral
delta, and vice-versa.

---

## 2. The five design principles (the logic the instrument encodes)

Each principle exists to defeat a specific failure mode. If you rebuild the instrument, keep
all five or state which you dropped and why.

1. **Observation over introspection.** Asking a model "would you have used plan-gate?" is
   fenced off across this library — introspection is not observation. So the prompt makes the
   model **do the work first**, then trace the path it *actually took*. Every reported line is
   tagged `OBSERVED` (did it) vs `INFERRED` (believes it applies). Defeats: armchair
   self-narration that doesn't match behavior.
2. **Non-leading task.** The scenario **never names a skill**. Naming one guarantees a "fire"
   and proves nothing. Phrasings are reused from the already-validated `evals/*.json` sets.
   Defeats: contaminated triggering.
3. **One scenario, all active governors + a control.** A single consequential task that
   naturally exercises `plan-gate` (a costly prod migration), `adversarial-verify` (a
   teammate artifact claimed to "work on my laptop"), and `scope-fence` (a *dangled*, not
   requested, adjacent cleanup) — plus a trivial sub-question as an **over-fire control**
   (ceremony on trivia is itself a failure). Defeats: needing four prompts and losing
   cross-governor interaction.
4. **Rigid, diffable output.** A fixed-section, fixed-field-name, controlled-vocabulary PATH
   TRACE so model A's Section N lines up against model B's Section N. Defeats: two prose blobs
   that can't be compared.
5. **Identical input to both models.** Same bytes. Any difference is then attributable to the
   model, not the prompt. Defeats: rephrasing as a hidden second variable.

**Known tension (state it, don't hide it):** the trace template lists the governor names, so
a single paste is not a clean cold-trigger test — it is a fair *comparison* (identical priming
both sides). For clean triggering use the two-paste variant or the `evals/*.json` harness.

---

## 3. The procedure, step by step

### Phase A — Prepare
1. Pick/author the scenario per principle 3. Reuse validated phrasings; keep the dangled
   work *dangled* ("you'll probably notice…"), never *requested* (requested = named = inside
   the fence, and `scope-fence` correctly stays silent — see LESSONS DEAD-1).
2. Confirm the active-governor list still matches `.claude/skills/` and the
   `instructions/claude-ai-custom-instructions.md` paste block. Update the Section 2
   vocabulary if a governor was added/retired.

### Phase B — Run (per model, per surface)
3. **Fresh session, no prior turns.** Prior turns pre-trigger skills.
4. **Confirm skills are present** in that session *before* running (claude.ai Skills panel +
   instructions pasted; or Claude Code skills list). **This is the #1 confound guard** — a
   "path difference" that is really an *install* difference. Record yes/no.
5. Paste identically. One paste (max comparability) or two-paste (task, then trace — cleaner
   triggers). Keep the choice consistent across models, or record the asymmetry.
6. **N ≥ 2 fresh runs per model per surface.** One run cannot separate "the models differ"
   from "the dice differed." N=2 is the floor (`research-methodology` R1); raise it for close
   calls.
7. **Capture everything verbatim:** the full PATH TRACE §0–8, plus — on Claude Code only — the
   **observed Skill-tool fire log**. That log is ground truth that converts §2 from
   introspection into observation. On claude.ai it does not exist; lean harder on step 4.

### Phase C — Analyze (this is where the rigor lives)
8. **Signature-hit matrix** — governor × model. Did each model produce each governor's
   signature? (plan-gate: goal/criteria before acting · adversarial-verify: exercise +
   refute + no-ship, not affirm · scope-fence: flag the dangled cleanup, fix only what breaks
   the named task · control: answer trivia with no ceremony.) Mark same/different per row.
9. **Convergences** — enumerate the items where both took the same path. Be specific
   (same defect caught with the same evidence, same fix, same verdict).
10. **Divergence ledger** — one row per difference: axis · model A · model B · read. Then
    **classify each divergence**:
    - *skill-driven* — a governor changed one model's path;
    - *base-model* — they'd differ regardless of skills;
    - *noise* — only appears in one of the N runs (needs N≥2 to call).
11. **Reconcile self-report against artifact.** Where the trace and the delivered artifact
    disagree, say so and resolve it. **This is not optional — it is the step that caught the
    biggest error in the first run (see §5, L1).**
12. **Instrument-validation checks** (does the method itself hold up?):
    - Did each model's §7 divergence self-flags *predict* the actual divergences? (In run 1,
      yes — both did. That is evidence §7 is load-bearing; keep it.)
    - Did the trace change the answer vs artifact-only inspection? (In run 1, yes — keep
      requiring the trace.)
13. **Verdict + caveats.** Record rates **dated**, never promoted to "always" (baseline
    measurement ≠ change acceptance — `governance-adoption-campaign` distinction). List every
    caveat that bounds the verdict (N, self-report, skills-present, protocol asymmetry).
14. **Apply `adversarial-verify` to your own comparison** before delivering: verify each
    convergence/divergence line against the actual files; try to refute your own read.

---

## 4. Output contract (what a finished run leaves behind)

Under `results/<date>/`:
- each model's deliverable (verbatim);
- `*-path-comparison.md` with: status, bottom line, signature-hit matrix, convergences,
  divergence ledger (classified), the reconciliation note, instrument-validation checks,
  verdict, caveats;
- a one-line pointer added here and in the instrument's Provenance if the method changed.

---

## 5. Transferable lessons from run 1 (2026-07-15, Sonnet vs Opus, claude.ai)

- **L1 — the trace corrects the artifact; inspecting the deliverable alone can invert the
  answer.** Both rewritten scripts *looked* like the dangled logging/dead-code cleanup was
  silently absorbed (a scope-fence *miss*). The §6 trace showed both models **flagged** it and
  fixed only the parse-breaking `print()` line as an in-scope bug — a scope-fence *hit*, with
  identical reasoning. **Always get §4–7, not just the Section 8 artifact.** (Ledger:
  INC-5.)
- **L2 — §7 divergence self-flags are predictive; keep them.** Opus's §7 named the
  `--data-only` fork; Sonnet took it. Sonnet's §7 named the blanket-`UPDATE` fork; Opus
  resolved it the other way. Each model correctly pointed at where the other diverged.
- **L3 — high cross-model consistency is achievable and was observed once.** Same diagnosis
  (both ran `bash -n`/shellcheck, both caught the script doesn't parse, both noted it
  contradicts "ran fine on my laptop"), same core fixes, same scope reasoning, same no-ship
  verdict, both passed the over-fire control. N=1, so it is "observed once, dated," not
  "always."
- **L4 — the durable divergence is *disposition*, not diagnosis.** Opus silently picks the
  safe default; Sonnet preserves original behavior and surfaces the call to the human, and
  goes deeper on correctness (sequence resync, re-entry precheck). If the goal is to make the
  two models *more* identical, that disposition gap — not the diagnosis — is the thing to
  steer, and steering it is a `research-methodology` hypothesis (below).

---

## 6. How to improve the system from here (the ratchet)

Do these in roughly this order; each closes a caveat from run 1.

1. **Capture §0–3 next run** (run header, task classification, the skills-engaged table, the
   step-by-step path). Run 1 only captured §4–8; §0–3 give a fuller path diff and the
   self-reported trigger *order*.
2. **N=2 per model** (a second fresh run) to move divergences out of "could be noise."
3. **Record skills-present confirmation every run** — close the install-vs-path confound
   (§3 step 4) so a divergence can never be secretly an install gap.
4. **Add a Claude Code run** to get the observable Skill-fire log — the only way, on current
   surfaces, to corroborate §2 self-report with observation.
5. **If tighter cross-model identity is the goal, treat the disposition gap (L4) as a
   hypothesis, not a bug to hand-fix.** Example, pre-registered per `research-methodology`:
   *"Adding a custom-instruction line — 'when a business-logic call is ambiguous, surface it,
   don't silently default' — makes Opus preserve-and-flag like Sonnet."* One variable, fresh
   A/B, N=2, any-regression-blocks. Do **not** reword and eyeball.
6. **Extend coverage:** other model pairs (e.g. Haiku vs Sonnet), other surfaces (interactive
   Claude Code), and — when a governor is added/retired — refresh the Section 2 vocabulary and
   the signature list.

---

## 7. Provenance and maintenance

Authored 2026-07-15 alongside the first run of the instrument. Method generalizes the
observed-fires-over-introspection doctrine (`governance-adoption-campaign`, "Wrong paths,
fenced off"), the N=2 / pre-registration / any-regression-blocks bar (`research-methodology`),
and the grade-and-refute discipline (`adversarial-verify`) into a cross-model comparison
procedure this library did not previously have written down.

Re-verify: the active-governor list in §2/§3 still matches `.claude/skills/`; the instrument
file still exists. Update when: a governor is added/retired (vocabulary + signature list), a
run adds a step or overturns a lesson, or a ratchet item in §6 is completed (record the date
and result).
