#!/usr/bin/env python3
"""make_findings.py — assemble work/reimpl/findings.json. 'observed' lines are taken verbatim from
repro-output.txt / mutate-output.txt / diag*.log (runs of padding spaces collapsed to one)."""
import json
import os
import re

W = "/tmp/claude-0/-home-user/ff01f16c-7b3f-5ea5-8051-7a95ac7cd1d1/scratchpad/merge-audit/work/reimpl"
REPRO = "python3 " + W + "/repro.py "
out_lines = [re.sub(r" {2,}", " ", ln.strip()) for ln in open(os.path.join(W, "repro-output.txt"))]
mut_lines = [re.sub(r" {2,}", " ", ln.strip()) for ln in open(os.path.join(W, "mutate-output.txt"))]


def obs(*prefixes):
    return "\n".join(ln for ln in out_lines if ln.startswith(prefixes))


def mut(*names):
    return "\n".join(ln for ln in mut_lines if ln.startswith(names))


def fx(*names):
    return [W + "/repro.py"] + [W + "/repro-fixtures/" + n + ".jsonl" for n in names]


d3 = max((json.loads(l) for l in open(os.path.join(W, "diag3.log"))), key=lambda x: x.get("rows", 0))
cases = json.load(open(os.path.join(W, "corpus", "cases.json")))
n_stop = sum(c["gate"] == "stop" for c in cases)
n_pre = sum(c["gate"] == "pre" for c in cases)

findings = [
    {
        "id": "RI-1",
        "title": "The merge gate lets a merge through when the owner writes \"Don’t merge yet\" with a curly apostrophe, or \"can't / cannot / shouldn't merge\", or puts more than one word between the negation and the word.",
        "component": "lib/hooks/turngate.py NEGATION + says_merge (used by turn-gates-pretool.py, F2)",
        "kind": "false_allow",
        "rule_quoted": "# \"Do not merge yet\" contains the word and forbids the act (refutation pass, 2026-10-29): an occurrence\n# counts only when no negation sits in the few words before it.",
        "rule_source": "lib/hooks/turngate.py:185-186",
        "repro_command": REPRO + "RI-1",
        "repro_files": fx("ri1-curly-dont-merge-yet", "ri1-cant-merge-until-ci", "ri1-do-not-go-ahead-and-merge", "ri1-curly-in-click") + [W + "/mutate.py", W + "/diag3.log"],
        "observed": obs("ri1-") + "\n" + mut("M4-", "M5-", "M6-"),
        "expected": "deny:merge-word on every line marked <<<: each message forbids the merge, exactly like the control \"Do not merge yet\", which is denied.",
        "how_it_arises": "Ordinary owner messages (plain string user rows, the shape of all 17 real owner messages in the catalog). NEGATION lists don't / dont / do not / never / not / no / without / hold off / wait to|before, with a straight apostrophe only, and allows at most ONE word between the negation and the word. So ’ (what iOS and macOS smart punctuation types), can't, cannot, shouldn't, won't and \"do not go ahead and merge\" are all read as the owner's word. Real record, counts only (diag3.log): %d of the 17 real owner messages contain a curly apostrophe and %d a straight one, so curly apostrophes do reach this owner's messages. The fixture does not pin any of it: adding the curly apostrophe and the contractions (M6) or narrowing the window to zero (M4) still passes 44/44; a wider window (M5) breaks the fixture's own case \"don't merge #26, merge #27\", so 'few' was tuned to one sentence (my own choice of three words fails that case and still misses the last three sentences here: the stated rule is silent on 'few'). Harm needs the assistant to attempt a merge after being told not to, which is the case this gate exists for." % (d3["owner_msgs_with_curly_apostrophe"], d3["owner_msgs_with_straight_apostrophe"]),
        "severity_guess": "critical",
    },
    {
        "id": "RI-2",
        "title": "The merge gate takes \"merged\" and \"merging\" for the owner's word, so a status question such as \"Is #34 merged yet?\" authorises a merge.",
        "component": "lib/hooks/turngate.py MERGE_WORD (used by turn-gates-pretool.py, F2: owner message, click, assistant text)",
        "kind": "false_allow",
        "rule_quoted": "A PR merge (`*merge_pull_request`, `gh pr merge`) is denied unless \"merge\" (word) is in the owner's latest message, or in a clickable answer after it, or in the assistant's last text before that message together with the PR's number.",
        "rule_source": "lib/experiments/hypothesis-2026-10-29-turn-gates.md:22",
        "repro_command": REPRO + "RI-2",
        "repro_files": fx("ri2-is-34-merged-yet", "ri2-you-merged-without-asking", "ri2-nothing-gets-merged", "ri2-click-merged-already", "ri2-assistant-text-was-merged") + [W + "/mutate.py"],
        "observed": obs("ri2-") + "\n" + mut("M3-"),
        "expected": "deny:merge-word on every line marked <<<: none of these texts contains the word \"merge\". The fixture's own case says \"'mergeable' is not the word 'merge'\"; the code's pattern is \\bmerg(e|ed|ing)\\b.",
        "how_it_arises": "Ordinary owner messages: asking whether something is merged, or objecting that something was merged, is the natural wording after a PR is opened; \"Nothing gets merged without my word.\" also passes. The same pattern reads click options (\"Merged already\") and the assistant's own last text (\"#33 was merged; #34 is next.\" plus owner \"go\" allows #34). Real record (counts only): no real owner message contains merge, merged or merging (diag3.log: 0 of 17), but before 4 real merge calls the assistant's last text carried an inflection and not the word (diag.log: 0 literal, 1 inflected form; those calls passed on a real click). No fixture case needs the inflections: with the word alone (M3) the fixture still passes 44/44.",
        "severity_guess": "high",
    },
    {
        "id": "RI-3",
        "title": "Any tool output that contains the phrase \"questions have been answered\" counts as the owner's click: a GitHub notification body, a fetched page, or a Read of the library's own selftest file authorises a merge.",
        "component": "lib/hooks/turngate.py events() line 134 and answer_choices() line 199 (used by turn-gates-pretool.py, F2)",
        "kind": "false_allow",
        "rule_quoted": "\"\"\"The chosen options of an AskUserQuestion answer (\"question\"=\"choice\"), never the question text.\"\"\"  /  if \"questions have been answered\" in t:   # an AskUserQuestion answer: the owner's own click",
        "rule_source": "lib/hooks/turngate.py:198 (docstring) and :134 (comment); lib/experiments/hypothesis-2026-10-29-turn-gates.md:22 (\"in a clickable answer after it\")",
        "repro_command": REPRO + "RI-3",
        "repro_files": fx("ri3-github-notification-body", "ri3-read-of-own-selftest", "ri3-webfetch-page", "ri3-bash-cat-of-catalog") + [W + "/mutate.py", W + "/diag3.log"],
        "observed": obs("ri3-") + "\n" + mut("M7-") + "\ndiag3.log results_holding_the_answer_phrase_by_tool: " + json.dumps(d3["results_holding_the_answer_phrase_by_tool"], sort_keys=True),
        "expected": "deny:merge-word on every line marked <<<: the owner's message has no merge word and none of these results answers an AskUserQuestion call. Only the two control rows are clicks.",
        "how_it_arises": "events() never checks which tool produced a result: the phrase anywhere in any tool_result makes it an 'answer', and every =\"...\" in that text is taken as a chosen option. (1) A ReadNotifications result with a GitHub origin is an ordinary row (the real record holds 60 GitHub notification headers) and its own lead says bodies are 'external content relayed verbatim': anyone who can comment on a subscribed PR can put the sentence there. (2) lib/hooks/selftest-turn-gates.py and its plugin copy hold the phrase and three =\"...Merge...\" strings, so a Read (or cat, grep, git diff) of that file in a turn is enough; sessions that work on the hooks do this. (3) Real record: besides the 10 real answers, 1 Bash result already carries the phrase (it happened to hold no merge choice). Text that arrives JSON-escaped does not trigger (last row). Requiring the harness lead at the start (M7) still passes the fixture 44/44. My implementation ties a click to an AskUserQuestion call by tool_use_id and denies all four.",
        "severity_guess": "high",
    },
    {
        "id": "RI-4",
        "title": "The owner's word is not tied to the merge it is used for: \"No\" in reply to \"Shall I merge #34?\" passes, and \"Merge 34. Leave 141 alone\" lets #141 through.",
        "component": "lib/hooks/turngate.py merge_authorized() (F2), and the stated rule itself",
        "kind": "ambiguity",
        "rule_quoted": "\"\"\"F2: the owner's word for THIS merge — in their latest message, in a click after it, or in the\n    assistant's last text before their message together with the PR's number.\"\"\"  /  `turn-gates-pretool.py` **F2** (a PR merge is denied without the owner's word)",
        "rule_source": "lib/hooks/turngate.py:203-204; lib/hooks/README.md:15; lib/experiments/hypothesis-2026-10-29-turn-gates.md:22",
        "repro_command": REPRO + "RI-4",
        "repro_files": fx("ri4-owner-says-no-wait", "ri4-incident-shape-with-the-word", "ri4-stale-text-two-turns-later", "ri4-same-sentence-merging-26", "ri4-merge-34-not-141", "ri4-click-library-only-merging-141") + [W + "/mutate.py", W + "/diag.log"],
        "observed": obs("ri4-") + "\n" + mut("M12-"),
        "expected": "By the headline (\"denied without the owner's word\", \"the owner's word for THIS merge\") every line marked <<< is a deny. By the detailed sentence (hypothesis:22) they are allows: clause 3 never reads the owner's reply and clauses 1-2 never read which PR. The documents contradict each other; the code follows the detailed sentence, and so does my implementation (it allows the same cases except one).",
        "how_it_arises": "Ordinary rows only (assistant text, owner string, card answer). (a) The assistant asks \"Shall I merge #34?\" and the owner answers \"No, wait until tomorrow.\": allowed. (b) The incident the docstring names (note says awaiting the owner's call, owner writes \"I've uploaded, proceed\") is allowed as soon as the note says \"ready to merge\" and \"#26\"; the fixture's R5 text passes only because it says \"mergeable\" and \"PR 26\". (c) pack/real-text-recording.txt: 4 of 14 assistant texts of 2026-11-12 were not recorded, so 'the last text' can be several turns old (stale-text case). (d) With two PRs open, as on 2026-11-12 (#34 and #141 in one card), a word or a click for one passes the other; the fixture pins \"don't merge #26, merge #27\" for #27, and #26 passes on the same sentence. Real record (diag.log, counts only): 2 of the 17 real merge calls (#29, #156, turn from 2026-10-21T23:25) passed on clause 3 alone, with no word and no click from the owner; the other 15 passed on a click, none on a word in the owner's message. A reply check (M12) still passes the fixture 44/44.",
        "severity_guess": "high",
    },
    {
        "id": "RI-5",
        "title": "An owner message that merely contains a harness marker string is thrown away, and when no owner message is left both gates switch off.",
        "component": "lib/hooks/turngate.py owner_index() line 72; turn-gates-pretool.py lines 42-43; governance-enforce.py line 77",
        "kind": "false_allow",
        "rule_quoted": "\"\"\"Index of the owner's latest message, or -1. Harness-written user rows are skipped.\"\"\"",
        "rule_source": "lib/hooks/turngate.py:66",
        "repro_command": REPRO + "RI-5",
        "repro_files": fx("ri5-newer-message-quotes-marker", "ri5-only-message-quotes-marker", "ri5-session-started-by-slash-command", "ri5-stop-only-message-quotes-marker", "ri5-stop-session-started-by-slash") + [W + "/mutate.py", W + "/diag3.log"],
        "observed": obs("ri5-") + "\n" + mut("M9-", "M10-"),
        "expected": "A message the owner typed is the owner's latest message whatever it quotes: deny:merge-word (none of these messages asks for a merge) and block:F1. With no owner message at all there is no owner word, so a merge is denied; the code exits 0 (allow) when the index is -1 and skips F1.",
        "how_it_arises": "owner_index() drops a user row when ANY marker occurs ANYWHERE in its text (\"[SYSTEM NOTIFICATION\", \"<task-notification>\", \"<wake \", \"<agent-message\", \"<webhook-payload\", \"<command-name>\", \"<local-command-stdout>\", \"<local-command-caveat>\"). An owner who pastes hook output or asks about one of these tags (this owner builds these hooks) has that message ignored: an older \"merge it\" is honoured over a newer \"do not merge\", and if it was the only message F2 allows every merge and F1 is skipped. Unusual input, plain string rows. Second route: a session whose only owner input is a slash command; the catalog has one real isMeta row starting <command-message>, but the <command-args> line in my fixture is not confirmed by the catalog. Real record: the original filter and mine pick the same 17 owner messages (diag3.log), so no real instance. Matching the marker at the start only (M9), or denying a merge when no owner message exists (M10), still passes the fixture 44/44.",
        "severity_guess": "high",
    },
    {
        "id": "RI-6",
        "title": "The Stop gate does not see a commit or push written with a git option before the subcommand (git -c ..., --no-pager, a quoted -C path), nor a scheduled task made with CronCreate or send_later.",
        "component": "lib/hooks/turngate.py OUTWARD_BASH (line 28) and OUTWARD_TOOL_SUFFIXES (lines 26-27), used by governance-enforce.py F1",
        "kind": "false_allow",
        "rule_quoted": "If the turn took an OUTWARD action — git commit/push, `gh pr create/merge`, a PR create/update/merge, a file push, a scheduled-task create/update/delete — then plan-gate must have loaded before the first such action and adversarial-verify after it. Independent of how the prompt is worded.",
        "rule_source": "lib/experiments/hypothesis-2026-10-29-turn-gates.md:21",
        "repro_command": REPRO + "RI-6",
        "repro_files": fx("ri6-commit-with-identity-flags", "ri6-commit-gpgsign-off", "ri6-push-with-config-flag", "ri6-cron-create", "ri6-send-later") + [W + "/mutate.py", W + "/diag3.log"],
        "observed": obs("ri6-") + "\n" + mut("M13-", "M14-"),
        "expected": "block:F1 on the commit, push and scheduled-task lines: each is an ungoverned outward action of a kind the rule names. For gh pr edit, update_pull_request_branch and enable_pr_auto_merge the rule names no tool (\"a PR ... update\"): those three lines are the rule being silent, and my choice.",
        "how_it_arises": "The shell pattern is \\bgit\\s+(-C\\s+\\S+\\s+)?(commit|push)\\b: any other option between git and the subcommand hides the action. git -c user.name=... -c user.email=... commit and git -c commit.gpgsign=false commit are common where no identity or signing key is configured. The tool list knows only *_trigger for scheduling; CronCreate and send_later are in pack/session-tools.txt. Real record (diag3.log, counts only): %d commit and %d push invocations, none with a global option, and no CronCreate or send_later call, so this record does not show the missed spellings; F1 verdicts agree at all 26 real stop points. The fixture pins little of the list: with git -c accepted (M13), or with update_pull_request, the file-push tools and the three trigger tools REMOVED from the outward list (M14), it still passes 44/44." % (d3["counts"].get("git_commit_invocations", 0), d3["counts"].get("git_push_invocations", 0)),
        "severity_guess": "high",
    },
    {
        "id": "RI-7",
        "title": "\"A scheduled run never merges\" holds for two spellings only: enable_pr_auto_merge (a tool the session has, not even routed to the hook), gh with a flag between \"pr\" and \"merge\", and the API route all pass.",
        "component": "lib/hooks/turngate.py is_merge() / MERGE_BASH (lines 34, 170-172); lib/.claude/settings.json and lib/plugin/core-governance/hooks/hooks.json PreToolUse matcher",
        "kind": "false_allow",
        "rule_quoted": "`turngate.py` gains `turn_start()`: a scheduled\n> run is a turn of its own, and never merges  /  # A scheduled run carries no owner message, so it carries no owner word to merge: it never merges.  /  told to the owner: \"It never merges (the new hook enforces that)\"",
        "rule_source": "lib/hooks/README.md:1-2; lib/hooks/turn-gates-pretool.py:45; pack/pr34-and-claims.md claim 9",
        "repro_command": REPRO + "RI-7",
        "repro_files": fx("ri7-sched-enable-auto-merge-tool", "ri7-sched-gh-repo-flag-first", "ri7-sched-gh-api-put", "ri7-ok-enable-auto-merge-tool"),
        "observed": obs("ri7-", "wiring", "session-tools.txt"),
        "expected": "deny:scheduled inside a scheduled run and deny:merge-word on \"ok\" for every route that merges a PR. `gh pr -R nic/lib merge 34` is a `gh pr merge` call, so that line breaks the rule as written; for auto-merge and the API route the documents name no form (they say \"never merges\" without limit), so those lines are the documents overclaiming.",
        "how_it_arises": "is_merge() knows a tool name ending merge_pull_request and the three words gh, pr, merge directly in a row. mcp__github__enable_pr_auto_merge is listed in pack/session-tools.txt and is not in the PreToolUse matcher of either wiring file, so the hook is never called for it. Limits I could not check (no GitHub call allowed): auto-merge works only where the repository allows it and a requirement is pending; gh is not installed in the owner's cloud session (session-tools.txt) though it may be on the owner's computer; the curl route needs a token. Both implementations also miss a merge run from a script file or through a shell variable (corpus pre-form-script-file-ok, pre-form-var-indirection-ok: allow).",
        "severity_guess": "medium",
    },
    {
        "id": "RI-8",
        "title": "Both gates match words, not commands: the only merge denial in the real-session replay falls on a 14-line command that runs cd, grep and python3, and a grep, an echo or a commit message that mentions the words is denied or counted as an outward action.",
        "component": "lib/hooks/turngate.py MERGE_BASH (line 34) and OUTWARD_BASH (line 28); governance-enforce.py F1 (no look at the call's result)",
        "kind": "false_block",
        "rule_quoted": "A PR merge (`*merge_pull_request`, `gh pr merge`) is denied unless \"merge\" (word) is in the owner's latest message ...  /  If the turn took an OUTWARD action — git commit/push, `gh pr create/merge`, ...",
        "rule_source": "lib/experiments/hypothesis-2026-10-29-turn-gates.md:22 and :21",
        "repro_command": REPRO + "RI-8",
        "repro_files": fx("ri8-grep-for-the-words", "ri8-commit-message-mentions", "ri8-heredoc-to-python", "ri8-stop-grep-git-commit", "ri8-stop-merge-denied-by-F2") + [W + "/diag2.log", W + "/mine-diag2/turn-gates-pretool.py", W + "/diag3.log"],
        "observed": obs("ri8-", "{\"command_chars\"") + "\ndiag3.log counts: " + json.dumps(d3["counts"], sort_keys=True),
        "expected": "allow on every line marked <<<: none of these commands merges a PR, commits or pushes, and a merge call the gate itself denied did not take an outward action (on that last point the rule is silent).",
        "how_it_arises": "Both patterns are searched over the whole command text. Real record: pack/replay-baseline.txt shows one merge:DENY:merge-word (turn from 2026-10-28T23:16). Replayed through a diagnostic hook that logs categories only (diag2.log; rerun: python3 <PACK>/pack/tools/replay_real.py --hooks <PACK>/work/reimpl/mine-diag2 --what pre), that call is a 986-character, 14-line Bash command whose programs are cd, grep and python3, with both hits of the three words inside a here-document body: not a merge. It is the only real call on which the two implementations disagree (92 of 93 agree). Over the record, %d of %d real Bash commands count as outward for the original and run no commit, push or gh by my parser. Anyone working on this library's hooks, tests or documents writes such commands. Consequence is limited: one denied command to reword, or one forced governor load. The last synthetic line assumes a hook-denied call is recorded as a tool_use plus an error result; I could not run a live session to confirm that shape." % (d3["counts"].get("bash_outward_original_only", 0), d3["counts"].get("bash_calls", 0)),
        "severity_guess": "medium",
    },
]

covered = [
    "F1 (Stop gate outward-action rule), synthetic: %d transcripts run through lib/hooks and through my re-implementation (86 tool calls x 2 governor patterns, 6 core actions x 13 load patterns, 27 row kinds x 3 positions, 13 owner-message shapes x 2, 12 notification variants x 2, 21 misc, 14 hand-written)" % n_stop,
    "F2 (merge-word gate and scheduled-run rule), synthetic: %d transcripts (92 owner messages + 18 across tool forms, 43 negation-word probes, 27 window and separator probes, 54 tool-call forms x 2 + 5 broken-transcript cases, 24 click cases, 34 assistant-text cases, 27 row kinds x 2, 13 owner shapes x 2, 12 notification variants x 4 + 3, 12 hand-written)" % n_pre,
    "Hand-written known answers from the stated rule (READING.md section D): 26 cases; lib/hooks 26/26, mine 26/26",
    "Real record, Stop: 26 real stop points replayed through my hook (replay_real.py --what stop); F1 verdict agrees 26/26 with pack/replay-baseline.txt",
    "Real record, PreToolUse: 93 real write/merge calls replayed through my hook; 92 agree, 1 differs (explained in RI-8)",
    "Real record, clause-level diagnostics (counts and categories only): 17 merge calls (diag.log), 1 disputed call (diag2.log), 26 stop points (diag3.log)",
    "Targeted reproductions: 90 fixtures in repro-fixtures/ (repro.py RI-1 ... RI-8, EXTRA), each section with controls of known answer",
    "Mutation check of hooks/selftest-turn-gates.py: 15 runs from scratch copies (mutate.py): 1 unchanged control passes, 2 controls caught, 1 more caught, 11 behaviour changes still pass 44/44",
    "Other hook sets on the same 910 cases: lib/plugin/core-governance/scripts (0 differ from lib/hooks), kit-full/hooks (0), deck-full/hooks (0), kit/hooks (0), deck/hooks (0), account plugin 0.1.4 (34 differ, all scheduled-run cases)",
    "Wiring of the pre-tool hook: PreToolUse matcher of lib/.claude/settings.json and of the plugin hooks.json evaluated against 2 tool names (RI-7)",
]

not_covered = [
    "F3 (plan-shown advisory), the prompt-class rule of governance-enforce.py, receipt-law-stop-gate.sh, governance-trigger.py, session-doctrine.sh, the two reminder hooks, run-unless-project-wired.sh: outside this brief, not tested",
    "A live session: whether the pending tool call is already a transcript row when PreToolUse fires, how a hook-denied call is recorded, tool calls made by a subagent, how a fresh-session scheduled run or a create_session child records its prompt (no live or scheduled run allowed)",
    "pack/diff.patch and pack/deck-pr141.patch: never opened; I compared behaviour of the merged files, not the change itself",
    "hooks/selftest-turn-gates.py: run and searched by line, not read in full",
    "sent/ packages and account skill copies: not unzipped, not compared",
    "Hook run time and the 10 s / 15 s timeouts",
    "How the real harness evaluates a matcher string (I evaluated it as a Python regular expression)",
]

not_verified = [
    "Slash-command turns: the catalog shows one real isMeta row starting <command-message>workflow-authoring; whether owner-typed arguments sit in that row (<command-args>) is not shown, so the slash-command lines of RI-5 use a shape I extrapolated",
    "A mid-turn owner message delivered as a queued_command attachment with origin.kind human is invisible to the original (repro.py EXTRA x-queued-owner-message-mid-turn: allow); that origin occurs 0 times in the real record, so I cannot show the harness writes it",
    "Rows such as <child-session-event>, \"[Artifact comment sent to Claude]\" or \"[Request interrupted by user]\" are not in the marker list and would be taken for owner messages if the harness writes them as plain user rows; none is in the catalog (corpus stop-own-interrupt-*: the original treats the interrupt text as an owner message)",
    "Whether enable_pr_auto_merge would actually merge on the owner's repositories (needs the repository's auto-merge setting and a pending requirement; no GitHub call allowed)",
    "Whether a merge denied by F2 is recorded as a tool_use row followed by an error tool_result (assumed in ri8-stop-merge-denied-by-F2)",
    "Whether the weekly task's session will run plugin 0.1.5 by 2026-11-16: pack/trigger-prompt.md says it runs the account plugin (0.1.4 today); on my corpus 0.1.4 allows the merge in every scheduled-run case (repro.py EXTRA x-account-plugin-scheduled)",
]

notes = (
    "Agreement, synthetic corpus: 787 of 910 cases (Stop 376 of 416, pre-tool 411 of 494). Agreement, real replay: Stop 26 of 26 stop points on the F1 verdict; pre-tool 92 of 93 real calls (prompt-class blocks and advisories ignored). "
    "The 123 synthetic differences by cause: 64 where the code departs from a stated rule (negation list and apostrophe 29, word forms 8, click source 3, marker anywhere 4, git options 2, shell wording 13, scheduled header from a non-notification result 4, crash on a non-object line 1); 57 where the rule is silent or contradicts itself and the code and I chose differently (the size of 'few' 3, extra negations hold off / wait before 2, forms the rule names no command or tool for (dry-run, gh pr edit, API merge, CronCreate / CronDelete / send_later, branch update, auto-merge) 15, owner-message shapes not named by the rule 22, no owner message 3, failed or denied call 2, orphan header 4, number format 6); 2 my own choices on shapes the harness never writes (Skill input key, leading slash). "
    "Where my reading was the weaker one: my three-word window denies the fixture's pinned control \"don't merge #26, merge #27\" (merging #27), and my number test accepts a PR number inside a date. "
    "Process: READING.md was written before any code; diff-run-1.txt (synthetic) was saved before I opened turngate.py, governance-enforce.py or turn-gates-pretool.py, and the replay section was appended before I opened them; pack/tools/mk.py was read in full beforehand (it is the fixture builder and shows five known answers). I never opened pack/diff.patch, pack/deck-pr141.patch or records/. The replay tool ran three diagnostic hooks of mine over the private record; they wrote only counts, booleans, PR numbers, tool names, option names and the program names cd, grep, python3 (diag.log, diag2.log, diag3.log), no transcript text. No hook denied any of my tool calls. lib/hooks/__pycache__ already existed (written 21:46:20, before my directory was created); my runs set PYTHONDONTWRITEBYTECODE=1. Observed lines are verbatim with runs of padding spaces collapsed. "
    "\nMORE: A scheduled-run boundary is taken from ANY tool result with a header line, not only ReadNotifications: repro.py EXTRA x-header-printed-by-bash gives deny:scheduled on the owner's own \"merge it\", and corpus stop-sched-sched-text-via-bash-i lets an ungoverned push before it go unjudged. No file in lib/, kit-full/ or deck-full/ holds such a line at line start, so it needs an unusual output; M8 still passes the fixture. "
    "\nMORE: A header line inside a GitHub notification body (external text) moves the boundary in both implementations: x-header-inside-github-body denies the owner's merge, x-stop-header-inside-github-body lets an ungoverned push pass F1. The stated regex cannot tell a body line from a header. "
    "\nMORE: test_gap: mutate.py changes 12 behaviours one at a time; the fixture (44 cases) still passes for 11 of them (M3 word forms, M4 window, M6 apostrophe and contractions, M7 click lead, M8 notification lead, M9 marker position, M10 no owner message, M11 number without '#', M12 reply check, M13 git -c, M14 file-push and scheduled-task tools removed from the outward list). Controls M1 and M2 are caught. hooks/README.md:18 says the gates are \"Pinned by `selftest-turn-gates.py`\". "
    "\nMORE: drift: the account plugin 0.1.4 has no scheduled-run rule: 34 of 910 corpus cases differ from the merged hooks, all scheduled (x-account-plugin-scheduled: allow). pack/trigger-prompt.md says the weekly task's session runs that plugin; claim 10 told the owner so, and claim 9 (\"the new hook enforces that\") is true only after the upload. "
    "\nMORE: After any Stop-hook block in a turn, F1 is not evaluated again (stop_hook_active): x-stop-push-after-an-earlier-stop-block allows an ungoverned commit and push made in the forced continuation, in both implementations (the stated 'single retry'). "
    "\nMORE: A card \"Merge PR #34 now?\" answered \"Yes (Recommended)\" is denied in both implementations (x-card-merge-34-answered-yes), as the rule says; the deny message does not tell the assistant that the option label must carry the word. "
    "\nMORE: Clause 3 needs \"#34\": \"Ready to merge PR 34.\" or a pull URL does not count (x-number-without-hash: deny), stricter than \"together with the PR's number\"; M11 still passes the fixture. "
    "\nMORE: governance-enforce.py exits 1 with a traceback on a transcript line that is valid JSON but not an object (corpus stop-misc-nondict-line: exit1); not a real row shape, and exit 1 does not block. "
    "\nMORE: `gh pr merge --help` is denied on \"ok\" (corpus pre-form-gh-help-ok); trivial."
)

report = {"findings": findings, "covered": covered, "not_covered": not_covered, "not_verified": not_verified, "notes": notes}
with open(os.path.join(W, "findings.json"), "w") as fh:
    json.dump(report, fh, indent=1, ensure_ascii=False)
print("findings:", len(findings), "| stop cases:", n_stop, "| pre cases:", n_pre)
for f in findings:
    assert f["observed"].strip(), f["id"]
    print("----", f["id"], f["kind"], f["severity_guess"])
    print(f["observed"])
