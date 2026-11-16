# Run section 9 of a guard text (the plugin twin) on a scratch copy of the tree, under one mutation.
# Usage: bash guard_section9.sh GUARD_TEXT_FILE TREE_COPY MUTATION   (M0 none, M2 one byte added to the plugin's
# selftest-reminders.sh, M2b the plugin's selftest-reminders.sh removed, M2c the plugin's receiptlaw.py removed)
set -u
G=$1; C=$2; M=$3
case "$M" in
  M2)  printf '#\n' >> "$C/plugin/core-governance/scripts/selftest-reminders.sh" ;;
  M2b) rm -f "$C/plugin/core-governance/scripts/selftest-reminders.sh" ;;
  M2c) rm -f "$C/plugin/core-governance/scripts/receiptlaw.py" ;;
esac
sec=$(awk '/^# --- 9\. Plugin twin/{f=1} /^if command -v claude/{f=0} f' "$G")
cd "$C" && FAIL=0 && ok() { printf "  ok    %s\n" "$*"; } && bad() { printf "  FAIL  %s\n" "$*"; FAIL=1; } && eval "$sec"
echo "  section 9: $([ $FAIL -eq 0 ] && echo PASS || echo FAIL)"
