# After the merge: what the owner does, in order

**Merging this pull request changes the hooks of sessions started inside this library only.** The weekly task's
session (a cloud session with several repositories attached) runs the account's plugin, and the kit and the
deck run their own copies. Each of those changes only when you do the step below for it.

| # | step | what it changes | how to check that it took |
|---|---|---|---|
| 1 | Upload the plugin `core-governance` 0.1.6 (below) | Cloud sessions with several repositories attached, the weekly task's among them, get the rebuilt merge gate, Stop gate and receipt gate: a scheduled run is a turn of its own and never merges, whatever you clicked before it. Until then those sessions run the version the account serves (0.1.4 on 2026-11-13), where a scheduled run inherits your last turn and can merge on an earlier "merge" word (findings F2-6, WR-1, SF-1) | In a NEW cloud session with two repositories attached: `grep -h '"version"' ~/.claude/plugins/synced/*/core-governance/.claude-plugin/plugin.json` prints `"version": "0.1.6",`. Then `python3 ~/.claude/plugins/synced/*/core-governance/scripts/selftest-turn-gates.py W` ends with `== 6 cases: 6 pass, 0 fail ==` |
| 2 | Merge the kit's sync pull request (`fantasy-basketball-2026-27`) | Sessions started inside the kit, its morning and afternoon runners among them, run the rebuilt hooks and the new wiring. The runners pick them up at their next run, when step 2 of their prompt merges main into `season/daily` | Inside the kit: `python3 hooks/selftest-turn-gates.py W` ends with `== 6 cases: 6 pass, 0 fail ==`, and `python3 hooks/selftest-turn-gates.py` with `== 740 cases: 740 pass, 0 fail ==` |
| 3 | Merge the deck's sync pull request (`yahoo-fantasy-basketball`) | The same for sessions started inside the deck | The same two commands inside the deck, the same two last lines |

Before step 2, read the lines marked **owner** in `other-repositories.md` (the table of what the kit's and the
deck's unattended runs do under the new gates). The morning runner, as its saved prompt words it, is neither
denied nor blocked. Three other stored instructions would be, and say what would have to change.

## Step 1 in detail

From a checkout of this library at the merged commit:

```bash
cd plugin && rm -rf core-governance/scripts/__pycache__ && mkdir -p ../dist && \
  zip -r ../dist/core-governance.plugin core-governance && unzip -l ../dist/core-governance.plugin
```

The listing must show one `core-governance/.claude-plugin/plugin.json`. Then on claude.ai: Customize → Plugins
→ Add → Upload plugin, and choose `dist/core-governance.plugin`.

What the check can and cannot show. A container syncs the account's plugins when it starts; a session that was
already running when you uploaded can keep the old copy. Run the check in a NEW session. If the weekly task's
own session still prints `"version": "0.1.4",`, that session has not synced again yet, and a scheduled run there
is still judged by 0.1.4.

## What does not change with any of these steps

- The weekly task stays off. Nothing here turns it back on.
- Nothing is merged for you: each step above is yours.
- A session on claude.ai (not Claude Code) runs no hooks at all.
