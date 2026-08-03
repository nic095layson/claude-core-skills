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

## plan-gate-first-write-reminder.sh (shipped 2026-08-03, UNMEASURED)

Same lever, aimed at plan-gate's blind spot: the DEAD-1 lesson class showed
that once the model is hands-on with concrete code it "just codes" and does
not consult governance skills, regardless of description wording. A PreToolUse
hook on Write|Edit|NotebookEdit injects a one-line plan reminder at the first
write-class tool use of each session — once, then silent. Deliberately
advisory, never blocking: a hook cannot judge triviality, and a hard block on
every edit would violate the anti-ceremony invariant (architecture-contract,
invariant 5).

Install (user scope):
1. `cp hooks/plan-gate-first-write-reminder.sh ~/.claude/hooks/` and `chmod +x` it.
2. Merge into `~/.claude/settings.json`:
   `{"hooks":{"PreToolUse":[{"matcher":"Edit|Write|NotebookEdit","hooks":[{"type":"command","command":"bash ~/.claude/hooks/plan-gate-first-write-reminder.sh","timeout":10}]}]}}`
   (coexists with scope-fence-reminder.sh — both may run on the same event;
   their messages are distinct and each fires once per session).
3. Verify: pipe-test (`echo '{"session_id":"t","tool_name":"Edit","tool_input":{}}' | bash ~/.claude/hooks/plan-gate-first-write-reminder.sh` → JSON once, empty on repeat), then observe on a real session's first write.

Pipe-tested both paths PASS 2026-08-03. **A/B ran same day: INCONCLUSIVE
(INC-9)** — plan-gate fired 6/6 by description on its eval prompts and no
baseline run reached a write, so the hook never activated; zero ceremony
added (harmless, effect untested). Needs a straight-to-edit instrument
(`results/2026-08-03/hook-ab/`). Wire it or not at owner's choice.

## ledger-recount-reminder.sh (shipped 2026-08-03, UNMEASURED)

The lever DEAD-2 named: append-on-diagnosis plateaued at ~80% under wording
(and 0/16 uncued in phase-2), with "mechanical enforcement (hooks), not
wording" recorded as the candidate next step. A UserPromptSubmit hook matches
costly-diagnosis recount phrasings (drawn from evals/lessons-ledger.json's
should-fire prompts: "burned/spent N hours", "turned out to be", "finally
figured/cracked it", "root cause was", "kept failing until", "chasing a bug")
and injects a one-line reminder to append to `.claude/LESSONS.md`. At most
once per session; extend the phrase list only through the A/B, not ad hoc.

Install (user scope):
1. `cp hooks/ledger-recount-reminder.sh ~/.claude/hooks/` and `chmod +x` it.
2. Merge into `~/.claude/settings.json`:
   `{"hooks":{"UserPromptSubmit":[{"hooks":[{"type":"command","command":"bash ~/.claude/hooks/ledger-recount-reminder.sh","timeout":10}]}]}}`
3. Verify: pipe-test a matching prompt (JSON once), a repeat (empty), and a
   non-matching prompt in a fresh session id (empty).

Pipe-tested all three paths PASS 2026-08-03. Regex corrected to spec the same
day after a deterministic pre-run check (id3's "took me all afternoon" was
missed; commit `848ee29`). **A/B ran same day: CONFIRMED for the cued-recount
class** — 6/6 with hook (five real appends + one drafted offer) vs 0/6
without, zero false fires on should-nots (`results/2026-08-03/hook-ab/`).
The reminder string and regex are now gated text: edits re-run the A/B.
Uncued planted-bug cell still open. **Recommended: install this one.**
