#!/usr/bin/env bash
# lint_skill.sh — mechanical lint for a Claude skill directory.
#
# Usage:   lint_skill.sh <path-to-skill-directory>
# Example: lint_skill.sh .claude/skills/plan-gate
#
# Checks (FAIL = must fix, WARN = should fix):
#   FAIL  SKILL.md missing
#   FAIL  YAML frontmatter missing or unparseable (needs python3 + PyYAML)
#   FAIL  frontmatter `name` missing/empty
#   FAIL  frontmatter `description` missing/empty
#   FAIL  `name` does not equal the directory basename
#   FAIL  description has no trigger language (nothing saying WHEN to load it)
#   FAIL  body (after frontmatter) is trivial (< 50 words)
#   WARN  no "Provenance" section heading in the body
#   WARN  no "When NOT to use" section heading in the body
#
# Exit codes: 0 = PASS (warnings allowed), 1 = FAIL, 2 = usage error.
#
# Dependencies: bash, python3 (+PyYAML), awk, grep, wc — nothing else.

set -u

if [ $# -ne 1 ]; then
    echo "usage: $0 <path-to-skill-directory>" >&2
    exit 2
fi

DIR="${1%/}"
SKILL="$DIR/SKILL.md"
FAILED=0
WARNED=0

fail() { echo "FAIL: $*"; FAILED=1; }
warn() { echo "WARN: $*"; WARNED=1; }
ok()   { echo "ok:   $*"; }

echo "== lint_skill: $DIR =="

if [ ! -d "$DIR" ]; then
    fail "not a directory: $DIR"
    echo "== RESULT: FAIL =="
    exit 1
fi

# --- Check 1: SKILL.md exists -------------------------------------------
if [ ! -f "$SKILL" ]; then
    fail "SKILL.md not found at $SKILL"
    echo "== RESULT: FAIL =="
    exit 1
fi
ok "SKILL.md exists"

# --- Checks 2-6: frontmatter (python3 + PyYAML does the parsing) --------
# The python helper prints its own ok:/FAIL: lines and exits nonzero on any
# frontmatter-level failure. Directory basename is passed in for the
# name-matches-dir check.
BASENAME="$(basename "$DIR")"
if ! python3 - "$SKILL" "$BASENAME" <<'PY'
import re, sys

path, basename = sys.argv[1], sys.argv[2]
failed = False

def ok(msg):   print(f"ok:   {msg}")
def fail(msg):
    global failed
    print(f"FAIL: {msg}")
    failed = True

text = open(path, encoding="utf-8").read()
m = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
if not m:
    fail("no YAML frontmatter block (file must start with --- ... ---)")
    sys.exit(1)

try:
    import yaml
except ImportError:
    yaml = None
    print("WARN: PyYAML not importable; using built-in fallback parser "
          "(handles name: and plain/'>-' block descriptions only — "
          "install PyYAML for full YAML validation)")

if yaml is not None:
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        fail(f"frontmatter is not valid YAML: {e}")
        sys.exit(1)
else:
    # Fallback: minimal parser for the two-field house frontmatter.
    # Supports `key: value` and `key: >-` / `key: >` folded blocks.
    fm, key, block = {}, None, []
    for line in m.group(1).splitlines():
        top = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if top:
            if key is not None:
                fm[key] = " ".join(block).strip()
            k, v = top.group(1), top.group(2).strip()
            if v in (">-", ">", "|", "|-"):
                key, block = k, []
            else:
                fm[k] = v.strip("'\"")
                key = None
        elif key is not None and (line.startswith("  ") or not line.strip()):
            block.append(line.strip())
        elif line.strip():
            fail(f"fallback parser cannot handle frontmatter line: {line!r}")
            sys.exit(1)
    if key is not None:
        fm[key] = " ".join(block).strip()

if not isinstance(fm, dict):
    fail("frontmatter parsed but is not a mapping (expected name:/description: keys)")
    sys.exit(1)
ok("frontmatter parses as YAML")

name = fm.get("name")
desc = fm.get("description")

if not (isinstance(name, str) and name.strip()):
    fail("frontmatter `name` is missing or empty")
else:
    ok(f"name present: {name.strip()!r}")
    if name.strip() != basename:
        fail(f"name {name.strip()!r} != directory basename {basename!r}")
    else:
        ok("name matches directory basename")

if not (isinstance(desc, str) and desc.strip()):
    fail("frontmatter `description` is missing or empty")
else:
    ok(f"description present ({len(desc.split())} words)")
    # The description is the trigger: it must say WHEN to load the skill.
    trigger_re = re.compile(
        r"use (this|it|when|whenever)|trigger|whenever|when the user"
        r"|when to|when you|load (this|when)|use for",
        re.IGNORECASE,
    )
    if trigger_re.search(desc):
        ok("description contains trigger language (says when to load)")
    else:
        fail("description has no trigger language "
             "(add e.g. 'Use this skill when...' / 'Triggers on: ...')")

sys.exit(1 if failed else 0)
PY
then
    FAILED=1
fi

# --- Check 7: body non-trivial ------------------------------------------
# Words in everything after the closing --- of the frontmatter.
BODY_WORDS="$(awk 'BEGIN{fm=0; body=0}
    NR==1 && /^---[[:space:]]*$/ {fm=1; next}
    fm==1 && /^---[[:space:]]*$/ {body=1; fm=2; next}
    body==1 {print}' "$SKILL" | wc -w)"
if [ "$BODY_WORDS" -lt 50 ]; then
    fail "body is trivial: $BODY_WORDS words after frontmatter (< 50)"
else
    ok "body non-trivial: $BODY_WORDS words after frontmatter"
fi

# --- Warnings: house-style sections --------------------------------------
if grep -qiE '^#{1,6}[[:space:]].*provenance' "$SKILL"; then
    ok "has a Provenance section heading"
else
    warn "no 'Provenance' section heading (house style: end with '## Provenance and maintenance')"
fi

if grep -qiE '^#{1,6}[[:space:]].*when not to use' "$SKILL"; then
    ok "has a 'When NOT to use' section heading"
else
    warn "no 'When NOT to use' section heading (house style: point to sibling skills)"
fi

# --- Verdict --------------------------------------------------------------
if [ "$FAILED" -ne 0 ]; then
    echo "== RESULT: FAIL =="
    exit 1
elif [ "$WARNED" -ne 0 ]; then
    echo "== RESULT: PASS (with warnings) =="
    exit 0
else
    echo "== RESULT: PASS =="
    exit 0
fi
