#!/usr/bin/env bash
# install-external-skill.sh — install vendored external skills on demand.
#
# Vendored skills live in external-skills/vendored/ (NOT .claude/skills/) so
# they cost zero context until installed. This script copies them into a
# skills directory, or packages one as a .skill zip for claude.ai per
# install-and-surfaces Runbook 2.
#
# Usage:
#   tools/install-external-skill.sh --list
#   tools/install-external-skill.sh [--target DIR] [--force] SKILL...
#   tools/install-external-skill.sh --package SKILL...
#
# Defaults: --target "$HOME/.claude/skills". Packages land in dist/.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENDORED="$REPO_ROOT/external-skills/vendored"
CORE="$REPO_ROOT/.claude/skills"
TARGET="${HOME}/.claude/skills"
MODE="install"
FORCE=0
SKILLS=()

while [ $# -gt 0 ]; do
  case "$1" in
    --list)
      printf '%-34s %s\n' "SKILL" "SOURCE"
      for d in "$VENDORED"/*/; do
        name="$(basename "$d")"
        src="$(sed -n 's/^- \*\*Source:\*\* \([^ ]*\).*/\1/p' "$d/PROVENANCE.md" 2>/dev/null | head -1)"
        printf '%-34s %s\n' "$name" "${src:-unknown}"
      done
      exit 0 ;;
    --target) TARGET="$2"; shift 2 ;;
    --package) MODE="package"; shift ;;
    --force) FORCE=1; shift ;;
    -h|--help) sed -n '2,14p' "$0"; exit 0 ;;
    *) SKILLS+=("$1"); shift ;;
  esac
done

[ ${#SKILLS[@]} -gt 0 ] || { echo "error: no skill named (try --list)" >&2; exit 1; }

for s in "${SKILLS[@]}"; do
  src="$VENDORED/$s"
  [ -f "$src/SKILL.md" ] || { echo "error: no vendored skill '$s' (try --list)" >&2; exit 1; }
  # collision guard: never shadow a core skill
  if [ -d "$CORE/$s" ]; then
    echo "error: '$s' collides with a core skill — refusing" >&2; exit 1
  fi
  if grep -q 'REFERENCE ONLY' "$src/PROVENANCE.md" 2>/dev/null && [ "$FORCE" -ne 1 ]; then
    echo "error: '$s' is marked REFERENCE ONLY (competes with a core skill's territory). Use --force only if you know why." >&2; exit 1
  fi

  if [ "$MODE" = "package" ]; then
    # .skill format per install-and-surfaces Runbook 2: zip root = <name>/SKILL.md
    mkdir -p "$REPO_ROOT/dist"
    tmp="$(mktemp -d)"
    mkdir "$tmp/$s"
    cp "$src/SKILL.md" "$tmp/$s/"
    (cd "$tmp" && zip -q "$s.skill" "$s/SKILL.md")
    mv "$tmp/$s.skill" "$REPO_ROOT/dist/$s.skill"
    rm -rf "$tmp"
    echo "packaged: dist/$s.skill  (upload via claude.ai Settings → Capabilities → Skills)"
    if [ -d "$src/scripts" ] || [ -d "$src/reference" ] || [ -d "$src/references" ]; then
      echo "  note: '$s' ships companion files that do NOT travel in a .skill — script-dependent steps degrade on claude.ai"
    fi
  else
    dst="$TARGET/$s"
    if [ -e "$dst" ] && [ "$FORCE" -ne 1 ]; then
      echo "error: $dst exists (use --force to overwrite)" >&2; exit 1
    fi
    mkdir -p "$TARGET"
    rm -rf "$dst"
    cp -R "$src" "$dst"
    echo "installed: $dst"
  fi
done

if [ "$MODE" = "install" ]; then
  cat <<'REMINDER'

Register-then-verify (install-and-surfaces): files in place is half an
install. Open a FRESH session and confirm the skill appears in the skills
list before relying on it. Installed copies are forks — after re-vendoring,
re-run this script (stale-copy class, debugging-playbook §4).
REMINDER
fi
