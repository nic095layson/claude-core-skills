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
