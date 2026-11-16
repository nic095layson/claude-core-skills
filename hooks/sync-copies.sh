#!/usr/bin/env bash
# sync-copies.sh — bring another repository's copy of these hooks to this library's.
#
#   bash hooks/sync-copies.sh <target repository root> [--proposed-settings FILE]
#
# Copies into <target>/hooks/ every file of this hooks/ folder that a project needs, and prints one line per file:
# "added", "updated" or "same". The list is computed, not typed: `python3 hooks/selftest-turn-gates.py --needs`
# (the scripts both wiring files of this library run, what those import or run, and the self-tests of them). No
# cache folder is copied. A file of <target>/hooks/ that is not on the list is left alone and named.
#
# It does NOT change <target>/.claude/settings.json: a repository may wire more than this library does. It prints,
# as a unified diff, what the settings would be with this library's wiring for these hooks (every command that
# runs one of these scripts is replaced by the library's groups; everything else in the file is kept). With
# --proposed-settings FILE it also writes that proposal to FILE, which must lie outside <target>.
#
# Then, inside the target: `python3 hooks/selftest-turn-gates.py W` (the wiring cases) and the rest of the table.
# Standard library only (python3). Exit status 0 when the copy is complete, 1 on any problem.
set -u
here="$(cd "$(dirname "$0")" && pwd)"
target="${1:-}"; shift || true
proposal=""
if [ "${1:-}" = "--proposed-settings" ]; then proposal="${2:-}"; fi
if [ -z "$target" ] || [ ! -d "$target" ]; then
  echo "usage: bash hooks/sync-copies.sh <target repository root> [--proposed-settings FILE]"; exit 1
fi
target="$(cd "$target" && pwd)"
if [ "$target" = "$(cd "$here/.." && pwd)" ]; then echo "the target is this library itself"; exit 1; fi
needs=$(PYTHONDONTWRITEBYTECODE=1 python3 "$here/selftest-turn-gates.py" --needs --hooks "$here")
if [ $? -ne 0 ]; then echo "this library's own hooks are incomplete:"; printf '%s\n' "$needs"; exit 1; fi
NEEDS="$needs" PYTHONDONTWRITEBYTECODE=1 python3 - "$here" "$target" "$proposal" <<'PY'
import difflib, filecmp, json, os, re, shutil, sys
here, target, proposal = sys.argv[1], sys.argv[2], sys.argv[3]
names = [line.split("|")[0].strip() for line in os.environ.get("NEEDS", "").splitlines() if "|" in line]
dst = os.path.join(target, "hooks")
os.makedirs(dst, exist_ok=True)
problems = 0
for n in names:
    src, out = os.path.join(here, n), os.path.join(dst, n)
    if os.path.isfile(out) and filecmp.cmp(src, out, shallow=False):
        print("same     hooks/%s" % n)
        continue
    word = "updated " if os.path.exists(out) else "added   "
    shutil.copy(src, out)                      # contents and mode bits
    print(word + " hooks/%s" % n)
for n in sorted(os.listdir(dst)):
    if n not in names and os.path.isfile(os.path.join(dst, n)):
        print("left     hooks/%s (not on the library's list; not changed)" % n)

# The settings: this library's wiring for these hooks, the rest of the target's file kept.
script = re.compile(r"/hooks/([A-Za-z0-9_.-]+\.(?:py|sh))\b")
library = json.load(open(os.path.join(here, "..", ".claude", "settings.json"), encoding="utf-8"))["hooks"]
ours = set(s for groups in library.values() for g in groups for h in g["hooks"] for s in script.findall(h["command"]))
path = os.path.join(target, ".claude", "settings.json")
try:
    before_text = open(path, encoding="utf-8").read()
    current = json.loads(before_text)
except FileNotFoundError:
    before_text, current = "", {}
except Exception:
    print("the target's .claude/settings.json cannot be read: no proposal")
    sys.exit(1)
hooks = dict(current.get("hooks") or {})
for event, groups in library.items():
    kept = []
    for g in hooks.get(event) or []:
        rest = [h for h in g.get("hooks") or [] if not (set(script.findall(str(h.get("command") or ""))) & ours)]
        if rest:
            kept.append(dict(g, hooks=rest))
    hooks[event] = list(groups) + kept
proposed = dict(current)
proposed.setdefault("$schema", "https://json.schemastore.org/claude-code-settings.json")
proposed["hooks"] = hooks
after_text = json.dumps(proposed, indent=2, ensure_ascii=False) + "\n"
diff = list(difflib.unified_diff(before_text.splitlines(True), after_text.splitlines(True),
                                 "a/.claude/settings.json", "b/.claude/settings.json (proposed)"))
print("--- settings: %s" % ("no change needed" if not diff else "proposed change (not applied):"))
sys.stdout.writelines(diff)
if proposal:
    if os.path.abspath(proposal).startswith(target + os.sep):
        print("--proposed-settings must lie outside the target")
        sys.exit(1)
    open(proposal, "w", encoding="utf-8").write(after_text)
    print("--- proposal written to %s" % proposal)
sys.exit(1 if problems else 0)
PY
