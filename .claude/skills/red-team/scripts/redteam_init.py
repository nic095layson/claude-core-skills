#!/usr/bin/env python3
"""Scaffold a project's standing red team: redteam/constants_registry.json, redteam/attacks.json,
redteam/live.py, redteam/README.md, plus an example sweep record and an example report that passes the bands
check, so the three checks can be run on the scaffold before a single real constant is registered.

    python3 redteam_init.py [--root DIR] [--force]

Refuses to overwrite an existing file unless --force. Prints every path it created. The five calibration
statuses are documented in the README it writes, with one example registry entry per status.
"""
import argparse
import contextlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STATUSES = ("settings", "structural", "measured", "declared_band", "uncalibrated")

REGISTRY = {
    "_about": ("Every judgment constant this system runs on, with its live value and its calibration status. "
               "registry_check.py compares each value to the live system (redteam/live.py) and refuses an entry "
               "whose status has no record or decision. Statuses: settings = read from a governing settings page "
               "(cite it); structural = no judgment in it (a hash, a reporting band, a format fact); measured = "
               "fit to a committed record (cite it); declared_band = hand-set, its sweep band published "
               "(carry 'band': the variants the sweep runs one at a time) and quoted by every report when "
               "FRAGILE; uncalibrated = hand-set, no band yet (carry 'decision': the id where that is decided). "
               "No value here is a source: the live system is; this file says what each value is FOR and what "
               "vouches for it. Replace the five examples with your constants."),
    "constants": [
        {"name": "EXAMPLE_TEAMS", "value": 12, "role": "league or cohort size (example: settings)",
         "status": "settings", "record": "settings/league.json teams"},
        {"name": "EXAMPLE_REPORT_BAND", "value": 0.5, "role": "rounding of reported figures (example: structural)",
         "status": "structural", "record": ""},
        {"name": "EXAMPLE_HOME_EDGE", "value": 0.03, "role": "home advantage (example: measured)",
         "status": "measured", "record": "records/home_edge_fit_2026.json"},
        {"name": "EXAMPLE_SHOCK", "value": 0.06, "role": "shared shock on a count (example: declared_band)",
         "status": "declared_band", "record": "redteam/records/sweep.example.json",
         "band": [{"label": "no shock", "value": 0.0}, {"label": "shock doubled", "value": 0.12}]},
        {"name": "EXAMPLE_INJURY_DISCOUNT", "value": 0.75,
         "role": "availability discount for a risk tier (example: uncalibrated)",
         "status": "uncalibrated", "record": "", "decision": "D-1 (calibrate after the first month of data)"},
    ],
}

LIVE_PY = '''"""Live values of the judgment constants, read from the running system, never typed from memory.

registry_check.py imports this file and calls live_values(). Replace the example body with code that reads
your engine's module-level constants (import the module and return {name: value}); keep the example until
your first real constant is registered so the scaffold's checks keep passing.
"""


def live_values():
    return {
        "EXAMPLE_TEAMS": 12,
        "EXAMPLE_REPORT_BAND": 0.5,
        "EXAMPLE_HOME_EDGE": 0.03,
        "EXAMPLE_SHOCK": 0.06,
        "EXAMPLE_INJURY_DISCOUNT": 0.75,
    }
'''

ATTACKS = {
    "_about": ("The standing attack list: every red-team check this system has faced, numbered, with the script "
               "that runs it, the record it writes, and the question it tries to break. attacks_check.py refuses "
               "a missing record or script and a record made on a different engine fingerprint than the live one "
               "(STALE). A new attack is a new row; a row is never deleted, only marked retired with a date. "
               "commit_field is the dotted path to the fingerprint inside the record; null means the record is "
               "UNFINGERPRINTED (allowed, counted) — set it to 'fingerprint' once the registry record carries one."),
    "attacks": [
        {"id": "A-1", "name": "constants registry vs live values",
         "question": "Does every judgment constant still equal its registered value, carry a calibration status, "
                     "and name what vouches for it?",
         "script": "redteam/live.py", "record": "redteam/records/constants.json", "commit_field": None,
         "added": "<today>"},
    ],
}

SWEEP_EXAMPLE = {
    "_about": ("An example sweep record in the shape bands_check.py and the report contract read. A real one is "
               "written by the project's sweep runner (see sweep_template.py in the red-team skill's scripts)."),
    "fingerprint": "example",
    "seeds": [1, 2],
    "tier_rule": "mean shift over seeds: ROBUST < 1, SENSITIVE 1-2, FRAGILE >= 2 headline points",
    "constants": {
        "EXAMPLE_SHOCK": {"tier": "FRAGILE", "max_abs_shift": 3.37, "variants": [
            {"label": "no shock", "shift_mean": 3.37, "shift_mean_1dp": "+3.4", "tier": "FRAGILE"},
            {"label": "shock doubled", "shift_mean": -2.33, "shift_mean_1dp": "-2.3", "tier": "FRAGILE"}]},
    },
    "fragile": ["EXAMPLE_SHOCK"],
    "sensitive": [],
}

REPORT_EXAMPLE = """# Example report (passes bands_check.py against redteam/records/sweep.example.json)

Headline: 21.4 ± 0.5 (sampling error, 6,000 samples x 2 seeds).

EXAMPLE_SHOCK is FRAGILE: +3.4 (no shock) / -2.3 (shock doubled); the headline 21.4 ± 0.5 sits inside that
band. Two error bars: the sampling error says how many times we ran it; the structural band says how much a
hand-set constant could move it. Uncalibrated: EXAMPLE_INJURY_DISCOUNT (decision D-1).
"""

README = """# Red team — this project's standing attack on its own model

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
"""


def scaffold(root, force=False, today=None):
    root = os.path.abspath(root)
    rt = os.path.join(root, "redteam")
    attacks = json.loads(json.dumps(ATTACKS))
    attacks["attacks"][0]["added"] = today or _today()
    files = {
        "redteam/constants_registry.json": json.dumps(REGISTRY, indent=1, ensure_ascii=False) + "\n",
        "redteam/live.py": LIVE_PY,
        "redteam/attacks.json": json.dumps(attacks, indent=1, ensure_ascii=False) + "\n",
        "redteam/records/sweep.example.json": json.dumps(SWEEP_EXAMPLE, indent=1, ensure_ascii=False) + "\n",
        "redteam/report.example.md": REPORT_EXAMPLE,
        "redteam/README.md": README,
    }
    existing = [rel for rel in files if os.path.exists(os.path.join(root, rel))]
    if existing and not force:
        raise FileExistsError("refusing to overwrite: " + ", ".join(existing) + " (use --force)")
    os.makedirs(os.path.join(rt, "records"), exist_ok=True)
    created = []
    for rel, text in files.items():
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        created.append(rel)
    # Run the registry check once so the example attack's record exists and all three checks pass on the
    # scaffold with no further step (a refuter found the attacks check failing MISSING until it was run).
    sys.path.insert(0, HERE)
    import registry_check  # noqa: E402
    with contextlib.redirect_stdout(io.StringIO()):
        code = registry_check.main(["--root", root, "--json", "redteam/records/constants.json"])
    if code == 0:
        created.append("redteam/records/constants.json")
    return created


def _today():
    import datetime
    return datetime.date.today().isoformat()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=os.getcwd())
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args(argv)
    try:
        created = scaffold(a.root, a.force)
    except FileExistsError as e:
        print(f"REDTEAM INIT: FAIL — {e}")
        return 1
    print(f"REDTEAM INIT: PASS — {len(created)} files under {os.path.abspath(a.root)}/redteam/")
    for rel in created:
        print("  " + rel)
    print("next: registry_check.py --root . --json redteam/records/constants.json; attacks_check.py --root . "
          "--out redteam/records/attacks.json; bands_check.py --report redteam/report.example.md "
          "--sweep redteam/records/sweep.example.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
