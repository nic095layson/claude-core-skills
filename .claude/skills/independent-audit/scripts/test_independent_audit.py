#!/usr/bin/env python3
"""Tests for the independent-audit scripts (claim_receipts, replay_gate, preflight). Stdlib only.

The claim cases are verbatim false claims recovered from a real project's history (2026-10-15..21,
each later shown false), plus their honest rewrites. Run:
    python3 .claude/skills/independent-audit/scripts/test_independent_audit.py
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

FALSE_CLAIMS = [
    "the weekly in-season pull keeps it green.",
    "Today it changes nothing either way, because all four recovery players are on IL.",
    "Retire the age flag; live verification supersedes it.",
    "Still only yours: attach the FantasyBot connector.",
    "the kit is this session's own repository.",
]
HONEST = [
    "the weekly pull keeps it green: `check_provenance.py --max-age-days 14` PASS on 2026-10-21 (run-ledger row 41).",
    "It changes nothing today: re-ran `league_sim.py --seeds 2` and title share moved 0.0 of 21.1.",
    "Live verification supersedes it — NOT-ATTEMPTED: no in-season verifier exists yet, so this stays a proposal.",
    "Still yours: attach the connector (checked `ListConnectors` at 14:02, it is absent).",
    "The kit is this session's repository: `git rev-parse --show-toplevel` returned /home/user/kit.",
]
PLAIN = [
    "The owner asked for a post-mortem of the draft.",
    "Victor Wembanyama leads the board in blocks.",
    "## 3. What waits on you",
]


class ClaimReceipts(unittest.TestCase):
    def setUp(self):
        import claim_receipts
        self.cr = claim_receipts

    def test_false_claims_flagged(self):
        for s in FALSE_CLAIMS:
            with self.subTest(s=s):
                self.assertTrue(self.cr.scan_text(s), f"not flagged: {s}")

    def test_honest_rewrites_pass(self):
        for s in HONEST:
            with self.subTest(s=s):
                self.assertEqual(self.cr.scan_text(s), [], f"flagged: {s}")

    def test_plain_sentences_pass(self):
        for s in PLAIN:
            with self.subTest(s=s):
                self.assertEqual(self.cr.scan_text(s), [])

    def test_code_fences_and_quotes_ignored(self):
        txt = "```\nthe pull keeps it green\n```\n> it changes nothing either way\n"
        self.assertEqual(self.cr.scan_text(txt), [])

    def test_quoted_and_struck_claims_are_reported_not_asserted(self):
        # red-team RT-2 (2026-10-21): corrections quote the old false claim; quoting it is not asserting it
        txt = ('On 10/21 I wrote that it "changes nothing either way"; it moved the share 2.2 points.\n\n'
               '- ~~Retire the age flag; live verification supersedes it.~~ WITHDRAWN\n\n'
               '| 6 | "Still only yours: attach the connector" | it was attached |\n')
        self.assertEqual(self.cr.scan_text(txt), [])

    def test_receipt_must_be_beside_the_claim(self):
        far = "The job runs every morning. " + ("Filler about layout and colours. " * 12) + "`ran x` PASS."
        self.assertTrue(self.cr.scan_text(far), "a receipt far from the claim excused it")

    def test_a_neighbouring_list_item_does_not_lend_its_receipt(self):
        # red-team RT-1 (2026-10-21): in a list with no blank lines, item 3's path excused items 4 and 5
        txt = ("1. `python3 build.py` prints BUILD: PASS.\n"
               "2. Three recorded inputs live in data/records/.\n"
               "3. The weekly sync keeps the records current.\n"
               "4. Raising the threshold changes nothing.\n")
        lines = sorted(f[0] for f in self.cr.scan_text(txt))
        self.assertEqual(lines, [3, 4])

    def test_cli_strict_exit_and_line(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "r.md")
            open(p, "w").write("Intro.\n\n" + FALSE_CLAIMS[0] + "\n")
            r = subprocess.run([sys.executable, os.path.join(HERE, "claim_receipts.py"), "--strict", p],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 1)
            self.assertIn("CLAIM RECEIPTS: FAIL", r.stdout)
            self.assertIn(":3:", r.stdout)  # file:line of the claim
            r = subprocess.run([sys.executable, os.path.join(HERE, "claim_receipts.py"), p],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, "advisory mode must not fail the build")
            self.assertIn("CLAIM RECEIPTS: ADVISORY", r.stdout)


class ReplayGate(unittest.TestCase):
    def test_fails_on_any_broken_input_and_names_it(self):
        with tempfile.TemporaryDirectory() as d:
            for name, body in (("a.txt", "ok"), ("b.txt", "boom"), ("c.txt", "ok")):
                open(os.path.join(d, name), "w").write(body)
            step = f"{sys.executable} -c \"import sys;t=open(sys.argv[1]).read();print('STEP: PASS' if t=='ok' else 'crash');sys.exit(t!='ok')\" {{input}}"
            r = subprocess.run([sys.executable, os.path.join(HERE, "replay_gate.py"), "--cmd", step,
                                "--inputs", os.path.join(d, "*.txt"), "--pass-re", "^STEP: PASS"],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 1, r.stdout)
            self.assertIn("REPLAY: FAIL", r.stdout)
            self.assertIn("b.txt", r.stdout)

    def test_exit_zero_without_pass_line_is_a_fail(self):
        with tempfile.TemporaryDirectory() as d:
            open(os.path.join(d, "a.txt"), "w").write("x")
            r = subprocess.run([sys.executable, os.path.join(HERE, "replay_gate.py"), "--cmd", "true {input}",
                                "--inputs", os.path.join(d, "*.txt"), "--pass-re", "^STEP: PASS"],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 1)

    def test_no_inputs_is_a_fail_not_a_pass(self):
        r = subprocess.run([sys.executable, os.path.join(HERE, "replay_gate.py"), "--cmd", "true {input}",
                            "--inputs", "/nonexistent/*.json", "--pass-re", "x"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn("no recorded inputs", r.stdout)

    def test_last_n_replays_the_most_recent_inputs_only(self):
        with tempfile.TemporaryDirectory() as d:
            for n, body in (("r_2026-10-01", "boom"), ("r_2026-10-20", "ok"), ("r_2026-10-21", "ok")):
                open(os.path.join(d, n + ".txt"), "w").write(body)
            step = f"{sys.executable} -c \"import sys;t=open(sys.argv[1]).read();print('STEP: PASS' if t=='ok' else 'crash');sys.exit(t!='ok')\" {{input}}"
            r = subprocess.run([sys.executable, os.path.join(HERE, "replay_gate.py"), "--cmd", step, "--last", "2",
                                "--inputs", os.path.join(d, "*.txt"), "--pass-re", "^STEP: PASS"],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertIn("REPLAY: PASS — 2 of 2", r.stdout)

    def test_all_pass(self):
        with tempfile.TemporaryDirectory() as d:
            for n in ("a", "b"):
                open(os.path.join(d, n + ".txt"), "w").write("ok")
            r = subprocess.run([sys.executable, os.path.join(HERE, "replay_gate.py"), "--cmd",
                                "echo STEP: PASS {input}", "--inputs", os.path.join(d, "*.txt"), "--pass-re", "^STEP: PASS"],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertIn("REPLAY: PASS — 2 of 2", r.stdout)


class Preflight(unittest.TestCase):
    def spec(self, d, checks):
        p = os.path.join(d, "preflight.json")
        json.dump({"name": "test run", "checks": checks}, open(p, "w"))
        return p

    def test_no_checkout_fails_loudly(self):
        with tempfile.TemporaryDirectory() as d:
            p = self.spec(d, [{"name": "repo checkout", "cmd": "git rev-parse --is-inside-work-tree"}])
            r = subprocess.run([sys.executable, os.path.join(HERE, "preflight.py"), "--spec", p], cwd=d,
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 1)
            self.assertRegex(r.stdout, r"PREFLIGHT: FAIL — test run: 'repo checkout'")

    def test_all_checks_pass(self):
        with tempfile.TemporaryDirectory() as d:
            p = self.spec(d, [{"name": "python", "cmd": f"{sys.executable} --version"},
                              {"name": "env", "env": ["PATH"]},
                              {"name": "writable", "writable": d}])
            r = subprocess.run([sys.executable, os.path.join(HERE, "preflight.py"), "--spec", p], cwd=d,
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertIn("PREFLIGHT: PASS — test run: 3 checks", r.stdout)

    def test_missing_env_and_unwritable(self):
        with tempfile.TemporaryDirectory() as d:
            p = self.spec(d, [{"name": "token", "env": ["SURELY_NOT_SET_9F3A"]}])
            r = subprocess.run([sys.executable, os.path.join(HERE, "preflight.py"), "--spec", p], cwd=d,
                               capture_output=True, text=True, env={k: v for k, v in os.environ.items() if k != "SURELY_NOT_SET_9F3A"})
            self.assertEqual(r.returncode, 1)
            self.assertIn("SURELY_NOT_SET_9F3A", r.stdout)

    def test_bad_spec_fails_not_passes(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "x.json"); open(p, "w").write("{not json")
            r = subprocess.run([sys.executable, os.path.join(HERE, "preflight.py"), "--spec", p],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 1)
            self.assertIn("PREFLIGHT: FAIL", r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=1)
