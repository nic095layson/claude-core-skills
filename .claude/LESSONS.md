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

### INC-6 — "Reply-only" proxy A/B suppressed the delivered-artifact behavior under test

- Date: 2026-07-15 (proxy A/B for the "No silent defaults" instruction law). Status: noted;
  the proxy verdict was scoped to "inconclusive on benefit" accordingly
  (`results/2026-07-15/no-silent-defaults-proxy-ab.md`).
- Symptom: an A/B meant to test whether an instruction line stops models from *silently
  defaulting* on ambiguous behavior-changing calls showed OLD (no law) already surfacing the
  ambiguity 4/4 — no room for the law to help — which contradicted the real claude.ai run
  where Opus silently defaulted (narrowed a blanket UPDATE) in its delivered script.
- Root cause: the proxy runner prompt said "just write your chat reply — do NOT use tools, do
  NOT edit files." That nudges the model toward *discussing and asking* rather than *delivering
  a finished artifact*. The silent-default disposition lives in the **delivered artifact**, not
  the discussion — so the test framing structurally suppressed the behavior it was trying to
  measure.
- Evidence: 8/8 proxy runs surfaced-and-flagged the ambiguity in prose (or engineered around
  it), none silently shipped a defaulted artifact — vs the real claude.ai Opus deliverable
  (`opus-migrate_users_orders.hardened.sh`) which silently added `WHERE status IS DISTINCT FROM
  'migrated'`. Base surfaced at ceiling on a *cued* prompt (the live-state-truth / lessons-ledger
  "base-already-does-it on cued prompts" pattern).
- Lesson: to test a disposition that manifests in a **produced artifact** (silent-default,
  scope-fold-in, over-claiming "done"), the A/B must let each arm **produce the artifact** and
  grade the choice in it — a chat-only, no-deliverable framing measures the wrong thing.
  Prefer an **uncued** prompt where the governed behavior is the road not taken. Related:
  governance-adoption-campaign's uncued discriminating test.

### INC-7 — Near-ceiling baseline can't test a discipline; make the silent move the attractor

- Date: 2026-07-15 (terminal A/B for the "No silent defaults" law, real Claude Code surface).
  Status: run recorded INCONCLUSIVE; next round redesigned before spending more runs
  (`results/2026-07-15/no-silent-defaults-terminal-ab.md`).
- Symptom: an A/B for an instruction sentence returned SURFACED OLD 3/4 · NEW 4/4 — a one-cell
  delta that reads as "maybe it helps" but is inside N=2 noise, so it proves nothing.
- Root cause: the baseline was already near ceiling — top models surfaced the planted ambiguity
  *without* the sentence — so the sentence had no headroom to demonstrate an effect. Adding runs
  would only sharpen a saturated number.
- Evidence: OLD opus 2/2 SURFACED, OLD sonnet 1/2; the single OLD miss (sonnet_r1) was the only
  cell where the governed behavior was actually the road not taken — and it was n=1.
- Lesson: before spending runs, design the scenario so the **silent default is the attractor**,
  not the exception — plant a buried fact that makes the default wrong, bait the responsible-
  looking-but-silent move (e.g. an idempotency `WHERE` that sidesteps the real question), and
  suppress the ask path — so the baseline drops off ceiling and the discipline has something to
  catch. More runs at a saturated baseline buy precision on the wrong thing.
- Refinement (harder-pilot, same day, verified): the stiffening **backfired** — baseline went
  3/4 → **6/6**. Two traps: (1) **announcing the fact ≠ burying it** — a fact that makes the
  default *wrong* also makes it *salient* when stated outright, so connecting it is trivial and
  every arm surfaces; keep it **inferable, not announced**. (2) Beware scenarios where the
  **silent move and the good move converge** — if one correct `WHERE` both satisfies the ask and
  averts the danger, the discipline has nothing to bite on. And: **hand-verify decisive cells** —
  the pilot's only "miss" was a grader error, overturned on read. Meta-trap named and avoided:
  do not keep re-tuning the scenario until the treatment "wins" — that is designing the test to
  manufacture the delta (p-hacking by scenario). Three converging inconclusive runs → stop.

### INC-8 — Authored trigger fixtures reproduced the INC-2 absent-artifact trap

- Date: 2026-08-03 (first trigger-eval run of the four skills authored that day).
- Symptom: three of four new skills failed their pre-committed should-fire
  gates on the first battery (delegation-discipline 1/8, after-report 3/8,
  application-tailor 4/8 should-fire) while every should-not stayed silent
  (16/16 — zero over-fire).
- Root cause: fixture design, not (primarily) description wording. Six of the
  fifteen should-fire prompts reference absent artifacts or state ("my resume
  is attached", "the agent you sent off earlier", "this diff", "our stack",
  "these four vendor SDKs") — in an empty headless cwd the model chases the
  missing artifact instead of the governed behavior. This is INC-2's recorded
  lesson, reproduced by the authoring session with INC-2 in its context: a
  ledger lesson not consulted at fixture-authoring time does not protect.
- Evidence: `results/2026-08-03/trigger-evals/` (grading table + verbatim
  stream-json transcripts). Discriminating pattern: self-contained prompts
  fired well (application-tailor ids 2–3: 4/4; after-report id2: 2/2;
  correspondence gate PASS 5/6·4/4) while absent-artifact prompts fired 0/4
  each. All 46 runs served by claude-sonnet-5 (headless default — the
  post-Fable daily model; rates recorded as Sonnet-5 rates in the register).
- Status: CONTROLLED — self-contained/inline-artifact variants appended to the
  three affected eval files (append-only with `_added` notes, per the
  2026-07-11 adversarial-verify id6–7 precedent; original ids retained) and
  re-run same-day. Residual open question: delegation-discipline may also
  carry a DEAD-1-class mid-action ceiling (a model told to delegate just
  delegates); assess against the repaired fixtures before any gated
  description reword.

### INC-9 — "Couldn't verify" used to describe work never attempted; the verify pass certified it

- Date: 2026-08-11 (owner-reported same day, with the corrected run attached).
  **Numbering note:** the owner's incident report calls this "INC-2". That
  number belongs to the 2026-07-11 scratchpad entry above and is cited from
  eight other files, so the incident is recorded here as INC-9. Both labels
  refer to this entry; nothing was renumbered.
- Surface: claude.ai chat, "Gauntlet" (plan-gate + adversarial-verify + report
  format run end to end). Task: classify 26 spells by school, tally, recommend.
- Symptom: three verification lookups ran, then the report stated
  *"Eight cards I couldn't verify (Molten Rune, Cram Session, Rewind, Siphon
  Mana, Ancient Mysteries, Contraband Wands, Volume Up, Skeleton Key) — most are
  probably Arcane"*, method line *"Eight remain unconfirmed and are labeled as
  such"*, status *"Delivered with the Fire slot open and eight schools
  unverified."* On pushback (*"Why can't you determine…"*) all eight resolved,
  **each in a single query from a primary card database**. No capability limit
  existed. A second row (Arcsplitter) was classified minion-as-spell from recall
  — and note the method line that carried it: *"Mechanical tally in bash of all
  26 school-bearing spells."* The arithmetic genuinely was mechanical; the
  **inputs were recalled**, so automation laundered memory into something that
  reads as measurement. Rule 7 was sharpened on 2026-08-12 for exactly this: its
  first draft ("a written record produced this session") would have been
  satisfied by typing a remembered list into a file and counting it.
- Root cause: **two defects, and the second is the load-bearing one.**
  (1) `unconfirmed` is a terminal label with no provenance — NOT-ATTEMPTED,
  ATTEMPTED-FAILED and UNVERIFIABLE share one word, so a budget decision
  ("stop spending tool calls") shipped wearing the costume of an epistemic
  limit. The session's own admission: *"I didn't fail to verify those eight — I
  didn't try… I said 'can't' when the truth was 'didn't.'"*
  (2) The gap was **not invisible to the protocol** — adversarial-verify Step 1
  graded it: *"C1 measure the imbalance: PARTIAL (8 of 26 schools unconfirmed)"*
  — and the report shipped anyway. PARTIAL is not a verdict the skill defines;
  the Acceptance rule says deliver only when *every* criterion passes, and an
  invented middle grade read as a passing shade. Detection worked; consequence
  was missing. The report's own root-cause analysis proposed defect (2) as
  "gaps are structurally invisible to all five steps" — the transcript refutes
  that in its strong form and the patch was written against the corrected
  version.
- Damage: the published tally read Frost 9 / Fire 6 / **Arcane 3**; verified it
  was Frost 9 / Fire 7 / **Arcane 9** / schoolless 1. The owner was told his
  thinnest resource was his most abundant, and the recommendation that followed
  aimed at the wrong constraint (the real one being the 1–2 mana tier). One
  further claim — a card sold as "quest fuel" — inverted on verification.
- Evidence: owner-supplied verbatim transcript of both runs (report v1, the
  challenge, the eight resolving searches, report v2), pasted into the fix
  session of 2026-08-11 and quoted above; incident report
  `INC2unattemptedverificationfix.md` (owner, same day).
- Status: **FIXED in text, UNMEASURED in behavior** (2026-08-11). Patches:
  adversarial-verify gap provenance + binary-grade rule + Step 6 gap audit +
  Acceptance/delivery-shape wiring + rules 6–7; plan-gate §2 stop-the-conversion
  rule; after-report §2/§4/claim-check; the standing-principles line in
  `instructions/claude-ai-custom-instructions.md` (**owner must re-paste**).
  Pre-registered in `experiments/hypothesis-2026-08-11-gap-provenance.md`, cases
  in `evals/gap-provenance.json`.
- Lesson: when a deliverable says it *cannot* know something, ask what was
  attempted — and if the answer is nothing, that is a decision, not a limit, and
  it belongs in the report as one. The rule against it already existed
  (plan-gate §2, "never deliberate about something you could simply look up"):
  the failure was not a missing law but a law with no check that could fail, so
  a fifth restatement would have bought nothing. **A protocol that runs, grades
  a gap, and ships anyway is worse than no protocol — it lends the work
  confidence it did not earn.**

### INC-10 — Inference from wording graded SUPPORTED after the owner agreed with the reasoning

- Date: 2026-08-11 (same session as INC-9; owner-reported, deliberately kept
  separate so it would not dilute a clean incident).
- Symptom: the session claimed Rommath's recast spells do not advance the quest.
  The owner corroborated it by reasoning from the card text's "cast" versus
  "played", and the claim was graded **SUPPORTED**. A source arguing the
  opposite surfaced later.
- Root cause (**probable, not confirmed**): the grade reported the strength of
  the reasoning, not the strength of the basis. after-report's claim-check
  defines SUPPORTED / UNSUPPORTED / PARTIAL but did not say what a SUPPORTED
  requires, so an INFERENCE reached the grade reserved for a checked primary
  source — the EVIDENCE/INFERENCE law restated one level up, where it had no
  enforcement. Aggravator: owner agreement on a chain of reasoning feels like
  corroboration and is not; two parties reasoning from the same words have added
  no evidence.
- Evidence: **incomplete, and that is why this is OPEN.** Owner's dated recount
  (2026-08-11); the contrary source was not captured, and the underlying game
  question is genuinely contested. No transcript quote on file.
- Status: **OPEN.** Not independently verified; the ledger's own bar ("an entry
  without evidence is a rumor") is met only by the dated owner observation, which
  is the weakest admissible form. Recorded rather than dropped because the
  mechanism is real and cheap to guard; **it drove exactly one line of patch** —
  the basis rule in after-report's claim-check step 3 — and no part of the INC-9
  fix rests on it. To close: capture both sources and settle the game question,
  or downgrade to a dead end.
- Lesson: a verdict label reports the *basis*, not the conviction. When the
  support for a claim is reasoning rather than a source, the honest grade is
  PARTIAL however sound the reasoning — and a user agreeing with you corroborates
  the reasoning, never promotes it to evidence.

### INC-11 — Validated GAUNTLET definition lost because its branch never merged; a diff-clean paste overwrote it live

- Date: developed 2026-07-16, silently lost 2026-08-03, discovered 2026-08-12
  when the owner asked a chat session to "Run Gauntlet" and it correctly replied
  that no such skill or definition existed.
- Symptom: a trigger word the owner had used successfully for weeks stopped
  meaning anything. The owner's first hypothesis was that a Max→Pro downgrade
  had removed it. It had not — the account skill roster was byte-identical
  before and after the downgrade (16 entries, verified live 2026-08-12).
- Root cause: **the validated work never reached `main`.** GAUNTLET was authored
  and measured on branch `claude/rivian-stock-analysis-h5y46x` (commits
  `b731746`, `f63a656`, `01f6788`, `f679404` — on-command 3/3, trivia-skip 3/3,
  always-on ~83% with 0/3 over-fire, then confirmed live on claude.ai in WIN-3),
  and the owner pasted it into the settings box. That branch was **never merged**
  — 17 commits and 239 files still sit unmerged. On 2026-08-03 a new instructions
  block was authored *from main*, which had never carried the word. It was
  diff-verified and honestly declared "base text otherwise verbatim" — **true
  against main, false against the live settings box.** Pasting it overwrote
  GAUNTLET. Same commit also dropped "The load is the procedure (law)", which
  main had likewise never carried.
- Evidence: `git log --all -S auntlet` → 6 commits, 4 on the unmerged branch;
  `git merge-base --is-ancestor <each> origin/main` → false for all four; main's
  own instruction-file history shows `gauntlet=0` at every revision; the
  2026-08-03 file states "base text otherwise verbatim (diff-verified at proposal
  time — only the declared changes)". All re-run 2026-08-12.
- Status: **PARTIALLY FIXED 2026-08-12.** GAUNTLET now exists as a *skill*
  (`.claude/skills/gauntlet/`, lints PASS, evals authored not run) and as pointer
  7 plus the always-on paragraph in the instructions block. **The stranded branch
  is still unmerged** and carries more than GAUNTLET — INC-8, DEAD-3, Phase 0/1/2
  hook research, and a validated Stop-hook enforcement pair
  (`governance-trigger.py` / `governance-enforce.py`, 0/3 → 3/3). Owner decision
  outstanding. Its ledger entries also collide with this one's numbering (that
  branch has its own INC-9, INC-10, INC-11) and must be reconciled on merge, not
  renumbered.
- Lesson: **a settings box is live state; a repo branch is not the record of it.**
  "Diff-verified against the base" proves nothing when the base is a branch the
  live system never came from — verify a steering artifact against *what is
  actually deployed*, which for claude.ai means copying the box out and diffing
  it. And measured, owner-confirmed work sitting on an unmerged branch is not
  saved; it is one paste away from being deleted by an author who cannot see it.

### DRIFT-1 — The ledger forked three ways; three branches each wrote their own INC-9

- Date: discovered 2026-08-12 during the repo-wide inventory
  (`results/2026-08-12/repo-inventory/REPORT.md`).
- Symptom: `INC-9`, `INC-10` and `INC-11` each name **different incidents** on
  `main`, on `claude/rivian-stock-analysis-h5y46x`, and on
  `claude/review-instructions-z0fhnb`. Nine entries, five numbers, no overlap in
  meaning. Separately, `adversarial-verify` rules **6 and 7** are two different
  pairs of rules on `main` (receipt law / aggregates-from-records, merged
  2026-08-11) and on `claude/aba-perspective-taking-slides-kzbj3c`
  (verify-at-source / a-broadly-failing-check-indicts-the-checker, 2026-07-21).
- Root cause: the ledger and the governors both use **monotonic integers assigned
  at authoring time**, on long-lived branches, with no reservation mechanism. Two
  sessions working in parallel both take the next free number, correctly, and
  neither can see the other. The rule "never renumber existing entries — later
  references depend on them" makes this unfixable *after* the fact by the obvious
  route: whichever branch merges second cannot simply shift.
- Evidence: `git show <branch>:.claude/LESSONS.md | grep '^### INC-(9|10|11)'`
  across the three branches, run 2026-08-12; `git show
  origin/claude/aba-perspective-taking-slides-kzbj3c:.claude/skills/adversarial-verify/SKILL.md`
  for the rule collision. Full table in the inventory report.
- Status: **OPEN — blocking.** Nothing merges cleanly until this is resolved. The
  reconciliation must **re-key, not renumber**: give colliding entries a
  date-and-origin key (`INC-2026-07-16-01`) or a suffix (`INC-9a/9b/9c`), keep
  every original number resolvable, and update every citing file in the same
  commit. INC-11 already showed what happens when a branch's record is treated as
  disposable.
- Lesson: **monotonic integers are a merge conflict waiting to happen in any
  artifact edited on parallel branches.** A ledger key should be collision-proof
  at authoring time — date plus a short origin token — so two sessions that never
  see each other cannot mint the same identifier. Same for numbered rules inside
  a governor: prefer named rules over positional ones, or reserve ranges per
  branch. Check the ledger's highest number **on every branch**, not just the one
  you are on, before appending.
