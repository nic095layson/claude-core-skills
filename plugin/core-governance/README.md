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

Every hook runs through `scripts/run-unless-project-wired.sh`. If the session's project
already wires the same hook in its own `.claude/settings.json`, the wrapper exits silently
(fail-open), so a single-repository session that carries the pack does not run each hook
twice. Where repository hooks are not read, the plugin's copy runs.

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
- Self-tests from the copied location: classifier + Stop gate 27/27, receipt law 10/10.
- Wrapper pipe tests: defers (no output) when the project wires the hook; runs the trigger on
  the incident message and stays silent on trivia when it does not; passes stdin through to the
  Stop gate (block observed on a synthetic transcript).
- `--plugin-dir` smoke, headless `claude -p`, one run per arm (a mechanism check, not the
  pre-registered A/B): incident message → trigger context injected once, `adversarial-verify`
  and `scope-fence` loaded, no block; "what time zone is the draft in?" → nothing fired, direct
  answer. Evidence: `results/2026-10-13/gauntlet-fortification/raw/plugin-smoke/`.

## Package for upload

```bash
cd plugin && rm -rf core-governance/scripts/__pycache__ && \
  zip -r ../dist/core-governance.plugin core-governance && unzip -l ../dist/core-governance.plugin
```

The archive must contain exactly one `.claude-plugin/plugin.json`. Bump `version` in
`plugin.json` when the hooks change: marketplace installs stay on the pinned version until it moves.
