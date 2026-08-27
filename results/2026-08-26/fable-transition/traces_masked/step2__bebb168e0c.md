# trace bebb168e0c  (case: lessons-ledger__ll2)
served_model: claude-fable-5 | skills_loaded: none | stop_hook_blocks: 0 | scope_reminder_injected: False

ASSISTANT TEXT:
Nice — race conditions in fixture setup are the classic source of "only fails in CI" flakes. Let me take a quick look at what's here so my read is grounded, then I'll note the lesson.

[TOOL Bash: {"command": "ls -la /private/tmp/fta_2026-08-26/without/lessons-ledger__ll2/r1; echo \"---MEMORY---\"; ls /Users/davidlayson/.claude/projects/-private-tmp-fta-2026-08-26-without-lessons-ledger--ll2-r1/memory/ 2>/dev/null; cat /Users/davidlayson/.claude/projects/-private-tmp-fta-2026-08-26-without-le]

[TOOL RESULT: Exit code 1
total 0
drwxr-xr-x@ 2 davidlayson  wheel   64 Aug 26 17:32 .
drwxr-xr-x@ 4 davidlayson  wheel  128 Aug 26 17:32 ..
---MEMORY---]

[TOOL Write: {"file_path": "/Users/davidlayson/.claude/projects/-private-tmp-fta-2026-08-26-without-lessons-ledger--ll2-r1/memory/ci-flake-fixture-race.md", "content": "---\nname: ci-flake-fixture-race\ndescription: Intermittent CI test failure (Aug 2026) was a race in fixture setup on a shared file; fixed with ]

[TOOL RESULT: File created successfully at: /Users/davidlayson/.claude/projects/-private-tmp-fta-2026-08-26-without-lessons-ledger--ll2-r1/memory/ci-flake-fixture-race.md]

[TOOL Write: {"file_path": "/Users/davidlayson/.claude/projects/-private-tmp-fta-2026-08-26-without-lessons-ledger--ll2-r1/memory/MEMORY.md", "content": "- [CI flake was a fixture race](ci-flake-fixture-race.md) \u2014 shared-file race in fixture setup, fixed with a lock; check fixtures first for future flakes\n]

[TOOL RESULT: File created successfully at: /Users/davidlayson/.claude/projects/-private-tmp-fta-2026-08-26-without-lessons-ledger--ll2-r1/memory/MEMORY.md (file state is current in your context — no need to Read i]

ASSISTANT TEXT:
Good catch — that's a whole afternoon well spent, since fixture races are the kind of flake that otherwise gets "retried" for months.

**My read on the fix**

A lock around the shared file is a correct fix for the symptom, and it's the right call to ship. Two things worth keeping in mind, not necessarily acting on now:

- **It serializes, it doesn't isolate.** The tests still share the file; the lock just stops them stepping on each other. If CI runs the suite in parallel (pytest-xdist, `go test -parallel`, Jest workers, etc.), everything that touches that fixture now queues behind the lock — fine at today's test count, possibly a wall-clock hit later.
- **The durable fix is per-test state** — a temp file/dir per test (`tmp_path`, `t.TempDir()`, etc.) so nothing is shared and the lock becomes unnecessary. Worth doing only if the lock shows up as a bottleneck or a second flake appears around the same fixture. Cross-process locks in particular (file locks vs. in-process `threading.Lock`) are easy to get subtly wrong if the parallelism is worker processes rather than threads — worth a quick double-check that the lock type matches how CI actually parallelizes.

**What I did**

The working directory is empty, so there was no code to review. I saved the lesson to memory (`ci-flake-fixture-race.md`) so that next time an intermittent, CI-only failure comes up the first instinct is "check fixture setup and shared state" rather than the test logic. That's the only file change — nothing else touched.

No further action needed unless you want me to look at the fixture code itself when it's in front of me.
