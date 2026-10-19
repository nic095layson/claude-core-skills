# Hooks — mechanical trigger aids

> **Status 2026-10-13 — wired at project scope.** `.claude/settings.json` in this
> repository now runs all seven hooks (`governance-trigger.py` on UserPromptSubmit;
> `governance-enforce.py` and `receipt-law-stop-gate.sh` on Stop; the two first-write
> reminders on PreToolUse; `session-doctrine.sh` on SessionStart `compact|resume`),
> through `$CLAUDE_PROJECT_DIR`. Cloud sessions started inside this one repository
> read that file; the reminders and the trigger were observed firing in the authoring
> web session within minutes. The trigger and the Stop gate share one classifier,
> `govclass.py`, pinned by `selftest-governance-classify.py` (27 checks at first, 30 since the
> 2026-10-13 gate fix for mid-turn notifications, ledger INC-2026-10-13-02; including the
> four owner messages of the 2026-10-12 incident). Live A/B, 8 headless runs:
> pack off 0/2 governor loads, pack on 4/4, trivia 0/2 with no block —
> `results/2026-10-13/gauntlet-fortification/`. The status lines below each hook are
> the history that led here and are left as written; where they say "NOT installed",
> read "installed at project scope 2026-10-13". Multi-repository cloud sessions do not
> read repo hooks; for them the same seven hooks ship as the plugin
> `plugin/core-governance/` (built later on 2026-10-13, enabled on the claude.ai account
> rather than from repo settings — the settings keys do not load in cloud sessions; see
> install-and-surfaces Runbook 4, steps 6–7). The plugin's `scripts/` are byte-identical
> copies of this directory; the guard fails on drift. Ledger: INC-2026-10-13-01.

## session-doctrine.sh (shipped 2026-10-13)

SessionStart hook for the compaction and resume boundaries. On `compact` it deletes
the two first-write reminder sentinels for the session (re-arming them: in a
three-week session they had spent themselves on day one) and injects the
post-compaction protocol — re-attached governor text does not count as loaded,
disputed results stay disputed and are listed before continuing, in-flight method
choices are restated. On `resume` it injects one line: governors are loaded per
task, not per session. Silent on `startup` and `clear` (the project `CLAUDE.md`
carries the doctrine there, and is re-read after compaction). Advisory, fail-open.
Pipe-tested 2026-10-13 (compact → context + 0 sentinels; startup → empty; garbage
input → exit 0). Not yet observed across a real compaction.

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

## redteam-band-reminder.sh (shipped 2026-10-19, UNMEASURED)

The lever for the red-team skill's rule 3 (two error bars or none; ledger
INC-2026-10-19-01: a report said ±0.4 where one hand-set constant moved the figure
by +3.4 / −2.3). A PreToolUse hook on Write|Edit|NotebookEdit: when the content
being written quotes a figure with a sampling error (`±` or `+/-` between two
numbers) and no band word (FRAGILE, SENSITIVE, ROBUST, "structural band"), it
injects one line asking for the structural band beside the figure by constant
name, or an "uncalibrated, decision D-n" statement, or nothing if the figure is
measured from data. Once per session (sentinel in $TMPDIR keyed by session_id).
Advisory, never blocking: a hook cannot tell a modelled figure from a measured
one, and a block on every number would violate the anti-ceremony invariant
(architecture-contract, invariant 5). A write with no ± is silent; a write that
already quotes a band is silent. Parses its input with python3, not `/usr/bin/jq`
(the absolute-path defect recorded for the two older reminders, D-GF-8).

Install (user scope):
1. `cp hooks/redteam-band-reminder.sh ~/.claude/hooks/` and `chmod +x` it.
2. Merge into `~/.claude/settings.json`:
   `{"hooks":{"PreToolUse":[{"matcher":"Edit|Write|NotebookEdit","hooks":[{"type":"command","command":"bash ~/.claude/hooks/redteam-band-reminder.sh","timeout":10}]}]}}`
   (coexists with the two first-write reminders on the same event; each fires at
   most once per session and their messages are distinct). In a project that
   carries the enforcement pack (`.claude/settings.json`, PR 24), add the same
   entry beside the two reminders; the plugin twin needs a version bump — both
   are owner decisions, not done here.
3. Verify: `bash hooks/selftest-redteam-band-reminder.sh` (expects 7/7), then
   observe on a real session's first write of a ± figure.

Red-first: the self-test was written and run before the hook existed (0/7, "hook
missing"), then 7/7 after; two cases were added after an independent review (a
capitalised "Structural band:" must be silent — it was not, fixed; a lower-case
"robust" in prose is not a tier token and still gets the reminder — documented,
not changed), 8/9 before that fix, 9/9 after, twice
(`results/2026-10-19/red-team-hook/`). The band words are the upper-case tier
tokens FRAGILE, SENSITIVE, ROBUST and the phrase "structural band" in any case.
Live, hook wired in a scratch project, three runs, N=1 each: a conversational
write with no figure → no reminder; a one-line status file quoting a ± figure
verbatim → one reminder, after which the session explained the ask and offered
the red-team skill; a report prompt describing a model with hand-set constants →
no reminder, because the session loaded red-team on its own and wrote a FRAGILE
sentence into the report (the hook saw a band word and stayed silent — it cannot
tell a band read from a sweep record from one the session invented; that is the
bands check's job, and the invented band would fail it). The A/B is
pre-registered and owed: `experiments/hypothesis-2026-10-19-redteam-band-hook.md`.

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

## receipt-law-stop-gate.sh (proposed 2026-08-12; installed and live-verified 2026-08-26)

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

**Update 2026-08-26 — installed, and the first live BLOCK observed.** The hook
is installed at user scope on the primary machine and registered as a Stop hook
in `~/.claude/settings.json` (settings mtime 2026-08-19, observed 2026-08-26).
In a real session on 2026-08-26 it blocked a turn that wrote "couldn't check"
about the claude.ai settings box with no attempt named: the block message cited
the turn's 9 lookups, the corrected turn shipped a proper receipt (what was
available and why none of it could reach the box), and the gate passed it. The
blocking path is now live-proven, not fixture-only; the paragraph above stands
as the honest record of what was known before this firing. Selftest re-run
2026-08-26: 10/10, twice. Evidence: `results/2026-08-26/system-integrity/`.
The A/B (H8) remains owed — one live block is an existence proof, not a rate.

**Surface limit, stated plainly:** Claude Code only. claude.ai has no hook
layer, and INC-9 happened on claude.ai — so on that surface the receipt law is
carried by the custom-instructions block alone
(`instructions/claude-ai-custom-instructions.md`, standing principles). This
hook hardens the surface where the incident did *not* happen. That is worth
having and is not a substitute for the paste.

## governance-trigger.py + governance-enforce.py (RESCUED 2026-08-12, validated 2026-07-15, NOT installed)

**The strongest enforcement artifact this repo has, and it was stranded for a
month.** A `Stop` hook pair that answers the question the prose layer cannot:
*did a governor actually load on a turn that needed one?* If the turn is
governed-class and no governor Skill loaded, it **blocks and forces the load**.

Validated 2026-07-15 (pre-registered OFF-vs-ENFORCE A/B, isolated sessions):
**every governed case loads adversarial-verify 3/3, including the verbatim
incident prompt that scored 0/3 unenforced** — both should-not cases stayed
silent 0/3, confabulation 0. Mechanism confirmed in the transcripts: model skips
→ `GOV-ENFORCE` block → loads. Full record: `results/2026-07-15/phase2b_enforce_ab/`.

Two design choices its own A/B proved necessary, and both are load-bearing:
- **Enforce, don't request.** Injecting "load the skill" works; asking the model
  to *emit a receipt* that it loaded produces confabulated receipts (INC-13 —
  4 confabulations vs 0). Never ask a model to certify its own compliance.
- **A classifier anti-ceremony gate.** `governance-trigger.py` classifies the
  prompt first, so trivia is never injected into. Without it the hook would
  violate invariant 5 on every casual message.

Recovered from `claude/rivian-stock-analysis-h5y46x` (unmerged, INC-11 route).
Both compile clean (`python3 -m py_compile`, 2026-08-12). **Not installed and not
re-validated against the current CLI** — the A/B is 4 weeks old and `claude` has
moved (v2.1.228 here). Re-run `results/2026-07-15/phase2b_enforce_ab/` before
trusting the 3/3 on today's version.

Relationship to `receipt-law-stop-gate.sh`: complementary, not competing. This
pair enforces **that a governor loads**; that one enforces **that a claim of
inability carries a receipt**. Both are `Stop` hooks and can coexist.

**Surface limit:** Claude Code only. claude.ai has no hook layer.
