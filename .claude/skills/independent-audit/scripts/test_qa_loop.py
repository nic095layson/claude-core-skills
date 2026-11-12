#!/usr/bin/env python3
"""Tests for the outcome loop's three scripts (2026-11-12): corrections_rate.py, stale_rules.py, weekly_review.sh.
Written before the scripts; pre-registered in experiments/hypothesis-2026-11-12-qa-loop.md."""
import json, os, subprocess, sys, tempfile, textwrap, unittest, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))


def run(*args, cwd=None):
    return subprocess.run(list(args), capture_output=True, text=True, cwd=cwd)


LOG = textwrap.dedent("""\
    # Corrections log

    | Date | What was said | What the records showed | How it was caught | The check that prevents it |
    |---|---|---|---|---|
    | 2026-11-11 | A | B | `git log -S` on the two scripts, then a replay | c |
    | 2026-11-11 | A | B | Reading the league move ledger | c |
    | 2026-11-11 | A | B | The owner's screenshot | c |
    | 2026-11-12 | A | B | The box-score split, run at the owner's request | c |
    | 2026-11-12 | A | B | Re-running attack A-10 | c |
    | 2026-11-20 | A | B | The session's own run | c |
    | not-a-date | A | B | whatever | c |
    """)


class CorrectionsRate(unittest.TestCase):
    S = os.path.join(HERE, "corrections_rate.py")

    def log(self, text):
        fd, p = tempfile.mkstemp(suffix=".md")
        os.write(fd, text.encode()); os.close(fd)
        self.addCleanup(os.unlink, p)
        return p

    def test_counts_by_iso_week_and_who_caught(self):
        r = run("python3", self.S, self.log(LOG), "--json")
        self.assertEqual(r.returncode, 0, r.stderr)
        j = json.loads(r.stdout)
        self.assertEqual(j["rows"], 6)
        self.assertEqual(j["unparsed"], 1)                       # the malformed row is counted, never dropped
        self.assertEqual(j["weeks"]["2026-W46"], {"total": 5, "owner_caught": 2, "session_caught": 3})
        self.assertEqual(j["weeks"]["2026-W47"], {"total": 1, "owner_caught": 0, "session_caught": 1})

    def test_missing_or_empty_log_is_zero_not_an_error(self):
        for p in ("/nonexistent/corrections-log.md", self.log("# Corrections log\n")):
            r = run("python3", self.S, p, "--json")
            self.assertEqual(r.returncode, 0)
            self.assertEqual(json.loads(r.stdout)["rows"], 0)

    def test_text_line_names_the_rate(self):
        r = run("python3", self.S, self.log(LOG))
        self.assertRegex(r.stdout, r"CORRECTIONS: 6 rows, 1 unparsed .*2026-W46: 5 \(owner caught 2\)")

    def test_a_pipe_inside_a_cell_does_not_shift_who_caught_it(self):
        # refutation pass 2026-11-12: `a | b` in the second cell moved "The owner saw it" out of column 4
        p = self.log("| Date | a | b | c | d |\n|---|---|---|---|---|\n| 2026-11-12 | used `a | b` here | x | The owner saw it | y |\n")
        j = json.loads(run("python3", self.S, p, "--json").stdout)
        self.assertEqual(j["weeks"]["2026-W46"]["owner_caught"], 1)

    def test_template_parses_as_empty(self):
        r = run("python3", self.S, os.path.join(HERE, "..", "corrections-log.template.md"), "--json")
        self.assertEqual(json.loads(r.stdout)["rows"], 0)


class StaleRules(unittest.TestCase):
    S = os.path.join(HERE, "stale_rules.py")

    def tree(self, body):
        d = tempfile.mkdtemp(); os.makedirs(os.path.join(d, ".claude", "skills", "x"))
        open(os.path.join(d, ".claude", "skills", "x", "SKILL.md"), "w").write(body)
        return d

    def test_old_marker_listed_fresh_marker_not(self):
        today = datetime.date(2026, 11, 12)
        d = self.tree("- Authored 2026-08-03; UNMEASURED — candidate.\n- Reworded %s and is **UNMEASURED**.\n- Measured 2026-07-11, 4/4.\n" % today)
        r = run("python3", self.S, "--root", d, "--today", str(today), "--json")
        self.assertEqual(r.returncode, 0, r.stderr)
        j = json.loads(r.stdout)
        self.assertEqual([(x["date"], x["age_days"]) for x in j["stale"]], [("2026-08-03", 101)])
        self.assertEqual(j["fresh"], 1)

    def test_undated_marker_is_reported_as_undated(self):
        d = self.tree("This wording is UNMEASURED.\n")
        j = json.loads(run("python3", self.S, "--root", d, "--today", "2026-11-12", "--json").stdout)
        self.assertEqual(j["undated"], 1)

    def test_runs_on_this_repository(self):
        r = run("python3", self.S, "--root", REPO, "--today", "2026-11-12")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertRegex(r.stdout, r"STALE RULES: \d+ older than 60 days")


class WeeklyReview(unittest.TestCase):
    def test_a_missing_project_directory_is_named_not_blank(self):
        r = run("bash", os.path.join(HERE, "weekly_review.sh"), REPO, "/nonexistent/project", cwd=REPO)
        self.assertEqual(r.returncode, 0)
        self.assertIn("/nonexistent/project: project directory not found", r.stdout)
        self.assertNotIn("No such file", r.stdout + r.stderr)

    def test_prints_three_sections_and_changes_nothing(self):
        before = run("git", "status", "--porcelain", cwd=REPO).stdout
        r = run("bash", os.path.join(HERE, "weekly_review.sh"), REPO, cwd=REPO)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        for head in ("== 1. Corrections", "== 2. Hook registry", "== 3. Stale rules"):
            self.assertIn(head, r.stdout)
        self.assertEqual(before, run("git", "status", "--porcelain", cwd=REPO).stdout)


if __name__ == "__main__":
    unittest.main(verbosity=1)
