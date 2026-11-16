#!/usr/bin/env bash
# truncation.sh — what section 2 of the evidence pack shows when several registered hook values have drifted.
# Run: bash /tmp/claude-0/-home-user/ff01f16c-7b3f-5ea5-8051-7a95ac7cd1d1/scratchpad/merge-audit/work/rev-weekly-run/truncation.sh
# Works on a scratch copy of the merged library only (work/rev-weekly-run/mut2).
set -u
PACK=/tmp/claude-0/-home-user/ff01f16c-7b3f-5ea5-8051-7a95ac7cd1d1/scratchpad/merge-audit
W=$PACK/work/rev-weekly-run; M=$W/mut2
export PYTHONDONTWRITEBYTECODE=1
rm -rf "$M"; mkdir -p "$M"; git -C "$PACK/lib" archive 1ce99d5 | tar -x -C "$M"
git -C "$M" init -q; git -C "$M" add -A; git -C "$M" -c user.name=audit -c user.email=audit@example.invalid commit -qm base
cd "$M"
# drift five registered values by one each (numbers only)
sed -i 's/^TRIVIA_MAX_CHARS = 400/TRIVIA_MAX_CHARS = 401/' hooks/governance-enforce.py
python3 - <<'PY'
import json, re, io
reg = json.load(open("redteam/constants_registry.json"))
entries = reg if isinstance(reg, list) else reg.get("constants") or reg.get("entries") or reg
names = [e.get("name") or e.get("id") for e in entries if isinstance(e, dict)] if isinstance(entries, list) else list(entries)
print("registry entries:", len(names))
changed = 0
import glob
for f in sorted(glob.glob("hooks/*.py") + glob.glob("hooks/*.sh")):
    if "selftest" in f:
        continue
    s = open(f).read()
    def bump(m):
        global changed
        if changed >= 6:
            return m.group(0)
        changed += 1
        return m.group(1) + str(int(m.group(2)) + 1)
    s2 = re.sub(r"(?m)^([A-Z][A-Z_]{3,} = )(\d+)\b", bump, s)
    if s2 != s:
        open(f, "w").write(s2)
print("numeric constants bumped by one in hooks/:", changed)
PY
echo "--- registry_check.py, FULL output (exit $(python3 .claude/skills/red-team/scripts/registry_check.py --root . > "$W/out/registry-full.txt" 2>&1; echo $?)): $(wc -l < "$W/out/registry-full.txt") lines"
sed 's/^/    /' "$W/out/registry-full.txt" | cut -c1-140
echo "--- the evidence pack, section 2 as the weekly run receives it:"
bash .claude/skills/independent-audit/scripts/weekly_review.sh "$M" 2>&1 | sed -n '/^== 2\./,/^== 3\./p' | sed 's/^/    /' | cut -c1-140
echo "--- pack exit code: $(bash .claude/skills/independent-audit/scripts/weekly_review.sh "$M" > /dev/null 2>&1; echo $?)"
cd /; rm -rf "$M"
