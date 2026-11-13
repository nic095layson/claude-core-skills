# Turn gates: the rules as the repository states them (verbatim extracts, with file:line)

This file is for the re-implementer. Every line below is copied by script from the merged library (commit
1ce99d5); nothing is paraphrased. It contains prose only: status notes, the pre-registration table, module
and function docstrings, and comments. It contains no executable logic. Where these statements are silent
or disagree with each other, that is a finding of kind "ambiguity"; do not guess what was meant.

Other allowed reading: lib/CLAUDE.md (the doctrine block), lib/.claude/settings.json (which tools each hook is
wired to), pack/real-row-shapes.md (what real transcript rows look like), pack/README.md (hook payloads),
kit/after-report-2026-11-04-turn-gate-scheduled.md (the report that introduced the scheduled-run rule).

## 1. Status notes (hooks/README.md)

```
hooks/README.md:1: > **Status 2026-11-12 — scheduled runs, standing registry.** `turngate.py` gains `turn_start()`: a scheduled
hooks/README.md:2: > run is a turn of its own, and never merges (built in the kit 2026-11-04, upstreamed here unchanged; fixture
hooks/README.md:3: > cases S1, S2, S5 fail on the 2026-11-02 hooks). Every hand-set value in this directory is now registered
hooks/README.md:4: > in `redteam/constants_registry.json` and the guard fails on drift (ledger INC-2026-11-12-01).

hooks/README.md:11: > **Status 2026-10-29 — turn gates.** The 2026-10-28 compliance audit of a two-week session found
hooks/README.md:12: > every governor miss in a short follow-up turn the prompt classifier does not match. New:
hooks/README.md:13: > `turngate.py` (shared), `governance-enforce.py` **F1** (a turn that committed, pushed, or created,
hooks/README.md:14: > updated or merged a PR must have loaded plan-gate before the first such action and
hooks/README.md:15: > adversarial-verify in the turn), `turn-gates-pretool.py` **F2** (a PR merge is denied without the
hooks/README.md:16: > owner's word) and **F3** (advisory: after a plan-gate load, the first write is preceded by a
hooks/README.md:17: > reminder unless a "Goal" text appears — advisory because a long cloud session's transcript did not
hooks/README.md:18: > record 7 of 13 of its texts). Pinned by `selftest-turn-gates.py` (33 cases, 9/33 on the old hooks).
hooks/README.md:19: > Replay over the whole real session: F1 blocks exactly the 7 audited turns and no other. Records:
hooks/README.md:20: > `results/2026-10-29/turn-gates/`; ledger INC-2026-10-29-01.
```

## 2. The pre-registration (experiments/hypothesis-2026-10-29-turn-gates.md)

```
experiments/hypothesis-2026-10-29-turn-gates.md:9: - plan-gate loaded before the first consequential action in 12 of 16 consequential owner turns;
experiments/hypothesis-2026-10-29-turn-gates.md:10:   adversarial-verify in 11 of 16. Every miss is a short follow-up turn ("Continue", "proceed", "re-pasted
experiments/hypothesis-2026-10-29-turn-gates.md:11:   instructions complete", merge-and-report) whose prompt the classifier does not match, so the existing
experiments/hypothesis-2026-10-29-turn-gates.md:12:   Stop gate (prompt-class based) never looked at it.
experiments/hypothesis-2026-10-29-turn-gates.md:13: - One merge (PR #26, 2026-10-20) ran on "I've uploaded, proceed" with no merge word anywhere.
experiments/hypothesis-2026-10-29-turn-gates.md:14: - Two turns loaded plan-gate and wrote/merged with no plan text in the transcript between the load and
experiments/hypothesis-2026-10-29-turn-gates.md:15:   the first write (2026-10-21 23:25; 2026-10-28 22:56).

experiments/hypothesis-2026-10-29-turn-gates.md:19: | id | hook | rule |
experiments/hypothesis-2026-10-29-turn-gates.md:20: |---|---|---|
experiments/hypothesis-2026-10-29-turn-gates.md:21: | F1 | `governance-enforce.py` (Stop) | If the turn took an OUTWARD action — git commit/push, `gh pr create/merge`, a PR create/update/merge, a file push, a scheduled-task create/update/delete — then plan-gate must have loaded before the first such action and adversarial-verify after it. Independent of how the prompt is worded. |
experiments/hypothesis-2026-10-29-turn-gates.md:22: | F2 | `turn-gates-pretool.py` (PreToolUse) | A PR merge (`*merge_pull_request`, `gh pr merge`) is denied unless "merge" (word) is in the owner's latest message, or in a clickable answer after it, or in the assistant's last text before that message together with the PR's number. |
experiments/hypothesis-2026-10-29-turn-gates.md:23: | F3 | `turn-gates-pretool.py` (PreToolUse) | When plan-gate loaded this turn, the first write-class action after the load (Edit/Write/NotebookEdit outside /tmp, `git checkout -b`, `sed -i`, git commit/push, PR create/update/merge, file push) is denied until an assistant text containing "Goal" appears after the load. Turns that never loaded plan-gate are untouched (no ceremony on trivia). |
experiments/hypothesis-2026-10-29-turn-gates.md:24: | F4 | doctrine block rule 5 | A skill the owner names is loaded, or the reply says in one line why another fits. |
experiments/hypothesis-2026-10-29-turn-gates.md:25: | L | doctrine block rule 6 | New pushed work names a model by a neutral label; the label-to-model map stays outside the repository; history is not rewritten. |
experiments/hypothesis-2026-10-29-turn-gates.md:26: 
experiments/hypothesis-2026-10-29-turn-gates.md:27: Shared helpers move to `hooks/turngate.py`. Plugin copies stay byte-identical (guard).

experiments/hypothesis-2026-10-29-turn-gates.md:50: 
experiments/hypothesis-2026-10-29-turn-gates.md:51: **Synthetic fixture** (new `hooks/selftest-turn-gates.py`): trivia with no tools → allow; edit-only turn
experiments/hypothesis-2026-10-29-turn-gates.md:52: with no outward action → F1 allow; `/tmp` writes → F3 allow; `git merge origin/main` (branch sync) → F2

experiments/hypothesis-2026-10-29-turn-gates.md:64: ## Outcome (2026-10-29, after the runs) — every prediction, hit or miss
experiments/hypothesis-2026-10-29-turn-gates.md:65: 
experiments/hypothesis-2026-10-29-turn-gates.md:66: Records: `results/2026-10-29/turn-gates/` (REPORT.md has the table).
experiments/hypothesis-2026-10-29-turn-gates.md:67: 
experiments/hypothesis-2026-10-29-turn-gates.md:68: - **Replay R1–R7 (F1) HIT** — 7/7 block; over every owner turn, the only blocks are these 7.
experiments/hypothesis-2026-10-29-turn-gates.md:69: - **Replay current-hooks column MISS for R4** — today's prompt-class gate already blocks it (analysis
experiments/hypothesis-2026-10-29-turn-gates.md:70:   pattern); predicted "allow".
experiments/hypothesis-2026-10-29-turn-gates.md:71: - **Control C4 MISS on the first draft** — F1 as first written (adversarial-verify after the first
experiments/hypothesis-2026-10-29-turn-gates.md:72:   outward action) blocked "verify, then commit and push"; rule narrowed to "anywhere in the turn".
experiments/hypothesis-2026-10-29-turn-gates.md:73: - **F2 HIT** — R5 denied; C1, C2, C3 allowed.
experiments/hypothesis-2026-10-29-turn-gates.md:74: - **F3 as pre-registered (deny) NOT RUN** — changed to advisory before any live run, because the
experiments/hypothesis-2026-10-29-turn-gates.md:75:   authoring session's transcript is missing 7 of 13 of its assistant texts (headless sessions: 11/11
experiments/hypothesis-2026-10-29-turn-gates.md:76:   recorded). Live (b) under the advisory variant: advisory fired 2/2, plan shown before the write 0/2.
experiments/hypothesis-2026-10-29-turn-gates.md:77: - **Live (a) HIT** 2/2; **live (c) HIT** 2/2.
experiments/hypothesis-2026-10-29-turn-gates.md:78: - **Fixture** red on main 9/33 → green 33/33 (3 negation/click cases added by the refutation pass after two F2 holes were found).
```

## 3. Stop gate, outward-action rule F1 (hooks/governance-enforce.py: docstring and comments only)

```
hooks/governance-enforce.py:2: """Stop hook: if the turn answered governed-class work AND no governor Skill loaded for it, BLOCK once
hooks/governance-enforce.py:3: and force the load. Single retry (stop_hook_active) => loop-safe. Fails open on every error.
hooks/governance-enforce.py:4: 
hooks/governance-enforce.py:5: This is the mechanism behind the kit's promise that "the core governors run on every session": a
hooks/governance-enforce.py:6: promise with no mechanism was INC-2026-10-13-01. Validated form (2026-07-15, phase 2b A/B): every
hooks/governance-enforce.py:7: governed case loaded the governor 3/3 under enforcement vs 0/3 without; both should-not cases silent.
hooks/governance-enforce.py:8: 
hooks/governance-enforce.py:9: Rebuilt 2026-10-13 on hooks/govclass.py (shared with the trigger) and made robust to user messages
hooks/governance-enforce.py:10: whose content is a list of blocks, which is how cloud sessions record them.
hooks/governance-enforce.py:11: 
hooks/governance-enforce.py:12: What counts as "loaded": a Skill tool call this turn whose input names the governor — including a
hooks/governance-enforce.py:13: synced copy such as "anthropic-skills:plan-gate". Governor text merely re-attached after a compaction
hooks/governance-enforce.py:14: does NOT count (it is bound to an earlier task); that distinction is the gauntlet skill's rule, and
hooks/governance-enforce.py:15: this hook enforces it by looking only at Skill calls after the latest owner message.
hooks/governance-enforce.py:67: # F1 (2026-10-29): gate on what the turn DID. If it took an outward action (commit, push, PR create/
hooks/governance-enforce.py:68: # update/merge, scheduled-task change), plan-gate must have loaded before the first such action and
hooks/governance-enforce.py:69: # adversarial-verify somewhere in the turn — whatever the prompt said. (First draft required
hooks/governance-enforce.py:70: # adversarial-verify AFTER the first outward action; the replay control "verify, then commit and push"
hooks/governance-enforce.py:71: # — 2026-10-21 17:13 — was blocked by it, so the rule was narrowed, not the fixture loosened.) Every governor miss in the 2026-10-28 session
hooks/governance-enforce.py:72: # audit was a short follow-up turn the prompt classifier does not match ("Continue", "proceed").
hooks/governance-enforce.py:73: # Pre-registered: experiments/hypothesis-2026-10-29-turn-gates.md.

hooks/governance-enforce.py:102:     # Harness-injected user entries (loaded skill text, hook feedback, compaction summaries) are
hooks/governance-enforce.py:103:     # marked isMeta / isCompactSummary. They are not the owner's request: in the 2026-10-13 live
hooks/governance-enforce.py:104:     # A/B the gate took a loaded skill's own text as "the prompt", put the Skill call before it,
hooks/governance-enforce.py:105:     # and blocked a compliant turn. Only un-marked user text counts.

hooks/governance-enforce.py:112:     # Harness-generated user turns (background-task notifications, wake envelopes, subagent hand-backs)
hooks/governance-enforce.py:113:     # are not the owner's request either. Before 2026-10-13 they were taken as "the prompt", classified
hooks/governance-enforce.py:114:     # as nothing, and let a governed, unloaded turn through whenever a background task finished
hooks/governance-enforce.py:115:     # mid-turn (reproduced red-first, results/2026-10-13/system-validation/).
```

## 4. Pre-tool gates F2 and F3 (hooks/turn-gates-pretool.py: docstring and comments only)

```
hooks/turn-gates-pretool.py:2: """PreToolUse turn gates (2026-10-29). Denies, before the tool runs:
hooks/turn-gates-pretool.py:3: 
hooks/turn-gates-pretool.py:4: F2 — a PR merge (`*merge_pull_request`, `gh pr merge`) without the owner's word for it: "merge" in the
hooks/turn-gates-pretool.py:5:      owner's latest message, in a clickable answer after it, or in the assistant's last text before that
hooks/turn-gates-pretool.py:6:      message together with this PR's number. The 2026-10-28 audit found PR #26 merged on "I've uploaded,
hooks/turn-gates-pretool.py:7:      proceed" while the assistant's own note said it was awaiting the owner's call.
hooks/turn-gates-pretool.py:8: F3 — the first write after a plan-gate load when no plan was shown: once plan-gate is loaded this turn,
hooks/turn-gates-pretool.py:9:      a write-class action (Edit/Write/NotebookEdit outside /tmp, `git checkout -b`, `sed -i`, commit,
hooks/turn-gates-pretool.py:10:      push, PR create/update/merge) waits for an assistant text containing "Goal". A turn that never
hooks/turn-gates-pretool.py:11:      loaded plan-gate is untouched, so trivia carries no ceremony. Two turns in the audit loaded
hooks/turn-gates-pretool.py:12:      plan-gate and wrote with no plan in the transcript between the load and the first write.
hooks/turn-gates-pretool.py:13: 
hooks/turn-gates-pretool.py:14: Fails open on every error. Pre-registered: experiments/hypothesis-2026-10-29-turn-gates.md;
hooks/turn-gates-pretool.py:15: pinned by hooks/selftest-turn-gates.py.
hooks/turn-gates-pretool.py:45:     # A scheduled run carries no owner message, so it carries no owner word to merge: it never merges.

hooks/turn-gates-pretool.py:60:         # ADVISORY, not deny (2026-10-29): the transcript does not record every assistant text — 7 of 13
hooks/turn-gates-pretool.py:61:         # texts written in the authoring turn were absent from it — so "no plan in the transcript" cannot
hooks/turn-gates-pretool.py:62:         # prove "no plan shown", and a deny could block an honest plan, repeatedly. One reminder per
hooks/turn-gates-pretool.py:63:         # plan-gate load; the sentinel keys it to the session, the owner message and the load.
```

## 5. Shared helpers (hooks/turngate.py: docstrings and comments only)

```
hooks/turngate.py:2: """Shared helpers for the turn gates (2026-10-29): what a turn DID, not how its prompt was worded.
hooks/turngate.py:3: 
hooks/turngate.py:4: Used by governance-enforce.py (Stop, F1) and turn-gates-pretool.py (PreToolUse, F2 merge word and F3
hooks/turngate.py:5: plan shown). Why: the 2026-10-28 compliance audit of a two-week session found every governor miss in a
hooks/turngate.py:6: short follow-up turn ("Continue", "proceed", "re-pasted instructions complete") that the prompt
hooks/turngate.py:7: classifier does not match, so the prompt-class gate never looked at it. Pre-registered in
hooks/turngate.py:8: experiments/hypothesis-2026-10-29-turn-gates.md; pinned by hooks/selftest-turn-gates.py.
hooks/turngate.py:9: 
hooks/turngate.py:10: Everything here reads the transcript and fails open: an unreadable transcript yields "no turn".

hooks/turngate.py:24: # OUTWARD actions (F1): leave the machine or change shared state. Edits alone are not outward; they reach
hooks/turngate.py:25: # anyone only through a commit, push or PR, which is outward.

hooks/turngate.py:30: # WRITE actions (F3): the first change of state, local or outward.

hooks/turngate.py:66:     """Index of the owner's latest message, or -1. Harness-written user rows are skipped."""

hooks/turngate.py:80: # owner build order 2026-11-04 (after-report-2026-11-03-runner-window.md, decision A option 1): a scheduled
hooks/turngate.py:81: # run starts a turn of its own. It arrives as a ReadNotifications tool_result whose text has one header line per
hooks/turngate.py:82: # notification; only the header form counts. The same result always carries a fixed paragraph with the words
hooks/turngate.py:83: # "A scheduled trigger is a stored prompt", so a plain substring match would mark every notification read, GitHub
hooks/turngate.py:84: # ones included (on the kit session of 2026-11-04: 75 of 75 by substring, 13 by this header).

hooks/turngate.py:94:     """Index of the last tool_result row that delivered a scheduled-trigger notification, or -1."""

hooks/turngate.py:107:     """Where "this turn" begins: the owner's latest message or, when later, the latest scheduled run (-1: none)."""

hooks/turngate.py:116:     """(kind, payload) after `start` in order: ("text", str), ("tool", block), ("answer", str)."""

hooks/turngate.py:185: # "Do not merge yet" contains the word and forbids the act (refutation pass, 2026-10-29): an occurrence
hooks/turngate.py:186: # counts only when no negation sits in the few words before it.

hooks/turngate.py:198:     """The chosen options of an AskUserQuestion answer ("question"="choice"), never the question text."""

hooks/turngate.py:203:     """F2: the owner's word for THIS merge — in their latest message, in a click after it, or in the
hooks/turngate.py:204:     assistant's last text before their message together with the PR's number."""
```

## 6. Plugin note for 0.1.5 (plugin/core-governance/README.md)

```
plugin/core-governance/README.md:92: ## 0.1.5 (2026-11-12)
plugin/core-governance/README.md:93: 
plugin/core-governance/README.md:94: A scheduled run is a turn of its own (upstreamed from the kit, where it was built on 2026-11-04): the
plugin/core-governance/README.md:95: turn gates start at the latest scheduled-trigger notification when it is later than the owner's last
plugin/core-governance/README.md:96: message, and a scheduled run never merges. Scripts re-synced byte-identical to `hooks/`.
plugin/core-governance/README.md:97: 
```
