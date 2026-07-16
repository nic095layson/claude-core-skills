# GAUNTLET trigger word — RESULT: validated concise trigger for claude.ai (2026-07-16)

**Idea:** a single codeword the user types to invoke the full governance process —
the ergonomic form of WIN-1's named cue. **Surface:** claude.ai proxy (headless, 3
governors + instructions incl. the GAUNTLET definition via `--append-system-prompt`),
Opus, N=3. FIRED = real `Skill` load in the run's stream-json.

## Result

| arm | prompt | adversarial-verify | full governance |
|---|---|---|---|
| no_trigger (control) | Rivian prompt alone | 1/3 (flaky) | 2/3 |
| **gauntlet** | Rivian prompt + `GAUNTLET` | **3/3** | plan-gate + adversarial-verify **3/3** |
| gauntlet_trivia (over-fire) | "what's 15% of 80? GAUNTLET" | 0/3 | **0/3 — skipped** |

Raw-grep confirmed 3 real `adversarial-verify` loads in the gauntlet arm. Trivia
answers stayed correct with no ceremony ("Trivial — 12. GAUNTLET skips: no skills
fired").

## Reading

- **GAUNTLET fires the full applicable governor set 3/3** (plan-gate +
  adversarial-verify) on the incident prompt — better than naming one skill (WIN-1's
  named cue fired only adversarial-verify).
- **Respects anti-ceremony**: the definition's "trivial → skip" carve-out held — the
  codeword on trivia skipped gracefully 3/3, no over-fire.
- The codeword needs its instructions definition (GAUNTLET has no inherent meaning);
  the definition → load indirection holds.

## Deployed

Added to `instructions/claude-ai-custom-instructions.md` (paste block). **The word is
swappable** — GAUNTLET is arbitrary; any distinctive token the owner prefers
(e.g. a personal codeword) works identically as long as the definition names it and
it won't appear in normal prompts. **Re-paste owed** to the settings box.

## Caveats

- N=3, proxy surface (inherits external validity from WIN-1 / the real-claude.ai 7/7
  cued acceptance). Swapping the word doesn't require a re-test (mechanism proven;
  the word is a label) but keep it distinctive to avoid accidental fires.
- Still user-driven — you must type GAUNTLET. On Claude Code the Phase-2b hook
  enforces without a codeword.

Artifacts: `results/2026-07-16/gauntlet_trigger_ab/` (9 transcripts, runner).
