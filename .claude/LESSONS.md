# Lessons Ledger — claude-core-skills

Project ledger per the lessons-ledger governor. Entries: symptom → root cause →
evidence → status. An entry without evidence is a rumor and does not belong here.

### INC-1 — Cloud GitHub grant assumed live in a local session

- Date: 2026-07-11 (discovered and worked around the same day).
- Symptom: owner had granted Claude GitHub access in claude.ai settings and had
  used it the previous day; a local Claude Code session on his Mac could not see
  or clone any private repo, and repeated "you already have permission"
  expectations failed.
- Root cause: integration grants made on claude.ai live on Anthropic's servers
  and are scoped to cloud sessions. They never reach a local machine, which
  needs its own credentials. The local Mac had none: no `~/.gitconfig`, no SSH
  keys, no `gh` CLI.
- Evidence: `gh auth status` before fix → "not logged into any GitHub hosts";
  `ls ~/.ssh` empty; `git config --global --list` empty. After installing gh
  v2.96.0 and device-flow login: authenticated as nic095layson, private repos
  listable. (Session of 2026-07-11.)
- Status: FIXED for the primary machine (gh installed at `~/.local/bin/gh`,
  authed via keyring, `gh auth setup-git` done). The general rule is codified in
  live-state-truth ("Environment boundaries") and debugging-playbook §5.
- Lesson: capabilities are per-environment facts — enumerate them live in the
  session that needs them; never infer access here from access somewhere else.
