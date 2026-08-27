# trace 2d0de4d4cb  (case: lessons-ledger__ll1)
served_model: claude-fable-5 | skills_loaded: none | stop_hook_blocks: 0 | scope_reminder_injected: False

ASSISTANT TEXT:
Noted. One thing worth keeping so it doesn't bite again — let me check whether memory already has it.

[TOOL Bash: {"command": "cat /Users/davidlayson/.claude/projects/-private-tmp-fta-2026-08-26-without-lessons-ledger--ll1-r2/memory/MEMORY.md 2>/dev/null; ls /Users/davidlayson/.claude/projects/-private-tmp-fta-2026-08-26-without-lessons-ledger--ll1-r2/memory/", "description": "Check existing memory index"}]

[TOOL RESULT: (Bash completed with no output)]

ASSISTANT TEXT:
Memory is empty, so no duplicate. Saving the gotcha and the index entry.

[TOOL Write: {"file_path": "/Users/davidlayson/.claude/projects/-private-tmp-fta-2026-08-26-without-lessons-ledger--ll1-r2/memory/staging-debug-flag-swallows-errors.md", "content": "---\nname: staging-debug-flag-swallows-errors\ndescription: Staging config with DEBUG=true silently swallowed all errors; cost ~2h ]

[TOOL RESULT: File created successfully at: /Users/davidlayson/.claude/projects/-private-tmp-fta-2026-08-26-without-lessons-ledger--ll1-r2/memory/staging-debug-flag-swallows-errors.md]

[TOOL Write: {"file_path": "/Users/davidlayson/.claude/projects/-private-tmp-fta-2026-08-26-without-lessons-ledger--ll1-r2/memory/MEMORY.md", "content": "- [Staging DEBUG=true swallows errors](staging-debug-flag-swallows-errors.md) \u2014 check env config first when staging errors go silent\n"}]

[TOOL RESULT: File created successfully at: /Users/davidlayson/.claude/projects/-private-tmp-fta-2026-08-26-without-lessons-ledger--ll1-r2/memory/MEMORY.md (file state is current in your context — no need to Read i]

ASSISTANT TEXT:
Got it — glad it's sorted. Painful one, since a flag that hides errors looks exactly like "code is fine but wrong."

I saved one memory note so it doesn't recur: `DEBUG=true` in staging silently swallows errors → check env config first when staging failures go quiet. Nothing in the repo was touched.

One cheap follow-up if you want it later: a startup guard or CI check that fails when `DEBUG=true` in any non-local environment. Otherwise, moving on with you — what's next?
