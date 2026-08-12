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

Pipe-tested both paths PASS 2026-08-03 (repo copy, this session). Live-fire on
the primary machine and the A/B measurement are owed:
`experiments/hypothesis-2026-08-03-hook-enforcement.md`.

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

Pipe-tested all three paths PASS 2026-08-03 (repo copy, this session,
including the "spent all afternoon" variant). Live-fire and A/B owed, same
experiment file.

## receipt-law-stop-gate.sh (PROPOSED 2026-08-12, pipe-tested, NOT installed)

The lever for INC-9. A **Stop** hook — the first in this pack that may *block*
rather than remind, and the reason it may is worth stating: the house rule
against blocking exists because a hook cannot judge triviality. This one never
has to. It asks a textual question with a factual answer — *does this claim of
inability name an attempt and a failure mode?* — and blocks only when the answer
is no. Once per turn, never on a continuation it caused, fail-open on any error.

**The design correction that matters.** The first version passed any turn in
which some verification tool had run. Tested against the real incident, that
**allowed it**: the founding session ran three searches, stopped, and then wrote
"couldn't verify" about eight items it had never touched. *Some tool ran* proves
nothing about a *specific* claim. The receipt is owed per claim, not per turn —
so the tool count now only enriches the block message and never grants a pass.
The regression is pinned as selftest case `t3-tools-ran-no-receipt`.

Install (user scope):
1. `cp hooks/receipt-law-stop-gate.sh ~/.claude/hooks/` and `chmod +x` it.
2. Merge into `~/.claude/settings.json`:
   `{"hooks":{"Stop":[{"hooks":[{"type":"command","command":"bash ~/.claude/hooks/receipt-law-stop-gate.sh","timeout":10}]}]}}`
3. Verify: `bash hooks/selftest-receipt-law.sh` (expects 10/10 PASS), then
   observe a real turn that claims an unreceipted inability.

Pipe-tested 10/10 PASS 2026-08-12, twice consecutively (repo copy), plus a
fixture built from the **verbatim INC-9 report text** including its three real
`WebSearch` calls: v1 → BLOCK, corrected v2 → ALLOW.

**Live-fired 2026-08-12** in an isolated `CLAUDE_CONFIG_DIR` with the hook wired
as a real Stop hook, `claude-sonnet-5`, 3 sessions:

- Ordinary turn ("default PostgreSQL port") — **not interrupted**, 6s, one-line
  answer. The deployment risk for a blocking Stop hook is that it degrades every
  turn it touches; it did not.
- INC-9-shaped turn (classify 10 packages by licence, tally, ship/no-ship, web
  tools disallowed) — run twice. **Gate stayed silent both times, correctly**:
  the model volunteered its own receipt ("from training knowledge, not verified
  live", "no web access", "run `license-checker` for a verified report"), which
  is precisely the ATTEMPTED-FAILED shape the rule asks for.
- **Zero false fires** across all live runs, verified against a clean `TMPDIR`
  (0 sentinels written), not against leftover state from the fixture tests.

Honest limit on this evidence: **no live BLOCK was observed**, because no live
run produced an unreceipted inability claim — two attempts, both self-corrected.
So the no-false-positive property is EVIDENCE from live sessions; the blocking
path remains proven by fixture only, including against the verbatim incident
text. A/B still owed (`experiments/hypothesis-2026-08-11-gap-provenance.md`, H8).

**Surface limit, stated plainly:** Claude Code only. claude.ai has no hook
layer, and INC-9 happened on claude.ai — so on that surface the receipt law is
carried by the custom-instructions block alone
(`instructions/claude-ai-custom-instructions.md`, standing principles). This
hook hardens the surface where the incident did *not* happen. That is worth
having and is not a substitute for the paste.
