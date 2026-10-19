#!/usr/bin/env python3
"""Red-first tests for the red-team toolkit (written 2026-10-19 BEFORE the scripts existed; the first run
must fail on import — the PR body quotes that run — and pass after).

The failures these pin are the incident's (kit post-mortem 2026-10-19): a registry value that no longer
matches the live system, a live constant nobody registered, a hand-set constant with neither a band nor a
decision, an attack record made on another engine, and a report that quotes a headline without the FRAGILE
band beside it.

    python3 .claude/skills/red-team/scripts/test_redteam_scripts.py
Dependency-free: unittest and the standard library only.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import attacks_check as A  # noqa: E402
import bands_check as B  # noqa: E402
import redteam_init as I  # noqa: E402
import registry_check as R  # noqa: E402
import sweep_template as S  # noqa: E402


def reg(*entries):
    return {"constants": list(entries)}


GOOD = {"name": "SHOCK", "value": 0.06, "role": "shared shock", "status": "declared_band",
        "record": "records/sweep.json", "band": [{"label": "no shock", "value": 0.0},
                                                 {"label": "shock doubled", "value": 0.12}]}
LIVE = {"SHOCK": 0.06}


class RegistryDrift(unittest.TestCase):
    def test_matching_registry_passes(self):
        ok, problems = R.check(reg(GOOD), LIVE)
        self.assertTrue(ok, problems)

    def test_stale_value_fails(self):
        ok, problems = R.check(reg(dict(GOOD, value=0.05)), LIVE)
        self.assertFalse(ok)
        self.assertTrue(any("SHOCK" in p and "live" in p for p in problems), problems)

    def test_unregistered_live_constant_fails(self):
        ok, problems = R.check(reg(GOOD), dict(LIVE, NEW_KNOB=1.0))
        self.assertFalse(ok)
        self.assertTrue(any("NEW_KNOB" in p and "not registered" in p for p in problems), problems)

    def test_registered_but_gone_fails(self):
        ok, problems = R.check(reg(GOOD, dict(GOOD, name="RETIRED_KNOB")), LIVE)
        self.assertFalse(ok)
        self.assertTrue(any("RETIRED_KNOB" in p for p in problems), problems)

    def test_dict_values_compare_by_content_not_order(self):
        cv = dict(GOOD, name="CV", value={"PTS": 0.30, "REB": 0.35})
        self.assertTrue(R.check(reg(cv), {"CV": {"REB": 0.35, "PTS": 0.30}})[0])
        self.assertFalse(R.check(reg(cv), {"CV": {"REB": 0.35, "PTS": 0.31}})[0])


class RegistryStatus(unittest.TestCase):
    def test_status_outside_the_five_fails(self):
        ok, problems = R.check(reg(dict(GOOD, status="fine")), LIVE)
        self.assertFalse(ok)
        self.assertTrue(any("status" in p for p in problems), problems)

    def test_measured_without_record_fails(self):
        self.assertFalse(R.check(reg(dict(GOOD, status="measured", record="")), LIVE)[0])

    def test_declared_band_without_record_fails(self):
        self.assertFalse(R.check(reg(dict(GOOD, record="")), LIVE)[0])

    def test_settings_without_record_fails(self):
        self.assertFalse(R.check(reg(dict(GOOD, status="settings", record="")), LIVE)[0])

    def test_uncalibrated_without_decision_fails(self):
        bare = dict(GOOD, status="uncalibrated")
        bare.pop("decision", None)
        ok, problems = R.check(reg(bare), LIVE)
        self.assertFalse(ok)
        self.assertTrue(any("decision" in p for p in problems), problems)

    def test_uncalibrated_with_decision_passes(self):
        self.assertTrue(R.check(reg(dict(GOOD, status="uncalibrated", decision="D-1")), LIVE)[0])

    def test_structural_needs_no_record(self):
        self.assertTrue(R.check(reg(dict(GOOD, status="structural", record="")), LIVE)[0])

    def test_declared_band_without_band_fails(self):
        nb = dict(GOOD)
        nb.pop("band")
        ok, problems = R.check(reg(nb), LIVE)
        self.assertFalse(ok)
        self.assertTrue(any("band" in p for p in problems), problems)

    def test_missing_role_fails(self):
        self.assertFalse(R.check(reg(dict(GOOD, role="")), LIVE)[0])


class RegistryLive(unittest.TestCase):
    def test_live_from_json_file_and_from_module(self):
        d = tempfile.mkdtemp()
        jp = os.path.join(d, "live.json")
        json.dump({"SHOCK": 0.06}, open(jp, "w"))
        self.assertEqual(R.load_live(jp, d), {"SHOCK": 0.06})
        mp = os.path.join(d, "live.py")
        open(mp, "w").write("def live_values():\n    return {'SHOCK': 0.06}\n")
        self.assertEqual(R.load_live(mp, d), {"SHOCK": 0.06})
        self.assertEqual(R.load_live('{"SHOCK": 0.06}', d), {"SHOCK": 0.06})

    def test_fingerprint_prefers_explicit_then_git_then_empty(self):
        d = tempfile.mkdtemp()
        self.assertEqual(R.fingerprint(d, "abc1234"), "abc1234")
        self.assertEqual(R.fingerprint(d), "")


class Attacks(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.d, "s"))
        open(os.path.join(self.d, "s", "attack.py"), "w").write("print('x')\n")
        json.dump({"fingerprint": "abc1234", "nested": {"fingerprint": "abc1234"}},
                  open(os.path.join(self.d, "rec.json"), "w"))

    def attacks(self, **over):
        row = {"id": "A-1", "name": "n", "question": "q", "script": "s/attack.py", "record": "rec.json",
               "commit_field": "fingerprint", "added": "2026-10-19"}
        row.update(over)
        return {"attacks": [row]}

    def test_current_record_passes(self):
        rec = A.check(self.attacks(), self.d, "abc1234")
        self.assertEqual(rec["verdict"], "PASS", rec)
        self.assertEqual(rec["attacks"][0]["status"], "CURRENT")

    def test_missing_record_fails(self):
        rec = A.check(self.attacks(record="nope.json"), self.d, "abc1234")
        self.assertEqual(rec["verdict"], "FAIL")
        self.assertEqual(rec["attacks"][0]["status"], "MISSING")

    def test_missing_script_fails(self):
        rec = A.check(self.attacks(script="s/gone.py"), self.d, "abc1234")
        self.assertEqual(rec["verdict"], "FAIL")
        self.assertEqual(rec["attacks"][0]["status"], "MISSING")

    def test_record_on_another_engine_is_stale(self):
        rec = A.check(self.attacks(), self.d, "def5678")
        self.assertEqual(rec["verdict"], "FAIL")
        self.assertEqual(rec["attacks"][0]["status"], "STALE")
        self.assertIn("abc1234", rec["attacks"][0]["why"])

    def test_no_live_fingerprint_cannot_pass_a_fingerprinted_record(self):
        # the edge the kit's prefix comparison misses: "".startswith() is always True
        rec = A.check(self.attacks(), self.d, "")
        self.assertEqual(rec["verdict"], "FAIL")
        self.assertEqual(rec["attacks"][0]["status"], "STALE")

    def test_nested_commit_field_is_read(self):
        rec = A.check(self.attacks(commit_field="nested.fingerprint"), self.d, "abc1234")
        self.assertEqual(rec["attacks"][0]["status"], "CURRENT")

    def test_unfingerprinted_is_allowed_and_counted(self):
        rec = A.check(self.attacks(commit_field=None), self.d, "zzz")
        self.assertEqual(rec["verdict"], "PASS")
        self.assertEqual(rec["attacks"][0]["status"], "UNFINGERPRINTED")
        self.assertEqual(rec["by_status"].get("UNFINGERPRINTED"), 1)

    def test_duplicate_ids_fail(self):
        a = self.attacks()
        a["attacks"].append(dict(a["attacks"][0]))
        rec = A.check(a, self.d, "abc1234")
        self.assertEqual(rec["verdict"], "FAIL")
        self.assertTrue(any("duplicate" in p.lower() for p in rec["problems"]), rec["problems"])

    def test_retired_row_is_kept_and_skipped(self):
        rec = A.check(self.attacks(retired="2026-10-19 superseded by A-2"), self.d, "zzz")
        self.assertEqual(rec["verdict"], "FAIL")  # only row is retired → nothing active
        self.assertEqual(rec["attacks"][0]["status"], "RETIRED")

    def test_out_writes_the_numbered_artifact(self):
        out = os.path.join(self.d, "attacks-out.json")
        code = A.main(["--attacks", self._write(self.attacks()), "--root", self.d, "--fingerprint", "abc1234",
                       "--out", out])
        self.assertEqual(code, 0)
        art = json.load(open(out))
        self.assertEqual([r["id"] for r in art["attacks"]], ["A-1"])

    def _write(self, obj):
        p = os.path.join(self.d, "attacks.json")
        json.dump(obj, open(p, "w"))
        return p


SWEEP = {"fragile": ["SHOCK"], "constants": {"SHOCK": {"tier": "FRAGILE", "variants": [
    {"label": "no shock", "shift_mean": 3.37}, {"label": "shock doubled", "shift_mean": -2.33}]}}}


class BandsRoundingBoundary(unittest.TestCase):
    def test_record_carries_the_quoted_string_so_a_boundary_value_cannot_split_writer_and_checker(self):
        # -2.35 formats as -2.4 in Python but a writer rounding by eye quotes -2.3; the record's
        # shift_mean_1dp is the one string both sides read
        sweep = {"fragile": ["SHOCK"], "constants": {"SHOCK": {"tier": "FRAGILE", "variants": [
            {"label": "shock doubled", "shift_mean": -2.35, "shift_mean_1dp": "-2.3"}]}}}
        self.assertTrue(B.check_text("SHOCK is FRAGILE: -2.3", sweep)[0])
        self.assertFalse(B.check_text("SHOCK is FRAGILE: -2.4", sweep)[0])


class Bands(unittest.TestCase):
    def test_report_quoting_the_band_passes(self):
        text = "Title share 21.4 ± 0.5 (MC). SHOCK is FRAGILE: +3.4 (no shock) / -2.3 (shock doubled)."
        ok, problems = B.check_text(text, SWEEP)
        self.assertTrue(ok, problems)

    def test_unicode_minus_is_accepted(self):
        text = "SHOCK is FRAGILE: +3.4 / −2.3 within the band."
        self.assertTrue(B.check_text(text, SWEEP)[0])

    def test_report_missing_the_name_fails(self):
        ok, problems = B.check_text("Title share 21.4 ± 0.5. Nothing else.", SWEEP)
        self.assertFalse(ok)
        self.assertTrue(any("never names" in p for p in problems), problems)

    def test_name_without_fragile_nearby_fails(self):
        text = "SHOCK is a constant. " + ("x" * 500) + " Something is FRAGILE. +3.4 -2.3"
        ok, problems = B.check_text(text, SWEEP)
        self.assertFalse(ok)
        self.assertTrue(any("400" in p for p in problems), problems)

    def test_missing_variant_figure_fails(self):
        ok, problems = B.check_text("SHOCK is FRAGILE: +3.4 (no shock).", SWEEP)
        self.assertFalse(ok)
        self.assertTrue(any("-2.3" in p for p in problems), problems)

    def test_no_fragile_constants_passes_any_report(self):
        self.assertTrue(B.check_text("anything", {"fragile": [], "constants": {}})[0])

    def test_check_reads_files(self):
        d = tempfile.mkdtemp()
        rp, sp = os.path.join(d, "r.md"), os.path.join(d, "s.json")
        open(rp, "w").write("SHOCK is FRAGILE: +3.4 / -2.3")
        json.dump(SWEEP, open(sp, "w"))
        self.assertTrue(B.check(rp, sp)[0])


class Init(unittest.TestCase):
    def test_scaffold_creates_the_files_with_one_example_per_status(self):
        d = tempfile.mkdtemp()
        created = I.scaffold(d)
        for rel in ("redteam/constants_registry.json", "redteam/attacks.json", "redteam/README.md",
                    "redteam/live.py"):
            self.assertTrue(os.path.exists(os.path.join(d, rel)), rel)
            self.assertIn(rel, created)
        regj = json.load(open(os.path.join(d, "redteam", "constants_registry.json")))
        self.assertEqual(sorted(e["status"] for e in regj["constants"]), sorted(R.STATUSES))
        readme = open(os.path.join(d, "redteam", "README.md")).read()
        for s in R.STATUSES:
            self.assertIn(s, readme)

    def test_scaffold_refuses_to_overwrite(self):
        d = tempfile.mkdtemp()
        I.scaffold(d)
        with self.assertRaises(FileExistsError):
            I.scaffold(d)

    def test_scaffold_passes_its_own_three_checks_end_to_end(self):
        d = tempfile.mkdtemp()
        I.scaffold(d)
        py = sys.executable
        env = dict(os.environ, PYTHONPATH=HERE)
        r1 = subprocess.run([py, "-I", os.path.join(HERE, "registry_check.py"), "--root", d, "--json",
                             os.path.join(d, "redteam", "records", "constants.json")],
                            capture_output=True, text=True)
        self.assertEqual(r1.returncode, 0, r1.stdout + r1.stderr)
        self.assertTrue(r1.stdout.startswith("CONSTANTS CHECK: PASS"), r1.stdout)
        r2 = subprocess.run([py, "-I", os.path.join(HERE, "attacks_check.py"), "--root", d, "--out",
                             os.path.join(d, "redteam", "records", "attacks.json")],
                            capture_output=True, text=True, env=env)
        self.assertEqual(r2.returncode, 0, r2.stdout + r2.stderr)
        self.assertTrue(r2.stdout.startswith("ATTACKS CHECK: PASS"), r2.stdout)
        r3 = subprocess.run([py, "-I", os.path.join(HERE, "bands_check.py"), "--report",
                             os.path.join(d, "redteam", "report.example.md"), "--sweep",
                             os.path.join(d, "redteam", "records", "sweep.example.json")],
                            capture_output=True, text=True)
        self.assertEqual(r3.returncode, 0, r3.stdout + r3.stderr)
        self.assertTrue(r3.stdout.startswith("BANDS CHECK: PASS"), r3.stdout)

    def test_scaffold_drift_is_caught_by_the_registry_check(self):
        d = tempfile.mkdtemp()
        I.scaffold(d)
        p = os.path.join(d, "redteam", "constants_registry.json")
        regj = json.load(open(p))
        regj["constants"][0]["value"] = "DRIFTED"
        json.dump(regj, open(p, "w"))
        r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "registry_check.py"), "--root", d],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertTrue(r.stdout.startswith("CONSTANTS CHECK: FAIL"), r.stdout)


class Sweep(unittest.TestCase):
    def test_tiers_follow_the_thresholds(self):
        self.assertEqual(S.tier(0.5, (1.0, 2.0)), "ROBUST")
        self.assertEqual(S.tier(-1.5, (1.0, 2.0)), "SENSITIVE")
        self.assertEqual(S.tier(2.0, (1.0, 2.0)), "FRAGILE")

    def test_tier_is_read_on_the_unrounded_mean(self):
        # 0.96 and 1.04 both print as 1.0; only the unrounded value tells them apart
        self.assertEqual(S.tier(0.96, (1.0, 2.0)), "ROBUST")
        self.assertEqual(S.tier(1.04, (1.0, 2.0)), "SENSITIVE")

    def test_baseline_outside_three_se_of_reference_raises_before_tiers(self):
        with self.assertRaises(S.BaselineError):
            S.assert_baseline({"1": 21.4, "2": 21.7}, {"1": 25.0, "2": 25.0}, se=0.5)
        S.assert_baseline({"1": 21.4, "2": 21.7}, {"1": 21.0, "2": 22.0}, se=0.5)

    def test_demo_sweep_runs_two_seeds_reloads_per_job_and_records_the_contract(self):
        d = tempfile.mkdtemp()
        out = os.path.join(d, "sweep.json")
        rec = S.demo(out, seeds=(1, 2), fingerprint="demo123")
        self.assertEqual(rec["seeds"], [1, 2])
        self.assertEqual(rec["fingerprint"], "demo123")
        self.assertIn("tier_rule", rec)
        self.assertIn("registry_sha256", rec)
        self.assertTrue(rec["baseline_within_3se"])
        self.assertIn("SHOCK", rec["constants"])
        self.assertEqual(rec["constants"]["SHOCK"]["tier"], "FRAGILE")
        # a patch must not leak: the baseline job that ran AFTER a patched job equals the unpatched headline
        self.assertEqual(rec["variants"]["baseline"]["headline"], rec["unpatched_rerun"])
        self.assertTrue(os.path.exists(out))


if __name__ == "__main__":
    unittest.main(verbosity=2)
