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
| 1 | Check live state over docs; measure, don't eyeball | Base model (skill RETIRED) | 2026-07-11, 8-cell cued+uncued | Opus 4.8, Sonnet 5 | RETIRE-CONFIRMED — zero delta in all cells *(superseded 2026-08-26 → row 14, verdict unchanged)* | Any daily model fails the uncued doc-lie catch (audit step 2) |
| 2 | Record costly diagnoses (append-on-diagnosis) | Skill (retired from installs) + `.claude/LESSONS.md` convention; hook candidate shipped 2026-08-03 | 2026-07-11 | Opus 4.8, Sonnet 5 | Uncued 0/16 both arms (INCONCLUSIVE); cued weak; wording ceiling ~80% (DEAD-2) *(superseded 2026-08-26 → row 15, verdict unchanged)* | Hook A/B results (`experiments/hypothesis-2026-08-03-hook-enforcement.md`) |
| 3 | Adjacent-work restraint while editing code | scope-fence skill + first-edit hook (2026-07-12) | 2026-07-11 | Opus 4.8, Sonnet 5 | Description-only triggers ~60–67%; inline-code class unfireable by wording (DEAD-1); behaves 4/4 when fired *(superseded 2026-08-26 → row 16: trigger gate now PASS on Fable 5, behavioral delta gone)* | Hook-arm measurement; any model-mix change |
| 4 | Plan-before-acting (goal, criteria, phases) | plan-gate skill (active governor) | 2026-07-11 post-trim re-run | Claude Code headless | Fired 6/6 should-fire (INC-3 evidence); behavioral delta un-isolated *(superseded 2026-08-26 → row 17: delta isolated, clean)* | Audit steps 3–4 on a new daily model; plan-gate hook A/B |
| 5 | Adversarial verification before delivery | adversarial-verify skill (active governor) | 2026-07-11 post-trim re-run | Claude Code headless | Fired 9/9 (INC-3 evidence) *(superseded 2026-08-26 → row 18)* | Audit steps 3–4 on a new daily model |
| 6 | Surface-and-flag on ambiguous behavior-changing defaults | Instructions line ("no silent defaults") — candidate | 2026-07-15, three-way A/B | Opus 4.8, Sonnet 5 | SATURATED on top-tier — no benefit shown, no regression; retained as cheap insurance | A weaker daily model joins the mix (the exact condition the law was insured against) |
| 7 | Same-skill same-path consistency across models | Instrument (`cross-model-path-consistency-*.md`) | 2026-07-15 | Sonnet 5 ↔ Opus 4.8, claude.ai | One durable divergence found (silent-defaults disposition; row 6) | Each new model pairing |
| 8 | Delegation discipline (brief/bound/verify subagents) | `delegation-discipline` skill | 2026-08-03, trigger evals (`results/2026-08-03/trigger-evals/`) | Sonnet 5, Code headless | Fires 5/6 on description-testing prompts, 0 over-fire; absent-artifact class is a recorded ceiling (INC-8); behavioral value unmeasured | Behavioral phase-2; any model-mix change |
| 9 | House report format + primary-source claim-check | `after-report` skill | 2026-08-03, trigger evals (same dir) | Sonnet 5, Code headless | Fires 7/8 on description-testing prompts, 0 over-fire; claude.ai triggering untested | claude.ai live-fire; behavioral phase-2 |
| 10 | Application tailoring, anti-fabrication fenced | `application-tailor` skill | 2026-08-03, trigger evals (same dir) | Sonnet 5, Code headless | Fires 8/8 on description-testing prompts, 0 over-fire; co-fired brand-standard 3/4 (compose design works); claude.ai untested | claude.ai live-fire; first live application |
| 11 | Email drafting in-voice, draft-never-send | `correspondence` skill — **need still unconfirmed** | 2026-08-03, trigger evals (same dir) | Sonnet 5, Code headless | Gate PASS as committed: 5/6 fire · 4/4 silent; trigger measured, lane unconfirmed | Owner confirms the lane is real |
| 12 | Fable→Opus classifier fallback (visibility of active model) | Platform (transcript notice, `/status`, statusline, `switchModelsOnFlag`) | 2026-08-03, docs re-verified | Fable 5 | Documented: noticed but sticky until `/model` | Docs change; any observed silent switch (would also be a lessons entry) |
| 13 | ~~Deterministic photo editing~~ **RETIRED 2026-08-12 (owner: no longer wanted; skill deleted, research kept)** — under the three laws (never-overwrite, measure-before-cut, see-edit-verify) | `photo-editing` skill (project scope) | 2026-08-10, trigger evals (`results/2026-08-10/trigger-evals-photo-editing/`) | Sonnet 5, Code headless | GATE PASS clean: 8/8 fire · 6/6 silent, 0 over-fire; laws held in-run (originals byte-stable, inspect-before-edit in all fire runs); behavioral delta vs no-skill un-isolated | claude.ai live-fire; any model-mix change; first live photo lane use |
| 14 | Check live state over docs — **re-measure of row 1** | Base model; skill RETIRED and, since the global doctrine (2026-07-13), un-loadable even when installed | 2026-08-26, 8-cell cued+uncued (`results/2026-08-26/fable-transition/`) | Fable 5 | **RETIRE-CONFIRMED holds** — native 8/8 (without-arm), with-retired 8/8 with **0/8 skill loads** (doctrine suppression, INC-2026-08-26-02); zero delta in every cell | Any daily model fails the uncued doc-lie catch; Decision 7 can only be re-argued with a doctrine-free with-arm (D-C) |
| 15 | Record costly diagnoses — **re-measure of row 2** | Base model memory feature (cued) + `.claude/LESSONS.md` convention; skill un-loadable under doctrine | 2026-08-26 | Fable 5 | Cued native 3/4 (memory-feature notes with frontmatter); with-retired 4/4 at 0/4 loads (second native replicate); **uncued 0/8 both arms → INCONCLUSIVE**, same shape as 2026-07-11; no re-open | Hook A/B (`ledger-recount-reminder.sh`, still not installed) |
| 16 | Adjacent-work restraint — **re-measure of row 3** | scope-fence skill + global-doctrine line + first-edit hook | 2026-08-26 | Fable 5 | **Trigger gate PASS for the first time:** core 6/6 (id1 2/2, id2 2/2, id3 2/2), id8 0/2, silent 4/4. Behavioral: with 4/4 · **without 4/4 — NO DELTA**; without-arm sessions cite "your scope-fence doctrine" by name; doctrine-carried vs native not separable (hook injected 0/24) | Doctrine-free without-arm (D-A/D-C); architecture-contract context-cost review |
| 17 | Plan-before-acting — **re-measure of row 4** | plan-gate skill | 2026-08-26 | Fable 5 | Trigger 6/6 · silent 4/4; behavioral with 4/4 · without 0/4 — **clean delta** (doctrine line present in both arms did not produce the gate block without the skill); loads adversarial-verify sequentially afterwards in 6/10 with-arm runs (doctrine sequence, not a co-fire defect) | Any model-mix change; co-fire gate wording (D-B) |
| 18 | Adversarial verification — **re-measure of row 5** | adversarial-verify skill | 2026-08-26 | Fable 5 | Trigger 6/6 · silent 4/4; behavioral structured with 4/4 · without 0/4; **substantive defect-finding 4/4 in both arms** — value is structure, as in July | Uncued should-verify prompt (D-F, owed since July) |
| 19 | Global doctrine (`~/.claude/CLAUDE.md`) as a behavior carrier — **new** | Prose loaded in every Claude Code session incl. headless; absent from the 2026-07-11 anchors (file mtime 2026-07-13) | 2026-08-26 (observed in-run, not designed-for) | Fable 5 | Suppresses retired-skill loading 16/16 even when installed (quoted); cited by without-arm sessions; present in both arms of every 2026-08-26 measurement | Any doctrine edit; any A/B that needs a doctrine-free arm |

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
