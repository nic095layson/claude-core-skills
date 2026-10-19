"""Live values of the governance stack's judgment constants, read from the hook files on disk.

Regexes are registered by the first 8 hex of the sha256 of their pattern source, so any edit to a pattern
reads as value drift. The repo root is three levels above this results folder's registry/ directory.
"""
import hashlib
import json
import os
import re
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))
HOOKS = os.path.join(REPO, "hooks")


def _h(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:8]


def _shell_regex(name):
    src = open(os.path.join(HOOKS, "receipt-law-stop-gate.sh"), encoding="utf-8").read()
    m = re.search(name + r" = re\.compile\(\n(.*?)\n\s*re\.IGNORECASE\)", src, re.S)
    return _h(m.group(1)) if m else None


def live_values():
    sys.path.insert(0, HOOKS)
    import govclass  # noqa: E402
    out = {f"CLASS_PATTERN_{k.upper()}": _h(v.pattern) for k, v in govclass.PATTERNS.items()}
    out["ENFORCED_CLASSES"] = list(govclass.ENFORCED)
    out["HARNESS_MARKERS"] = list(govclass.HARNESS_MARKERS)
    enf = open(os.path.join(HOOKS, "governance-enforce.py"), encoding="utf-8").read()
    out["GOV_GATE_ANY_ONE_GOVERNOR_SUFFICES"] = "if loaded & needed:" in enf
    out["GOV_GATE_LOADED_MATCH_IS_SUBSTRING_OF_INPUT"] = "if g in inp:" in enf
    out["GOV_GATE_RETRIES"] = 1 if "stop_hook_active" in enf else 0
    out["RECEIPT_INABILITY_PATTERN"] = _shell_regex("INABILITY")
    out["RECEIPT_RECEIPT_PATTERN"] = _shell_regex("RECEIPT")
    rem = open(os.path.join(HOOKS, "plan-gate-first-write-reminder.sh"), encoding="utf-8").read()
    out["REMINDER_FIRES_PER_SESSION"] = 1 if "sentinel" in rem else 0
    out["REMINDER_JQ_PATH"] = "/usr/bin/jq" if "/usr/bin/jq" in rem else "PATH"
    band = open(os.path.join(HOOKS, "redteam-band-reminder.sh"), encoding="utf-8").read()
    out["BAND_HOOK_WIRED"] = "redteam-band-reminder" in open(os.path.join(REPO, ".claude", "settings.json")).read()
    out["BAND_HOOK_SOURCE"] = _h(band)
    st = json.load(open(os.path.join(REPO, ".claude", "settings.json")))
    out["HOOK_TIMEOUTS_S"] = sorted({h.get("timeout") for gs in st["hooks"].values() for g in gs for h in g["hooks"]})
    ev = json.load(open(os.path.join(REPO, "evals", "red-team.json")))
    out["TRIGGER_EVAL_GATE_TEXT"] = ev["_grading"]["gate"]
    lint = open(os.path.join(REPO, ".claude", "skills", "diagnostics-and-tooling", "scripts", "lint_skill.sh")).read()
    out["DESCRIPTION_FAIL_CHARS"] = 1024 if "longer than 1024" in lint else None
    out["DESCRIPTION_WARN_CHARS"] = 1000 if "longer than 1000" in lint else None
    return out


if __name__ == "__main__":
    print(json.dumps(live_values(), indent=1))
