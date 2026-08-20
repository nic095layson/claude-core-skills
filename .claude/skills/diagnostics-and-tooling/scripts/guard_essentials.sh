#!/usr/bin/env bash
# guard_essentials.sh — the no-regression guard.
#
# Asserts every property the 2026-08-11 integrity audit and the 2026-08-12
# pre-merge validation established as essential. Run it BEFORE an operation to
# take a baseline and AFTER to prove nothing was lost. Exit 0 = all hold.
#
# Why this exists: INC-11 lost a validated feature because a change was verified
# against the wrong baseline. A merge that "looks additive" is not proof. This
# script is the proof, and it fails loudly.
#
# Usage: bash .claude/skills/diagnostics-and-tooling/scripts/guard_essentials.sh
set -u
cd "$(git rev-parse --show-toplevel)" || exit 2
FAIL=0
ok()   { printf "  ok    %s\n" "$*"; }
bad()  { printf "  FAIL  %s\n" "$*"; FAIL=1; }
have() { grep -qF "$2" "$1" 2>/dev/null; }

echo "== guard_essentials =="

# --- 1. Every skill still lints ------------------------------------------
n=0; f=0
for d in .claude/skills/*/; do
  n=$((n+1))
  bash .claude/skills/diagnostics-and-tooling/scripts/lint_skill.sh "$d" 2>/dev/null | tail -1 | grep -q "RESULT: PASS" || { f=$((f+1)); bad "lint: $(basename "$d")"; }
done
[ "$f" -eq 0 ] && ok "lint: $n/$n skills PASS"

# --- 2. Governor mechanisms present (INC-9 patch) ------------------------
A=.claude/skills/adversarial-verify/SKILL.md
P=.claude/skills/plan-gate/SKILL.md
R=.claude/skills/after-report/SKILL.md
G=.claude/skills/gauntlet/SKILL.md
# whitespace-normalized: line wraps must not create false failures (2026-08-12)
chk() { python3 - "$1" "$2" "$3" <<'PY'
import re,sys
try: t=re.sub(r'\s+',' ',open(sys.argv[1],encoding='utf-8').read())
except Exception: sys.exit(1)
sys.exit(0 if re.sub(r'\s+',' ',sys.argv[2]) in t else 1)
PY
if [ $? -eq 0 ]; then ok "$3"; else bad "$3 — MISSING from $1"; fi; }

chk "$A" "Gap provenance"                                  "adversarial-verify: gap provenance"
chk "$A" "NOT-ATTEMPTED"                                   "adversarial-verify: NOT-ATTEMPTED state"
chk "$A" "The grade is binary"                             "adversarial-verify: binary-grade rule"
chk "$A" "6. The gap audit"                                "adversarial-verify: Step 6"
chk "$A" "no load-bearing gap remains"                     "adversarial-verify: Acceptance wired"
chk "$A" "needs a receipt"                                 "adversarial-verify: rule 6 receipt law"
chk "$A" "Mechanizing the arithmetic does not verify the inputs" "adversarial-verify: rule 7 loophole closed"
chk "$A" "The pass is proportional"                        "adversarial-verify: proportionality valve"
chk "$P" "Stopping the conversion"                         "plan-gate: stop-the-conversion rule"
chk "$P" "A cheap unknown never becomes an assumption"     "plan-gate: cheap-unknown clause"
chk "$P" "No ceremony on trivia"                           "plan-gate: anti-ceremony valve"
chk "$P" "The sizing test — the compressed form is earned, not chosen" "plan-gate: sizing test (INC-2026-08-19-01 D1)"
chk "$P" "emitted as its own turn content before the first" "plan-gate: gate-emitted-pre-work rule (D2)"
chk "$P" "Mandatory, not optional, for any phase whose expected observation depends on a source outside the" "plan-gate: branch rules mandatory when externally dependent"
chk "$G" "Named firing covers shape, not just load"      "gauntlet: shape-aware named firing"
chk "$R" "Quoting a source that states the claim"          "after-report: SUPPORTED basis rule"
chk "$R" "in scope and unverified"                         "after-report: Bounds split"
chk "$G" "plan-gate before acting"                         "gauntlet: the sequence"
chk "$G" "Triage first"                                    "gauntlet: triage valve"

# --- 3. Instructions block: GAUNTLET + receipt law survive ---------------
I=instructions/claude-ai-custom-instructions.md
BLOCK=$(awk '/^---- BEGIN PASTE ----$/{f=1;next} /^---- END PASTE ----$/{f=0} f' "$I" 2>/dev/null)
printf '%s' "$BLOCK" | grep -q "GAUNTLET"        && ok "instructions: GAUNTLET in paste block" || bad "instructions: GAUNTLET MISSING"
printf '%s' "$BLOCK" | grep -q "needs a receipt" && ok "instructions: receipt law in paste block" || bad "instructions: receipt law MISSING"
printf '%s' "$BLOCK" | grep -q "never from recall" && ok "instructions: aggregates law in paste block" || bad "instructions: aggregates law MISSING"
CH=$(printf '%s\n' "$BLOCK" | wc -c)
grep -q "$(printf "%s" "$CH" | sed 's/\(.\)\(...\)$/\1,\2/')" "$I" && ok "instructions: stated char count matches measured ($CH)" \
  || bad "instructions: stated char count disagrees with measured ($CH)"

# --- 4. Descriptions unchanged in shape (trigger surface) ----------------
python3 - <<'PY'
import re,glob,sys
bad=0
for p in sorted(glob.glob('.claude/skills/*/SKILL.md')):
    t=open(p,encoding='utf-8').read()
    m=re.match(r'\A---\s*\n(.*?)\n---\s*\n',t,re.DOTALL)
    if not m: print("  FAIL  no frontmatter: %s"%p); bad=1; continue
    try:
        import yaml; fm=yaml.safe_load(m.group(1))
    except Exception as e:
        print("  FAIL  frontmatter unparseable: %s"%p); bad=1; continue
    d=(fm or {}).get('description','') or ''
    if len(d.strip())>1024: print("  FAIL  description >1024 (INC-3): %s"%p); bad=1
print("  ok    descriptions: all parse, all <=1024 chars" if not bad else "")
sys.exit(bad)
PY
[ $? -eq 0 ] || FAIL=1

# --- 5. Ledger integrity: no duplicate keys ------------------------------
# The char class MUST include "-": ledger Rule 3 (2026-08-12) mints date keys
# like INC-2026-08-19-01, and the original class stopped at the first hyphen, so
# every date key collapsed to "INC-2026". The first date key passed; the SECOND
# would have reported a duplicate that does not exist. Caught 2026-08-20 by
# probing the check instead of trusting its PASS (CLAUDE.md: a failing check
# earns the same scrutiny as a failing artifact — so does a passing one).
dup=$(grep -oE "^### (INC|DEAD|DRIFT)-[0-9A-Za-z-]+" .claude/LESSONS.md 2>/dev/null | sort | uniq -d)
[ -z "$dup" ] && ok "ledger: no duplicate keys" || bad "ledger: DUPLICATE KEYS -> $dup"

# --- 6. Nothing deleted vs main ------------------------------------------
# Compare against the MERGE-BASE, not origin/main's tip. Against the tip, every
# file main gained after this branch started reads as "deleted here" — a false
# alarm that trained me to ignore a real one. The question is what THIS branch
# removed, and merge-base is the only baseline that answers it.
if git rev-parse --verify -q origin/main >/dev/null; then
  base=$(git merge-base HEAD origin/main 2>/dev/null)
  # Include the WORKING TREE and the index, not just committed history. The first
  # version compared "$base"..HEAD only, so a staged deletion passed clean until
  # after it was committed — the guard was blind exactly when it mattered most.
  DEL=$( { git diff --diff-filter=D --name-only "$base"..HEAD;
           git diff --diff-filter=D --name-only HEAD;
           git diff --cached --diff-filter=D --name-only HEAD; } 2>/dev/null | sort -u )
  ACK=.guard-acknowledged-deletions
  unack=""
  for f in $DEL; do
    grep -qE "^[[:space:]]*${f//./\.}([[:space:]]|#|$)" "$ACK" 2>/dev/null || unack="$unack $f"
  done
  nd=$(printf '%s\n' $DEL | grep -c . || true)
  if [ -z "$(echo $unack)" ]; then
    [ "$nd" -eq 0 ] && ok "no files deleted" || ok "$nd deletion(s), all acknowledged in $ACK"
  else
    bad "UNACKNOWLEDGED DELETION(S):"; for f in $unack; do echo "        $f"; done
  fi
  r=$(git diff --diff-filter=R --name-only "$base"..HEAD 2>/dev/null | wc -l)
  [ "$r" -eq 0 ] && ok "no files renamed vs merge-base" || bad "$r files renamed vs merge-base"
  behind=$(git rev-list --count HEAD..origin/main 2>/dev/null)
  [ "$behind" -eq 0 ] && ok "branch is current with origin/main" || bad "branch is BEHIND origin/main by $behind commit(s) — merge main before trusting this run"
fi

# --- 7. JSON + shell validity --------------------------------------------
jb=0; for f in evals/*.json; do python3 -c "import json;json.load(open('$f'))" 2>/dev/null || { bad "invalid JSON: $f"; jb=1; }; done
[ "$jb" -eq 0 ] && ok "evals: all JSON valid"
sb=0; for f in hooks/*.sh .claude/skills/*/scripts/*.sh; do [ -f "$f" ] || continue; bash -n "$f" 2>/dev/null || { bad "shell syntax: $f"; sb=1; }; done
[ "$sb" -eq 0 ] && ok "hooks/scripts: shell syntax valid"

echo "== RESULT: $([ $FAIL -eq 0 ] && echo PASS || echo FAIL) =="
exit $FAIL
