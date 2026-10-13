# Claude Code documentation quotes, fetched 2026-10-13 (WebFetch, verbatim lines from the fetched page text)

## https://code.claude.com/docs/en/settings — Settings in cloud sessions
## Settings in cloud sessions

A [cloud session](/docs/en/claude-code-on-the-web) runs in a [cloud environment](/docs/en/cloud-environments) on a fresh clone of your repository, not on your machine. That changes which settings reach it:

* **Shared project settings** (`.claude/settings.json`): read in a session with one repository, because the file is part of the clone and the session starts inside it. Commit a setting there to apply it in those sessions. In an Anthropic-hosted environment, a session with several repositories starts above the clones and reads only the `enabledPlugins` and `extraKnownMarketplaces` keys from each repository's `.claude/settings.json`, not permission rules, hooks, `env`, or other keys. The marketplaces and plugins those two keys declare still [don't load in a cloud session](/docs/en/cloud-environments#what-carries-over-from-your-setup). For a self-hosted environment, see [which repository's settings apply](/docs/en/self-hosted-environments-configuration#repository-settings-in-sessions-with-several-repositories).
* **User and project local settings** (`~/.claude/settings.json` and `.claude/settings.local.json`): not read. Both stay on your machine, and the local file isn't in the clone.
* **Managed settings**: a `managed-settings.json` file or MDM profile on your device doesn't reach a cloud session. Your organization's [server-managed settings](/docs/en/server-managed-settings) do; [surface coverage](/docs/en/model-config#surface-coverage) lists which cloud sessions receive them. A [self-hosted environment](/docs/en/self-hosted-environments) also reads the managed settings file in its runner image. [How Claude Code combines managed sources](/docs/en/managed-settings#how-claude-code-combines-managed-sources) says when that file applies.
* **`/config`**: in your browser at claude.ai/code, opens the Claude Code section of your claude.ai settings instead of changing a value. To change a setting for a cloud session, set an [environment variable](/docs/en/cloud-environments#set-environment-variables) on the environment, or in a session with one repository, commit the key to that repository's `.claude/settings.json`.

## https://code.claude.com/docs/en/settings — scope table row
| Shared project | `.claude/settings.json` | Everyone working in the folder that contains it. In a git repository, commit it so teammates get it | Team permissions, hooks, plugins, and the environment variables the project needs |

## https://code.claude.com/docs/en/hooks-guide
### Re-inject context after compaction

When Claude's context window fills up, compaction summarizes the conversation to free space. This can lose important details. Use a `SessionStart` hook with a `compact` matcher to re-inject critical context after every compaction.
Your script can parse that JSON and act on any of those fields. `UserPromptSubmit` hooks get the `prompt` text instead, `SessionStart` hooks get a `source` of `startup`, `resume`, `clear`, `compact`, or `fork`, and so on. See [Common input fields](/docs/en/hooks#common-input-fields) in the reference for shared fields, and each event's section for event-specific schemas.
For `UserPromptSubmit` hooks, use `hookSpecificOutput.additionalContext` instead to inject text into Claude's context. Nest `additionalContext` inside `hookSpecificOutput`; if you place it at the top level of the JSON, Claude Code silently ignores it. For example, this output adds the current branch state to every prompt:
| `SessionStart` | how the session started | `startup`, `resume`, `clear`, `compact`, `fork` |
| `PreCompact`, `PostCompact` | what triggered compaction | `manual`, `auto` |
| `.claude/settings.json` | Single project | Yes, can be committed to the repo |
Claude Code overrides a Stop hook after it blocks eight times in a row with no tool call from Claude in between. Your hook script needs to check whether it already triggered a continuation. Parse the `stop_hook_active` field from the JSON input and exit early if it's `true`:

## https://code.claude.com/docs/en/memory
| **User instructions** | `~/.claude/CLAUDE.md` | Personal preferences for all projects | Code styling preferences, personal tooling shortcuts | Only you (all projects) |
Claude Code loads `CLAUDE.md` and `CLAUDE.local.md` from your current working directory and every directory above it. Run Claude Code in `foo/bar/` and it loads instructions from `foo/bar/CLAUDE.md`, `foo/CLAUDE.md`, and any `CLAUDE.local.md` files alongside them.
Auto memory is machine-local. All worktrees and subdirectories within the same git repository share one auto memory directory. Files are not shared across machines or cloud environments.
### Instructions seem lost after `/compact`

Project-root CLAUDE.md survives compaction: after `/compact`, Claude re-reads it from disk and re-injects it into the session. Nested CLAUDE.md files in subdirectories and rules with [`paths:` frontmatter](#path-specific-rules) load again on demand.

If an instruction disappeared after compaction, it was given only in conversation, lives in a nested CLAUDE.md that hasn't reloaded yet, or is a path-scoped rule that hasn't matched a file since. Add conversation-only instructions to CLAUDE.md to make them persist. See [What survives compaction](/docs/en/context-window#what-survives-compaction) for the full breakdown.
