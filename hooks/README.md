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
