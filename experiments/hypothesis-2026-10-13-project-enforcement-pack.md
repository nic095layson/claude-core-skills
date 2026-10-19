# Hypothesis: a project-scope enforcement pack forces governor loads on the incident's own message

**Status:** pre-registered 2026-10-13 BEFORE any live run. Written in the session that builds the
pack (`results/2026-10-13/gauntlet-fortification/`). Incident: `.claude/LESSONS.md`
INC-2026-10-13-01 (kit after-report `after-report-2026-10-13-scope-fence.md`).

## Observation that motivates it

A three-week Claude Code cloud session on the kit loaded **zero** governors (census: 4 Skill-tool
loads since 2026-09-23, none plan-gate / scope-fence / adversarial-verify / gauntlet; recounted
2026-10-13 from `out/timeline.json`). Nothing could have loaded them: `~/.claude/CLAUDE.md` is absent
on the cloud surface, the kit has no `.claude/` directory, and this library's hooks were wired
nowhere. The validated enforcement pair (`governance-trigger.py` + `governance-enforce.py`,
3/3 vs 0/3 on 2026-07-15) existed only as files.

A pre-run fixture test (2026-10-13, this session) showed the 2026-07-15 classifier would have stayed
**silent on 3 of the 4 owner messages** of the incident and **fired on "what time zone is the draft
in?"** (`draft (a|the|me)?` matched "draft in").

## The change (three variables, tested separately)

V1 — **classifier** (`hooks/govclass.py`, shared by both hooks): a `dispute` class (the owner
questions or disputes the work's method/data/result → adversarial-verify + scope-fence), an advisory
`requirement` class ("X is critical" → scope-fence note, never enforced), and the `draft` pattern
narrowed to `draft (a|an|the|me|us|this|some|one)\b`.

V2 — **wiring**: `.claude/settings.json` at project scope (travels with the repo, so cloud sessions
of the repo run it), hooks referenced through `$CLAUDE_PROJECT_DIR`.

V3 — **compaction/resume hook** (`hooks/session-doctrine.sh`): post-compaction protocol injected and
the once-per-session reminders re-armed.

## Pre-registered predictions

**P1 (fixture, mechanical).** `python3 hooks/selftest-governance-classify.py` passes every case:
the 4 incident messages classify as governed (23:41 and 23:51 → adversarial-verify + scope-fence;
23:42 → scope-fence advisory only; 23:54 → adversarial-verify + scope-fence + plan-gate); the 7
should-stay-silent cases (including "draft in", "why is the sky blue?", "who did the Lakers draft
last year?") classify as nothing; the Stop gate blocks on the unloaded 23:41 message (string and
list content), allows on a loaded synced copy, allows on requirement-only and trivia, and allows
when `stop_hook_active` is set.

**P2 (live, headless `claude -p` from this cloud container, default model, fresh scratch project
per run, N=2 per arm).** Prompt = the owner's 23:41 message verbatim.
- OFF arm (no `.claude/settings.json`): governor Skill loads **0/2**.
- ON arm (pack wired): governor Skill loads **2/2** (a Skill tool_use naming plan-gate, scope-fence
  or adversarial-verify appears in the stream after the prompt). At least one run shows the
  `GOV-ENFORCE` block text if the model did not load on the trigger alone.
- ON arm, trivia ("what's 15% of 80?" and "what time zone is the draft in?"): governor loads
  **0/2**, no `GOV-ENFORCE` block, and the answer is a direct one-liner. **Any over-fire blocks
  acceptance** (architecture-contract invariant 3 and 5).

**P3 (pipe tests).** `session-doctrine.sh` emits SessionStart `additionalContext` on `compact` and
`resume`, nothing on `startup`, and removes both reminder sentinels on `compact`. The two
first-write reminders and the receipt-law gate still pass their own pipe tests after wiring.

**What is NOT measured here (stated so it is not read as measured):** behavioral value of the three
governor body edits made the same day (plan-gate §3/§5 method-parameter rule, scope-fence §2
question-gets-an-assessment and rule 4 requirement clause, gauntlet re-attached-is-not-loaded).
Descriptions are byte-identical to `HEAD`, so trigger rates are unaffected by construction; the body
edits are UNMEASURED candidates until a behavioral A/B with a data-analysis fixture runs. Also not
measured: whether the web-session harness (as opposed to `claude -p` inside the same container)
runs project-scope hooks — see the report's docs evidence and bounds.

## Fenced (do not redo)

- Asking the model to emit a governance receipt (INC-13: 4 confabulations vs 0). The trigger asks
  for a LOAD; the gate checks the transcript for the load.
- Widening governor descriptions to catch this class (DEAD-3: no effect on the analysis class).
- A blocking hook on every file write (invariant 5).

---

## OUTCOME (2026-10-13, same session; full record in `results/2026-10-13/gauntlet-fortification/`)

- **P1 fixture: HELD** — 27/27 after two additions during the work (a harness-notification case
  and the isMeta transcript shape, both from defects found live). First version 23/24 — the
  `migrat\w*` pattern matched the noun "migration" in a review prompt; narrowed to verb forms.
- **P2 live, 8 headless runs, 1.15 USD:** OFF **0/2** loads (predicted 0/2); ON incident message
  **4/4** loads of adversarial-verify + scope-fence, all on the trigger alone (predicted 2/2 in
  N=2; run twice because the first batch exposed a gate defect); trivia ON **0/2** loads, **0**
  blocks, direct answers (predicted 0/2). **Defect found by the run:** the first gate build
  blocked two compliant runs — it took `isMeta` user entries (loaded skill text, hook feedback)
  as the owner's prompt. Fixed, pinned, re-run: on-3 and on-4 **0** blocks. A legitimate live
  block was not observed (the trigger sufficed every time); the blocking logic is fixture-proven,
  and the harness's handling of `decision: "block"` was observed in the two false firings.
- **P3 pipe tests: HELD** — `session-doctrine.sh` emits on `compact` and `resume`, silent on
  `startup`, removes both sentinels; reminders and receipt-law gate 10/10 unchanged.
- **Unplanned observation:** the project hooks fired in the *authoring* web session itself within
  minutes of `.claude/settings.json` being written (first-write reminders on an Edit; the trigger
  on a background-task notification, which exposed and fixed an over-fire on harness text).
- **Not measured, as pre-registered:** the governor body edits; multi-repository cloud sessions
  (documentation says repo hooks are not read there; `UNVERIFIABLE` from a single-repo session).
- **Disposition:** V1 + V2 + V3 ACCEPTED for single-repository sessions (every prediction held,
  one regression found and cleared before acceptance). Multi-repo coverage stays OPEN (ledger
  INC-2026-10-13-01).
