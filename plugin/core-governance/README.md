# core-governance — the enforcement pack as a Claude Code plugin

The same seven governance hooks that `.claude/settings.json` wires at project scope in
`nic095layson/claude-core-skills`, packaged so they can reach sessions that do not read a
repository's settings. Built 2026-10-13 after `.claude/LESSONS.md` INC-2026-10-13-01 (a
three-week cloud session on a governed repository loaded no governor: nothing on that surface
carried the mechanism).

## What it does

| Event | Hook | Effect |
|---|---|---|
| `UserPromptSubmit` | `governance-trigger.py` | classifies the owner's message (`govclass.py`); on governed work injects one line naming the governor to load |
| `Stop` | `governance-enforce.py` | blocks a governed-class turn that finished without a governor `Skill` load after the owner's latest message |
| `Stop` | `receipt-law-stop-gate.sh` | the receipt law ("can't" needs a receipt) |
| `PreToolUse` (`Edit\|Write\|NotebookEdit`) | `plan-gate-first-write-reminder.sh`, `scope-fence-reminder.sh` | once-per-session reminders at the first file write |
| `SessionStart` (`compact\|resume`) | `session-doctrine.sh` | post-compaction protocol; re-arms the reminders |

Every hook runs through `scripts/run-unless-project-wired.sh`. It yields (exits silently,
fail-open) only where repository hooks are known to run: a **local** session
(`CLAUDE_CODE_REMOTE` unset) whose project `.claude/settings.json` wires this same hook under
its `hooks` key (parsed, not grepped: an allow rule naming the file does not count). In a
**cloud** session the plugin always runs. Reason: the cloud harness reads repository hooks in
a one-repository session and not in a several-repository one, and a hook process cannot tell
which it is in; a yield there could silence both copies in exactly the case the plugin exists
for (independent verifier finding, 2026-10-13). The cost is a duplicate trigger line in a
one-repository cloud session that also carries the pack; the first-write reminders and the
receipt-law gate keep per-session sentinels and do not double-fire. The rule is pinned by
`scripts/selftest-wrapper.sh` (9 cases).

`scripts/*.py` and `scripts/*.sh` (other than the wrapper) are **byte-identical copies** of
`hooks/*` in this repository; the guard (`guard_essentials.sh`) fails if they drift. Edit
`hooks/`, run the self-tests, then re-copy. Symlinks are not an option: the validator rejects
component paths that leave the plugin root.

## Routes to a session (what is documented, what is observed — 2026-10-13)

1. **claude.ai account (the route for cloud sessions).** Customize → Plugins → Add → Upload
   plugin, as a `.plugin` or `.zip` holding one `.claude-plugin/plugin.json`. The claude.com
   plugins page: a plugin added to the account "downloads as a synced plugin the next time you
   start a session signed in to the same account." The loading reference: in terminal sessions a
   synced plugin's "skills, agents, hooks, MCP servers, and LSP servers all load." **Observed**
   in the authoring cloud container: a claude.ai-synced plugin was present and reported
   `loaded` (`claude plugin list`), so account plugins do reach cloud sessions. **Not observed:**
   a synced plugin's hooks firing in a cloud session — the synced plugin at hand had no hooks.
   Verify after upload: in a cloud session, `claude plugin list` shows `core-governance@synced`
   loaded, and a disputed question produces the trigger line.
   **Observed 2026-10-13:** loaded and running (Stop gates through the wrapper) in a long-lived
   cloud session with three repositories attached, minutes after the upload. **Not loaded** in a
   fresh session created through the remote-session API (no plugins three minutes in). Fresh
   sessions started from claude.ai/code: not yet measured.
2. **Marketplace (terminal).** `claude plugin marketplace add nic095layson/claude-core-skills`
   then `claude plugin install core-governance@core-skills`, or in one step
   `/plugin install core-governance --marketplace nic095layson/claude-core-skills`.
   The marketplace manifest is `.claude-plugin/marketplace.json` at the repository root.
3. **Testing.** `claude --plugin-dir /path/to/plugin/core-governance`.
4. **Not a route:** `extraKnownMarketplaces` + `enabledPlugins` in a repository's
   `.claude/settings.json`. The settings documentation (read 2026-10-13): a multi-repository
   cloud session reads those two keys, but "the marketplaces and plugins those two keys declare
   still don't load in a cloud session"; the loading reference adds that a cloud session never
   shows the trust dialog that adding a repository-declared marketplace requires. The
   2026-10-13 after-report's §4.4 proposed this route from the first sentence alone; this README
   and Runbook 4 supersede it.

## Verification record

- `claude plugin validate --strict` on the plugin and on the marketplace: `Validation passed`
  (Claude Code 2.1.296, 2026-10-13).
- Self-tests from the copied location: classifier + Stop gate 27/27 at 0.1.0, 30/30 at 0.1.1;
  receipt law 10/10.
- Wrapper pipe tests: defers (no output) when the project wires the hook; runs the trigger on
  the incident message and stays silent on trivia when it does not; passes stdin through to the
  Stop gate (block observed on a synthetic transcript).
- `--plugin-dir` smoke, headless `claude -p`, one run per arm (a mechanism check, not the
  pre-registered A/B): incident message → trigger context injected once, `adversarial-verify`
  and `scope-fence` loaded, no block; "what time zone is the draft in?" → nothing fired, direct
  answer. Evidence: `results/2026-10-13/gauntlet-fortification/raw/plugin-smoke/`.

- Hook-source attribution: the stream-json of the smoke runs names the hook event but not its
  command, so it cannot by itself show the plugin fired. A separate one-turn run with
  `--debug-file` (trivia prompt, same plugin, scratch directory) logged "Read hooks.json for
  plugin core-governance", "Loading hooks from plugin: core-governance" and "Registered 6
  hooks", and named no project settings file: `raw/plugin-smoke/attribution-debug-2026-10-13.txt`.
- Wrapper self-test (`scripts/selftest-wrapper.sh`): 9/9 — yields only local+wired; runs on
  cloud+wired, allow-rule-only, bare, and unparseable settings; stdin reaches the Stop gate.
- Independent verifier (read-only agent, 2026-10-13): validator, hooks.json shape, parity,
  symlinks/modes, ignore rules, wrapper behaviour, smoke fields, plugin.json fields all PASS;
  it flagged the stream-attribution gap (answered by the debug run above), the original yield
  rule (replaced by the rule above), and a hard-coded `/usr/bin/jq` in the two first-write
  reminders inherited from `hooks/` (not fixed here; owner decision in the after-report).

## 0.1.3 (2026-10-29)

Turn gates (ledger INC-2026-10-29-01): the Stop gate also checks what the turn DID — an outward action
(commit, push, PR create/update/merge) needs plan-gate before it and adversarial-verify in the turn,
however short the owner's message; a new PreToolUse hook denies a PR merge without the owner's word
and reminds (advisory) when plan-gate is loaded but no plan has been shown before the first write.
Scripts re-synced byte-identical to `hooks/`; `hooks.json` gains one PreToolUse group.

## 0.1.2 (2026-10-20)

The red-team fixes (`results/2026-10-19/system-red-team/REPORT.md`, owner-approved): the trigger
drops the skip clause on build prompts and gains the advisory cue tier; the Stop gate matches Skill
names exactly, requires each class's primary governor, ignores slash-command echoes, and allows
review-only no-tool short answers; the receipt gate handles curly quotes, paraphrases and word
boundaries and requires the receipt beside the claim; jq is gone from the reminders and the
compaction hook (`selftest-reminders.sh` pins it). Scripts re-synced byte-identical to `hooks/`.
Known cost, now measured rather than assumed (D-GF-9, red-team run L8): in a one-repository cloud
session that also carries the pack, the Stop BLOCK doubles as well as the trigger line — accepted,
the owner decided, as noisy but harmless; the reminders and receipt gate still dedupe by sentinel.

## 0.1.1 (2026-10-13)

`governance-enforce.py` now skips harness-written user entries (task notifications, wake envelopes)
when it looks for the owner's prompt. Before, a background task finishing mid-turn let a governed,
unloaded answer through (ledger INC-2026-10-13-02; reproduced red-first, pinned by three fixture checks).

## Package for upload

```bash
cd plugin && rm -rf core-governance/scripts/__pycache__ && \
  zip -r ../dist/core-governance.plugin core-governance && unzip -l ../dist/core-governance.plugin
```

The archive must contain exactly one `.claude-plugin/plugin.json`. Bump `version` in
`plugin.json` when the hooks change: marketplace installs stay on the pinned version until it moves.
