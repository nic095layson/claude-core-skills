# Lessons Ledger — claude-core-skills

Project ledger per the lessons-ledger governor. Entries: symptom → root cause →
evidence → status. An entry without evidence is a rumor and does not belong here.

### INC-1 — Cloud GitHub grant assumed live in a local session

- Date: 2026-07-11 (discovered and worked around the same day).
- Symptom: owner had granted Claude GitHub access in claude.ai settings and had
  used it the previous day; a local Claude Code session on his Mac could not see
  or clone any private repo, and repeated "you already have permission"
  expectations failed.
- Root cause: integration grants made on claude.ai live on Anthropic's servers
  and are scoped to cloud sessions. They never reach a local machine, which
  needs its own credentials. The local Mac had none: no `~/.gitconfig`, no SSH
  keys, no `gh` CLI.
- Evidence: `gh auth status` before fix → "not logged into any GitHub hosts";
  `ls ~/.ssh` empty; `git config --global --list` empty. After installing gh
  v2.96.0 and device-flow login: authenticated as nic095layson, private repos
  listable. (Session of 2026-07-11.)
- Status: FIXED for the primary machine (gh installed at `~/.local/bin/gh`,
  authed via keyring, `gh auth setup-git` done). The general rule is codified in
  live-state-truth ("Environment boundaries") and debugging-playbook §5.
- Lesson: capabilities are per-environment facts — enumerate them live in the
  session that needs them; never infer access here from access somewhere else.

### INC-2 — Headless scratchpad state confounds file-referencing trigger evals

- Date: 2026-07-11 (research-methodology A/B session).
- Symptom: scope-fence id1 and lessons-ledger id1 fired 2/2 in Phase 1 but
  0/2–1/2 when re-run this session; the "regression" looked like it was caused by
  a reword.
- Root cause: Phase 1 ran in a scratchpad holding leftover probe files; this
  session's harness cleans the scratchpad to empty. Prompts that name a concrete
  symbol in an absent file (id1 "parseConfig() … in that file") make the model
  fixate on the missing file / empty dir and never reach the governed behavior —
  independent of OLD vs NEW wording.
- Evidence: same-condition OLD re-baselines — scope-fence id1 1/2 (empty) / 0/2
  (seeded) vs Phase 1 2/2; lessons-ledger id1 0/2 vs Phase 1 2/2. Controlled
  OLD-vs-NEW at fixed scratchpad state showed no real regression.
  (`results/2026-07-11/RESULTS-AB.md`.)
- Status: CONTROLLED — OLD was re-baselined in identical conditions for every
  governor before comparing; cross-condition Phase 1 numbers are not
  same-surface for file-referencing prompts.
- Lesson: hold scratchpad state fixed across OLD and NEW; a trigger prompt that
  names an absent artifact tests file-discovery, not the governor. Prefer inline
  artifacts or abstract situation descriptions.

### DEAD-1 — scope-fence "restrain adjacent work while editing concrete code" is unfireable in headless via wording

- Date: 2026-07-11 (research-methodology A/B session). Status: **ABANDONED**
  (description lever exhausted; escalated to architecture-contract).
- Symptom: scope-fence NEW1 fixed the abstract-description should-fire prompts
  (id2, id3: 0/2→2/2) but the id1-class ("fix this code, and while you're in it
  notice adjacent work") never fired — governor stuck at 4/6, below the ≥83% gate.
- Root cause: when handed concrete code the model just codes and handles adjacent
  work inline; it does not pause to consult a governance skill, regardless of
  description wording.
- Evidence: id1-class 0/2 under BOTH OLD and NEW1 across 4 framings — id1
  absent-file (empty & seeded), id6 inline-trivial, id7 inline-named-work (a test
  design error — named work is inside the fence), id8 inline-dangled-nontrivial.
  (`results/2026-07-11/RESULTS-AB.md`; `experiments/hypothesis-scope-fence.md`.)
- Lesson: don't re-run scope-fence wording experiments against inline-code
  should-fire prompts expecting a load; this is a triggering ceiling, not a
  wording bug. Personal copy reverted to OLD. NEW1 retained in experiments/ as an
  owner-adoptable regression-free improvement.

### DEAD-2 — lessons-ledger append-on-diagnosis plateaus ~80% under wording, below the gate

- Date: 2026-07-11 (research-methodology A/B session). Status: **ABANDONED**
  (2 honest rewords, budget exhausted; escalated to architecture-contract).
- Symptom: two rewords lifted headless should-fire from 17% to 78% (NEW1) and 80%
  (NEW2, N=5) with zero should-not regression, but neither reached the ≥83% gate.
- Root cause: residual run-to-run noise — the model often responds
  conversationally or offers to log ("want me to jot a ledger entry?") without
  invoking the Skill tool, even on clear costly-diagnosis recounts.
- Evidence: NEW2 N=5 → id1 4/5, id2 3/5, id3 5/5 = 12/15 (80%). The N=3 read
  (8/9) was small-sample optimism; the pre-committed N=5 escalation exposed it.
  (`results/2026-07-11/RESULTS-AB.md`; `experiments/hypothesis-lessons-ledger.md`.)
- Lesson: the append-on-diagnosis trigger has a ~80% wording ceiling in headless;
  don't keep iterating descriptions. Personal copy reverted to OLD; NEW2 retained
  in experiments/ as an owner-adoptable improvement. Candidate next lever:
  mechanical enforcement (hooks), not wording.

### INC-3 — Accepted rewords exceed the 1024-char description limit (claude.ai upload risk)

- Date: 2026-07-11 (research-methodology A/B session). Status: **RESOLVED same day**
  — all five trimmed ≤1000 chars and re-run; rates held, zero should-not regressions
  (`experiments/hypothesis-2026-07-11-length-compliance.md`). Lint gained no length
  check yet (still suggested). Bonus finding: the shorter scope-fence description
  fired its id1 3/5 vs 0/2 at over-length — less dilution triggers more reliably.
- Symptom: the three accepted rewords pushed their `description` field over the
  documented 1024-char Agent-Skills limit — plan-gate 1322, live-state-truth 1156,
  adversarial-verify 1144 (OLD were 965 / 863 / 827).
- Root cause: adding trigger-surface examples lengthens the description; no repo
  lint checks length, so it passed unnoticed until the adversarial-verify pass
  measured chars.
- Evidence: char counts measured this session; the three nonetheless loaded and
  FIRED in Claude Code headless (6/6, 9/9, 9/9), so the limit is not enforced on
  that surface. (`results/2026-07-11/RESULTS-AB.md`.)
- Lesson: Claude Code headless tolerates >1024-char descriptions, but claude.ai's
  upload validator may not — re-uploading these three could silently fail to
  register (the founding-incident class). Do NOT trim-to-fit without re-running
  the A/B (shipping untested wording violates research-methodology). Suggest adding
  a description-length check to the lint. Owner decision pending.

### INC — Phase 2 "without-library" arm was contaminated by project-scope skills

- Date: 2026-07-11 (Phase 2 behavioral evals). Status: **RESOLVED same day** —
  re-ran all 40 sessions with cwd outside the repo & `~/.claude`; without-arm then
  fired 0/20 (`results/2026-07-11/phase2/RESULTS-PHASE2.md`, "v2").
- Symptom: the A/B "WITHOUT governors" arm moved the five personal-scope governors
  out of `~/.claude/skills/`, but plan-gate still fired a full gate block in the
  without-arm.
- Root cause: the run directories lived *inside* this repo, and the repo ships the
  governors at **project scope** (`.claude/skills/`). Project-scope skills load from
  cwd/ancestors regardless of personal-scope state, so "without" still had all five
  (plus the repo's `CLAUDE.md` and all 13 skills as context).
- Evidence: `transcripts/plan-gate__pg1__without__r1.jsonl` — `SKILLS_FIRED:
  ['plan-gate']` with cwd under the repo tree; after moving RUNROOT to
  `/private/tmp/phase2v2_f46b83c8`, `transcripts_v2/*__without__*` fired 0/20.
- Lesson: A/B skill tests must run with cwd **outside any repo that ships the skills
  at project scope** (and outside `~/.claude`, whose name matches `.claude`-ancestor
  discovery). Phase 1 got this right (scratchpad outside the repo); Phase 2's first
  pass regressed it. When moving personal-scope out to test "without", verify the
  arm is truly empty by asserting 0 skill-fires, not just that the dir was moved.

### INC — Concurrent worker / summarized-context collision on ~/.claude/skills

- Date: 2026-07-11 (Phase 2). Status: noted; no harm (byte-identical restore verified).
- Symptom: mid-run, helper files this session did not author appeared
  (`grade_workflow.js`, `extract_traces.py`, `before_full_manifest.txt`), the
  with-arm transcript count jumped past a crash point, and `ps` showed a
  `without_arm.sh` actively moving the governors out of `~/.claude/skills/` while
  this session was still setting up.
- Root cause: an earlier portion of this same long session was summarized out of
  context; its background jobs (a resumed with-arm fill, a launched without-arm) kept
  running and kept writing files — indistinguishable at first from a second worker.
  Either way: two executions manipulating the same global `~/.claude/skills/`.
- Evidence: all tasks under one job dir (`f46b83c8`); helper files matched this
  session's methodology exactly; `ps` showed `bash without_arm.sh` (PID 68356) with
  the governors already relocated to `~/.claude/skills_phase2_backup/`.
- Lesson: moving a global, shared resource (`~/.claude/skills/`) is unsafe when a
  concurrent/backgrounded execution may also move it — races can lose the user's
  install. Do not launch a competing governor-move; let the trap-guarded restore of
  the in-flight one complete, verify byte-identical against a pre-recorded baseline,
  then proceed. A pre-recorded sha256 baseline + trap-guarded restore made the
  collision harmless here.

### INC-4 — Two concurrent Phase 2 jobs swapping ~/.claude/skills contaminated each other's arms

- Date: 2026-07-11 (Phase 2 behavioral evals). Status: **RESOLVED via reconciliation** —
  the clean dataset was identified and graded twice; the contaminated arm was excluded.
  Sharpens the prior (hedged) concurrent-worker entry above with cross-job evidence.
- Symptom: two out-of-repo Phase 2 runs of the *same* governors disagreed on with-arm
  governor firing — job `f46b83c8` fired **20/20**, job `594d5c68` fired **5/20** — for
  a nominally identical condition (personal-scope governors present, cwd outside repo).
- Root cause (**probable**, stated as probable): the two jobs ran genuinely concurrently
  and **both mutated the single shared `~/.claude/skills/`** to build their "without"
  arms. Job `f46b83c8`'s without-arm move-out emptied `~/.claude/skills/` *partway through*
  job `594d5c68`'s with-arm run, so the latter's later runs executed with no governors
  installed and could not fire.
- Evidence: the two are distinct jobs — distinct job dirs `594d5c68` ≠ `f46b83c8` (not one
  session's own backgrounded work, which the earlier entry could not rule out). Firing in
  `594d5c68`'s with-arm died *in run order*: plan-gate 4/4 (early) → adversarial-verify
  1/4 → live-state-truth 0/4 → scope-fence 0/4 → lessons-ledger 0/4 (all later) — the
  signature of a move-out window opening mid-run. `f46b83c8`'s without-arm fired 0/20
  (its own arms were internally consistent). One job's file ops also deleted the other's
  in-progress `transcripts/` mid-write (an ll2 run died with `FileNotFoundError`).
- Status: `f46b83c8`'s `transcripts_v2/` adopted as authoritative (blind-regraded here,
  cell-for-cell agreement); `594d5c68`'s 5/20 with-arm excluded from rates, retained as
  evidence (`results/2026-07-11/phase2/RECONCILED-PHASE2.md`).
- Lesson: an experiment that mutates shared global state (`~/.claude/skills/`) must hold a
  **lockfile** or run against an **isolated config dir** (`CLAUDE_CONFIG_DIR`) — never
  toggle the user's live install while another job might. **Concurrent campaign sessions in
  one repo are forbidden** (now codified in governance-adoption-campaign's protocol). A
  20/20-vs-5/20 firing gap for the same condition is a contamination smell, not real
  triggering variance — reconcile before believing either number.

### INC-5 — Deliverable-only inspection inverted the scope-fence verdict; the trace corrected it

- Date: 2026-07-15 (first cross-model path-consistency run, Sonnet vs Opus, claude.ai).
  Status: **RESOLVED same run** — the PATH TRACE §6 was captured and overturned the
  artifact-only read (`results/2026-07-15/sonnet-opus-path-comparison.md`).
- Symptom: reading the two hardened migration scripts alone, both *looked* like each model
  had silently absorbed the dangled logging/dead-code cleanup into a rewrite — i.e. a
  `scope-fence` **miss** (fixed adjacent work instead of flagging it). An interim comparison
  was written on that basis.
- Root cause: both models responded to "make it production-ready" with a **full rewrite**, so
  consistent logging and the absence of dead code are *byproducts of writing fresh code*, not
  a cleanup task taken on. The actual scope decision (flag vs fix) lived in the chat prose /
  trace, not in the delivered `.sh`. Artifact inspection cannot see a decision that leaves no
  artifact trace.
- Evidence: §6 of both traces — Opus "logging + dead code: flagged-only; the `print()` line's
  runtime breakage counted as in-scope blocker #1"; Sonnet "logging + dead-code block:
  flagged-only; `print()` fixed not flagged since it's a parse-breaking bug, not a style
  choice." Both drew the identical in-scope-bug vs out-of-scope-cleanup line. Both also passed
  the over-fire control (answered "5432" with no ceremony).
- Lesson: in path-consistency runs, **never grade a governor signature from the deliverable
  alone** — the deliverable is Section 8, and scope/plan/verify decisions often leave no mark
  in it. Require the PATH TRACE §4–7 and reconcile self-report against artifact (method §3
  step 11). Codified in `evals/cross-model-path-consistency-METHOD.md` L1.
