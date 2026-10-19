#!/usr/bin/env python3
"""Sweep template: the contract a project's assumption sweep must meet (red-team skill, step 4), shown as a
runnable generic runner with a built-in demo. Generalized 2026-10-19 from the fantasy-basketball kit's
sweep.py (ledger INC-2026-10-19-01). The sweep itself stays project-specific: the project supplies the model
module and its headline function; this file supplies the discipline around them.

The contract (each clause came from a recorded failure):
  1. Reload the model module per job — a patch that leaked between jobs produced seed gaps of 3-4 points
     before the reload was added (kit, 2026-10-19). Here every job imports the module fresh by path.
  2. Patch one constant at a time, everything else held; a patch naming a constant the module lacks is an
     error, never a silent no-op.
  3. Assert the baseline within 3 SE of the published reference on every seed BEFORE any tier is read
     (BaselineError otherwise) — a sweep on a drifted baseline tiers the wrong engine.
  4. Two seeds minimum; shifts are averaged over seeds.
  5. Tiers are read on the unrounded mean shift (0.96 and 1.04 both print as 1.0 and sit in different tiers).
  6. The record carries the engine fingerprint, the tier rule and the registry hash, so a report can say
     which configuration its bands were made on and attacks_check.py can call it STALE.

The project's model module must expose: module-level constants named in the registry, and
    headline(seed: int, seasons: int) -> float        the figure the report will quote
Variants come from the registry: every `declared_band` entry's `band` list, each item {"label", "value"}.
A project whose patches are not simple constants (a function swapped, a literal inside a function) extends
apply_patch() in its own copy; the rest of the contract stands.

    python3 sweep_template.py --model model.py --registry redteam/constants_registry.json --out sweep.json \\
        [--seeds 1 2] [--seasons 6000] [--reference '{"1": 21.4, "2": 21.7}'] [--se 0.54] \\
        [--fingerprint abc1234] [--tiers 1.0 2.0]
    python3 sweep_template.py --demo sweep.json          # the built-in toy model, end to end
"""
import argparse
import hashlib
import importlib.util
import json
import os
import sys
import tempfile
import uuid


class BaselineError(RuntimeError):
    """The baseline did not reproduce the published reference within 3 SE; no tier may be read."""


def tier(shift, thresholds=(1.0, 2.0)):
    """ROBUST below the first threshold, SENSITIVE below the second, FRAGILE at or above it (absolute)."""
    a = abs(float(shift))
    if a < thresholds[0]:
        return "ROBUST"
    if a < thresholds[1]:
        return "SENSITIVE"
    return "FRAGILE"


def assert_baseline(baseline, reference, se):
    """baseline and reference: {seed: value}. Raises BaselineError unless every seed is within 3 SE."""
    bad = []
    for seed, value in baseline.items():
        ref = reference.get(str(seed), reference.get(seed))
        if ref is None:
            continue
        if abs(float(value) - float(ref)) >= 3 * float(se):
            bad.append(f"seed {seed}: baseline {value} vs reference {ref} (3 SE = {3 * float(se):.3f})")
    if bad:
        raise BaselineError("baseline outside 3 SE of the reference: " + "; ".join(bad))
    return True


def load_model(path):
    """A FRESH import of the model module every call (contract clause 1)."""
    name = f"redteam_model_{uuid.uuid4().hex}"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sys.modules.pop(name, None)
    return mod


def apply_patch(mod, patch):
    """Set each {name: value} on the freshly imported module; a missing name is an error (clause 2)."""
    for name, value in patch.items():
        if not hasattr(mod, name):
            raise AttributeError(f"patch names {name}, which the live model does not have")
        setattr(mod, name, value)


def run_job(model_path, patch, seed, seasons):
    mod = load_model(model_path)
    apply_patch(mod, patch)
    return float(mod.headline(seed, seasons))


def variants_from_registry(registry):
    out, labels = [], set()
    for e in registry.get("constants", []):
        if e.get("status") != "declared_band":
            continue
        if not e.get("band"):
            raise ValueError(f"{e.get('name')} is declared_band with no band")
        for b in e["band"]:
            if b["label"] in labels:
                raise ValueError(f"two band variants share the label {b['label']!r}")
            labels.add(b["label"])
            out.append(dict(constant=e["name"], label=b["label"], patch={e["name"]: b["value"]}))
    return out


def summarize(headlines, variants, seeds, thresholds):
    """headlines: {label: {seed: value}} incl. 'baseline'. Tiers per constant on the unrounded mean."""
    seeds = [str(s) for s in seeds]
    base = headlines["baseline"]
    consts = {}
    for v in variants:
        shifts = {s: headlines[v["label"]][s] - base[s] for s in seeds}
        mean = sum(shifts.values()) / len(seeds)
        c = consts.setdefault(v["constant"], {"variants": [], "tier": "ROBUST", "max_abs_shift": 0.0})
        c["variants"].append(dict(label=v["label"], shift={s: round(x, 3) for s, x in shifts.items()},
                                  shift_mean=round(mean, 3), shift_mean_unrounded=mean,
                                  shift_mean_1dp=f"{mean:+.1f}",   # the string a report quotes, verbatim
                                  tier=tier(mean, thresholds)))
        if abs(mean) > c["max_abs_shift"]:
            c["max_abs_shift"], c["tier"] = abs(mean), tier(mean, thresholds)
    return {"constants": consts,
            "fragile": [k for k, c in consts.items() if c["tier"] == "FRAGILE"],
            "sensitive": [k for k, c in consts.items() if c["tier"] == "SENSITIVE"]}


def run_sweep(model_path, registry, out, seeds=(1, 2), seasons=1000, reference=None, se=None,
              fingerprint="", thresholds=(1.0, 2.0)):
    if len(seeds) < 2:
        raise ValueError("two seeds minimum (contract clause 4)")
    variants = variants_from_registry(registry)
    labels = ["baseline"] + [v["label"] for v in variants]
    headlines = {lb: {} for lb in labels}
    for sd in seeds:
        headlines["baseline"][str(sd)] = run_job(model_path, {}, sd, seasons)
    within = None
    if reference is not None:
        if se is None:
            raise ValueError("--se is required with --reference")
        assert_baseline(headlines["baseline"], reference, se)          # clause 3: before any tier
        within = {str(sd): True for sd in seeds}
    for v in variants:
        for sd in seeds:
            headlines[v["label"]][str(sd)] = run_job(model_path, v["patch"], sd, seasons)
    unpatched_rerun = {str(sd): run_job(model_path, {}, sd, seasons) for sd in seeds}   # clause 1, checkable
    rec = dict(seasons=seasons, seeds=list(seeds), fingerprint=fingerprint, model=os.path.basename(model_path),
               registry_sha256=hashlib.sha256(json.dumps(registry, sort_keys=True).encode()).hexdigest()[:12],
               reference=reference, se=se, baseline_within_3se=within,
               tier_rule=(f"mean shift over seeds: ROBUST < {thresholds[0]}, SENSITIVE {thresholds[0]}-"
                          f"{thresholds[1]}, FRAGILE >= {thresholds[1]} headline points"),
               variants={lb: dict(headline=headlines[lb]) for lb in labels},
               unpatched_rerun=unpatched_rerun)
    rec.update(summarize(headlines, variants, seeds, thresholds))
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False)
        f.write("\n")
    return rec


DEMO_MODEL = '''"""Toy model for the sweep template's demo: a headline that moves with one hand-set constant."""
import random

BASE = 21.4
SHOCK = 0.06           # the hand-set constant under attack
SENSITIVITY = -56.0    # headline points per unit of SHOCK (no shock -> +3.36, doubled -> -3.36)


def headline(seed, seasons):
    rng = random.Random(seed)
    return BASE + SENSITIVITY * (SHOCK - 0.06) + rng.gauss(0.0, 0.05)
'''

DEMO_REGISTRY = {"constants": [
    {"name": "SHOCK", "value": 0.06, "role": "shared shock", "status": "declared_band",
     "record": "sweep.json", "band": [{"label": "no shock", "value": 0.0},
                                      {"label": "shock doubled", "value": 0.12}]},
]}


def demo(out, seeds=(1, 2), fingerprint="demo"):
    d = tempfile.mkdtemp()
    model = os.path.join(d, "toy_model.py")
    with open(model, "w", encoding="utf-8") as f:
        f.write(DEMO_MODEL)
    return run_sweep(model, DEMO_REGISTRY, out, seeds=seeds, seasons=1000,
                     reference={str(s): 21.4 for s in seeds}, se=0.5, fingerprint=fingerprint)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model")
    ap.add_argument("--registry")
    ap.add_argument("--out")
    ap.add_argument("--seeds", type=int, nargs="+", default=[1, 2])
    ap.add_argument("--seasons", type=int, default=1000)
    ap.add_argument("--reference", help='JSON {seed: published headline}, e.g. \'{"1": 21.4, "2": 21.7}\'')
    ap.add_argument("--se", type=float, help="the published sampling error, for the 3 SE baseline assertion")
    ap.add_argument("--fingerprint", default="")
    ap.add_argument("--tiers", type=float, nargs=2, default=[1.0, 2.0])
    ap.add_argument("--demo", metavar="OUT", help="run the built-in toy model end to end, write OUT")
    a = ap.parse_args(argv)
    if a.demo:
        rec = demo(a.demo, tuple(a.seeds), a.fingerprint or "demo")
    else:
        if not (a.model and a.registry and a.out):
            ap.error("--model, --registry and --out are required (or --demo OUT)")
        with open(a.registry, encoding="utf-8") as f:
            registry = json.load(f)
        reference = json.loads(a.reference) if a.reference else None
        rec = run_sweep(a.model, registry, a.out, tuple(a.seeds), a.seasons, reference, a.se, a.fingerprint,
                        tuple(a.tiers))
    print(f"SWEEP: {rec['seasons']:,} seasons x seeds {rec['seeds']} on {rec['fingerprint'] or 'no fingerprint'}; "
          f"baseline within 3 SE: {rec['baseline_within_3se']}")
    for name, c in rec["constants"].items():
        for v in c["variants"]:
            print(f"  {v['label']:<40} shift {v['shift_mean']:+.2f}  {v['tier']:<9} [{name}]")
    print("FRAGILE:", rec["fragile"] or "none", "  SENSITIVE:", rec["sensitive"] or "none")
    return 0


if __name__ == "__main__":
    sys.exit(main())
