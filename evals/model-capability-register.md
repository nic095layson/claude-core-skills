# Model-capability register — what carries the discipline, measured on which model, when

Seeded 2026-08-03 (Fable 5 session, proposal 4 of
`results/2026-08-03/skill-proposals/`). One row per calibrated behavior: what
supplies the discipline today, the last measurement that supports that claim,
and the condition that re-opens it. Rates are rates — never promoted to
"always". Companion: `fable-transition-audit.md` (the runbook that refreshes
this file).

**The honest headline at seeding:** the library's load-bearing measurements
(2026-07-11 campaign, 2026-07-15 runs) were taken on **Opus 4.8 and Sonnet 5 —
the post-Fable daily models themselves**. Fable's departure therefore does not
invalidate the measured rows below; what leaves with Fable is un-measured
capacity — authoring judgment, orchestration depth, report rigor — which is
exactly what the 2026-08-03 authored artifacts attempt to preserve as prose.
The register's job is to catch the *next* mix change, and to record whether
the unmeasured rows hold up once the daily models are all that's left.

| # | Behavior / discipline | Carried by | Last measured | Models | Verdict (dated) | Re-opens when |
|---|---|---|---|---|---|---|
| 1 | Check live state over docs; measure, don't eyeball | Base model (skill RETIRED) | 2026-07-11, 8-cell cued+uncued | Opus 4.8, Sonnet 5 | RETIRE-CONFIRMED — zero delta in all cells | Any daily model fails the uncued doc-lie catch (audit step 2) |
| 2 | Record costly diagnoses (append-on-diagnosis) | **Hook (measured)** + `.claude/LESSONS.md` convention; skill retired | 2026-08-03 hook A/B (`results/2026-08-03/hook-ab/`) | Sonnet 5, Code headless | **Hook CONFIRMED, cued-recount class: 6/6 with vs 0/6 without, 0 false fires**; uncued planted-bug cell still open; prior 2026-07-11 skill rates unchanged | Uncued cell run; regex/reminder edits (gated text — re-run the A/B) |
| 3 | Adjacent-work restraint while editing code | scope-fence skill + first-edit hook (2026-07-12) | 2026-07-11 | Opus 4.8, Sonnet 5 | Description-only triggers ~60–67%; inline-code class unfireable by wording (DEAD-1); behaves 4/4 when fired | Hook-arm measurement; any model-mix change |
| 4 | Plan-before-acting (goal, criteria, phases) | plan-gate skill (active governor); first-write hook = harmless, effect untested (INC-9) | 2026-08-03 hook A/B baseline (re-confirms 2026-07-11) | Sonnet 5, Code headless | Fired 6/6 by description on its eval prompts — at ceiling there; hook never activated (no baseline run wrote); zero ceremony added | Straight-to-edit instrument (DEAD-1 class prompts, append-only) |
| 5 | Adversarial verification before delivery | adversarial-verify skill (active governor) | 2026-07-11 post-trim re-run | Claude Code headless | Fired 9/9 (INC-3 evidence) | Audit steps 3–4 on a new daily model |
| 6 | Surface-and-flag on ambiguous behavior-changing defaults | Instructions line ("no silent defaults") — candidate | 2026-07-15, three-way A/B | Opus 4.8, Sonnet 5 | SATURATED on top-tier — no benefit shown, no regression; retained as cheap insurance | A weaker daily model joins the mix (the exact condition the law was insured against) |
| 7 | Same-skill same-path consistency across models | Instrument (`cross-model-path-consistency-*.md`) | 2026-07-15 | Sonnet 5 ↔ Opus 4.8, claude.ai | One durable divergence found (silent-defaults disposition; row 6) | Each new model pairing |
| 8 | Delegation discipline (brief/bound/verify subagents) | `delegation-discipline` skill | 2026-08-03, trigger evals + behavioral A/B (`results/2026-08-03/{trigger-evals,hook-ab}/`) | Sonnet 5, Code headless | Fires 5/6 clean prompts, 0 over-fire; **behavioral delta on delegation conduct: 2/2 with vs 0/2 without (id7)**; acceptance case saturated by adversarial-verify (id8) — net-new value is briefing/checkpoint, not acceptance | Any model-mix change; claude.ai N/A (no subagents) |
| 9 | House report format + primary-source claim-check | `after-report` skill | 2026-08-03, trigger evals (same dir) | Sonnet 5, Code headless | Fires 7/8 on description-testing prompts, 0 over-fire; claude.ai triggering untested | claude.ai live-fire; behavioral phase-2 |
| 10 | Application tailoring, anti-fabrication fenced | `application-tailor` skill | 2026-08-03, trigger evals (same dir) | Sonnet 5, Code headless | Fires 8/8 on description-testing prompts, 0 over-fire; co-fired brand-standard 3/4 (compose design works); claude.ai untested | claude.ai live-fire; first live application |
| 11 | Email drafting in-voice, draft-never-send | `correspondence` skill — **need still unconfirmed** | 2026-08-03, trigger evals + behavioral A/B | Sonnet 5, Code headless | Gate PASS 5/6 · 4/4; **behavioral: send-refusal policy 2/2 with vs 0/2 without** ("even though you said to just send it"); lane unconfirmed | Owner confirms the lane is real |
| 12 | Fable→Opus classifier fallback (visibility of active model) | Platform (transcript notice, `/status`, statusline, `switchModelsOnFlag`) | 2026-08-03, docs re-verified | Fable 5 | Documented: noticed but sticky until `/model` | Docs change; any observed silent switch (would also be a lessons entry) |

## Maintenance

Append rows, never silently rewrite them — supersede with a new dated row and
strike the old verdict inline. Every audit run (`fable-transition-audit.md`)
refreshes the Last-measured / Models / Verdict columns it touched and links
its results directory. An entry without a dated measurement behind it is a
rumor and does not belong here (ledger doctrine, applied to capabilities).

Sources at seeding: architecture-contract weak-point 5 table (rows 1–2),
`hooks/README.md` + `.claude/LESSONS.md` DEAD-1/DEAD-2/INC-3 (rows 2–5),
`instructions/claude-ai-custom-instructions.md` provenance + `results/2026-07-15/`
(rows 6–7), `results/2026-08-03/` (rows 8–12).
