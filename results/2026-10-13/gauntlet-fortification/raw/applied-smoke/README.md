# Applied-pack smoke (2026-10-13, after PRs 105 and 106 were opened)

One headless `claude -p` run per clone, inside the real checkout of each branch
(`/home/user/fantasy-basketball-2026-27` and `/home/user/yahoo-fantasy-basketball` at the PR
heads), default model, `--max-turns 12`, `--allowedTools Skill,Read,Glob,Grep`, prompt = the
owner's 2026-10-12 23:41 message verbatim. Nothing but the committed files was present: the
hooks ran from each clone's own `.claude/settings.json`. A mechanism check (N=1 per clone), not
the pre-registered A/B. `summary.json` is the tally; `out.jsonl` the full streams. The kit run
ended on the turn cap (`error_max_turns`) after the governors loaded; the deck run completed
with an assessment.
