> **Status 2026-11-15 — the turn gates rebuilt.** An outside audit of the hooks as merged on 2026-11-12
> recorded 128 findings. The three files behind the merge gate and the Stop gate (`turngate.py`,
> `turn-gates-pretool.py`, `governance-enforce.py`) are rewritten from one specification
> (`results/2026-11-15/turn-gates-fix/CORE-SPEC.md` and its addendum), on the owner's decisions of 2026-11-13
> and 2026-11-15. The rules as they stand are in "The turn gates" below; the older status blocks are history
> and say so where a rule changed. `selftest-turn-gates.py` is now a table of 349 cases (204 of them fail on the
> hooks before the rebuild: `results/2026-11-15/turn-gates-fix/red-on-merged.txt`), and
> `selftest-mutations.py` is a standing list of 156 deliberate breaks that the guard runs, so a rule that no
> case tests fails the guard. Every upper-case constant of the three files is in the registry. Not measured:
> a live session.

> **Status 2026-11-12 — scheduled runs, standing registry.** `turngate.py` gains `turn_start()`: a scheduled
> run is a turn of its own, and never merges (built in the kit 2026-11-04, upstreamed here unchanged; cases
> S1, S2, S5 of that day's fixture fail on the 2026-11-02 hooks; since 2026-11-15 the rule is carried by the
> test table and stated in "The turn gates" below). Every hand-set value in this directory is now registered
> in `redteam/constants_registry.json` and the guard fails on drift (ledger INC-2026-11-12-01).

> **Status 2026-11-02 — decision-cards reminder.** `governance-trigger.py` adds one advisory line on the
> owner's next message when the previous reply posed a decision as a "(Recommended)" list line without an
> AskUserQuestion call (Solo-Leveling-System after-report: 5 of 13 decisions went out as text lists). Pinned
> by `selftest-turn-gates.py` cases O15 to O20 (D1–D6 of the fixture of that day; red on the old trigger,
> green now). Never blocks.

> **Status 2026-10-29 — turn gates, the first build** (rebuilt 2026-11-15; the rules as they stand are in
> "The turn gates" below). The 2026-10-28 compliance audit of a two-week session found every governor miss in
> a short follow-up turn the prompt classifier does not match. New that day: `turngate.py` (shared), the
> outward-action rule of `governance-enforce.py` (then called **F1**: what a turn that commits, pushes or
> changes a pull request must have loaded), the merge gate of `turn-gates-pretool.py` (then **F2**: a merge
> is denied without the owner's word; since 2026-11-15 that word must name the pull request) and the
> plan-shown advisory (then **F3**; advisory because a long cloud session's transcript did not record 7 of
> 13 of its texts). Pinned that day by 33 fixture cases (9/33 on the hooks before it); every case of that
> fixture is carried by the test table of 2026-11-15 or listed with the decision that changed it
> (`results/2026-11-15/turn-gates-fix/old-selftest-mapping.md`). Replay over the whole real session that
> day: F1 blocks exactly the 7 audited turns and no other. Records: `results/2026-10-29/turn-gates/`; ledger
> INC-2026-10-29-01.

# Hooks — mechanical trigger aids

> **Status 2026-10-20 — red-team fixes landed.** The owner's red-team of the merged system
> (`results/2026-10-19/system-red-team/REPORT.md`) found the hooks firing as built but failing
> their purpose in places; on the owner's "proceed with recommendations", these changed, each
> red-first (16 new fixture cases failing on the old hooks, then green:
> `results/2026-10-19/redteam-fixes/`):
> - `governance-trigger.py` drops the "skip if trivial" clause on build-class prompts (live, the
>   clause was taken in 4/4 build runs and the governor loaded only after the Stop block; with it
>   removed, plan-gate loaded BEFORE the first write 2/2) and adds an **advisory cue tier**
>   (D-SV-3 option c): owner prompts the patterns miss get one advisory line — measured on the
>   sealed set, the cue covers 21/22 pattern-missed governed prompts (the 22nd, "audit every
>   skill's frontmatter", is 4 words and under the cue's word floor) and also cues on 25/36
>   negatives, the accepted cost of an advisory line that licenses skipping; the blocking
>   classifier is unchanged.
> - `governance-enforce.py` matches the loaded Skill's NAME exactly (an unrelated skill whose
>   arguments mentioned a governor used to count — attack G3), requires each enforced class's
>   PRIMARY governor (a dispute passed on scope-fence alone — G4), ignores slash-command echoes
>   (G5; since 2026-11-15 only the echo of a command the program ran itself is ignored, and the arguments of
>   any other slash command are the owner's prompt), and allows a review-only turn that ran no tool and answered under 400 characters
>   (D-SV-5: "2+2=4, right?" was blocked 2/2).
> - `receipt-law-stop-gate.sh` normalizes curly quotes ("couldn’t verify" passed 2/2 live — R2),
>   adds paraphrases (R3-R4), uses word boundaries ("veteran" no longer contains the receipt
>   "ran " — R6), and requires the receipt within 400 characters of the claim (R5).
> - the two first-write reminders and `session-doctrine.sh` read JSON with python3, not jq
>   (D-GF-8: the hard-coded `/usr/bin/jq` made a jq-elsewhere machine share one sentinel per
>   machine; no jq on PATH silenced the compaction protocol entirely). Pinned by the new
>   `selftest-reminders.sh` (8 cases).
> The cue-tier word floor (5), the trivia allowance (400 chars) and the receipt window (400
> chars) are hand-set, uncalibrated; live acceptance 8/8 pre-registered in
> `experiments/hypothesis-2026-10-19-redteam-fixes.md`. Known residuals, deliberately not fixed
> here: the receipt gate's turn boundary (attacks R7-R9) and an unrelated-but-near receipt word
> (R5's cousin inside the window); the band hook's B3-B5; the classifier's sealed-set recall
> (D-SV-3 options a/b stand).

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

## The turn gates: turngate.py, turn-gates-pretool.py, governance-enforce.py (rebuilt 2026-11-15)

Three files. `turngate.py` reads the session record once and answers two questions: what each row IS (the
owner typing, a wake-up, a tool result, a stop) and what a tool call DOES (a shell command is parsed: a word in
command position is an act, anything else is data). The two hooks decide on that: `turn-gates-pretool.py`
before a tool call (the merge gate and the plan-shown advisory), `governance-enforce.py` when the assistant
stops (the Stop gate). The specification and its addendum are in `results/2026-11-15/turn-gates-fix/`
(`CORE-SPEC.md`, `CORE-SPEC-ADDENDUM.md`); the wanted verdict of every test case was fixed before any run, in
`experiments/hypothesis-2026-11-15-turn-gates-cases.md`. Where an older status block of this file states one
of these rules differently, this section is the rule.

### The merge word (merge gate, before a tool call)

What the owner decided (three card answers, 2026-11-13):

- **D1.** A merge is authorized only by the owner's click on a card (AskUserQuestion) that names the pull
  request, or by a message the owner typed that orders the merge and names its number. A bare "yes",
  "proceed", "go ahead" or "merge it" authorizes nothing: the denial tells the assistant to ask with a card
  that names the pull request.
- **D2.** The word covers only the pull requests it names, and it ends when the assistant stops. Work started
  by a later notification or wake-up starts with no word.
- **D3.** Switching auto-merge on, and a direct push to a default branch, need the same word. In a scheduled
  run all of them are always denied.

What is gated. The merge and auto-merge tools of any connector (the part of the tool's name after the last
`__` is matched); the command-line merge, with or without `--auto`, and the merge routes of the REST and
GraphQL API through the command line or an HTTP program; a push to `main`, `master` or the default branch
the checkout records; a push of every branch (`--all`, `--mirror`, `--branches`, a wildcard refspec); a file
pushed to a default branch through a tool or the API. A command is read through `bash -c`, `eval`, command
substitution, a pipe or here-document into a shell, wrappers such as `sudo`, `env`, `timeout` and `xargs`, and
a script file it runs. A command that only mentions the words (a search, an echo, a commit message, a script
that is written and not run) is not gated.

What makes the word.

| the owner's word | grants |
|---|---|
| a typed order: the verb starts its clause (after words such as "ok, please", "go ahead and", "can you") and the numbers follow it: "Merge #34.", "ok, merge 34 and 141", "Can you merge #34?", a pull-request address, `owner/repo#34` | those pull requests; an address or `owner/repo#34` binds the repository too |
| the verb with no number: "merge it", "yes", "proceed and merge" | nothing |
| the verb negated, asked about, reported or not at the start of its clause: "Don't merge #34" (straight or curly apostrophe), "Don't, under any circumstances, merge #34", "Is #34 safe to merge?", "#34 is ready to merge" | nothing; a negated clause takes its numbers out of the grant, or empties it when it names none |
| "Merge #34, not #141", "Merge 34. Leave 141 alone", "Merge everything except #141" | #34; #34; nothing |
| an order for later or under a condition: "Merge #34 once CI is green" | nothing, and nothing is taken back |
| a card: the chosen option is an order ("Merge #34", "Merge both") or a yes on a question that asks for a merge | the numbers in the chosen option; with no number there, the question's pull request when the question names exactly one, or all of them when the option says both / all / every / each / everything |
| "Yes" or "Merge library only" on a card whose question names several pull requests | nothing: the gate cannot tell which |
| a card option that refuses or defers ("Wait", "Not yet", "Merge neither", "Merge after the audit"), or any other option of a merge card | nothing; the question's numbers leave the grant |
| free text typed into a card | read as a typed message; an order without a number ("merge it, squash please") takes the question's pull request under the rule for an option without a number |
| a push to a default branch: a typed order that names the branch as its destination ("push this to main", "land it on the default branch"), or a card that asks exactly that and is answered yes or with the order | the word for that push. "Merge main into my branch" and "commit the fix in main.py" name the word and order no push. A word for pull request n does not cover a push to main |
| the assistant's own text; a tool's output, whatever it quotes; a notification body; a stored prompt; a compaction summary; a helper agent's row; any row the program wrote | nothing. Only the result of the card's own call, paired with it by id, is a click |

The operations of one message apply in the order they were said: "Merge #34. No wait." grants and then
empties. "No rush", "no objections", "why not" and their like refuse nothing.

What ends the word, and what does not.

| event | effect |
|---|---|
| a message the owner types while the assistant is idle (a typed slash command and a message with only an image included) | a new window: the earlier word is gone |
| a completed stop; an interrupt; a wake row (a notification, a task or a peer message that only an idle session receives) | the word is gone |
| the restart notice of the worker process | the word is gone (`RESTART_ENDS_WORD`, a default the owner was not asked about) |
| a scheduled notification read in the middle of the owner's turn | the word given before it is gone; a card the owner answers after it grants again (the owner's answer of 2026-11-15: "No, ask me again") |
| a blocked stop; a notification queued mid-turn; a GitHub notification read mid-turn; a skill load; a compaction | nothing: the word stands |
| a later refusal by the owner, typed mid-turn or clicked | the refused numbers leave the grant; a bare refusal empties it |

A card counts by where its ANSWER sits: a card shown before a restart notice and answered after it is answered
in the current window. In a scheduled run nothing merges unless the owner types the order while it runs; a
card answered inside the run grants nothing, also after the owner writes. A helper agent's call is judged like
any call, on the main session's record (`DELEGATE_MAY_MERGE`, a default the owner was not asked about).

A push whose branch the gate cannot read (a bare push from a directory it cannot read, a branch held in a
variable it cannot resolve) is denied only where the owner is not present in the window (the owner's answer:
"An order naming the branch"; `PUSH_UNKNOWN_BRANCH_POLICY`). The branch of a bare push is read from the
checkout's `HEAD` file; no program is started.

Every denial reads `TURN-GATE (merge word) [code]: ...`. Codes: `no-record`, `branch-unknown`, `scheduled`,
`delegate`, `no-owner-word`, `target-unknown` (the pull request cannot be read from the call), `merge-word`,
`default-branch`, `gate-error`.

### The Stop gate (when the assistant stops)

**Outward actions.** What counts (the owner's answer: "Commits, pushes, PRs, scheduling"): a commit (also by
revert, cherry-pick or am), a push, creating, changing, merging or auto-merging a pull request, updating its
branch, a workflow run, a file pushed through a tool or the API, and every change to a scheduled task, the
session's own wake-ups included. Not counted: comments, reviews, issues, creating a branch or a repository,
mail, drive, messages to other sessions. Not an action at all: a command that only mentions the words, a dry
run, a help page, a call that was denied or rejected, and the last step of an and-chain that failed.

- **What one stop judges: the stretch.** The rows since the owner's latest message or the latest completed
  stop, whichever is later. A blocked stop is not a completed stop. A miss that was let go at its own stop is
  not raised again at a later one.
- **What must be loaded.** plan-gate before each outward action and adversarial-verify anywhere, both inside
  the governance turn: since the owner's message, or since a scheduled run began. A load is a Skill call whose
  name, after any scope prefix, is the governor's and whose result is not an error. Work woken by a
  notification after a completed stop keeps the loads made since the owner's message. A scheduled run is judged
  on its own loads; when a run begins inside the stretch, the part before it is judged on the owner turn's loads
  and the part after it on the run's.
- **After a compaction** (the owner's answer: "Yes after compaction") the governors must be loaded again
  before the next outward action: plan-gate after the latest compaction that precedes the action, and
  adversarial-verify after the latest compaction that precedes the last action of the part judged. A compaction
  that comes after the last action voids nothing. The rule is judged per action. The block says so in plain
  words when this is the miss.
- **How often it blocks** (the owner's answer: "Yes, twice at most"). At most twice in one stretch: again when
  its first block was not answered, then the stop is let go. After its own block, a plan-gate load made since
  answers it although it can no longer come first. The retry flag (`stop_hook_active`) decides nothing by
  itself: it is set after ANY Stop hook blocked. The rule counts its own earlier blocks from the record; only
  when the flag is set and the record shows no block at all is the stop let go.

**Prompt class.** The owner's prompts of the turn are what the owner types (the owner's answer: "No, only what
you type"): the message that starts the turn, a slash command's arguments, and every message sent while the
assistant worked. A clicked card label is not a prompt; a row the program wrote is not; a message that merely
quotes a harness marker is the owner's and is classified. When the prompts match an enforced class of
`govclass.py`, the primary governor of every matched class must have been loaded in the governance turn (for
this rule a load made before a compaction counts; a load made before the turn does not). The rule is judged
only at the first stop after the owner's message: it is silent in a scheduled run, when the record holds no
owner message, and after a completed stop or a wake row. Allowance: the classes are review only, no tool other
than Skill ran, and the answer is shorter than 400 characters (the final answer the program hands the hook is
read when the record does not hold it). It blocks once in a stretch; a block by the other rule or by another
Stop hook does not use that up.

### The plan-shown advisory (before a tool call)

After a plan-gate load, the first real write (a file outside scratch, a shell command that writes, an outward
action, a scheduled-task change) is preceded by one reminder when the record holds no text of the assistant
with the word "Goal" since the load. Once per load. It never blocks. **Its stated limit:** the record does not
keep every message, so the reminder can be a false alarm, and its text says so. A command that only mentions
write words, or writes only to scratch (`/tmp`, `/var/tmp`, `$TMPDIR`), does not spend it. A helper agent's call gets none:
the helper's own load and plan are not in the record the hook reads.

### Which way each failure goes

| failure | a merge, an auto-merge, a push to a default branch | any other call | the Stop gate |
|---|---|---|---|
| the hook's input is not JSON | DENY `gate-error` when the raw text crudely looks like one | allow | allow |
| `turngate.py` is missing or cannot be loaded | DENY `gate-error` when the tool name or the command crudely looks like one | allow | allow |
| the record's path is empty or missing, or the file holds no readable row | DENY `no-record` | allow | allow |
| an error while judging | DENY `gate-error` (by the call's classification once there is one, else by the crude screen) | allow | allow |
| a shell command the parser cannot read | a crude screen of its words decides: merge words make it a merge, judged like one | commit and push words make it an outward action for the Stop gate; otherwise nothing | - |
| the hook is still running after 8 seconds | DENY `gate-error`, as for an error | allow | allow |

Every path of both hooks ends with exit status 0 and prints one JSON object or nothing: the program lets a
call through when a hook exits with an error or is cut off, so neither may happen. The crude screens are one
pass over the words of the text, so no text can keep them busy. They are crude on purpose: on a failure path
`git push origin main-fix` is taken for a push to main and denied. No environment variable and no key of a
hook's input switches a rule off.

### Helper agents

A helper agent's rows are not in the record the hooks are handed. So when a call that carries `agent_id` holds
an action the Stop gate counts and is not denied, the pre-tool hook notes it in a small ledger
(`delegate-<hash of the record's path>.jsonl` in `$TURNGATE_STATE_DIR`, else `$TMPDIR/turn-gates`, else
`/tmp/turn-gates`), and the Stop gate counts the note as an outward action of the stretch. A note is placed by
its time stamp, so it stays usable after the record was rewritten at a compaction. Limits: a helper's call that
was let through and then failed still counts; when the ledger cannot be written nothing is counted and nothing
is blocked; the ledger is lost with the container.

### The owner's answers, one constant each

Each answer is one upper-case name in `turngate.py`, so another answer changes one line. Every upper-case
module-level name of the three files is registered in `redteam/constants_registry.json` with what it decides
and what vouches for it; `registry_check.py` (run by the guard) fails on a value that is added or changed and
not registered.

| question | the owner's answer | constant |
|---|---|---|
| a scheduled notification lands between the order and the merge | "No, ask me again" (2026-11-15) | `SCHEDULED_READ_ENDS_WORD = True` |
| what authorizes a direct push to main | "An order naming the branch" (2026-11-15) | `PUSH_ORDER`, `DEFAULT_BRANCH_WORD`; `PUSH_UNKNOWN_BRANCH_POLICY = "deny-unattended"` |
| block again after a Stop block that was not answered | "Yes, twice at most" (2026-11-15) | `F1_MAX_BLOCKS = 2`, `PROMPT_CLASS_MAX_BLOCKS = 1` |
| governor loads after a compaction inside the turn | "Yes after compaction" (2026-11-15) | `COMPACTION_VOIDS_LOADS = True`, `WAKE_TURN_INHERITS_LOADS = True` |
| is a clicked card label the owner's prompt | "No, only what you type" (2026-11-15) | `CLASSIFY_CARD_ANSWERS = False` |
| which actions the Stop gate counts | "Commits, pushes, PRs, scheduling" (2026-11-15) | `F1_COUNTED_KINDS` |
| which calls need the merge word | D1 to D3 (2026-11-13) | `MERGE_GATED_KINDS`, `MERGE_TOOL_LEAVES` |

Two defaults were taken without a question and are open for the owner (registry decision D-TG-2):
`RESTART_ENDS_WORD = True` and `DELEGATE_MAY_MERGE = True`. `F1_COUNTED_KINDS` (what the Stop gate counts) can
be changed without touching the merge gate: what needs the owner's word is `MERGE_GATED_KINDS`, and the pre-tool
hook looks at every call that holds a gated act, a write, or a push whose branch it cannot read (cases `X06a`
and `X06b` run the hooks with a shorter Stop list and still expect the denials).

### Tests

    python3 hooks/selftest-turn-gates.py              # the table: 349 cases, one line each; exit 0 only when all pass
    python3 hooks/selftest-turn-gates.py --only-failing J04 X05     # by the start of a name
    python3 hooks/selftest-turn-gates.py --hooks DIR  # another copy of the hooks
    python3 hooks/selftest-mutations.py               # the break list: 156 deliberate breaks, each must be caught
    python3 hooks/selftest-mutations.py --list        # what each break removes, and the cases named for it

`selftest-turn-gates.py` builds a session record in the real row shapes for every case (`selftest_rows.py` is
its row builder), runs a hook as the program would, and compares the verdict with the wanted one. The wanted
verdicts of the pre-registered cases are never changed to make a case pass; cases added later carry new names.
`selftest-mutations.py` proves the table can fail: it applies one text replacement at a time to a copy of the
hooks and expects at least one case to fail; a break that survives, or whose text is no longer found, fails the
run. The guard runs both. Evidence of 2026-11-15, in `results/2026-11-15/turn-gates-fix/`: the table on the
hooks before the rebuild (`red-on-merged.txt`), on the rebuilt hooks (`pass-on-fixed.txt`), the break list
(`mutations.txt`), the replay of a real session record against its baseline (`replay-vs-baseline.md`), the run
time (`timing.txt`), the guard (`guard-after.txt`).

### Limits, stated as limits

- A program in another language that merges through a library or a subprocess is not seen. A script file is
  read as it is when the hook runs; one that is missing, larger than 256 KB, or named relative to a directory
  the gate does not know contributes nothing. A loop over directories is not unrolled, so a push inside it has
  no readable branch.
- A notification body that imitates exactly the next expected header line of its batch takes that header's
  place. It can make a GitHub batch look scheduled (the word ends: the gate fails closed) or hide a scheduled
  header that is not the first of its batch.
- The word lists and patterns that read the owner's messages are hand-set and were not measured against real
  messages (registry status `uncalibrated`, decision D-TG-1, open). An order worded in a way the grammar does
  not take as an order costs one card; every refusal reading fails closed.
- The deadline inside the hooks relies on the alarm signal (Linux and macOS; a pattern match that runs long is
  interrupted there: checked 2026-11-15, the denial came at 8.0 s). On a system without that signal the
  fallback timer cannot interrupt a single long call.
- A record without stop rows is judged as never judged before: every real record has a stop row at every stop.
- The replay tool judges a recorded push that names no branch against the checkout as it is at replay time,
  not as it was when the push was made (`replay-vs-baseline.md` shows one denial that comes from this).
- These gates run where hooks run: Claude Code. On claude.ai nothing here is enforced.
- Not measured: behaviour in a live session; a blocked stop followed by a merge, a message sent mid-turn, a
  scheduled delivery and a helper agent's outward call are tested on built records only, because the real
  record holds none of them.

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

**Since 2026-11-15** the Stop half is two rules on one turn model. What it reads as the owner's prompt, when it
judges, what counts as loaded and how often it blocks are stated in "The turn gates" above; the paragraphs of
this section are the history of the pair.

Relationship to `receipt-law-stop-gate.sh`: complementary, not competing. This
pair enforces **that a governor loads**; that one enforces **that a claim of
inability carries a receipt**. Both are `Stop` hooks and can coexist.

**Surface limit:** Claude Code only. claude.ai has no hook layer.
