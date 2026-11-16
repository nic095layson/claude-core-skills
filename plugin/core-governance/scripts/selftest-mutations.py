#!/usr/bin/env python3
"""The standing list of deliberate breaks of the turn gates and of the receipt gate, and its runner.

A test table that passes proves little by itself: it also has to fail when the code is wrong. Each break below
is ONE text replacement in one file (turngate.py, turn-gates-pretool.py, governance-enforce.py, receiptlaw.py,
receipt-law-stop-gate.sh, the project's wiring file or the plugin's). The runner copies the hooks and both wiring
files (the plugin's with its wrapper), applies one break to the copy, and runs the test table
(selftest-turn-gates.py) on it: the cases named for the break first and, if none of them fails, the whole table.

    python3 hooks/selftest-mutations.py [--hooks DIR] [--jobs N] [--list] [--every-case] [--work DIR] [id ...]

One line per break, then the counts:

    id | file | caught by <case> | the rule the break removes
    == N breaks: C caught, S survived, T stale; control: 0 failing of M cases ==

  caught     at least one case fails on the broken copy (the first failing case is named)
  SURVIVED   every case still passes: the table does not test the rule, or the code path is dead
  STALE      the text to replace is not found exactly once: the code moved on and the break must follow it
  ERROR      the table could not be run on the copy
  not run    the break is of a wiring file this layout does not have (the plugin's, in a project without it)

The control is the same run with no change; it must show 0 failing cases. Exit status 0 only when the control
is clean and every break is caught (a break of a wiring file the layout does not have is not run). `--list` prints the list and runs nothing. `--every-case` runs the whole
table for every break and prints every case that catches it (slow; for choosing the named cases). `--work DIR`
keeps the copies. An id, or the start of one, selects breaks.

When a rule changes on purpose, the break that pins the old rule goes STALE or SURVIVES here: rewrite the break
for the new rule (or remove it and say why in the commit), never the other way round.

`origin` says where a break comes from: "B:" and "A:" are the two break lists of the designs behind the
specification (results/2026-11-15/turn-gates-fix/CORE-SPEC.md, section 6.3), the rest are the recorded
mutations of the findings and the cases of the new rules. The breaks RC.. and RD.. are the receipt gate's: the
13 mutations the audit recorded for it (finding RL-8, "RL-8 Mnn"), one for every hand-set value of receiptlaw.py
and one for every rule of it that is not a value. The breaks RE.. are the same for the rules the prose scan added.

Standard library only; imports nothing; runs on Python 3.8 and later. Needs no git program and no network.
"""
import concurrent.futures
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True        # this folder is copied byte for byte: a run leaves no cache file in it

# ------------------------------------------------------------------ hand-set values of the runner
TG, PRE, ENF = "turngate.py", "turn-gates-pretool.py", "governance-enforce.py"
RCP, RCW = "receiptlaw.py", "receipt-law-stop-gate.sh"       # the receipt gate: its module and its wired script
WIRING = "wiring"                     # the project's wiring file (.claude/settings.json)
PLUGIN_WIRING = "plugin-wiring"       # the plugin's wiring file (hooks/hooks.json of the plugin)
TABLE_SCRIPT = "selftest-turn-gates.py"
WIRING_PLACES = {WIRING: (os.path.join("..", ".claude", "settings.json"),),
                 PLUGIN_WIRING: (os.path.join("..", "hooks", "hooks.json"),
                                 os.path.join("..", "plugin", "core-governance", "hooks", "hooks.json"))}
WIRING_COPIES = {WIRING: os.path.join("project", "settings.json"),      # the table tells the two apart by name
                 PLUGIN_WIRING: os.path.join("plugin", "hooks", "hooks.json")}
WRAPPER = "run-unless-project-wired.sh"   # copied with the plugin's wiring: the table runs its commands
HOOKS_COPY = "hooks"
CONTROL_ID = "control"
DEFAULT_JOBS = 4                      # breaks tested at the same time
NAMED_JOBS = 2                        # hooks run at the same time while the named cases of one break run
TABLE_JOBS = 4                        # the same for a whole-table run
TABLE_WAIT_SECONDS = 600              # a table run that takes longer than this has failed
FAIL_MARK = "| FAIL"
SUMMARY = re.compile(r"^== (\d+) cases: (\d+) pass, (\d+) fail ==$", re.M)
SHOWN_CASES = 6                       # how many catching cases `--every-case` prints by name

# ------------------------------------------------------------------ the breaks
# (id, file, the text to replace (found exactly once), its replacement, the rule it removes, the cases
#  expected to catch it, origin)
BREAKS = [
    # ---- rows: who wrote a row, and where turns, windows and stretches begin
    ("RW01", TG, '    if row.get("isCompactSummary"):\n        return "SUMMARY", False',
     '    if row.get("isCompactSummary"):\n        return "OWNER", True',
     "a compaction summary is not the owner's message",
     ("T25-compact-summary-is-not-owner", "P08-compact-summary-is-not-the-prompt"), "B:N02a A:B35; TB-8 M2, PC-7 M4"),
    ("RW02", TG, '        return ("WAKE" if has_origin else "META"), False', '        return "OWNER", True',
     "a row the program marks isMeta is not the owner's message", ("T26-meta-row-is-not-owner",), "B:N02b A:B02; TB-8 M2"),
    ("RW03", TG, '    if row.get("isSidechain") is True:\n        return "SIDECHAIN", False',
     '    if False:\n        return "SIDECHAIN", False',
     "a helper agent's row is never the owner's", ("G03-sidechain-prompt-is-not-owner",), "B:N48 A:B02b"),
    ("RW04", TG, '        return ("OWNER", True) if owner_origin else ("WAKE", False)', '        return ("OWNER", True)',
     "a row whose origin is not the owner's is a wake, not the owner",
     ("M20-card-click-inside-scheduled-run", "T28-peer-session-message-is-not-owner"), "B:N51; TB-8 C2"),
    ("RW05", TG, '    return "OWNER", (not strict)   # a row without', '    return "OWNER", True   # a row without',
     "a row without origin grants nothing in a record whose rows carry origin",
     ("T37-row-without-origin-in-a-file-that-has-origin",), "B:N50"),
    ("RW06", TG, '    if s.startswith(WAKE_LEADS):\n        return "WAKE", False',
     '    if any(lead in s for lead in WAKE_LEADS):\n        return "WAKE", False',
     "a harness lead counts only at the START of a row's text (rows)", ("F21-owner-quotes-marker-previous-turn-loaded",),
     "B:N25; reimpl M9"),
    ("RW07", TG, '    return (text or "").lstrip().startswith(HARNESS_MARKERS)',
     '    return any(lead in (text or "") for lead in HARNESS_MARKERS)',
     "a harness lead counts only at the START of a prompt (classifier)",
     ("P02a-build-prompt-quotes-notification-banner", "P02b-legacy-build-prompt-contains-marker"), "A:B07; reimpl M9"),
    ("RW08", TG, '                ev = Ev(i, "STOP_BLOCKED" if row.get("hookErrors") else "STOP_DONE")',
     '                ev = Ev(i, "STOP_DONE")',
     "a blocked stop (a stop row with hook errors) is not a completed stop",
     ("J01a-blocked-stop-real-order-merge", "J01b-blocked-stop-real-order-stop", "M27-blocked-stop-is-not-a-stop"),
     "B:N52 A:B58; new rule J01"),
    ("RW09", TG, '    if kind in OWNER_ORIGIN_KINDS and not flagged:\n        return Ev(i, "QUEUED_OWNER", text, True)',
     '    if False:\n        return Ev(i, "QUEUED_OWNER", text, True)',
     "a message the owner sends while the assistant works is read",
     ("T19-queued-owner-message-orders", "T20-queued-owner-message-refuses"), "B:N40 A:B42"),
    ("RW10", TG, "            elif idle and not local:", "            elif False:",
     "a slash command recorded as a harness row starts a turn when the session was idle",
     ("J03a-meta-slash-command-starts-turn-write", "J03b-meta-slash-command-starts-turn-commit"), "new rule J03"),
    ("RW11", TG, "            elif idle and not local:", "            elif not local:",
     "the arguments of a skill the assistant launched mid-turn are not the owner's prompt",
     ("p_ctl_assistant_skill_args_are_not_a_prompt",), "A:B66"),
    ("RW12", TG, "        self.stretch_start = max(self.last_owner, self.stops_done[-1] if self.stops_done else -1)",
     "        self.stretch_start = self.last_owner",
     "a stop judges only the rows since the latest completed stop",
     ("F34-miss-let-go-at-its-own-stop-is-not-raised-later",), "B:N37 A:B48"),
    ("RW13", TG, "        self.stretch_start = max(self.last_owner, self.stops_done[-1] if self.stops_done else -1)",
     "        self.stretch_start = self.gov_start",
     "the stretch starts at the owner's message or the last stop, not at the governance turn",
     ("J02-midturn-delivery-with-idle-nudge",), "new rule J02"),
    ("RW14", TG, 'bounds = rows_of("OWNER", "WAKE", "STOP_DONE", "INTERRUPT") + (', 'bounds = rows_of("OWNER", "INTERRUPT") + (',
     "the owner's word ends at a completed stop and at a wake", ("M16-click-then-stop-then-wake", "T30-order-then-stop-then-wake"),
     "B:N30"),
    ("RW15", TG, 'bounds = rows_of("OWNER", "WAKE", "STOP_DONE", "INTERRUPT") + (',
     'bounds = rows_of("OWNER", "WAKE", "INTERRUPT") + (',
     "the owner's word ends when the assistant stops", ("G02-helper-merge-after-main-stopped",), "A:B13"),
    ("RW16", TG, 'bounds = rows_of("OWNER", "WAKE", "STOP_DONE", "INTERRUPT") + (',
     'bounds = rows_of("OWNER", "STOP_DONE", "INTERRUPT") + (',
     "a wake row ends the owner's word", ("T30b-order-then-wake-with-no-stop-row",), "A:B63"),
    ("RW17", TG, 'bounds = rows_of("OWNER", "WAKE", "STOP_DONE", "INTERRUPT") + (',
     'bounds = rows_of("OWNER", "WAKE", "STOP_DONE") + (',
     "an interrupt ends the owner's word", ("T33-interrupt-after-order",), "A:B59"),
    ("RW18", TG, '        marks = [(r, "owner") for r in self.owner_rows] + [(r, "scheduled") for r in self.run_starts]',
     '        marks = [(r, "owner") for r in self.owner_rows]',
     "a scheduled run is a governance turn of its own",
     ("F16a-scheduled-run-ungoverned-commit", "P04b-legacy-scheduled-run-after-review-remark"),
     "A:B03 B:N07; TB-8 M10"),
    ("RW19", TG, "        self.turn_marks = sorted(marks)",
     '        self.turn_marks = sorted(marks, key=lambda mark: (mark[1] == "scheduled", mark[0]))',
     "the owner's message after a scheduled run starts the owner's turn",
     ("P17-owner-prompt-after-a-scheduled-run", "F29-owner-message-after-scheduled-run"), "B:N05 A:B05; TB-8 M5"),
    ("RW20", TG, "        if any(r >= self.auth_start and not self.midturn(r) for r in self.sched_reads):",
     "        if any(not self.midturn(r) for r in self.sched_reads):",
     "a past scheduled run does not mark the owner's later turn as scheduled", ("S11-owner-types-after-scheduled-run",),
     "A:B05b; TB-8 M5"),
    ("RW21", TG, "            if not self.midturn(r):", "            if True:",
     "a delivery read in the middle of an owner turn starts no scheduled run",
     ("F19b-midturn-read-does-not-cut-governed-turn", "S10b-midturn-scheduled-read-then-click"), "TB-3"),
    ("RW22", TG, "    parts += [(r - 1, r - 1, kind) for r, kind in cuts]",
     "    parts += [(parts[0][0], r - 1, kind) for r, kind in cuts]",
     "a scheduled run is judged on its own loads: the LATEST run governs, not an earlier turn",
     ("F28-two-scheduled-runs-latest-governs",), "B:N03 A:B03b; TB-8 M3"),
    ("RW23", TG, "    parts = [(max([r for r, _kind in model.turn_marks if r <= start] or [-1]), start, None)]",
     "    parts = [(-1, start, None)]",
     "governor loads made before the governance turn do not count (outward rule)",
     ("F22-loads-of-previous-turn-do-not-count",), "B:N19b; PC-7 M3"),
    # ---- scheduled deliveries
    ("SC01", TG, "    out, expect, total = [], 1, None",
     '    if SCHEDULED_ORIGIN_PREFIX in (text or ""):\n        return [SCHEDULED_ORIGIN_PREFIX]\n    out, expect, total = [], 1, None',
     "a scheduled delivery is known by its header line, not by the words anywhere",
     ("S14-origin-words-in-body-not-header", "S09-github-body-quotes-scheduled-header"), "B:N04 A:B04; TB-8 M4, reimpl M8"),
    ("SC02", TG, "        if i != expect or n != total:\n            continue", "        if False:\n            continue",
     "a header line quoted inside a notification body is body text", ("S09-github-body-quotes-scheduled-header",), "A:B65"),
    ("SC03", TG, '                    genuine = not use[3] and use[2].get("name") in NOTIF_READ_TOOLS',
     "                    genuine = True",
     "only the result of a notification read can deliver a scheduled run", ("S08-bash-prints-old-scheduled-header",),
     "A:B64"),
    ("SC04", TG, '    if word["scheduled"]:\n        named = ', '    if False:\n        named = ',
     "in a scheduled run a merge is always denied, with the scheduled-run reason",
     ("M20-card-click-inside-scheduled-run", "S01-scheduled-merge-tool"), "B:N31"),
    ("SC05", TG, "                may_grant = not scheduled           # a card answered inside a scheduled run grants nothing",
     "                may_grant = True",
     "a card answered inside a scheduled run grants nothing, also after the owner writes",
     ("S17-card-inside-run-then-owner-message",), "A:B14"),
    # ---- the owner's word: typed orders
    ("WD01", TG, "            if cue_any:\n                refs = pr_refs(c) | _bare_numbers(c[cue_any.end():])",
     "            if False and cue_any:\n                refs = pr_refs(c) | _bare_numbers(c[cue_any.end():])",
     "a refusal takes its pull requests out of the grant", ("T20-queued-owner-message-refuses", "T05d-dont-merge-26-comma-merge-27-call-26"),
     "B:N21; reimpl M1"),
    ("WD02", TG, "                cue = REFUSAL_CUE.search(rest)", "                cue = None",
     "a refusal inside an order (\"merge everything except #141\") is read", ("T15-merge-everything-except-141",),
     "reimpl M1"),
    ("WD03", TG, '                elif op[0] == "revoke":\n                    prs = set(g for g in prs if not any(_same_pr(g, x) for x in op[1]))',
     '                elif op[0] == "revoke":\n                    pass',
     "a later refusal of a named pull request takes its grant back",
     ("M24-click-wait-revokes-typed-order", "T20c-queued-curly-refusal-revokes"), "A:B43"),
    ("WD04", TG, '                if op[0] == "revoke_all":\n                    prs, branch = set(), False',
     '                if op[0] == "revoke_all":\n                    pass',
     "a bare refusal empties the grant", ("J06-order-then-refusal", "m_queued_stop_revokes_all"), "A:B43"),
    ("WD05", TG, "                elif len(c.split()) <= STANDALONE_REFUSAL_MAX_WORDS and REFUSAL_START.match(c):",
     "                elif False:",
     "a short refusal with no verb (\"No wait.\", \"stop\") empties the grant",
     ("m_queued_stop_revokes_all", "J06-order-then-refusal"), "A:B72"),
    ("WD06", TG, 'MERGE_VERB_TEXT = r"(?:(?:auto|squash|rebase)[- ]?)?merge"',
     'MERGE_VERB_TEXT = r"(?:(?:auto|squash|rebase)[- ]?)?merg(?:e|ed|ing)"',
     "\"merged\" and \"merging\" are not the order to merge", ("M26-click-merged-already",), "B:N23 A:B10; reimpl M3"),
    ("WD07", TG, '("’", "\'"), ', "",
     "a curly apostrophe is read as an apostrophe", ("T06-curly-dont-merge", "T20c-queued-curly-refusal-revokes"),
     "B:N24 A:B09; reimpl M6"),
    ("WD08", TG, 'TYPED_ORDER = re.compile(r"^" + ORDER_LEADIN + r"(" + MERGE_VERB_TEXT + r")(?![\\w-])")',
     'TYPED_ORDER = re.compile(r"^.*?(" + MERGE_VERB_TEXT + r")(?![\\w-])")',
     "an order starts its clause: the verb somewhere in a clause is not an order",
     ("T06-curly-dont-merge", "T05a-do-not-merge-34-merge-35-call-34"), "A:B08; reimpl M4, M5"),
    ("WD09", TG, 'r"|(?:\\b(?:prs?|pull requests?|pull)\\s*(?:number\\s*|no\\.?\\s*)?#?\\s*(?P<pn>\\d+))"',
     'r"|(?:\\bZZZZ(?P<pn>\\d+))"',
     "\"PR 34\" names a pull request without the hash sign",
     ("M08-number-without-hash-in-question", "T13-please-merge-pr-34-and-pr-141"), "B:N26; reimpl M11"),
    ("WD10", TG, "                named = _object_refs(head)", "                named = pr_refs(c)",
     "an order names only the list that follows its verb, not every number in the clause", ("T16d-merge-34-and-close-35",),
     "B:N27"),
    ("WD11", TG, "    return grant[1] == call[1] and (", "    return (grant[1] == call[1] or True) and (",
     "the word covers only the pull requests it names", ("M02-card-for-34-141-call-35", "T01b-typed-merge-34-call-35"),
     "B:N29 A:B12"),
    ("WD12", TG, "(grant[0] is None or call[0] is None or grant[0].lower() == call[0].lower())", "(True)",
     "a word that names a repository covers that repository only", ("T35-url-of-other-repo",), "new rule T35"),
    ("WD13", TG, "                if DEFER_CUE.search(rest):\n                    continue",
     "                if False:\n                    continue",
     "an order for later or under a condition is no order for now",
     ("m_conditional_order_is_not_for_now", "T16b-merge-34-after-you-fix-35-call-34"), "A:B53"),
    ("WD14", TG, "                if question and not POLITE_REQUEST.match(c):\n                    continue",
     "                if False:\n                    continue",
     "a question is not an order", ("m_question_form_is_no_order",), "A:B52"),
    ("WD15", TG, "                if negator and not MERGE_ANY.search(c[negator.end():]):\n                    open_neg = True",
     "                if negator and not MERGE_ANY.search(c[negator.end():]):\n                    open_neg = False",
     "a negation whose verb comes in a later clause still negates it", ("J05-open-negation", "T05e-dont-under-any-circumstances-merge-34"),
     "new rule J05"),
    ("WD16", TG, '            for op in ops:\n                if op[0] == "revoke_all":',
     '            for op in sorted(ops, key=lambda item: item[0] == "grant"):\n                if op[0] == "revoke_all":',
     "the operations of one message apply in the order they were said", ("J06-order-then-refusal",), "new rule J06"),
    ("WD17", TG, "    for phrase in AFFIRMATIVE_PHRASES:", "    for phrase in ():",
     "\"no rush\", \"no objections\" and their like refuse nothing", ("J07-affirmative-no", "m_f2_8d_no_objections_merge"),
     "new rule J07"),
    ("WD18", TG, '            if ev.kind == "OWNER" and ev.i == self.auth_start:\n                ops, may_grant = typed_ops(ev.text), ev.grantable',
     '            if ev.kind == "OWNER" and ev.i == self.auth_start:\n                ops, may_grant = typed_ops(ev.text) + [("grant", pr_refs(normalize('
     '" ".join(self.evs[ev.i - 1].says))))] * (ev.i > 0), ev.grantable',
     "the assistant's own text grants nothing", ("T03-yes-after-offer",), "A:B11; reimpl M12"),
    ("WD19", TG, '    if not word["log"]:\n        return _deny("no-owner-word", REASON_NO_OWNER_WORD)',
     '    if not word["log"]:\n        return True, "ok", ""',
     "a merge with no owner word in the window is denied", ("T22-file-starts-at-compaction", "T21c-legacy-local-command-echo-only"),
     "B:N01 A:B01; TB-8 M1, reimpl M10"),
    ("WD20", TG, '    if gated and not readable:\n        return _deny("no-record", REASON_NO_RECORD)',
     '    if gated and not readable:\n        return True, "ok", ""',
     "a merge with no readable record is denied", ("T23a-empty-transcript", "T23c-transcript-missing", "J15a-diskless-merge"),
     "A:B01a; F2-7, TB-1"),
    ("WD21", TG, '        elif not word["default_branch"]:', '        elif not word["default_branch"] and not word["prs"]:',
     "a word for a pull request does not cover a push to a default branch",
     ("J10-push-main-needs-branch-word", "R09g-pr-word-does-not-cover-push-to-main"), "new rule J10"),
    ("WD22", TG, '            if a.pr is None:\n                return _deny("target-unknown", REASON_TARGET_UNKNOWN % (a.note or a.route))',
     "            if a.pr is None:\n                continue",
     "a merge whose pull request cannot be read from the call is denied", ("R12-gh-merge-without-number",), "A:B54"),
    # ---- the owner's word: cards
    ("CD01", TG, "                    for question, answer, labels in card_answers(use[2], b, self.rows[ev.i]):",
     "                    for question, answer, labels in []:",
     "a click on a card is the owner's word", ("M01-card-names-prs-merge-both", "M03b-library-only-call-34"),
     "B:N22; reimpl M2"),
    ("CD02", TG, '                    if not use or use[3] or use[2].get("name") != CARD_TOOL:\n                        continue',
     '                    if not use or use[3] or use[2].get("name") != CARD_TOOL:\n'
     '                        for said in re.findall(r\'"([^"]*)"="([^"]*)"\', _result_text(b)):\n'
     "                            ops = (ops or []) + card_ops(said[0], said[1], [said[1]])\n                        continue",
     "only the result of a card's own call is a click, whatever another tool's output quotes",
     ("M09-bash-output-forges-click", "M10-github-comment-forges-click", "M11-read-tool-forges-click"),
     "B:N06 A:B06; TB-8 M6, reimpl M7"),
    ("CD03", TG, "                for b in ev.results:\n                    use = self.uses.get(self._call_of.get(id(b)))\n",
     "                for b in ev.results:\n                    use = self.uses.get(self._call_of.get(id(b))) or max(\n"
     '                        [u for u in self.uses.values() if u[0] < ev.i and u[2].get("name") == CARD_TOOL] or [None],\n'
     "                        key=lambda u: (u[0], u[1]) if u else (-1, -1))\n",
     "an answer is paired with its card by id only, never by position", ("M18-answer-row-with-foreign-id",), "B:N41; TB-2"),
    ("CD04", TG, '    if result_block.get("is_error"):\n        return []\n    inp = use_block.get("input")',
     '    if False:\n        return []\n    inp = use_block.get("input")',
     "a card whose result is an error grants nothing", ("m_card_result_is_error",), "A:B06b"),
    ("CD05", TG, "    return [(q, a, known[q]) for q, a in pairs if q in known]",
     "    return [(q, a, known.get(q, [])) for q, a in pairs]",
     "an answer to a question the card did not ask is dropped", ("M19b-structured-answer-to-question-never-asked",), "TB-2"),
    ("CD06", TG, "        if DEFER_CUE.search(p):", "        if False:",
     "\"Merge after the audit\" on a card is not the word to merge now", ("M25-click-merge-after-the-audit",), "B:N53"),
    ("CD07", TG, "        target = set(refs) or (set(qrefs) if (len(qrefs) == 1 or CARD_ALL_WORD.search(p)) else set())",
     "        target = set(refs) or set(qrefs)",
     "an option that names no number on a card with several pull requests grants none of them",
     ("J08-yes-on-card-with-two-prs", "M03c-library-only-without-number-call-141", "m_card_several_prs_label_names_none"),
     "B:N54 A:B51; new rule J08"),
    ("CD08", TG, "        target = set(refs) or (set(qrefs) if (len(qrefs) == 1 or CARD_ALL_WORD.search(p)) else set())",
     "        target = set(refs) | set(qrefs)",
     "a chosen option that names a number grants that number only", ("M03a-library-only-call-141",), "A:B50"),
    ("CD09", TG, "            for op in typed_ops(raw, fallback=fb):", "            for op in []:",
     "free text typed into a card is read as a typed message", ("m_d1_card_free_text_order", "M14-free-text-answer-merge-it"),
     "A:B44; reimpl M2"),
    ("CD10", TG, 'ANSWER_LEADS = ("Your questions have been answered:", "The user answered:")',
     'ANSWER_LEADS = ("Your questions have been answered:",)',
     "the second form of a card's answer text is read", ("J12-free-text-answer-second-form",), "new rule J12"),
    ("CD11", TG, "        if REFUSAL_CUE.search(_strip_affirmative(p)):", "        if False:",
     "a chosen option that refuses (\"Merge neither\", \"Wait\") grants nothing and takes the grant back",
     ("M06b-click-merge-nothing-on-one-pr-card",), "F2-3"),
    # ---- what a call does
    ("CL01", TG, 'FILE_PUSH_LEAVES = ("push_files", "create_or_update_file", "delete_file")', "FILE_PUSH_LEAVES = ()",
     "the file-push tools are outward acts", ("R10a-push-files-to-main", "F24c-push-files"),
     "B:N08 A:B20; F1-7 M1a, reimpl M14"),
    ("CL02", TG, 'SCHEDULE_LEAVES = ("create_trigger", "update_trigger", "delete_trigger", "fire_trigger", "send_later")',
     "SCHEDULE_LEAVES = ()",
     "the scheduled-task tools are outward acts", ("F05-send-later", "F24c-create-trigger"), "B:N09 A:B21; F1-7 M1b"),
    ("CL03", TG, 'SCHEDULE_TOOLS = ("CronCreate", "CronDelete", "ScheduleWakeup")', 'SCHEDULE_TOOLS = ("ScheduleWakeup",)',
     "the built-in scheduling tools are outward acts", ("F05-cron-create", "F05-cron-delete"), "A:B21b; F1-3"),
    ("CL04", TG, 'PR_WRITE_LEAVES = ("create_pull_request", "update_pull_request", "update_pull_request_branch", "disable_pr_auto_merge",\n'
     '                   "actions_run_trigger")', 'PR_WRITE_LEAVES = ("create_pull_request",)',
     "updating a pull request is an outward act", ("F05-update-pr-branch", "F24c-update-pull-request"),
     "B:N10 A:B22; F1-7 M1c"),
    ("CL05", TG, 'GH_PR_WRITE_SUBS = ("create", "edit", "close", "reopen", "ready", "update-branch")', "GH_PR_WRITE_SUBS = ()",
     "creating or editing a pull request from the command line is an outward act", ("F24b-gh-pr-create", "F06a-gh-pr-edit"),
     "B:N11 A:B23; F1-7 M2"),
    ("CL06", TG, "        if a in GIT_GLOBAL_WITH_VALUE:\n            if a == GIT_DIR_FLAG and j + 1 < len(argv):",
     "        if a == GIT_DIR_FLAG:\n            if a == GIT_DIR_FLAG and j + 1 < len(argv):",
     "git's own options before the verb do not hide the verb", ("F02-commit-with-identity-flags",),
     "B:N12 A:B19; F1-7 M3, reimpl M13"),
    ("CL07", TG, 'GIT_COMMIT_VERBS = ("commit", "revert", "cherry-pick", "am")', 'GIT_COMMIT_VERBS = ("revert", "cherry-pick", "am")',
     "a commit is an outward act", ("F01-ungoverned-commit",), "B:N28 A:B24; F1-7 C2, reimpl M14"),
    ("CL08", TG, 'GIT_COMMIT_VERBS = ("commit", "revert", "cherry-pick", "am")', 'GIT_COMMIT_VERBS = ("commit",)',
     "revert and cherry-pick make commits", ("F04-revert-makes-a-commit", "s_f1_4_cherry_pick"), "F1-4"),
    ("CL09", TG, 'MERGE_TOOL_LEAVES = ("merge_pull_request", "enable_pr_auto_merge")', 'MERGE_TOOL_LEAVES = ("merge_pull_request",)',
     "switching auto-merge on needs the same word as a merge", ("R01a-auto-merge-tool-no-word", "S02-scheduled-auto-merge-tool"),
     "B:N33 A:B15"),
    ("CL10", TG, "    try:\n        cmds = parse_shell(text, cwd)\n    except (ShellParseError, RecursionError, IndexError):",
     '    try:\n        raise ShellParseError("deliberate break")\n    except (ShellParseError, RecursionError, IndexError):',
     "a shell command is parsed: a word in command position is an act, anything else is data",
     ("N03-commit-message-mentions", "R04b-gh-number-last-with-word"), "B:N34; RI-8"),
    ("CL11", TG, "    return acts, True\n\n\ndef _leaf(name):",
     '    return acts + [a for a in _fallback_acts(text) if a.kind == "merge"], True\n\n\ndef _leaf(name):',
     "a command that only mentions the merge words is no merge", ("N01-grep-for-the-words",), "A:B38"),
    ("CL12", TG, "    return acts, True\n\n\ndef _leaf(name):",
     '    return acts + [a for a in _fallback_acts(text) if a.kind != "merge"], True\n\n\ndef _leaf(name):',
     "a command that only mentions commit or push is no outward act", ("F07a-grep-git-commit", "F07b-echo-git-push"),
     "A:B38b"),
    ("CL13", TG, '        return [] if method in API_READ_METHODS else [Act("merge", "api merge", pr=int(merge.group(1)), repo=repo)]',
     '        return [Act("merge", "api merge", pr=int(merge.group(1)), repo=repo)]',
     "reading the merge state through the API is no merge", ("N09-api-get-merged-state",), "B:N42; RI-8"),
    ("CL14", TG, "    try:\n        path = _join_dir(cwd, path)", "    return []\n    try:\n        path = _join_dir(cwd, path)",
     "a script file a command runs is read for its acts", ("R08-script-file", "s_f1_4_release_script"), "B:N44 A:B55"),
    ("CL15", TG, "            found, j = _option_at(argv, j, GH_GLOBAL_WITH_VALUE)", "            found, j = _option_at(argv, j, ())",
     "an option with a value between the command-line words does not hide the merge",
     ("R03-gh-flag-before-pr", "m_d3_cli_global_repo_flag"), "A:B17"),
    ("CL16", TG, 'API_MERGE_PATH = re.compile(r"pulls/(\\d+)/merge$")', 'API_MERGE_PATH = re.compile(r"(?!x)xpulls/(\\d+)/merge$")',
     "the merge route of the REST API is a merge", ("R05-gh-api-put-merge", "R06-curl-put-merge"), "A:B18"),
    ("CL17", TG, "        if any(f in rest for f in GIT_NO_COMMIT_FLAGS[verb]):\n            return []",
     "        if False:\n            return []",
     "a dry run is no commit", ("F07d-commit-dry-run",), "A:B39"),
    ("CL18", TG, "    if rest and rest[0] in HELP_FLAGS:", "    if False:",
     "a help page is no act", ("F07e-commit-help",), "A:B39b"),
    ("CL19", TG, '    p = os.path.normpath(path) + "/"', '    p = path + "/"',
     "a path is normalised before it is called scratch (/tmp/../repo is not scratch)", ("A04-tmp-dotdot-path-is-a-repo-file",),
     "A:B46; ADV-4"),
    ("CL20", TG, 'DEFAULT_BRANCHES = ("main", "master")', 'DEFAULT_BRANCHES = ("master",)',
     "main is a default branch", ("R09a-git-push-origin-main", "R09b-git-push-head-to-main"), "A:B49"),
    ("CL21", TG, 'SHELL_TOOLS = ("Bash", "Monitor")', 'SHELL_TOOLS = ("Bash",)',
     "every tool that runs a shell command is read as one", ("m_cli_merge_through_monitor_tool", "s_f1_4_monitor_tool_push"),
     "A:B56; F1-4"),
    ("CL22", TG, "        c.stdin_args = stdin_args\n        out.append(c)\n",
     "        c.stdin_args = stdin_args\n        out.append(c)\n        for h in c.heredocs:\n"
     '            out += parse_shell(h["body"], here, depth + 1, "heredoc", dict(env))\n',
     "a here-document is data unless a shell reads it", ("N05-script-written-not-run", "F07c-script-written-not-run"), "A:B57"),
    ("CL23", TG, "                    acts = [a for a in acts if not a.last_step]", "                    pass",
     "the last step of an and-chain that failed was not taken",
     ("F08b-commit-failed-nothing-to-commit", "s_f1_6_single_push_failed"), "B:N35b A:B68; F1-6"),
    ("CL24", TG, '                if denied or (block.get("is_error") and b.get("name") not in SHELL_TOOLS):', "                if False:",
     "a call that was denied or rejected was not taken", ("F08a-merge-call-denied-by-gate", "s_f1_6_commit_rejected_at_prompt"),
     "B:N35a A:B40; F1-6"),
    ("CL25", TG, '            if res is not None and res[1].get("is_error"):\n                continue                            # the call failed',
     "            if False:\n                continue                            # the call failed",
     "a Skill call that failed loaded nothing", ("F14-skill-call-errored",), "B:N39 A:B45; F1-8"),
    ("CL26", TG, '    return str((inp.get("skill") if isinstance(inp, dict) else "") or "").split(":")[-1].strip()',
     '    return next((g for g in GOVERNORS if g in json.dumps(inp)), "")',
     "a governor is loaded by a Skill call of that name, not by one that mentions it", ("F25-skill-args-mention-governor",),
     "B:N13 A:B25; F1-7 M4, PC-7 M11"),
    ("CL27", TG, 'or "").split(":")[-1].strip()', 'or "").strip()',
     "a scope prefix before a skill's name is dropped", ("O03-synced-copy-skill-names-count",), "A:B70; F1-7 C4"),
    # ---- the Stop gate: outward actions
    ("ST01", TG, "    acts = model.outward(start, ledger)\n    if not acts:", "    acts = model.outward(start, ledger)\n    if len(acts) != 1:",
     "the rule holds for any number of outward acts", ("F23-commit-and-push", "F12-retry-after-other-hooks-block"),
     "B:N17 A:B28; F1-7 M7"),
    ("ST02", TG, " and ((li, lk) < (i, k) or (remedy is not None and li > remedy))", "",
     "plan-gate is loaded BEFORE the outward act", ("F31-plan-gate-after-first-act",), "A:B29; F1-7 C1"),
    ("ST03", TG, "        verify_ok = any(g == VERIFY_GOVERNOR and li > floor for li, _lk, g in loads)",
     "        verify_ok = any(g == VERIFY_GOVERNOR and li > max(floor, mine[0][0]) for li, _lk, g in loads)",
     "adversarial-verify counts anywhere in the turn, before or after the act", ("F30-verify-then-commit-and-push",),
     "A:B30; F1-7 C3"),
    ("ST04", TG, "        if plan_ok and verify_ok:\n            continue", "        if plan_ok:\n            continue",
     "adversarial-verify is required", ("O01-plan-gate-without-adversarial-verify",), "A:B30b"),
    ("ST05", TG, "    if stop_hook_active and not model.feedback(start):\n        return False, [], []",
     "    if stop_hook_active:\n        return False, [], []",
     "the retry flag alone does not switch the outward rule off",
     ("F12-retry-after-other-hooks-block", "J01b-blocked-stop-real-order-stop"), "B:N38 A:B31; F1-2, PC-4"),
    ("ST06", TG, "    if len(own) >= F1_MAX_BLOCKS:\n        return False, [], []", "    if False:\n        return False, [], []",
     "the outward rule blocks a bounded number of times in one stretch", ("F13b-third-stop-is-let-go",), "A:B32"),
    ("ST07", ENF, "    except BaseException:\n        answer = None", "    except BaseException:\n        raise",
     "an error in the Stop hook ends it quietly with status 0", ("X05c-internal-error-stop-is-allowed",),
     "B:N14 A:B26; F1-7 M5"),
    ("ST08", ENF, ' Load the missing governor with the "\n             "Skill tool now and follow it.")', '")',
     "the block reason names the remedy", ("F26-block-reason-carries-the-remedy",), "B:N16 A:B27; F1-7 M6"),
    ("ST09", ENF, "turngate.f1_decision(model, turngate.ledger_read(path), active)", "turngate.f1_decision(model, (), active)",
     "a helper agent's noted outward calls are counted", ("F09-delegate-pushes-main-turn-loads-nothing",),
     "B:N36 A:B60; F1-1"),
    ("ST10", TG, "        if not mine:\n            continue\n        loads = model.loads(gov, high)",
     "        if not mine or (cuts and n == 0):\n            continue\n        loads = model.loads(gov, high)",
     "the part of a stretch before a scheduled run began is judged too",
     ("J11b-run-after-owner-miss-no-stop-row", "F19c-legacy-owner-push-then-scheduled-run-loads-both"), "A:B67; TB-3"),
    ("ST11", TG, "                    counted = float(noted_at) > since", "                    counted = rows_then > after",
     "a helper's note is placed by its time stamp, not by a row count that restarts when the record is rewritten",
     ("J16b-stale-ledger-note-is-not-counted",), "new rule J16"),
    ("ST12", TG, '                rows_then = int(note.get("rows"))\n',
     '                rows_then = int(note.get("rows"))\n                if rows_then > len(self.rows):\n                    continue\n',
     "a helper's note still counts after the record was rewritten and holds fewer rows", ("J16-ledger-after-rewrite",),
     "new rule J16"),
    ("ST13", TG, "((li, lk) < (i, k) or (remedy is not None and li > remedy))", "((li, lk) < (i, k))",
     "after this rule's own block, a plan-gate load made since answers it", ("F11b-chain-stop2-remedied",), "F1-2"),
    # ---- the Stop gate: prompt class
    ("PC01", ENF, "    if (all(c in TRIVIA_CLASSES for c in classes) and", "    if (any(c in TRIVIA_CLASSES for c in classes) and",
     "the short-answer allowance is for review-only prompts", ("P10a-allowance-is-review-only",), "B:N18 A:B33; PC-7 M1"),
    ("PC02", ENF, "    loaded = set(governor for _row, _block, governor in model.loads(model.gov_start))",
     "    loaded = set(governor for _row, _block, governor in model.loads(-1))",
     "governor loads made before the prompt do not count (prompt class)", ("P11-loads-before-the-prompt-do-not-count",),
     "B:N19a A:B34; PC-7 M3"),
    ("PC03", ENF, "    needed = set(govclass.GOVERNORS_FOR[c][0] for c in classes)",
     "    needed = set([govclass.GOVERNORS_FOR[classes[0]][0]])",
     "every matched class needs its governor", ("P09-every-class-needs-its-governor",), "B:N20 A:B36; PC-7 M5"),
    ("PC04", ENF, " and model.tools_ran(model.gov_start) == 0\n", "\n",
     "the short-answer allowance needs a turn with no tool call", ("p_ctl_review_with_tool_is_not_trivia",),
     "A:B69; PC-7 K1"),
    ("PC05", ENF, "    if any(row > model.gov_start for row in model.stops_done + model.idle_wakes):", "    if False:",
     "the owner's prompt is judged at its own stop only, not again after a completed stop or a wake",
     ("P05-github-wake-after-review-remark",), "A:B37 A:B71; PC-5, TB-7"),
    ("PC06", TG, '            if e.kind == "QUEUED_OWNER":\n                out.append(e.text)',
     '            if False:\n                out.append(e.text)',
     "a prompt the owner sends while the assistant works is classified",
     ("J13-queued-prompt-is-classified", "p_queued_message_is_classified"), "new rule J13"),
    ("PC07", ENF, "    if active and not model.feedback(start):", "    if active:",
     "the retry flag alone does not switch the prompt-class rule off", ("P07-retry-after-receipt-block-rearms",), "PC-4"),
    ("PC08", ENF, '    said = model.prose(model.gov_start, data.get("last_assistant_message"))',
     "    said = model.prose(model.gov_start)",
     "the final answer the program hands the hook is read when the record lacks it", ("P14-long-answer-not-in-record",),
     "PC-2"),
    # ---- the plan-shown advisory and the helper ledger
    ("AD01", PRE, "    if not any(a.kind in looked_at or a.note == turngate.NOTE_BRANCH_UNKNOWN for a in acts):",
     "    if not any(a.kind in looked_at or a.note == turngate.NOTE_BRANCH_UNKNOWN for a in acts) and name not in turngate.SHELL_TOOLS:",
     "a shell command that writes nothing does not spend the advisory", ("A02a-readonly-grep-mention", "A02b-echo-mention"),
     "A:B47; ADV-4"),
    ("AD02", PRE, '"The record does not keep every message, so this may be a false alarm: if you have shown the owner the "',
     '"If you have shown the owner the "',
     "the advisory states its limit: the record does not keep every message", ("a_adv1_advisory_states_its_limit",),
     "A:B73; ADV-1"),
    ("AD03", PRE, "                pass                        # no note: nothing is counted and nothing is blocked\n        return None",
     "                pass                        # no note: nothing is counted and nothing is blocked\n"
     "        return advisory(turngate, model, data) if model is not None else None",
     "a helper agent's call gets no advisory", ("J14-helper-advisory-silent",), "new rule J14"),
    ("AD04", PRE, "        if os.path.exists(marker):\n            return None", "        if False:\n            return None",
     "the advisory is given once per plan-gate load", ("O13-advisory-once-per-load",), "ADV-2"),
    ("AD05", PRE, "    if any(turngate.PLAN_MARK.search(text) for text in model.prose(row)):\n        return None",
     "    if False:\n        return None",
     "no advisory when the plan text is on record after the load", ("A07-plan-shown",), "ADV-1"),
    ("AD06", PRE, "                turngate.ledger_add(path, len(rows), str(agent), str(name), counted)", "                pass",
     "a helper agent's outward call is noted for the Stop gate", ("F09-delegate-pushes-main-turn-loads-nothing",), "F1-1"),
    # ---- which way a failure goes
    ("FP01", PRE, "        return deny(REASON_GATE_ERROR % ERROR_INTERNAL) if merge_route() else None\n\n\nif __name__",
     "        return None\n\n\nif __name__",
     "an error while judging a merge denies it", ("X05a-internal-error-merge-is-denied",), "B:N15 A:B41"),
    ("FP02", PRE, '        return deny(REASON_GATE_ERROR % ERROR_MODULE) if _state["crude"] else None', "        return None",
     "a merge is denied when the shared module cannot be loaded", ("X04a-shared-module-missing-merge",), "A:B41b"),
    ("FP03", PRE, '        return deny(REASON_GATE_ERROR % ERROR_INPUT) if crude_merge(raw or "") else None', "        return None",
     "an input that is not JSON and names a merge route is denied", ("X01a-payload-not-json-names-merge-tool",), "fail-safe"),
    ("FP04", PRE, "        signal.alarm(HOOK_DEADLINE_SECONDS)", "        signal.alarm(0)",
     "the pre-tool hook answers before the program cuts it off", ("J04a-deadline-merge-tool",), "new rule J04"),
    ("FP05", ENF, "        signal.alarm(HOOK_DEADLINE_SECONDS)", "        signal.alarm(0)",
     "the Stop hook ends itself before the program cuts it off", ("J04c-deadline-stop",), "new rule J04"),
    ("FP06", PRE, "    finish(deny(REASON_GATE_ERROR % ERROR_DEADLINE) if merge_route() else None)", "    finish(None)",
     "at its deadline the pre-tool hook denies a merge", ("J04a-deadline-merge-tool",), "new rule J04"),
    ("FP07", PRE, "    finish(deny(REASON_GATE_ERROR % ERROR_DEADLINE) if merge_route() else None)",
     "    finish(deny(REASON_GATE_ERROR % ERROR_DEADLINE))",
     "at its deadline the pre-tool hook lets every other call through", ("J04b-deadline-edit",), "new rule J04"),
    ("FP08", PRE, "        return deny(REASON_GATE_ERROR % ERROR_INTERNAL) if merge_route() else None\n\n\nif __name__",
     "        return deny(REASON_GATE_ERROR % ERROR_INTERNAL)\n\n\nif __name__",
     "an error while judging any other call lets it through",
     ("X05b-internal-error-edit-is-allowed", "X05d-internal-error-commit-is-allowed"), "fail-safe"),
    ("FP09", PRE, "        for wanted in CRUDE_MERGE_WORDS + CRUDE_PUSH_WORDS:", "        for wanted in CRUDE_MERGE_WORDS:",
     "the failure paths know a push to a default branch as they know a merge",
     ("X04c-shared-module-missing-push-main", "X05e-error-while-classifying-push-main"), "D3"),
    ("FP10", PRE, 'CRUDE_PUSH_WORDS = (("git", "push", "main"),', 'CRUDE_PUSH_WORDS = (("git", "push"), ("git", "push", "main"),',
     "the failure paths let a push to another branch through",
     ("X04d-shared-module-missing-push-branch", "X05f-error-while-classifying-push-branch"), "D3"),
    ("FP11", PRE, ' ("git", "push", "all"),', "",
     "the failure paths know a push of every branch", ("X04e-shared-module-missing-push-all",), "D3"),
    ("FP12", PRE, '("git", "push", "mirror"), ', "",
     "the failure paths know a mirror push", ("X04f-shared-module-missing-push-mirror",), "D3"),
    ("FP13", PRE, 'CRUDE_MERGE = re.compile(r"merge_pull_request|', 'CRUDE_MERGE = re.compile(r"',
     "the failure paths know the merge tool by its name",
     ("X04a-shared-module-missing-merge", "X01a-payload-not-json-names-merge-tool"), "fail-safe"),
    ("FP14", PRE, "HOOK_DEADLINE_SECONDS = 8 ", "HOOK_DEADLINE_SECONDS = 12",
     "the pre-tool hook's own deadline is shorter than the wired timeout", ("J04a-deadline-merge-tool",), "new rule J04"),
    ("FP15", PRE, "    looked_at = turngate.WRITE_KINDS + turngate.MERGE_GATED_KINDS",
     '    looked_at = turngate.F1_COUNTED_KINDS + ("write",)',
     "the merge gate looks at its own list of gated acts, not at the Stop gate's list of counted ones",
     ("X06a-merge-gate-keeps-its-own-list-merge", "X06b-merge-gate-keeps-its-own-list-push-main"), "review 2026-11-15"),
    # ---- the policy switches (the owner's answers): each flipped or changed
    ("PS01", TG, "SCHEDULED_READ_ENDS_WORD = True ", "SCHEDULED_READ_ENDS_WORD = False",
     "a scheduled notification read mid-turn ends the word given before it",
     ("S10a-midturn-scheduled-read-ends-earlier-word",), "B:N46 A:B74; owner's answer 1"),
    ("PS02", TG, "RESTART_ENDS_WORD = True ", "RESTART_ENDS_WORD = False",
     "the restart notice of the worker process ends the word", ("T32-worker-restart-after-order",), "policy switch"),
    ("PS03", TG, "PUSH_UNKNOWN_BRANCH_POLICY = POLICY_DENY_UNATTENDED", "PUSH_UNKNOWN_BRANCH_POLICY = POLICY_ALLOW",
     "a push whose branch cannot be read is denied where the owner is absent", ("J09-unresolved-push-unattended",),
     "B:N49; new rule J09; owner's answer 2"),
    ("PS04", TG, "PUSH_UNKNOWN_BRANCH_POLICY = POLICY_DENY_UNATTENDED", "PUSH_UNKNOWN_BRANCH_POLICY = POLICY_DENY",
     "a push whose branch cannot be read is let through where the owner is present",
     ("R09h-bare-push-branch-unreadable",), "owner's answer 2"),
    ("PS05", TG, "DELEGATE_MAY_MERGE = True ", "DELEGATE_MAY_MERGE = False",
     "a helper agent may merge what the owner's standing word names", ("G01a-helper-merge-with-live-word",), "policy switch"),
    ("PS06", TG, "F1_MAX_BLOCKS = 2 ", "F1_MAX_BLOCKS = 1 ",
     "an unanswered block of the outward rule is repeated once", ("F13a-second-block-when-nothing-loaded",),
     "owner's answer 3"),
    ("PS07", TG, "F1_MAX_BLOCKS = 2 ", "F1_MAX_BLOCKS = 3 ",
     "the outward rule blocks twice at most in one stretch", ("F13b-third-stop-is-let-go",), "owner's answer 3"),
    ("PS08", TG, "PROMPT_CLASS_MAX_BLOCKS = 1 ", "PROMPT_CLASS_MAX_BLOCKS = 0 ",
     "the prompt-class rule blocks", ("P01-build-no-governor",), "owner's answer 3"),
    ("PS09", TG, "PROMPT_CLASS_MAX_BLOCKS = 1 ", "PROMPT_CLASS_MAX_BLOCKS = 2 ",
     "the prompt-class rule blocks once in one stretch", ("P06-single-retry-understood",), "owner's answer 3"),
    ("PS10", TG, "WAKE_TURN_INHERITS_LOADS = True ", "WAKE_TURN_INHERITS_LOADS = False",
     "work woken after a completed stop keeps the turn's governor loads", ("F33-wake-turn-inherits-owner-turn-loads",),
     "A:B61; owner's answer 4"),
    ("PS11", TG, "COMPACTION_VOIDS_LOADS = True ", "COMPACTION_VOIDS_LOADS = False",
     "an outward act after a compaction needs the governors loaded again",
     ("F15-loads-before-compaction-do-not-count", "J21-verify-before-compaction-only", "J22-act-before-and-after-compaction"),
     "B:N45 A:B62; addendum, owner's answer 4"),
    ("PS12", TG, "CLASSIFY_CARD_ANSWERS = False", "CLASSIFY_CARD_ANSWERS = True ",
     "a clicked card label is not a prompt for the prompt-class rule", ("P13-build-ordered-by-click",), "owner's answer 5"),
    ("PS13", TG, 'MERGE_GATED_KINDS = ("merge", "push_default")', 'MERGE_GATED_KINDS = ("merge",)',
     "a push to a default branch needs the same word as a merge", ("R09a-git-push-origin-main", "S05-scheduled-push-main"),
     "B:N32 A:B16; D3"),
    ("PS14", TG, 'MERGE_GATED_KINDS = ("merge", "push_default")', 'MERGE_GATED_KINDS = ("push_default",)',
     "a merge needs the owner's word", ("M02-card-for-34-141-call-35",), "D1"),
    ("PS15", TG, '"push", "commit", "pr_write", "file_push", "schedule")', '"push", "commit", "pr_write", "file_push")',
     "the Stop gate counts a change to a scheduled task", ("F05-send-later", "F05-cron-create"), "owner's answer 6"),
    ("PS16", TG, '"push", "commit", "pr_write", "file_push", "schedule")', '"push", "pr_write", "file_push", "schedule")',
     "the Stop gate counts a commit", ("F01-ungoverned-commit",), "owner's answer 6"),
    ("PS17", TG, '"push", "commit", "pr_write", "file_push", "schedule")', '"commit", "pr_write", "file_push", "schedule")',
     "the Stop gate counts a push", ("F03b-push-quoted-dir",), "owner's answer 6"),
    ("PS18", TG, '"push", "commit", "pr_write", "file_push", "schedule")', '"push", "commit", "file_push", "schedule")',
     "the Stop gate counts a pull-request change", ("F24b-gh-pr-create", "F24c-create-pull-request"), "owner's answer 6"),
    ("PS19", TG, 'F1_COUNTED_KINDS = ("merge", "push_default", "push", "commit", "pr_write", "file_push", "schedule")',
     'F1_COUNTED_KINDS = ("push_default", "push", "commit", "pr_write", "file_push", "schedule")',
     "the Stop gate counts a merge", ("F24c-merge-pull-request", "F05-auto-merge"), "owner's answer 6"),
    ("PS20", TG, 'F1_COUNTED_KINDS = ("merge", "push_default", "push", "commit", "pr_write", "file_push", "schedule")',
     'F1_COUNTED_KINDS = ("merge", "push_default", "push", "commit", "pr_write", "schedule")',
     "the Stop gate counts a file pushed through a tool", ("F24c-push-files", "F24c-delete-file"), "owner's answer 6"),
    ("PS21", ENF, "TRIVIA_MAX_CHARS = 400", "TRIVIA_MAX_CHARS = 0",
     "a short review answer with no tool call passes without a governor", ("P10b-review-only-short-answer",), "PC-7"),
    ("PS22", ENF, "TRIVIA_MAX_CHARS = 400", "TRIVIA_MAX_CHARS = 400000",
     "a long answer is not a short answer", ("P14-long-answer-not-in-record",), "PC-2"),
    # ---- the wiring: which calls the program sends to the pre-tool hook. Re-targeted 2026-11-16: the turn-gate
    # matcher is now two groups (the merge tools alone, with the bare command; every other gated name, behind a
    # file test). WI01, WI02 and WI04 hit the second group; their texts are found there unchanged.
    ("WI01", WIRING, "|fire_trigger|send_later))$", "|fire_trigger|send_later))",
     "the matcher is anchored at its end: a name that only starts like a gated one is not sent", ("W01-matcher",),
     "new rule W01"),
    ("WI02", WIRING, "|fire_trigger|send_later))$", "|fire_trigger))$",
     "every name the code classifies is sent to the pre-tool hook (a name dropped from the matcher)", ("W01-matcher",),
     "new rule W01"),
    ("WI03", TG, 'MERGE_TOOL_LEAVES = ("merge_pull_request", "enable_pr_auto_merge")',
     'MERGE_TOOL_LEAVES = ("merge_pull_request", "enable_pr_auto_merge", "merge_queue_add")',
     "every name the code classifies is sent to the pre-tool hook (a name added to the code only)",
     ("W01-matcher", "W03-wiring-merge-tools-have-a-group-of-their-own"), "new rule W01"),
    ("WI04", WIRING, '"matcher": "^(Edit|Write|NotebookEdit|Bash|', '"matcher": "(Edit|Write|NotebookEdit|Bash|',
     "the matcher is anchored at its start: a name that only ends like a gated one is not sent", ("W01-matcher",),
     "new rule W01"),
    # ---- the wiring, 2026-11-16 (findings SF-2, SF-4): the merge tools' own group, what a missing script does,
    # every event's scripts. The auditor's recorded wiring changes are WI11 to WI18 (rev-surfaces M3, M4, M5; the
    # verifier's N1, N2, N3), each made as one replacement on the two-group wiring.
    ("WI05", WIRING, '|enable_pr_auto_merge)$"', '|enable_pr_auto_merge)"',
     "the merge tools' group is anchored at its end", ("W03-wiring-merge-tools-have-a-group-of-their-own",), "SF-4"),
    ("WI06", WIRING, '"matcher": "^mcp__.*__(merge_pull_request|', '"matcher": "mcp__.*__(merge_pull_request|',
     "the merge tools' group is anchored at its start", ("W03-wiring-merge-tools-have-a-group-of-their-own",), "SF-4"),
    ("WI07", WIRING, "(merge_pull_request|enable_pr_auto_merge)$", "(merge_pull_request)$",
     "the merge tools' group selects every merge tool (auto-merge dropped)",
     ("W03-wiring-merge-tools-have-a-group-of-their-own", "W01-matcher"), "SF-4"),
    ("WI08", WIRING, r'"command": "python3 \"$CLAUDE_PROJECT_DIR\"/hooks/turn-gates-pretool.py"',
     r'"command": "if [ -f \"$CLAUDE_PROJECT_DIR\"/hooks/turn-gates-pretool.py ]; then python3 '
     r'\"$CLAUDE_PROJECT_DIR\"/hooks/turn-gates-pretool.py; fi"',
     "a missing pre-tool script denies a merge (the merge group's command keeps no file test)",
     ("W04-wiring-missing-script-denies-only-the-merge-tools",), "SF-2"),
    ("WI09", WIRING, r'"command": "if [ -f \"$CLAUDE_PROJECT_DIR\"/hooks/turn-gates-pretool.py ]; then python3 '
     r'\"$CLAUDE_PROJECT_DIR\"/hooks/turn-gates-pretool.py; fi"',
     r'"command": "python3 \"$CLAUDE_PROJECT_DIR\"/hooks/turn-gates-pretool.py"',
     "a missing pre-tool script does not deny every Bash, Edit and Write call (the file test of the other group)",
     ("W04-wiring-missing-script-denies-only-the-merge-tools",), "SF-2"),
    ("WI10", WIRING, r'if [ -f \"$CLAUDE_PROJECT_DIR\"/hooks/governance-trigger.py ]',
     r'if [ -f \"$CLAUDE_PROJECT_DIR\"/hooks/governance-trigger.pyc ]',
     "the file test runs the script when it is there (a test of the wrong file runs nothing)",
     ("W06-wiring-commands-run-the-hooks",), "SF-4"),
    ("WI11", WIRING, ',\n          {\n            "type": "command",\n            "command": "if [ -f '
     r'\"$CLAUDE_PROJECT_DIR\"/hooks/receipt-law-stop-gate.sh ]; then bash '
     r'\"$CLAUDE_PROJECT_DIR\"/hooks/receipt-law-stop-gate.sh; fi",' '\n            "timeout": 10\n          }', "",
     "the project's Stop event runs the receipt gate", ("W02-wiring-every-event-runs-its-scripts",), "SF-4 M5"),
    ("WI12", WIRING, '"matcher": "^(Edit|Write|NotebookEdit|Bash|Monitor|CronCreate|CronDelete|ScheduleWakeup|'
     'mcp__.*__(disable_pr_auto_merge|create_pull_request|update_pull_request|update_pull_request_branch|push_files|'
     'create_or_update_file|delete_file|actions_run_trigger|create_trigger|update_trigger|delete_trigger|fire_trigger|'
     'send_later))$"', '"matcher": "Edit|Write|NotebookEdit|Bash"',
     "the project's pre-tool hook is sent the PR and scheduling tools", ("W01-matcher",), "SF-4 M3"),
    ("WI13", WIRING, '"matcher": "^mcp__.*__(merge_pull_request|enable_pr_auto_merge)$"',
     '"matcher": "Edit|Write|NotebookEdit|Bash"',
     "the project's pre-tool hook is sent the merge tools", ("W03-wiring-merge-tools-have-a-group-of-their-own",),
     "SF-4 M3"),
    ("WI14", PLUGIN_WIRING, '"matcher": "^(Edit|Write|NotebookEdit|Bash|Monitor|CronCreate|CronDelete|ScheduleWakeup|'
     'mcp__.*__(disable_pr_auto_merge|create_pull_request|update_pull_request|update_pull_request_branch|push_files|'
     'create_or_update_file|delete_file|actions_run_trigger|create_trigger|update_trigger|delete_trigger|fire_trigger|'
     'send_later))$"', '"matcher": "Edit|Write|NotebookEdit|Bash"',
     "the plugin's pre-tool hook is sent the PR and scheduling tools", ("W01-matcher",), "SF-4 M4"),
    ("WI15", PLUGIN_WIRING, '"matcher": "^mcp__.*__(merge_pull_request|enable_pr_auto_merge)$"',
     '"matcher": "Edit|Write|NotebookEdit|Bash"',
     "the plugin's pre-tool hook is sent the merge tools", ("W03-wiring-merge-tools-have-a-group-of-their-own",),
     "SF-4 M4"),
    ("WI16", WIRING, '"matcher": "^mcp__.*__(merge_pull_request|enable_pr_auto_merge)$"', '"matcher": "NoSuchTool"',
     "the project's merge group reaches a tool that exists", ("W03-wiring-merge-tools-have-a-group-of-their-own",),
     "SF-4 N1"),
    ("WI17", PLUGIN_WIRING, '"matcher": "^(Edit|Write|NotebookEdit|Bash|Monitor|CronCreate|CronDelete|ScheduleWakeup|'
     'mcp__.*__(disable_pr_auto_merge|create_pull_request|update_pull_request|update_pull_request_branch|push_files|'
     'create_or_update_file|delete_file|actions_run_trigger|create_trigger|update_trigger|delete_trigger|fire_trigger|'
     'send_later))$"', '"matcher": "NoSuchTool"',
     "the plugin's other gated names reach the pre-tool hook", ("W01-matcher",), "SF-4 N3"),
    ("WI18", WIRING, '{\n            "type": "command",\n            "command": "if [ -f '
     r'\"$CLAUDE_PROJECT_DIR\"/hooks/plan-gate-first-write-reminder.sh ]; then bash '
     r'\"$CLAUDE_PROJECT_DIR\"/hooks/plan-gate-first-write-reminder.sh; fi",' '\n            "timeout": 10\n'
     '          },\n          ', "",
     "the project's first write runs the plan-gate reminder", ("W02-wiring-every-event-runs-its-scripts",), "SF-4 N2"),
    ("WI19", PLUGIN_WIRING, ',\n          {\n            "type": "command",\n            "command": '
     r'"w=\"${CLAUDE_PLUGIN_ROOT}/scripts/run-unless-project-wired.sh\"; if [ -f \"$w\" ]; then bash \"$w\" '
     'receipt-law-stop-gate.sh; fi",\n            "timeout": 10\n          }', "",
     "the plugin's Stop event runs the receipt gate", ("W02-wiring-every-event-runs-its-scripts",), "SF-4"),
    ("WI20", PLUGIN_WIRING, '>&2; exit 2; fi"', '>&2; exit 0; fi"',
     "a plugin missing its pre-tool script denies a merge",
     ("W04-wiring-missing-script-denies-only-the-merge-tools",), "SF-2"),
    ("WI21", PLUGIN_WIRING, r'"w=\"${CLAUDE_PLUGIN_ROOT}/scripts/run-unless-project-wired.sh\"; if [ -f \"$w\" ]; '
     r'then bash \"$w\" governance-trigger.py; fi"',
     r'"bash \"${CLAUDE_PLUGIN_ROOT}/scripts/run-unless-project-wired.sh\" governance-trigger.py"',
     "a plugin command whose wrapper is missing ends with status 0",
     ("W04-wiring-missing-script-denies-only-the-merge-tools",), "SF-2"),
    ("WI22", PLUGIN_WIRING, r'bash \"$w\" session-doctrine.sh', r'bash \"$w\" session-doctrin.sh',
     "every script the plugin's wiring names is beside the hooks", ("W05-wiring-scripts-beside-the-hooks",), "SF-2"),
    ("WI23", WIRING, '"matcher": "compact|resume"', '"matcher": "compact"',
     "the session hook runs on a resume as well as after a compaction",
     ("W02-wiring-every-event-runs-its-scripts",), "SF-4"),
    ("WI24", WIRING, r'then python3 \"$CLAUDE_PROJECT_DIR\"/hooks/governance-trigger.py; fi',
     r'then python3 \"$CLAUDE_PROJECT_DIR\"/hooks/governance-triggers.py; fi',
     "every script the project's wiring runs is beside the hooks", ("W05-wiring-scripts-beside-the-hooks",), "SF-2"),
    ("WI25", PLUGIN_WIRING, "|fire_trigger|send_later))$", "|fire_trigger|send_later))",
     "the plugin's matcher is anchored at its end", ("W01-matcher",), "SF-4"),
    ("WI26", PLUGIN_WIRING, '|enable_pr_auto_merge)$"', '|enable_pr_auto_merge)"',
     "the plugin's merge group is anchored at its end", ("W03-wiring-merge-tools-have-a-group-of-their-own",), "SF-4"),
    # ---- the receipt gate (receiptlaw.py, run by receipt-law-stop-gate.sh): table "R" of the test table
    # -- the 13 recorded breaks of the 2026-11-12 audit (finding RL-8), re-targeted at the rebuilt gate
    ("RC01", RCP, '    if data.get("stop_hook_active") and not model.feedback(start):', "    if False:",
     "the retry flag with no block on record lets the stop go (the one retry)", ("RLX06-flag-set-and-no-block-on-record",),
     "RL-8 M01"),
    ("RC02", RCP, "start = turngate.stop_span(model)[0] - 1 ", "start = -1 ",
     "the gate judges the stretch, not the whole session",
     ("RLT04-new-owner-message-starts-a-new-stretch", "RLD73-claim-of-an-earlier-turn-only"), "RL-8 M02; RL-7, TB-5"),
    ("RC03", RCP, 'model.prose(start, data.get("last_assistant_message")):', 'model.prose(start, data.get("last_assistant_message"))[-1:]:',
     "every text of the stretch is read, not only the last",
     ("RLD70-bare-claim-in-an-earlier-text-of-the-stretch", "RLT02-claim-then-repeated-skill-load"), "RL-8 M03"),
    ("RC04", RCP, '("modal", re.compile(r"\\b%s%s\\s+%s"', '("modal", re.compile(r"(?!)%s%s\\s+%s"',
     "\"could not / cannot / can't\" with a verb of verifying is a claim", ("RLP00-couldnt-verify",), "RL-8 M04"),
    ("RC05", RCP, "ATTEMPT.search(text) or FAILURE.search(text)", "FAILURE.search(text)",
     "a named attempt is a receipt", ("RLD31-attempt-before-the-claim",), "RL-8 M05"),
    ("RC06", RCP, " or FAILURE.search(text)", "",
     "a named failure mode is a receipt", ("RLVC7-the-login-failed", "RLVC3-refused-the-connection"), "RL-8 M05; RL-4"),
    ("RC07", RCP, "\n                or CHOICE.search(text))", ")",
     "a stated choice in the claim's sentence is a receipt", ("RLD42-claim-and-the-choice-in-one-sentence",), "RL-8 M05"),
    ("RC08", RCP, "any(mark in text for mark in EVIDENCE_MARKS) or ", "",
     "a code span or a fenced block in the claim's sentence is a receipt",
     ("RLD124-code-spans-are-the-only-receipt", "RLD27-fenced-block-directly-under-the-claim"), "RL-4"),
    ("RC09", RCP, "    text = INLINE_CODE.sub(MARK_CODE, text)\n", "",
     "words inside inline code are not the assistant's claim", ("RLD136-status-word-inside-inline-code",), "RL-8 M06"),
    ("RC10", RCP, "        if not _has_receipt(reach) and", '        if not _has_receipt(" ".join(outside)) and',
     "one sentence's receipt does not excuse a claim in another sentence",
     ("RLD22-one-receipted-claim-one-bare-claim", "RLVE4-receipt-about-other-items"), "RL-8 M07; RL-6"),
    ("RC11", RCP, '("modal", re.compile(r"\\b%s%s\\s+%s" % (MODAL_NOT, _advs, _vverb), re.I), True),',
     '("modal", re.compile(r"\\b%s%s\\s+%s" % (MODAL_NOT, _advs, _vverb), 0), True),',
     "a claim is matched whatever its letter case", ("RLD02-upper-case", "RLD03-sentence-starts-with-the-claim"), "RL-8 M08"),
    ("RC12", RCP, "model.feedback(start, turngate.RECEIPT_BLOCK_MARK)", "model.feedback(-1, turngate.RECEIPT_BLOCK_MARK)",
     "the gate's earlier blocks are counted in the stretch, not in the session",
     ("RLX08-own-block-of-an-earlier-stretch-does-not-count", "RLD74-three-bare-claims-in-three-turns"), "RL-8 M09"),
    ("RC13", RCP, '                carry = (parts.pop(), "items", indent if kind == "item" else -1)', "                pass",
     "a line that ends with a colon goes on in the list items under it",
     ("RLD34-label-then-list-each-item-with-its-receipt", "RLD44-lead-in-blank-line-then-items-with-receipts"),
     "RL-8 M10 (the receipt's reach made narrower)"),
    ("RC14", RCP, 'RECEIPT_SCOPE = "sentence" ', 'RECEIPT_SCOPE = "neighbours" ',
     "a receipt counts only in the claim's own sentence",
     ("RLD20-receipt-in-the-sentence-before", "RLD21-receipt-in-the-sentence-after"), "RL-8 M11 (made wider); RL-6"),
    ("RC15", RCP, '("‘", "\'"), ', "",
     "a left curly single quote is read as a quotation mark", ("RLD137-passive-phrase-in-curly-single-quotes",), "RL-8 M12"),
    ("RC16", RCP, "    text = BLOCKQUOTE.sub(MARK_BLOCK + \"\\n\", text)\n", "",
     "a block quote is not the assistant's claim", ("RLQ01-claim-in-a-block-quote", "RLO04-phrase-only-in-code-and-block-quote"),
     "RL-8 M13"),
    # -- the retry flag, the count, the stretch, the final answer
    ("RC17", RCP, 'if data.get("stop_hook_active") and not model.feedback(start):', 'if data.get("stop_hook_active"):',
     "the retry flag alone does not switch the gate off",
     ("RLX01-retry-forced-by-the-other-hook", "RLX03-flag-set-after-the-other-hooks-block-and-work"), "RL-2, FU2-1"),
    ("RC18", RCP, "model.feedback(start, turngate.RECEIPT_BLOCK_MARK)", "model.feedback(start)",
     "only this gate's own blocks count against it", ("RLX01-retry-forced-by-the-other-hook",), "RL-2, FU2-1"),
    ("RC19", RCP, "RECEIPT_MAX_BLOCKS = 1 ", "RECEIPT_MAX_BLOCKS = 2 ",
     "at most one block of this gate in a stretch", ("RLX04-own-block-then-the-claim-again", "RLX05-own-block-counted-from-the-record-flag-off"),
     "constant RECEIPT_MAX_BLOCKS"),
    ("RC20", RCP, "RECEIPT_MAX_BLOCKS = 1 ", "RECEIPT_MAX_BLOCKS = 0 ",
     "the gate blocks a bare claim at all", ("RLP00-couldnt-verify",), "constant RECEIPT_MAX_BLOCKS"),
    ("RC21", RCP, 'model.prose(start, data.get("last_assistant_message")):', "model.prose(start, None):",
     "the final answer is read from the input when the record lacks it",
     ("RLT06b-answer-only-in-the-input", "RLY01-answer-missing-from-the-record"), "FU2-9"),
    ("RC22", RCP, '    if not any(row.get("type") != "BAD" for row in rows):\n        return None                         # no record to judge\n', "",
     "with no record to count blocks from, the stop is let go", ("RLZ06-no-record-path",), "design 6"),
    # -- which way a failure goes
    ("RC23", RCP, "HOOK_DEADLINE_SECONDS = 8 ", "HOOK_DEADLINE_SECONDS = 80 ",
     "the gate ends itself before the program cuts it off", ("RLZ16-deadline",), "constant HOOK_DEADLINE_SECONDS; H4"),
    ("RC24", RCP, "    arm_deadline()\n    try:\n        answer = main()", "    try:\n        answer = main()",
     "the gate has a deadline of its own", ("RLZ16-deadline",), "H4"),
    ("RC25", RCP, "    except BaseException:\n        answer = None\n    finish(answer)", "    except KeyboardInterrupt:\n        answer = None\n    finish(answer)",
     "an error inside the module lets the stop go with exit status 0",
     ("RLZ17-module-by-itself-internal-error", "RLZ18-module-by-itself-input-not-json"), "design 6"),
    ("RC26", RCW, "exit 0  ", "exit $?  ",
     "the wired script ends with exit status 0 whatever the module did",
     ("RLZ12-module-missing-beside-the-wired-script", "RLZ13-no-python3-on-path"), "design 1"),
    ("RC27", RCW, 'python3 "$here/receiptlaw.py"', 'python3 "receiptlaw.py"',
     "the wired script runs the module that lies beside it", ("RLP00-couldnt-verify",), "design 1"),
    # -- policy values and the block reason
    ("RC28", RCP, 'SCOPE_NEIGHBOURS = "neighbours" ', 'SCOPE_NEIGHBOURS = "sentence" ',
     "the wider scope is applied only when it is chosen", ("RLD20-receipt-in-the-sentence-before",), "constant SCOPE_NEIGHBOURS"),
    ("RC29", RCP, "NOT_VERIFIED_IS_A_CLAIM = False ", "NOT_VERIFIED_IS_A_CLAIM = True ",
     "\"was not verified\" with no \"could not\" is no claim by default", ("RLVB04-was-not-verified", "RLD109-not-verified-this-session"),
     "constant NOT_VERIFIED_IS_A_CLAIM"),
    ("RC30", RCP, '("not-verified", re.compile(r"(?<!have\\s)', '("not-verified", re.compile(r"(?!)(?<!have\\s)',
     "with the other reading chosen, \"was not verified\" is a claim", ("RLD93-other-reading-was-not-verified-is-a-claim",),
     "family not-verified"),
    ("RC31", RCP, "REASON_EXCERPT_CHARS = 160 ", "REASON_EXCERPT_CHARS = 16000 ",
     "the block reason quotes the start of the sentence, not all of it", ("RLD81-reason-quotes-the-start-of-the-sentence",),
     "constant REASON_EXCERPT_CHARS"),
    ("RC32", RCP, "REASON = ('Receipt law: this answer", "REASON = ('Receipt rule: this answer",
     "the block reason starts with the gate's mark", ("RLP00-couldnt-verify", "RLX04-own-block-then-the-claim-again"), "constant REASON; design 5"),
    ("RC33", RCP, '"  1. Run the check. If it is cheap, this is almost always the right move.\\n"', '""',
     "the block reason gives the three ways out", ("RLD80-reason-quotes-the-claim-and-gives-three-ways-out",), "design 5"),
    # -- reading a text: marks, quotes, code, structure
    ("RC34", RCP, 'MARK_QUOTE = "\\ue002"', 'MARK_QUOTE = "\\ue001"',
     "words in quotation marks are no receipt", ("RLD125-words-in-quotation-marks-are-no-receipt",), "constant MARK_QUOTE"),
    ("RC35", RCP, 'MARK_CODE = "\\ue001"', 'MARK_CODE = "\\ue002"',
     "an inline code span is evidence", ("RLD124-code-spans-are-the-only-receipt",), "constant MARK_CODE"),
    ("RC36", RCP, 'MARK_BLOCK = "\\ue000"', 'MARK_BLOCK = "\\ue002"',
     "the mark of a fenced block is not the mark of quoted words", ("RLD125-words-in-quotation-marks-are-no-receipt",),
     "constant MARK_BLOCK"),
    ("RC37", RCP, '(("’", "\'"), ', "(",
     "a curly apostrophe is read as an apostrophe", ("RLO09-curly-apostrophe", "RL1C4-we-cant-curly-apostrophe"), "constant CHAR_MAP; RL-1"),
    ("RC38", RCP, '("“", \'"\'), ("”", \'"\'), ', "",
     "curly double quotes are quotation marks", ("RLD138-passive-phrase-in-curly-double-quotes",), "constant CHAR_MAP"),
    ("RC39", RCP, '("–", " - "), ("—", " - "),', "",
     "a dash continues the sentence and ends what was not verified", ("RLD26-receipt-after-a-dash",), "constant CHAR_MAP"),
    ("RC40", RCP, "    text = FENCE_ONE_LINE.sub(MARK_CODE, text)\n", "",
     "a fence that opens and closes on one line hides only itself", ("RLD126-text-after-a-one-line-fence-is-read",),
     "constant FENCE_ONE_LINE"),
    ("RC41", RCP, '    text = FENCE.sub("\\n" + MARK_BLOCK + "\\n", text)\n', "",
     "words inside a fenced block are not the assistant's claim", ("RLD65-claim-inside-a-fenced-block-only",), "constant FENCE"),
    ("RC42", RCP, "    text = QUOTED_DOUBLE.sub(MARK_QUOTE, text)\n", "",
     "words in double quotation marks are not the assistant's claim", ("RLH02-phrase-inside-double-quotes",),
     "constant QUOTED_DOUBLE; RL-5"),
    ("RC43", RCP, "    text = QUOTED_SINGLE.sub(MARK_QUOTE, text)\n", "",
     "words in single quotation marks are not the assistant's claim", ("RLD127-phrase-in-single-quotes",), "constant QUOTED_SINGLE"),
    ("RC44", RCP, '    return EMPHASIS.sub("", text)', "    return text",
     "bold or italic marks inside a claim do not hide it", ("RLP06-bold-not", "RLP07-italic-not"), "constant EMPHASIS; RL-3"),
    ("RC45", RCP, "        elif HEADING.match(line):", "        elif False:",
     "a heading is a title, not a claim", ("RLD64-heading-only",), "constant HEADING"),
    ("RC46", RCP, "            item = LIST_ITEM.match(line)", "            item = None",
     "a list item is a sentence of its own", ("RLD35-label-then-list-one-item-bare",), "constant LIST_ITEM"),
    ("RC47", RCP, "        if TABLE_ROW.match(line):", "        if False:",
     "a table row is a sentence of its own", ("RLD128-each-table-row-is-a-sentence",), "constant TABLE_ROW"),
    ("RC48", RCP, "        if len(rows) >= 2 and TABLE_RULE.match(rows[1]):", "        if False:",
     "a table's header is found by the rule line under it", ("RLH09-table-of-test-cases",), "constant TABLE_RULE"),
    ("RC49", RCP, "for w in EXAMPLE_TABLE_WORDS + ASSUMPTION_TABLE_WORDS):", "for w in ASSUMPTION_TABLE_WORDS):",
     "a row of a table of examples is not a claim", ("RLH09-table-of-test-cases", "RLVD5-table-of-test-cases"),
     "constant EXAMPLE_TABLE_WORDS; RL-5"),
    ("RC50", RCP, "for w in EXAMPLE_TABLE_WORDS + ASSUMPTION_TABLE_WORDS):", "for w in EXAMPLE_TABLE_WORDS):",
     "a row of a register of assumptions is not an inability claim",
     ("RLD104-assumptions-table", "RLD120-plan-register-table-content-basis-status"), "constant ASSUMPTION_TABLE_WORDS"),
    ("RC51", RCP, "            parts = [s.strip() for s in SENTENCE_END.split(joined) if s.strip()]", "            parts = [joined.strip()]",
     "a paragraph is cut into sentences", ("RLD20-receipt-in-the-sentence-before", "RLR10-the-hook-ran-then-bare-claim"),
     "constant SENTENCE_END; RL-6"),
    ("RC52", RCP, "LABEL_MAX_CHARS = 60 ", "LABEL_MAX_CHARS = 6 ",
     "a short label line may introduce the block under a claim", ("RLF01-command-and-error-in-a-fenced-block",),
     "constant LABEL_MAX_CHARS; RL-4"),
    ("RC53", RCP, "    return any(w in words for w in LABEL_WORDS)", "    return True",
     "only a label that speaks of an attempt, an error or an output joins the block to the claim",
     ("RLD29-fenced-block-after-a-label-that-names-no-attempt",), "constant LABEL_WORDS"),
    ("RC54", RCP, "                if len(out) >= 2 and _is_label(out[-1]):", "                if False:",
     "\"Attempt and failure:\" joins the block under it to the claim before it", ("RLF01-command-and-error-in-a-fenced-block",), "RL-4"),
    ("RC55", RCP, "len(s) > LABEL_MAX_CHARS or find_claims(s):", "len(s) > LABEL_MAX_CHARS:",
     "a sentence that makes a claim is never a label", ("RLD133-a-claim-is-never-a-label-for-the-block-under-it",), "new rule"),
    ("RC56", RCP, '                out[-1] = out[-1] + " " + MARK_BLOCK', "                pass",
     "a fenced block belongs to the sentence above it", ("RLD27-fenced-block-directly-under-the-claim",), "RL-4"),
    ("RC57", RCP, '            elif following[0] == "rows" or (following[0] == "para" and kind == "para"):',
     '            elif following[0] == "para" and kind == "para":',
     "a line that ends with a colon goes on in the rows of the table under it", ("RLD46-lead-in-then-table-rows-with-receipts",),
     "new rule"),
    ("RC58", RCP, '            elif following[0] == "rows" or (following[0] == "para" and kind == "para"):',
     '            elif following[0] == "rows":',
     "a line that ends with a colon goes on in the paragraph after it", ("RLD49a-lead-in-continues-in-the-next-paragraph",),
     "new rule"),
    # -- claims: the word lists
    ("RC59", RCP, '_advs = r"(?:\\s+%s){0,2}" % ADVERB', '_advs = ""',
     "an adverb between \"could not\" and the verb does not hide the claim",
     ("RLP08-adverb-between", "RLP10-could-not-yet-verify"), "constant ADVERB; RL-3"),
    ("RC60", RCP, 'MODAL_NOT = r"(?:can\'t|cannot|', 'MODAL_NOT = r"(?:cannot|',
     "the contraction \"can't\" is matched", ("RLP01-cant-verify", "RLP02-cant-confirm", "RLP03-cant-determine"),
     "constant MODAL_NOT; RL-1"),
    ("RC61", RCP, '"cross-check", "validate", ', '"cross-check", ',
     "the verbs of verifying are a list, and \"validate\" is on it", ("RLP18-couldnt-validate",), "constant VERIFY_VERBS; RL-3"),
    ("RC62", RCP, 'VERIFY_PARTICIPLES = ("verified", ', "VERIFY_PARTICIPLES = (",
     "\"could not be verified\" is a claim", ("RLP11-passive-could-not-be-verified",), "constant VERIFY_PARTICIPLES; RL-3"),
    ("RC63", RCP, 'CLAIM_GERUNDS = ("verifying", "confirming", ', 'CLAIM_GERUNDS = ("verifying", ',
     "\"no way of confirming\" is a claim", ("RLVB08-no-way-of-confirming",), "constant CLAIM_GERUNDS; RL-3"),
    ("RC64", RCP, '"info", "figure", "figures", ', '"info", ',
     "\"not available\" is a claim when it is said of data", ("RLP04-not-available",), "constant DATA_NOUNS; RL-3"),
    ("RC65", RCP, 'UNVERIFIED_FOLLOWERS = ("at", ', "UNVERIFIED_FOLLOWERS = (",
     "\"unverified at the end\" is a predicate, not a description", ("RLP14-were-unverified",), "constant UNVERIFIED_FOLLOWERS"),
    ("RC66", RCP, 'DEGREE_WORDS = ("yet", ', "DEGREE_WORDS = (",
     "\"not yet available\" is a claim", ("RLD134-not-yet-available",), "constant DEGREE_WORDS"),
    ("RC67", RCP, 'LINK_WORDS = ("for", ', "LINK_WORDS = (",
     "\"the figures for 2024 are not available\" is a claim", ("RLD135-figures-for-a-year-are-not-available",), "constant LINK_WORDS"),
    # -- claims: the families (constant CLAIM_FAMILIES), one break each
    ("RC68", RCP, '("passive", re.compile(r"\\b%s', '("passive", re.compile(r"(?!)%s',
     "family: could not be verified", ("RLP11-passive-could-not-be-verified", "RLP12-passive-cannot-be-confirmed"), "RL-3"),
    ("RC69", RCP, '("unable", re.compile(r"\\bunable', '("unable", re.compile(r"(?!)unable',
     "family: unable to verify", ("RLP38-unable-to-verify-alone", "RLP09-unable-to-fully-confirm"), "RL-8 M04"),
    ("RC70", RCP, '("not-able", re.compile(r"(?:', '("not-able", re.compile(r"(?!)(?:',
     "family: not able to verify", ("RLP26-im-not-able-to", "RLP27-we-werent-able-to", "RLP28-havent-been-able-to"), "RL-3"),
    ("RC71", RCP, '("failed-to", re.compile(r"\\bfailed', '("failed-to", re.compile(r"(?!)failed',
     "family: failed to confirm", ("RLP31-failed-to-confirm",), "RL-3"),
    ("RC72", RCP, '("no-way", re.compile(r"\\bno', '("no-way", re.compile(r"(?!)no',
     "family: no way to verify", ("RLP23-no-way-of-knowing", "RLVB08-no-way-of-confirming"), "RL-3"),
    ("RC73", RCP, '("no-access", re.compile(r"\\b(?:', '("no-access", re.compile(r"(?!)(?:',
     "family: no access to", ("RLP25-dont-have-access",), "RL-3"),
    ("RC74", RCP, '("impossible", re.compile(r"%s\\s+(?:for', '("impossible", re.compile(r"(?!)%s\\s+(?:for',
     "family: impossible to verify", ("RLP24-impossible-to-verify", "RLD13-not-possible-to-verify"), "RL-3"),
    ("RC75", RCP, '("impossible", re.compile(r"\\b(?:verification', '("impossible", re.compile(r"(?!)(?:verification',
     "family: verification was not possible", ("RLP32-verification-was-not-possible",), "RL-3"),
    ("RC76", RCP, '("unverified", re.compile(r"(?<![\\w-])(?:unverified', '("unverified", re.compile(r"(?!)(?:unverified',
     "family: unverified, unconfirmed", ("RLP13-remains-unverified", "RLP34-table-cells", "RLP35-label-form"), "RL-8 M04; RL-3"),
    ("RC77", RCP, '("not-available", re.compile(r"\\b%s', '("not-available", re.compile(r"(?!)%s',
     "family: not available", ("RLP04-not-available", "RLP05-isnt-available"), "RL-3"),
    ("RC78", RCP, '("no-data", re.compile(r"\\bno', '("no-data", re.compile(r"(?!)no',
     "family: no data exists", ("RLP39-no-data-exists", "RLP30-no-records-exist"), "RL-8 M04; RL-3"),
    ("RC79", RCP, '("unverified", re.compile(r"(?<![\\w-])(?:unverified', '("unverified", re.compile(r"\\b(?:unverified',
     "a compound that ends in -unverified is a name, not a claim", ("RLD108-section-name-as-a-compound",), "house form"),
    # -- claims: whose claim it is
    ("RC80", RCP, '("modal", re.compile(r"\\b%s%s\\s+%s" % (MODAL_NOT, _advs, _vverb), re.I), True),',
     '("modal", re.compile(r"\\b%s%s\\s+%s" % (MODAL_NOT, _advs, _vverb), re.I), False),',
     "somebody else's inability is not the assistant's claim", ("RLD50-third-party-noun-subject", "RLD51-general-you"), "RL-5"),
    ("RC81", RCP, 'SELF_SUBJECTS = ("i", "we")', 'SELF_SUBJECTS = ("i",)',
     "\"we\" is the assistant", ("RLD05-we-couldnt-reach", "RLP27-we-werent-able-to"), "constant SELF_SUBJECTS"),
    ("RC82", RCP, 'SELF_NOUNS = ("session", ', "SELF_NOUNS = (",
     "\"this session cannot ...\" is the assistant's claim", ("RLD07-this-session-cannot-reach",), "constant SELF_NOUNS"),
    ("RC83", RCP, 'IMPERSONAL_SUBJECTS = ("there",)', "IMPERSONAL_SUBJECTS = ()",
     "\"there is no way to ...\" is the assistant's claim", ("RLD130-there-is-no-way-to",), "constant IMPERSONAL_SUBJECTS"),
    ("RC84", RCP, 'JOINING_WORDS = ("and", ', "JOINING_WORDS = (",
     "a claim joined by \"and\" with its subject left out is the assistant's", ("RLD111-first-person-left-out-before-a-joining-word",),
     "constant JOINING_WORDS"),
    ("RC85", RCP, '            if SELF_WORD.search(head):\n                return "self"\n', "",
     "\"I\" in the joined clause makes the claim the assistant's", ("RLD131-first-person-inside-the-joined-clause",),
     "constant SELF_WORD"),
    ("RC86", RCP, '            return "other" if OTHER_START.match(head) else "none"', '            return "none"',
     "a joined clause about something else is not the assistant's claim", ("RLD110-other-subject-before-a-joining-word",),
     "constant OTHER_START"),
    ("RC87", RCP, 'SKIPPED_WORDS = ("am", "is", "are", "was", ', 'SKIPPED_WORDS = ("am", "is", "are", ',
     "auxiliaries between the subject and the claim are passed over", ("RLP17-unable-to-check", "RLP09-unable-to-fully-confirm"),
     "constant SKIPPED_WORDS"),
    ("RC88", RCP, "SUBJECT_REACH = 6 ", "SUBJECT_REACH = 0 ",
     "the subject is looked for before the claim", ("RLP00-couldnt-verify",), "constant SUBJECT_REACH"),
    ("RD10", RCP, "BEFORE_REACH = 600 ", "BEFORE_REACH = 0 ",
     "the words before a claim are read", ("RLH01-nothing-i-couldnt-verify", "RLD50-third-party-noun-subject"),
     "constant BEFORE_REACH"),
    ("RD11", RCP, "            before = sentence[max(0, start - BEFORE_REACH):start]", "            before = sentence[:start]",
     "a very long sentence is read in time", ("RLZ19-one-very-long-sentence-does-not-run-into-the-deadline",),
     "constant BEFORE_REACH"),
    ("RC89", RCP, 'CLAUSE_OPENERS = ":;(,|"', 'CLAUSE_OPENERS = ";(,|"',
     "a claim right after a colon has no subject and is the assistant's", ("RLD10-list-item-could-not-verify",),
     "constant CLAUSE_OPENERS"),
    ("RC90", RCP, 'SUBJECT_PRONOUNS = ("i", ', "SUBJECT_PRONOUNS = (",
     "\"if I cannot ...\": the pronoun between the condition and the claim", ("RLH04-conditional-promise",),
     "constant SUBJECT_PRONOUNS"),
    # -- sentences that hold the words and make no claim
    ("RC91", RCP, "    if QUESTION_END.search(sentence):\n        return []\n", "",
     "a question makes no claim", ("RLD68-question-with-first-person",), "constant QUESTION_END; RL-5"),
    ("RC92", RCP, "            if (NEGATED_BEFORE.search(before) or ", "            if (",
     "\"nothing I couldn't verify\" is no claim", ("RLH01-nothing-i-couldnt-verify", "RLVD1-nothing-i-couldnt-verify"),
     "constant NEGATED_BEFORE; RL-5"),
    ("RC93", RCP, "CONDITIONAL_BEFORE.search(before) or ", "",
     "\"if I cannot verify ...\" is no claim", ("RLH04-conditional-promise", "RLD54-conditional-whatever"),
     "constant CONDITIONAL_BEFORE; RL-5"),
    ("RC94", RCP, " or REPORTED_BEFORE.search(before)", "",
     "what a tool or a person said is not the assistant's claim", ("RLD58-reported-log-line", "RLH15-tools-error-text-after-a-colon"),
     "constant REPORTED_BEFORE; RL-5"),
    ("RC95", RCP, "or SUPERSEDED_BEFORE.search(before) ", "",
     "\"at first I could not ...\" is about a state that ended", ("RLH12-resolved-inside-the-sentence", "RLD60-superseded-initially"),
     "constant SUPERSEDED_BEFORE; RL-5"),
    ("RC96", RCP, 'SUPERSEDED_WORDS = ("at first", ', "SUPERSEDED_WORDS = (",
     "\"at first\" marks a state that ended", ("RLH12-resolved-inside-the-sentence",), "constant SUPERSEDED_WORDS"),
    ("RC97", RCP, " or MENTION_BEFORE.search(before)", "",
     "a sentence about wording is no claim", ("RLH07-sentence-about-the-rule-unquoted", "RLD59-sentence-about-the-wording"),
     "constant MENTION_BEFORE; RL-5"),
    ("RC98", RCP, 'MENTION_WORDS = ("phrase", ', "MENTION_WORDS = (",
     "\"phrase\" marks a sentence about wording", ("RLH07-sentence-about-the-rule-unquoted",), "constant MENTION_WORDS"),
    ("RC99", RCP, '            if family == "passive" and GENERIC_BEFORE.search(before):', "            if False:",
     "a general statement in the passive is no claim", ("RLD206-general-statement-with-a-verb-of-verifying",), "constant GENERIC_BEFORE"),
    ("RD01", RCP, "                    NEGATED_CLAUSE.search(before) or ", "                    ",
     "\"none is unverified\" is no claim", ("RLH05-none-is-unverified", "RLH06-no-items-are-unverified"),
     "constant NEGATED_CLAUSE; RL-5"),
    ("RD02", RCP, "ASSUMPTION_BEFORE.search(before) or SECTION_BEFORE", "SECTION_BEFORE",
     "the status of an assumption is no inability claim", ("RLD105-assumption-in-parentheses",), "constant ASSUMPTION_BEFORE"),
    ("RD03", RCP, " or SECTION_BEFORE.search(before)", "",
     "the section name \"In scope and unverified\" is no claim", ("RLD101-section-label-with-provenance",),
     "constant SECTION_BEFORE"),
    ("RD04", RCP, "                    or LABELLED_BEFORE.search(before) or ", "                    or ",
     "\"labelled as unverified\" names a label", ("RLD107-labelled-as-unverified",), "constant LABELLED_BEFORE"),
    ("RD05", RCP, " or ATTRIBUTIVE_BEFORE.search(before)", "",
     "\"an unverified, old assertion\" is a description", ("RLD122-attributive-before-a-comma",), "constant ATTRIBUTIVE_BEFORE"),
    ("RD06", RCP, " and STATUS_BEFORE.search(before)", " and False",
     "\"Status: unconfirmed\" is a field of the plan's register", ("RLD103-assumption-register-status",),
     "constant STATUS_BEFORE"),
    # -- receipts: what was not verified is not its own receipt
    ("RD07", RCP, "        begin = label.end() if label else end", "        begin = end",
     "in \"Unverified: X\" the words after the colon say what was not verified",
     ("RLD132-label-form-what-was-not-verified-follows-the-colon",), "constant LABEL_COLON"),
    ("RD08", RCP, "        finish = min(stop.start() if stop else len(sentence), limit)", "        finish = end",
     "a receipt word inside what was not verified is no receipt",
     ("RLR01-receipt-word-is-the-unverified-thing", "RLR03-permission-is-the-object", "RLR07-404-is-the-object"),
     "constant OBJECT_END; RL-6"),
    ("RD09", RCP, "        finish = min(stop.start() if stop else len(sentence), limit)", "        finish = limit",
     "what was not verified ends at a colon, a dash, a bracket or a clause word",
     ("RLF00-ran-and-returned", "RLF05-server-answered-http-500"), "constant OBJECT_END; RL-4"),
    # -- the rules of the prose scan (results/2026-11-15/receipt-gate-fix/prose-scan.md) and the two classes of verbs
    ('RE01', RCP, '"access", "obtain", ',
     '"access", ',
     '"could not obtain" is a claim', ('RLD06-couldnt-obtain',), 'constant ACCESS_VERBS; RL-3'),
    ('RE02', RCP, '"found", "reached", ',
     '"found", ',
     '"could not be reached" is a claim', ('RLD142-past-passive-could-not-be-reached',), 'constant ACCESS_PARTICIPLES; RL-3'),
    ('RE03', RCP, '_advs, _apart), re.I), False),',
     '_advs, _vpart), re.I), False),',
     'family: could not be reached (the past passive of the verbs of reaching)', ('RLD142-past-passive-could-not-be-reached', 'RLD143-past-passive-could-not-be-determined'), 'RL-3'),
    ('RE04', RCP, '% (MODAL_NOT_PAST, _advs, _advs, _apart)',
     '% (MODAL_NOT, _advs, _advs, _apart)',
     '"cannot be determined at compile time" describes code: only the past form is a report', ('RLD147-general-passive-cannot-be-determined', 'RLD140-general-passive-about-code'), 'constant MODAL_NOT_PAST'),
    ('RE05', RCP, '("modal-access", re.compile(r"\\b%s',
     '("modal-access", re.compile(r"(?!)%s',
     'family: could not access, find, reach', ('RLP20-couldnt-access', 'RLD05-we-couldnt-reach'), 'RL-3'),
    ('RE06', RCP, '            if family == "modal-access" and who == GENERAL_SUBJECT and not PAST_MODAL.match(sentence, m.start()):\n                continue\n',
     '',
     '"we can\'t access X from a worker" describes code', ('RLD145-general-we-cant-access',), 'constant GENERAL_SUBJECT'),
    ('RE07', RCP, ' and not PAST_MODAL.match(sentence, m.start()):',
     ':',
     '"we couldn\'t access X" reports what happened', ('RLD146-we-couldnt-access',), 'constant PAST_MODAL'),
    ('RE08', RCP, 'GENERAL_SUBJECT = "we" ',
     'GENERAL_SUBJECT = "i" ',
     'the subject that also speaks for code is "we", not "I"', ('RLD145-general-we-cant-access', 'RLP20-couldnt-access'), 'constant GENERAL_SUBJECT'),
    ('RE09', RCP, '(?:(?:this|that|it|them|these|those)\\s+)?(?:in|out|off)',
     '(?:in|out|off)',
     '"check this in" is not a check', ('RLD166-cant-check-this-in',), 'constant ACCESS_VERBS'),
    ('RE10', RCP, 'reasons?|differences?|',
     'reasons?|',
     '"could not find any difference" reports a result', ('RLD196-could-not-find-any-difference',), 'constant ACCESS_VERBS'),
    ('RE11', RCP, 'r"duplicates?|typos?)\\b)(?!\\s+a\\s+single\\b)"',
     'r"duplicates?|typos?)\\b)"',
     '"could not find a single ..." reports a result', ('RLD164-could-not-find-a-single-failing-test',), 'constant ACCESS_VERBS'),
    ('RE12', RCP, '                r"(?!\\s+(?:any|one|another)\\s+(?:\\w+\\s+)?(?:failing|failed|broken|failures?|counter-?examples?)\\b)"\n',
     '',
     '"could not find any failing tests" reports a result', ('RLD212-couldnt-find-any-failing-tests',), 'constant ACCESS_VERBS'),
    ('RE13', RCP, '                r"(?!\\s+(?:a|an|any)\\s+(?:better|simpler|cheaper|faster|cleaner|shorter|smaller|safer|stronger|more\\s+\\w+|less\\s+\\w+)\\b)",\n',
     ',\n',
     '"could not find a better X" reports a result', ('RLD188-couldnt-find-a-better-trade',), 'constant ACCESS_VERBS'),
    ('RE14', RCP, '(?:(?:a|an|any|the|another)\\s+)?(?:\\w+\\s+)?(?:conclusion',
     '(?:(?:a|an|any|the|another)\\s+)?(?:conclusion',
     '"could not reach a different conclusion" is not about reaching a place', ('RLD167-couldnt-reach-a-different-conclusion',), 'constant ACCESS_VERBS'),
    ('RE15', RCP, 'r"locate\\b(?!\\s+a\\s+single\\b)"',
     '"locate"',
     '"could not locate a single ..." reports a result', ('RLD197-couldnt-locate-a-single-call-site',), 'constant ACCESS_VERBS'),
    ('RE16', RCP, '("know", re.compile(r"\\bno',
     '("know", re.compile(r"(?!)no',
     'family: no way to know, no way of knowing', ('RLP23-no-way-of-knowing', 'RLD178-i-have-no-way-to-know'), 'constant KNOW_VERBS; RL-3'),
    ('RE17', RCP, '("know", re.compile(r"%s',
     '("know", re.compile(r"(?!)%s',
     'family: impossible to tell', ('RLD191-it-was-impossible-to-tell',), 'RL-3'),
    ('RE18', RCP, 'KNOW_GERUNDS = ("knowing", ',
     'KNOW_GERUNDS = (',
     '"no way of knowing" is a claim', ('RLP23-no-way-of-knowing',), 'constant KNOW_GERUNDS'),
    ('RE19', RCP, 'KNOW_VERBS = (r"know\\b", ',
     'KNOW_VERBS = (',
     '"no way to know" is judged as a statement that may be general', ('RLD159-no-way-to-know-what-the-caller-intended', 'RLD178-i-have-no-way-to-know'), 'constant KNOW_VERBS'),
    ('RE20', RCP, '_not_know = r"(?!%s)" % _know',
     '_not_know = ""',
     '"impossible to tell from ..." is judged with "know", not with "verify"', ('RLD187-impossible-to-tell-from-the-box-score',), 'new rule'),
    ('RE21', RCP, "(?:\\bnot|n't)\\s+(?:possible|feasible))",
     '\\bnot\\s+(?:possible|feasible))',
     '"wasn\'t possible to ..." is a claim', ('RLD175-wasnt-possible-to-obtain',), 'constant NOT_POSSIBLE; RL-3'),
    ('RE22', RCP, 'OWN_IN_CLAIM.search(m.group(0)) or ',
     '',
     '"no way for me to know" is the assistant\'s claim', ('RLD210-no-way-for-me-to-know',), 'constant OWN_IN_CLAIM'),
    ('RE23', RCP, '(personal and who != "none")',
     'False',
     '"I have no way to know" is the assistant\'s claim', ('RLD178-i-have-no-way-to-know', 'RLP23-no-way-of-knowing'), 'new rule'),
    ('RE24', RCP, '\n                                         or PAST_STATE.search(sentence[max(0, start - PAST_REACH):m.end()]))',
     ')',
     '"there was no way to tell" reports what happened', ('RLD177-there-was-no-way-to-tell', 'RLD191-it-was-impossible-to-tell'), 'constant PAST_STATE'),
    ('RE25', RCP, 'PAST_REACH = 30 ',
     'PAST_REACH = 0 ',
     'the word that makes it a report is looked for before the claim', ('RLD177-there-was-no-way-to-tell',), 'constant PAST_REACH'),
    ('RE26', RCP, '(CAUSATIVE_BEFORE.search(before) or HYPOTHETICAL_BEFORE.search(before))',
     '(HYPOTHETICAL_BEFORE.search(before))',
     '"a bug made it impossible to ..." is about the bug', ('RLD162-a-regression-made-it-impossible-to-obtain',), 'constant CAUSATIVE_BEFORE'),
    ('RE27', RCP, '(CAUSATIVE_BEFORE.search(before) or HYPOTHETICAL_BEFORE.search(before))',
     '(CAUSATIVE_BEFORE.search(before))',
     '"it would be impossible to ..." claims nothing that happened', ('RLD208-it-would-be-impossible',), 'constant HYPOTHETICAL_BEFORE'),
    ('RE28', RCP, 'STREAM_WORDS = ("more", ',
     'STREAM_WORDS = (',
     '"there is no more data to read" is about a stream', ('RLD207-no-more-data-to-read',), 'constant STREAM_WORDS'),
    ('RE29', RCP, '_data_end = r"(?=\\s*(?:$|[.,;:!?)\\]]|(?:%s)\\b))" % "|".join(DATA_FOLLOWERS)',
     '_data_end = ""',
     '"no data loss", "no record type": the noun is part of a name', ('RLD156-no-data-loss', 'RLD157-no-record-type'), 'constant DATA_FOLLOWERS'),
    ('RE30', RCP, 'DATA_FOLLOWERS = ("for", ',
     'DATA_FOLLOWERS = (',
     '"there is no data for 2019" is a claim', ('RLP29-there-is-no-data-for', 'RLD179-no-data-for-a-year'), 'constant DATA_FOLLOWERS'),
    ('RE31', RCP, 'SCOPE_WORDS = ("at", ',
     'SCOPE_WORDS = (',
     '"not available at compile time" says where a thing is offered', ('RLD158-not-available-at-compile-time',), 'constant SCOPE_WORDS'),
    ('RE32', RCP, 'HERE_AND_NOW = (r"the\\s+moment", ',
     'HERE_AND_NOW = (',
     '"not available at the moment" is a claim', ('RLD182-not-available-at-the-moment',), 'constant HERE_AND_NOW'),
    ('RE33', RCP, '(CONDITION_BEFORE.search(before) or REPORTED_THAT.search(before))',
     '(REPORTED_THAT.search(before))',
     'a clause that states a condition claims nothing', ('RLD150-condition-whenever-could-not-be-reached', 'RLD151-a-bug-where-could-not-be-found', 'RLD152-when-the-checksum-cannot-be-verified', 'RLD153-if-the-migration-could-not-be-verified'), 'constant CONDITION_BEFORE'),
    ('RE34', RCP, '"where", "whose", ',
     '"where", ',
     '"a player whose team could not be found": a clause that describes', ('RLD186-a-player-whose-team-could-not-be-found',), 'constant CONDITION_WORDS'),
    ('RE35', RCP, '[^,;:.!?()]*$" % "|".join(CONDITION_WORDS)',
     '[^;:.!?()]*$" % "|".join(CONDITION_WORDS)',
     'a comma ends the condition: what follows is a claim again', ('RLD176-a-comma-ends-the-condition',), 'constant CONDITION_BEFORE'),
    ('RE36', RCP, '(CONDITION_BEFORE.search(before) or REPORTED_THAT.search(before))',
     '(CONDITION_BEFORE.search(before))',
     '"he wrote that the figures were not available" is what he wrote', ('RLD190-he-wrote-that-the-figures-were-not-available', 'RLD204-the-model-card-says-the-data-is-not-available'), 'constant REPORTED_THAT'),
    ('RE37', RCP, '|told\\s+\\w+)(?:\\s+that)?\\b|',
     '|told\\s+\\w+)\\s+that\\b|',
     'reported speech needs no "that"', ('RLD204-the-model-card-says-the-data-is-not-available',), 'constant REPORTED_THAT'),
    ('RE38', RCP, '\\s+that\\b)[^,;:.!?()]*$"\n',
     '\\s+that\\b)[^.!?()]*$"\n',
     'a semicolon ends what was said', ('RLD205-a-semicolon-ends-what-was-said',), 'constant REPORTED_THAT'),
    ('RE39', RCP, 'REPORTED_NOUNS = "claim|',
     'REPORTED_NOUNS = "',
     '"the claim that X could not be verified" names a claim', ('RLD198-the-old-claim-that-is-withdrawn',), 'constant REPORTED_NOUNS'),
    ('RE40', RCP, "(?:\\b(?:%s|not)|n't)\\s+that",
     '(?:\\b(?:%s|not))\\s+that',
     '"it isn\'t that the data is not available" denies it', ('RLD199-it-isnt-that-the-data-is-not-available',), 'constant REPORTED_THAT'),
    ('RE41', RCP, "(?:\\b(?:%s|not)|n't)\\s+that",
     "(?:\\b(?:%s)|n't)\\s+that",
     '"it is not that the data is unavailable" denies it', ('RLD211-it-is-not-that',), 'constant REPORTED_THAT'),
    ('RE42', RCP, ' or REPORTED_OPEN.search(before)',
     '',
     '"it says so (can\'t confirm ...)": the parenthesis holds what was said', ('RLD170-reported-in-parentheses',), 'constant REPORTED_OPEN'),
    ('RE43', RCP, 'REPORTED_VERBS = (r"said|says|',
     'REPORTED_VERBS = (r"said|',
     '"says" is a verb of saying', ('RLD170-reported-in-parentheses', 'RLD204-the-model-card-says-the-data-is-not-available'), 'constant REPORTED_VERBS'),
    ('RE44', RCP, '\n                    or SUPERSEDED_AFTER.match(sentence[m.end():m.end() + AFTER_REACH])',
     '',
     '"couldn\'t find it at first; ..." is about a state that ended', ('RLD168-couldnt-find-it-at-first',), 'constant SUPERSEDED_AFTER'),
    ('RE45', RCP, 'SUPERSEDED_AFTER_WORDS = ("at first", ',
     'SUPERSEDED_AFTER_WORDS = (',
     '"at first" after the claim marks a state that ended', ('RLD168-couldnt-find-it-at-first',), 'constant SUPERSEDED_AFTER_WORDS'),
    ('RE46', RCP, '            if family in EVENT_FAMILIES and PERIOD_AFTER.match(sentence[m.end():m.end() + AFTER_REACH]):\n                continue\n',
     '',
     '"could not be reached while ..." tells of an event and its period', ('RLD193-could-not-be-reached-while',), 'constant PERIOD_AFTER'),
    ('RE47', RCP, 'PERIOD_WORDS = ("while", ',
     'PERIOD_WORDS = (',
     '"while" opens the period of an event', ('RLD193-could-not-be-reached-while',), 'constant PERIOD_WORDS'),
    ('RE48', RCP, 'EVENT_FAMILIES = ("passive", "passive-past")',
     'EVENT_FAMILIES = ("passive",)',
     'the period is read for the past passive too', ('RLD193-could-not-be-reached-while',), 'constant EVENT_FAMILIES'),
    ('RE49', RCP, ' or ENUMERATION_BEFORE.search(before)',
     '',
     '"verified, likely, and unverified" is a list of labels; "12 verified, 3 unverified" a tally', ('RLD169-a-list-of-tiers', 'RLD174-a-tally-of-statuses'), 'constant ENUMERATION_BEFORE'),
    ('RE50', RCP, '|(?<![\\w-])A\\d{1,2}\\b)',
     ')',
     'an assumption named by its number ("A1 ... is unconfirmed") carries a status, not a claim', ('RLD171-an-assumption-named-by-its-number',), 'constant ASSUMPTION_BEFORE'),
    ('RE51', RCP, '        if label and family in SUBJECT_FIRST and re.search',
     '        if False and re.search',
     '"X cannot be reproduced: ...": the colon opens the explanation', ('RLD173-the-re-run-gives-another-number', 'RLD214-the-re-run-names-the-attempt'), 'constant SUBJECT_FIRST'),
    ('RE52', RCP, ' and re.search(r"[A-Za-z]", sentence[:start]):',
     ':',
     '"Unverified: X" at the start of a sentence still lists what was not verified', ('RLD132-label-form-what-was-not-verified-follows-the-colon', 'RLP35-label-form'), 'constant SUBJECT_FIRST'),
    ('RE53', RCP, 'SUBJECT_FIRST = ("passive", ',
     'SUBJECT_FIRST = (',
     'the passive is one of the families whose subject stands first', ('RLD213-the-record-shows-none', 'RLD214-the-re-run-names-the-attempt'), 'constant SUBJECT_FIRST'),
    ('RE54', RCP, '        if not _has_receipt(reach) and not placed[n]:',
     '        if not _has_receipt(reach):',
     '"couldn\'t find X in the repository" names what was searched', ('RLD200-couldnt-find-it-in-the-repo', 'RLD195-couldnt-find-anything-in-the-diff'), 'constant SEARCHED_PLACE'),
    ('RE55', RCP, 'SEARCH_CLAIM = re.compile(r"(?:find|locate)$"',
     'SEARCH_CLAIM = re.compile(r"(?:find|locate|verify)$"',
     'only a search names its place: "couldn\'t verify X in the config" stays bare', ('RLD203-couldnt-verify-it-in-the-repo',), 'constant SEARCH_CLAIM'),
    ('RE56', RCP, '\\s(?:in|on|under|across|within|among)\\s+(?:the|this',
     '\\s(?:under|across|within|among)\\s+(?:the|this',
     '"in the ..." names the place that was searched', ('RLD200-couldnt-find-it-in-the-repo',), 'constant SEARCHED_PLACE'),
    ('RE57', RCP, 'login|permissions?|path|route|way|means|connection)|',
     'login|permissions?)|',
     '"there is no live path to prod" names the missing means', ('RLD172-no-live-path-names-the-missing-means',), 'constant FAILURE'),
    ('RE58', RCP, "without\\s+[\\w'./-]+|",
     'without\\s+(?:sudo|root)|',
     '"without the raw body" names the missing means', ('RLD163-we-cant-verify-without-the-raw-body', 'RLD161-impossible-to-determine-without-consuming'), 'constant FAILURE'),
    ('RE59', RCP, '    r"(?:shows?|showed|gives?|gave|lists?|listed|holds?|held|contains?|contained)\\s+(?:none|nothing)|',
     '    r"',
     '"the record shows none" is a failure mode', ('RLD213-the-record-shows-none',), 'constant FAILURE'),
    ('RE60', RCP, 'sampled|sampling|spot-check(?:s|ed|ing)?|',
     '',
     '"sampled 200" names an attempt', ('RLD209-sampled-names-the-attempt',), 'constant ATTEMPT'),
    ('RE61', RCP, 're-?runs?|\\d+\\s+(?:runs|',
     '\\d+\\s+(?:runs|',
     '"the re-run gives 13" names an attempt', ('RLD214-the-re-run-names-the-attempt',), 'constant ATTEMPT'),
    ('RE62', RCP, '\\d+\\s+(?:runs|attempts|tries|trials|iterations|passes|requests|searches|queries|retries)|',
     '',
     '"50 runs" names an attempt', ('RLD165-couldnt-reproduce-in-fifty-runs',), 'constant ATTEMPT'),
    ('RE64', RCP, 'AFTER_REACH = 300 ',
     'AFTER_REACH = 0 ',
     'the words after a claim are read', ('RLD168-couldnt-find-it-at-first', 'RLD193-could-not-be-reached-while', 'RLD200-couldnt-find-it-in-the-repo'), 'constant AFTER_REACH'),
    ('RE63', RCP, ',\\s+(?=(?:which|where|that)\\s+(?:i|we)\\b)|',
     '',
     '", which I searched": what the assistant did is outside what was not verified', ('RLD189-no-record-which-i-searched',), 'constant OBJECT_END'),
]


# ------------------------------------------------------------------ the runner
def find_wiring(hooks):
    """The wiring files that belong to a hooks folder: {kind: path} for the project's and the plugin's found."""
    found = {}
    for kind, places in sorted(WIRING_PLACES.items()):
        for place in places:
            path = os.path.normpath(os.path.join(hooks, place))
            if os.path.isfile(path):
                found[kind] = path
                break
    return found


def make_copy(hooks, wiring, root, name):
    """A copy of the hooks (every plain file) and of each wiring file in a folder of its own -> (hooks copy,
    {kind: wiring copy}). The plugin's wiring file is copied with the wrapper beside it, as in the plugin."""
    folder = os.path.join(root, name)
    copy = os.path.join(folder, HOOKS_COPY)
    os.makedirs(copy)
    for entry in sorted(os.listdir(hooks)):
        src = os.path.join(hooks, entry)
        if os.path.isfile(src):
            shutil.copy(src, copy)
    wired = {}
    for kind, path in sorted(wiring.items()):
        wired[kind] = os.path.join(folder, WIRING_COPIES[kind])
        os.makedirs(os.path.dirname(wired[kind]))
        shutil.copy(path, wired[kind])
        wrapper = os.path.join(os.path.dirname(os.path.dirname(path)), "scripts", WRAPPER)
        if kind == PLUGIN_WIRING and os.path.isfile(wrapper):
            os.makedirs(os.path.join(folder, "plugin", "scripts"))
            shutil.copy(wrapper, os.path.join(folder, "plugin", "scripts", WRAPPER))
    return copy, wired


def run_table(copy, wired, names, jobs):
    """Run the test table on a copy -> (names of the failing cases, number of cases), or None when the table
    did not run to its last line."""
    cmd = [sys.executable, os.path.join(copy, TABLE_SCRIPT), "--hooks", copy, "--jobs", str(jobs), "--only-failing"]
    for kind in sorted(wired):
        cmd += ["--wiring", wired[kind]]
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        p = subprocess.run(cmd + list(names), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True,
                           env=env, timeout=TABLE_WAIT_SECONDS)
    except (OSError, subprocess.TimeoutExpired):
        return None
    summary = SUMMARY.search(p.stdout)
    if p.returncode not in (0, 1) or not summary:
        return None
    failing = [line.split("|")[0].strip() for line in p.stdout.splitlines() if line.rstrip().endswith(FAIL_MARK)]
    if len(failing) != int(summary.group(3)):
        return None
    return failing, int(summary.group(1))


def test_break(entry, hooks, wiring, root, every_case):
    """-> (state, text): state is caught | SURVIVED | STALE | ERROR."""
    bid, fname, old, new, _rule, cases, _origin = entry
    if fname in (WIRING, PLUGIN_WIRING) and fname not in wiring:
        return "absent", "not run: this layout has no %s file (a project without the plugin)" % fname
    copy, wired = make_copy(hooks, wiring, root, bid)
    target = wired.get(fname) if fname in (WIRING, PLUGIN_WIRING) else os.path.join(copy, fname)
    try:
        with open(target, encoding="utf-8") as fh:
            text = fh.read()
    except (OSError, TypeError):
        return "ERROR", "ERROR (no file to break: %s)" % fname
    found = text.count(old)
    if found != 1 or old == new:
        return "STALE", "STALE (its text is found %d times)" % found
    with open(target, "w", encoding="utf-8") as fh:
        fh.write(text.replace(old, new))
    if not every_case:
        named = run_table(copy, wired, cases, NAMED_JOBS)
        if named is None:
            return "ERROR", "ERROR (the named cases did not run)"
        if named[0]:
            return "caught", "caught by " + named[0][0]
    whole = run_table(copy, wired, (), TABLE_JOBS)
    if whole is None:
        return "ERROR", "ERROR (the table did not run)"
    failing = whole[0]
    if not failing:
        return "SURVIVED", "SURVIVED"
    if every_case:
        unnamed = "" if any(c in failing for c in cases) else "; none of the named cases"
        more = ", ..." if len(failing) > SHOWN_CASES else ""
        return "caught", "caught by %d cases: %s%s%s" % (len(failing), ", ".join(failing[:SHOWN_CASES]), more, unnamed)
    return "caught", "caught by %s (not one of the named cases)" % failing[0]


def list_problems(hooks):
    """What is wrong with the list itself: an id used twice, a case named that the table does not have."""
    problems, seen = [], set()
    try:
        p = subprocess.run([sys.executable, os.path.join(hooks, TABLE_SCRIPT), "--list"], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, universal_newlines=True, timeout=TABLE_WAIT_SECONDS)
        known = set(line.split("|")[0].strip() for line in p.stdout.splitlines() if "|" in line)
    except (OSError, subprocess.TimeoutExpired):
        known = set()
    if not known:
        return ["the test table (%s) could not be listed" % TABLE_SCRIPT]
    for bid, fname, _old, _new, _rule, cases, _origin in BREAKS:
        if bid in seen or bid == CONTROL_ID:
            problems.append("%s: the id is used twice" % bid)
        seen.add(bid)
        if fname not in (TG, PRE, ENF, RCP, RCW, WIRING, PLUGIN_WIRING):
            problems.append("%s: %s is not a file this list may break" % (bid, fname))
        if not cases:
            problems.append("%s: names no case" % bid)
        problems += ["%s: the table has no case named %s" % (bid, c) for c in cases if c not in known]
    return problems


def main(argv):
    hooks, jobs, work, listing, every_case, wanted = HERE, DEFAULT_JOBS, None, False, False, []
    args = list(argv)
    while args:
        a = args.pop(0)
        if a in ("--hooks", "--jobs", "--work"):
            if not args:
                print("usage: %s needs a value" % a)
                return 2
            value = args.pop(0)
            if a == "--hooks":
                hooks = os.path.abspath(value)
            elif a == "--jobs":
                jobs = max(1, int(value))
            else:
                work = os.path.abspath(value)
        elif a == "--list":
            listing = True
        elif a == "--every-case":
            every_case = True
        elif a in ("-h", "--help"):
            print(__doc__)
            return 0
        elif a.startswith("--"):
            print("unknown option %s" % a)
            return 2
        else:
            wanted.append(a)
    chosen = [b for b in BREAKS if not wanted or any(b[0].startswith(w) for w in wanted)]
    if not chosen:
        print("no break has an id that starts with: %s" % " ".join(wanted))
        return 2
    if listing:
        for bid, fname, _old, _new, rule, cases, origin in chosen:
            print("%-5s | %-21s | %s | %s | %s" % (bid, fname, rule, ", ".join(cases), origin))
        return 0
    problems = list_problems(hooks)
    if problems:
        for line in problems:
            print("LIST: " + line)
        print("== the list itself is wrong in %d places; nothing was run ==" % len(problems))
        return 1
    wiring = find_wiring(hooks)
    if work is not None:
        os.makedirs(work, exist_ok=True)
    root = os.path.abspath(tempfile.mkdtemp(prefix="turn-gates-breaks-", dir=work))
    counts = {"caught": 0, "SURVIVED": 0, "STALE": 0, "ERROR": 0, "absent": 0}
    try:
        copy, wired = make_copy(hooks, wiring, root, CONTROL_ID)
        control = run_table(copy, wired, (), TABLE_JOBS)          # alone, before the breaks start
        if control is None:
            control_text, clean = "the table did not run on an unchanged copy", False
        else:
            control_text, clean = "%d failing of %d cases" % (len(control[0]), control[1]), not control[0]
            for name in control[0]:
                print("%-5s | %-21s | fails with no change: %s" % (CONTROL_ID, "-", name))
        with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
            futures = [(b, pool.submit(test_break, b, hooks, wiring, root, every_case)) for b in chosen]
            for (bid, fname, _old, _new, rule, _cases, _origin), future in futures:
                try:
                    state, text = future.result()
                except Exception as exc:
                    state, text = "ERROR", "ERROR (%s)" % type(exc).__name__
                counts[state] += 1
                print("%-5s | %-21s | %s | %s" % (bid, fname, text, rule))
                sys.stdout.flush()
    finally:
        if work is None:
            shutil.rmtree(root, ignore_errors=True)
    tail = "" if not counts["ERROR"] else ", %d could not be run" % counts["ERROR"]
    tail += "" if not counts["absent"] else ", %d not run (their wiring file is not in this layout)" % counts["absent"]
    print("== %d breaks: %d caught, %d survived, %d stale%s; control: %s ==" % (
        len(chosen), counts["caught"], counts["SURVIVED"], counts["STALE"], tail, control_text))
    return 0 if clean and counts["caught"] + counts["absent"] == len(chosen) and counts["caught"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
