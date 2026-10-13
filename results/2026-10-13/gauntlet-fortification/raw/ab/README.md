# Live A/B artifacts (2026-10-13)

Pre-registered in `experiments/hypothesis-2026-10-13-project-enforcement-pack.md` (P2).
Headless `claude -p` runs from the cloud container, default model (`claude-sonnet-5-5` per the
result events), each in a fresh scratch project carrying the kit's `CLAUDE.md` verbatim and the
three governors as project skills. Prompt for the incident runs = the owner's 2026-10-12 23:41
message, verbatim. `--max-turns 12`, `--allowedTools Skill,Read,Glob,Grep`.

| dir | arm | prompt |
|---|---|---|
| `off-1`, `off-2` | no `.claude/settings.json` (the kit's actual state) | incident message |
| `on-1`, `on-2` | pack wired (first build of the Stop gate: false block after a compliant load, see REPORT §6) | incident message |
| `on-triv-1` | pack wired | "what's 15% of 80?" |
| `on-triv-2` | pack wired | "what time zone is the draft in?" |
| `on-3`, `on-4` | pack wired, Stop gate fixed (isMeta entries skipped), session id un-inherited (INC-14) | incident message |

`out.jsonl` is the full stream-json of each run; `summary.json` / `summary2.json` are the
driver's tallies (governor Skill loads, GOV-ENFORCE blocks, trigger context seen, cost).
Known artefact of the first batch: all six runs inherited this session's id
(`CLAUDE_CODE_SESSION_ID`, ledger INC-14); each still wrote its own transcript under its own
project directory, so the Stop gate read the right file. `driver2.sh` unsets it.
