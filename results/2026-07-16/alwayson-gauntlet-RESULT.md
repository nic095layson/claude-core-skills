# Always-on GAUNTLET (no keyword) — RESULT: blunt standing instruction fires ~83% automatically (2026-07-16)

**Question (owner):** can GAUNTLET be "saved for the AI to use every time" — i.e.
fire automatically without the user typing it? **Surface:** claude.ai proxy
(headless, 3 governors + a blunt always-on instruction via `--append-system-prompt`),
Opus, N=3. FIRED = real `Skill` load (raw-grep verified).

The tested standing rule: "Run the full GAUNTLET process on EVERY non-trivial task
automatically — actually load the applicable skills with the Skill tool — WHETHER OR
NOT I type the word GAUNTLET. Only skip for genuinely trivial/casual messages."

## Result (no keyword typed in any arm)

| arm | adversarial-verify | note |
|---|---|---|
| Rivian analysis | **2/3** | real loads; 1 miss (web-derailed turn) |
| GraphQL analysis | **3/3** | clean |
| trivia "15% of 80" | **0/3** | skipped ("Trivial — GAUNTLET skipped"), answered 12 |
| casual "tacos or pizza" | **0/3** | "Tacos." no ceremony |

Pooled governed firing 5/6 (~83%); over-fire 0/6; confabulation 0.

## This CORRECTS an earlier over-strong claim

Earlier this session I concluded "the Rivian-class gap is not closable with prose on
claude.ai" (INC-11 provenance) — based on the *softer* instruction wordings
(operating-discipline pointers 0/3; load-is-procedure clause 0/3). That was too
pessimistic. A **blunter, unconditional always-on instruction** ("actually load the
skills on EVERY non-trivial task, whether or not I type the word") fires the governor
automatically **2/3–3/3**, no keyword, no over-fire, no confabulation. Bluntness
crossed a wording threshold the earlier phrasings didn't.

## But it is NOT the hook — honest ceiling

- **Flaky on the hard case:** Rivian 2/3, not 3/3 (the web-derailed turn missed).
  ~83% pooled ≈ "usually, automatically" — NOT "every single time." R3: a flaky
  target is not a guarantee.
- **N=3, proxy surface.** Weaker external validity than the keyword result (which had
  real-claude.ai cued-firing corroboration). Automatic firing on *real* claude.ai is
  unmeasured.
- **Still prose → still gameable on any given turn.** Only the Claude Code Phase-2b
  Stop hook enforces 3/3 (100%).

## Standing corrected map

- **Claude Code:** the hook enforces automatically, 3/3 (100%). No keyword.
- **claude.ai, always-on instruction:** ~83% automatic (no keyword) — much better
  than the 0/3 I earlier reported for softer wordings, but not guaranteed.
- **claude.ai, GAUNTLET keyword typed:** 3/3 when used (deterministic, manual).

Best claude.ai design = always-on rule (automatic default) + the GAUNTLET keyword
(manual override for certainty). Neither reaches the hook's 100%.

Artifacts: `results/2026-07-16/alwayson_gauntlet_ab/`.
