import subprocess, sys, unittest
class T(unittest.TestCase):
    def test_build_passes(self):
        r = subprocess.run([sys.executable, "scripts/build.py"], capture_output=True, text=True)
        self.assertIn("BUILD: PASS", r.stdout)
