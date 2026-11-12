# Red team: the governance stack's standing registry

Every hand-set value in `hooks/` (patterns, thresholds, tool lists, modes) is listed in
`constants_registry.json` with what it is for and what vouches for it. `live.py` reads the values from
the hook files on disk. The guard runs:

```
python3 .claude/skills/red-team/scripts/registry_check.py --root .
```

It fails when a live value differs from the registry or a new one is unregistered. When it fails after a
deliberate hook change: re-register the value with its status and the decision that will calibrate it.
Never just overwrite the number to make the check pass.

History: made 2026-10-19 as a one-off under `results/2026-10-19/system-red-team/registry/`; found stale on
2026-11-12 (6 drifted, 15 unregistered) and moved here as a standing gate. `attacks.json` is the
2026-10-19 attack list, kept as written; its records are fingerprinted to that day's hooks and are STALE
by the red-team skill's rule 4 until the attacks are re-run (owner decision D-QA-2).
