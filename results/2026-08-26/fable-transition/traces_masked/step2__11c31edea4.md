# trace 11c31edea4  (case: lessons-ledger__ll1)
served_model: claude-fable-5 | skills_loaded: none | stop_hook_blocks: 0 | scope_reminder_injected: False

ASSISTANT TEXT:
Noted — that's a classic one. DEBUG=true muffling errors in staging is exactly the kind of thing that's worth a one-liner somewhere so nobody re-chases it. Let me check if this project already has a place for that.

[TOOL Bash: {"command": "ls -la /private/tmp/fta_2026-08-26/with/lessons-ledger__ll1/r1; ls /Users/davidlayson/.claude/projects/-private-tmp-fta-2026-08-26-with-lessons-ledger--ll1-r1/memory/ 2>/dev/null; cat /Users/davidlayson/.claude/projects/-private-tmp-fta-2026-08-26-with-lessons-ledger--ll1-r1/memory/MEMO]

[TOOL RESULT: Exit code 1
total 0
drwxr-xr-x@ 2 davidlayson  wheel  64 Aug 26 17:27 .
drwxr-xr-x@ 3 davidlayson  wheel  96 Aug 26 17:27 ..]

[TOOL Write: {"file_path": "/Users/davidlayson/.claude/projects/-private-tmp-fta-2026-08-26-with-lessons-ledger--ll1-r1/memory/staging-debug-true-swallowed-errors.md", "content": "---\nname: staging-debug-true-swallowed-errors\ndescription: Staging config with DEBUG=true silently swallowed all errors \u2014 cost]

[TOOL RESULT: File created successfully at: /Users/davidlayson/.claude/projects/-private-tmp-fta-2026-08-26-with-lessons-ledger--ll1-r1/memory/staging-debug-true-swallowed-errors.md]

[TOOL Write: {"file_path": "/Users/davidlayson/.claude/projects/-private-tmp-fta-2026-08-26-with-lessons-ledger--ll1-r1/memory/MEMORY.md", "content": "- [Staging DEBUG=true swallowed errors](staging-debug-true-swallowed-errors.md) \u2014 2h lost 2026-08-26; check DEBUG flag first when an env goes silent\n"}]

[TOOL RESULT: File created successfully at: /Users/davidlayson/.claude/projects/-private-tmp-fta-2026-08-26-with-lessons-ledger--ll1-r1/memory/MEMORY.md (file state is current in your context — no need to Read it b]

ASSISTANT TEXT:
Logged it. Recap:

- **Recorded** the DEBUG=true staging incident as a project memory (symptom → root cause → how to avoid re-chasing it), so future sessions in this project will know to check env flags before digging into application code when staging goes silent.
- **Didn't** load the `lessons-ledger` skill — your global doctrine retired it on 2026-07-11 and says not to reactivate, so I just wrote the note directly.
- One adjacent thought, not acted on since you didn't ask: a startup assertion or CI check that fails when `DEBUG` is true outside local dev would make this class of bug impossible to repeat. Say the word if you want that wired up.

Otherwise, nothing else pending — what's next?
