# Red team — this project's standing attack on its own model

Scaffolded by the `red-team` skill's `redteam_init.py`. Three checks, run as gates before any report that
quotes a headline figure:

```
python3 <skill>/scripts/registry_check.py --root . --json redteam/records/constants.json
python3 <skill>/scripts/attacks_check.py  --root . --out  redteam/records/attacks.json
python3 <skill>/scripts/bands_check.py    --report <your report> --sweep <your sweep record>
```

`<skill>` is the red-team skill directory (`.claude/skills/red-team` in a project that carries it, or
`~/.claude/skills/red-team`). The scaffold passes all three as shipped: `redteam_init.py` ran the registry
check once and wrote `redteam/records/constants.json`, the one example attack is UNFINGERPRINTED
(allowed), and `report.example.md` quotes the example band.

## The five calibration statuses (every registered constant carries one)

| status | meaning | must carry |
|---|---|---|
| `settings` | read from a governing settings page or contract | `record`: where |
| `structural` | no judgment in it: a hash, a reporting band, a format fact | nothing |
| `measured` | fit to a committed record | `record`: the fit |
| `declared_band` | hand-set; its sweep band is published and every report quotes it when FRAGILE | `record` and `band` |
| `uncalibrated` | hand-set, no band yet | `decision`: the id where it will be decided |

## How to make it real

1. `live.py`: make `live_values()` read your engine's constants from the running code (import the module,
   return `{name: value}`). Never type a value from memory.
2. `constants_registry.json`: one entry per judgment constant with its role and status. Delete the examples.
3. A sweep runner: copy `sweep_template.py` from the skill's scripts and implement its contract (reload the
   model per job, patch one constant, assert the baseline within 3 SE of the published reference before any
   tier is read, two seeds, tiers on the unrounded mean, record the fingerprint and the tier rule). Its record
   is what `bands_check.py` reads.
4. `attacks.json`: one row per attack (known-answer re-implementation, consistency between instruments, the
   sweep, decision robustness); set `commit_field` once records carry a fingerprint, so STALE can fail.
5. Fingerprint: inside git, the checks use `git rev-parse --short HEAD`; elsewhere pass `--fingerprint`.

## Proportionality

A question answered from a figure already published: quote the last sweep's band beside it. A new report with
a headline figure: the three checks, minutes. A new model, a changed constant or input set, or a post-mortem:
the full pass (the skill's procedure, steps 1 to 8).
