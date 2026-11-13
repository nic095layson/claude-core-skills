#!/usr/bin/env bash
# assumptions.sh — evidence from the pack for what the seven stored steps assume. Read-only on the pack.
# Run: bash /tmp/claude-0/-home-user/ff01f16c-7b3f-5ea5-8051-7a95ac7cd1d1/scratchpad/merge-audit/work/rev-weekly-run/assumptions.sh [section ...]
# Sections: preflight week records brief parity wiring promises   (default: all)
set -u
PACK=/tmp/claude-0/-home-user/ff01f16c-7b3f-5ea5-8051-7a95ac7cd1d1/scratchpad/merge-audit
P=$PACK/pack/trigger-prompt.raw.txt
export PYTHONDONTWRITEBYTECODE=1
cd "$PACK"
want() { [ $# -eq 0 ] && return 0; }
SECTIONS="${*:-preflight week records brief parity wiring promises history}"
has() { case " $SECTIONS " in *" $1 "*) return 0;; *) return 1;; esac; }

if has preflight; then
echo "### preflight — the library's rule for unattended runs, and the weekly task"
grep -n "Preflight every unattended run\|An unchecked run is a failed run" lib/.claude/skills/independent-audit/SKILL.md | cut -c1-120
echo "the word 'preflight' in the stored prompt:            $(grep -ci preflight "$P") occurrence(s)"
echo "preflight specs (*.json naming preflight) in the library: $(find lib -path lib/.git -prune -o -iname '*preflight*.json' -print | wc -l)"
echo "                                           in the kit:    $(find kit-full -path kit-full/.git -prune -o -iname '*preflight*.json' -print | tr '\n' ' ')"
echo "library files that call preflight.py or name a spec:  $(grep -rl 'preflight' lib --include=*.sh --include=*.json --include=*.py | grep -v '/.git/' | grep -v 'scripts/preflight.py\|test_independent_audit.py' | wc -l)"
echo
fi

if has week; then
echo "### week — what 'this week' is at Monday 06:43 Pacific"
python3 - <<'PY'
import datetime, re
PACK = "/tmp/claude-0/-home-user/ff01f16c-7b3f-5ea5-8051-7a95ac7cd1d1/scratchpad/merge-audit"
rows = [datetime.date.fromisoformat(m.group(1)) for m in re.finditer(r"^\| (\d{4}-\d\d-\d\d) \|", open(PACK + "/kit-full/report/corrections-log.md").read(), re.M)]
def wk(d):
    y, w, _ = d.isocalendar(); return "%d-W%02d" % (y, w)
for run in (datetime.date(2026, 11, 16), datetime.date(2026, 11, 23)):
    print("run on %s (%s): its ISO week is %s, which began %s 00:00, 6h43m before the run (Pacific)" % (run, run.strftime("%A"), wk(run), run))
    print("   kit rows in the run's own ISO week (%s): %d   | in the ISO week before (%s): %d   | in the 7 days before the run: %d"
          % (wk(run), sum(wk(d) == wk(run) for d in rows), wk(run - datetime.timedelta(7)), sum(wk(d) == wk(run - datetime.timedelta(7)) for d in rows),
             sum(run - datetime.timedelta(7) <= d < run for d in rows)))
PY
echo "the evidence pack's own unit:  $(grep -n 'per ISO week' lib/.claude/skills/independent-audit/scripts/weekly_review.sh | cut -c1-90)"
echo "the stored prompt's words:     $(grep -o "this week's new rows[^,]*\|the week's corrections rate per project\|If the week has no new corrections and nothing drifted, say so in five lines and propose nothing\|rate this week vs last\|dated in the last 7 days" "$P" | tr '\n' '|')"
echo
fi

if has records; then
echo "### records — 'each project's corrections log' and 'ledger entries (.claude/LESSONS.md)'"
for r in lib kit-full deck-full; do
  printf "%-10s corrections log: %-34s ledger at .claude/LESSONS.md: %-4s ledger elsewhere: %s\n" "$r" \
    "$( (ls $r/report/corrections-log.md $r/corrections-log.md 2>/dev/null || echo none) | tr '\n' ' ')" \
    "$([ -f $r/.claude/LESSONS.md ] && echo yes || echo no)" "$(ls $r/LESSONS.md 2>/dev/null || echo -)"
done
grep -n "Corrections\*\* → \`report/corrections-log.md\` in each project" lib/CLAUDE.md | cut -c1-110
echo
fi

if has brief; then
echo "### brief — the contract step 4 hands the auditor, and the question step 4 asks"
grep -n "^\*\*Objective\.\*\*\|^\*\*Output\.\*\* Exactly this\|^AUDIT: <n> claims\|^Notes: " lib/.claude/skills/independent-audit/auditor-brief.md | cut -c1-175
echo "stored prompt, step 4: $(grep -o 'Its question: [^?]*?' "$P")"
echo "stored prompt, step 4: $(grep -o 'It returns findings only\.' "$P")"
echo
fi

if has parity; then
echo "### parity — 'check that the hook files ... are identical across the three repos (cmp / checksum)'"
for r in lib kit-full deck-full; do echo "$r/hooks: $(git -C $r ls-files hooks | wc -l) tracked files"; done
echo "tracked in lib/hooks and absent from kit and deck: $(comm -23 <(git -C lib ls-files hooks | sort) <(git -C kit-full ls-files hooks | sort) | tr '\n' ' ')"
echo "of the files all three track, differing: $(for f in $(git -C kit-full ls-files hooks); do cmp -s lib/$f kit-full/$f && cmp -s lib/$f deck-full/$f || echo $f; done | wc -l)"
echo
fi

if has wiring; then
echo "### wiring — which tool calls of the run the pre-tool gate is run for at all"
grep -o '"matcher": "Edit|Write|NotebookEdit|Bash[^"]*"' lib/plugin/core-governance/hooks/hooks.json
echo "merge patterns the gate knows (hooks/turngate.py): $(grep -n '^MERGE_BASH\|return name.endswith("merge_pull_request")' lib/hooks/turngate.py | cut -c1-140 | tr '\n' ' ')"
echo "session tools that can put a change on main or merge, by name: $(grep -o 'enable_pr_auto_merge\|merge_pull_request\*\|push_files\*\|create_or_update_file\*\|update_pull_request_branch\*' pack/session-tools.txt | tr '\n' ' ')"
echo
fi

if has promises; then
echo "### promises — what a hook can see of each promise (the gate tests are extra_cases.py X10-X13)"
echo "the only scheduled-run rule in the hooks: $(grep -n 'scheduled run never merges' lib/hooks/turn-gates-pretool.py | cut -c1-110)"
for w in "draft" "proposal" "weekly-review" "enable_pr_auto_merge" "auto_merge"; do
  printf "  hook code lines (comments excluded) that test for %-22s %s\n" "'$w':" "$(grep -v '^\s*#' lib/hooks/turngate.py lib/hooks/turn-gates-pretool.py | grep -ic "$w")"
done
echo
fi

if has history; then
echo "### history — the library's own recorded registry failure of 2026-11-12, as section 2 of the pack would have shown it (tail -3)"
echo "full record: $(wc -l < lib/results/2026-11-12/qa-loop/p5-old-registry-on-live.txt) lines; first line: $(head -1 lib/results/2026-11-12/qa-loop/p5-old-registry-on-live.txt | cut -c1-90)"
tail -3 lib/results/2026-11-12/qa-loop/p5-old-registry-on-live.txt | sed 's/^/    | /' | cut -c1-150
grep -n "tail -3\|head -40\|^exit 0" lib/.claude/skills/independent-audit/scripts/weekly_review.sh | cut -c1-120
fi
