# Hooks — mechanical trigger aids

## scope-fence-reminder.sh (shipped 2026-07-12)

The lever past the description-triggering ceiling (campaign finding: scope-fence
behaves 4/4 when fired but triggers ~60-67% by description alone). A PreToolUse
hook on Edit|Write injects a one-line scope reminder into model context at the
first file edit of each session — once, then silent (sentinel in $TMPDIR keyed
by session_id).

Install (user scope):
1. `cp hooks/scope-fence-reminder.sh ~/.claude/hooks/` and `chmod +x` it.
2. Merge into `~/.claude/settings.json`:
   `{"hooks":{"PreToolUse":[{"matcher":"Edit|Write","hooks":[{"type":"command","command":"bash ~/.claude/hooks/scope-fence-reminder.sh","timeout":10}]}]}}`
3. Verify: pipe-test (`echo '{"session_id":"t","tool_name":"Edit","tool_input":{}}' | bash ~/.claude/hooks/scope-fence-reminder.sh` → JSON once, empty on repeat), then observe the reminder arrive on a session's first real edit.

Verified live 2026-07-12 on the primary machine: pipe-test both paths PASS;
reminder observed injected into a running session's context on first Write;
sentinel confirmed; silent thereafter.

## governance-trigger.py + governance-enforce.py (validated 2026-07-15) — the enforcement lever

The lever past the **description ceiling** (DEAD-3: no wording fires
adversarial-verify on the produce-an-analysis class) and past the **requested-receipt
failure** (INC-9: a hook that *asks* for a receipt gets a confabulated ✓). This pair
makes a governor load **mechanically enforced** on governed-class turns, on Claude
Code (claude.ai has no hook layer, so this cannot exist there).

Two hooks keyed to a shared keyword classifier:
- **`governance-trigger.py`** (`UserPromptSubmit`): classifies the prompt; for
  governed work injects a load-only nudge ("Load <governor> with the Skill tool
  before answering"). **No receipt is requested** — so there is nothing to
  confabulate. Silent on trivia (the classifier is the anti-ceremony gate).
- **`governance-enforce.py`** (`Stop`): reads the turn's transcript; if the prompt
  was governed AND **no governor `Skill` actually loaded**, returns
  `{"decision":"block", reason:"…load it now…"}`, forcing a retry. Single-retry via
  `stop_hook_active` (loop-safe). Silent (allow) on trivial or already-complied turns.

**Validated result (pre-registered A/B, `results/2026-07-15/phase2b-enforce-RESULT.md`,
Claude Code headless, Opus, N=3):** governed cases 0/3 → **3/3** loads — including the
**verbatim Rivian incident prompt (0→3/3)** — with **zero** over-fire (trivia stayed
silent) and **zero** confabulation. The block-then-load mechanism was confirmed by
reading the transcripts (model skips → GOV-ENFORCE block → loads).

Install (user scope):
1. `cp hooks/governance-trigger.py hooks/governance-enforce.py ~/.claude/hooks/` and `chmod +x` them.
2. Merge into `~/.claude/settings.json`:
   `{"hooks":{"UserPromptSubmit":[{"hooks":[{"type":"command","command":"python3 ~/.claude/hooks/governance-trigger.py","timeout":10}]}],"Stop":[{"hooks":[{"type":"command","command":"python3 ~/.claude/hooks/governance-enforce.py","timeout":15}]}]}}`
3. Verify: pipe-test the classifier (`echo '{"prompt":"analyze X and advise when it hits $Y"}' | python3 ~/.claude/hooks/governance-trigger.py` → JSON inject; `echo '{"prompt":"what is 15% of 80?"}' | …` → empty), then observe a governed prompt force a load in a live session.

**Caveats, stated plainly:**
- **Owner decision to enable.** The library ships prose-only by default
  (architecture-contract Decision 1 / weak-point 3); a `Stop` hook that *blocks* turns
  is a real behavior change to every session. Adopting it into the standing footprint
  is the owner's call — these files are shipped as validated artifacts, not
  auto-enabled.
- **Classifier is the ceiling.** Enforcement only fires on prompts the keyword
  classifier flags; a governed prompt with novel phrasing that dodges the keywords
  gets no enforcement. Widen the classifier (or swap in an LLM classifier) to raise
  coverage.
- **Single-retry.** Blocks once; a model that refused on the retry would escape
  (none did in testing, 3/3).
- **Claude Code only** — no claude.ai equivalent exists.
