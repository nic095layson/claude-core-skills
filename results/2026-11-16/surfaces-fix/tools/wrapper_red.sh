# Red-first for the wrapper case (SF-6, M8): the auditor's wrapper mutation in a scratch copy of the plugin,
# then the wrapper self-test as it stood at the start and as it is now. Usage: bash wrapper_red.sh TREE WORK
set -u
TREE=$1; W=$2; rm -rf "$W"; mkdir -p "$W"
cp -r "$TREE/plugin/core-governance" "$W/cg"; rm -rf "$W/cg/scripts/__pycache__"
git -C "$TREE" show HEAD:plugin/core-governance/scripts/selftest-wrapper.sh > "$W/cg/scripts/selftest-wrapper-start.sh"
sed -i 's/            if sys.argv\[2\] in str(x.get("command", "")):/            if True:/' "$W/cg/scripts/run-unless-project-wired.sh"
echo "mutated lines in the wrapper copy: $(grep -c 'if True:' "$W/cg/scripts/run-unless-project-wired.sh")"
echo "--- unmutated wrapper, the self-test now:"; bash "$TREE/plugin/core-governance/scripts/selftest-wrapper.sh" | tail -2
echo "--- mutated wrapper, the self-test as it stood at the start:"; bash "$W/cg/scripts/selftest-wrapper-start.sh" | tail -1
echo "--- mutated wrapper, the self-test now:"; bash "$W/cg/scripts/selftest-wrapper.sh" | grep -E 'FAIL|passed'
