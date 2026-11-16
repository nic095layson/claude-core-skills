"""Live values of the governance stack's judgment constants, read from the hook files on disk.

Regexes are registered by the first 8 hex of the sha256 of their pattern source, so any edit to a pattern
reads as value drift. Standing copy since 2026-11-12 (the 2026-10-19 one-off under results/ went stale within
a day: the hooks changed and nothing re-ran it); the guard runs registry_check.py against this file.

The three files of the turn gates (TURN_GATE_FILES) are read whole since 2026-11-15: every upper-case
module-level name of each is a live value, found by parsing the file, so a value that is added there, or
changed, fails the check until it is registered. Nothing in them is picked by hand here. Their entries are
named `<file>:<NAME>`; a compiled pattern is the hash of its source AND its flags. Limit: a hand-set value
written inside a function, or under a lower-case name, is not seen.

The receipt gate's module (RECEIPT_GATE_FILES: receiptlaw.py) is read the same way since 2026-11-15, when the
rule moved out of the shell script into it. Its entries replace the three values that used to be cut out of the
script's text (the two patterns and the window).
"""
import ast
import hashlib
import importlib.util
import json
import os
import re
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HOOKS = os.path.join(REPO, "hooks")
TURN_GATE_FILES = ("turngate.py", "turn-gates-pretool.py", "governance-enforce.py")
RECEIPT_GATE_FILES = ("receiptlaw.py",)     # read whole, like the three above
TURN_GATE_HOOK = "turn-gates-pretool"       # the wiring group whose matcher is registered
PATTERN_TYPE = type(re.compile(""))


def _h(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:8]


def _plain(value):
    """A value as the registry holds it: a pattern as the hash of its source and flags, a tuple or a set as a
    list, anything else that JSON cannot hold as its repr."""
    if isinstance(value, PATTERN_TYPE):
        return _h("%s\x00flags=%d" % (value.pattern, int(value.flags)))
    if isinstance(value, dict):
        return {str(k): _plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(v) for v in value]
    if isinstance(value, (set, frozenset)):
        return sorted(_plain(v) for v in value)
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return repr(value)


def _assigned_names(nodes):
    """Every name assigned at module level, in order: also inside an if, a try, a with or a loop there, never
    inside a function or a class."""
    for node in nodes:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        targets = []
        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, (ast.AnnAssign, ast.AugAssign)):
            targets = [node.target]
        for target in targets:
            for leaf in ast.walk(target):
                if isinstance(leaf, ast.Name):
                    yield leaf.id
        for field in ("body", "orelse", "finalbody", "handlers"):
            yield from _assigned_names(getattr(node, field, None) or [])


def module_constants(filename):
    """{"<file>:<NAME>": value} for every upper-case module-level name of one hook file. The names come from
    the file's syntax tree; the values from the module as Python builds it (its `__main__` part does not run)."""
    path = os.path.join(HOOKS, filename)
    with open(path, encoding="utf-8") as fh:
        names = [n for n in _assigned_names(ast.parse(fh.read()).body) if n.isupper()]
    spec = importlib.util.spec_from_file_location("registry_" + re.sub(r"\W", "_", filename), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return {f"{filename}:{n}": _plain(getattr(module, n)) for n in dict.fromkeys(names)}


def _turn_gate_matchers(path):
    """The matcher of every PreToolUse group of a wiring file that runs the pre-tool hook of the turn gates."""
    with open(path, encoding="utf-8") as fh:
        groups = json.load(fh)["hooks"].get("PreToolUse", [])
    return [g.get("matcher") for g in groups if any(TURN_GATE_HOOK in str(h.get("command")) for h in g.get("hooks", []))]


def live_values():
    sys.dont_write_bytecode = True      # hooks/ is copied byte for byte: reading it leaves no cache file in it
    sys.path.insert(0, HOOKS)
    import govclass  # noqa: E402
    out = {f"CLASS_PATTERN_{k.upper()}": _h(v.pattern) for k, v in govclass.PATTERNS.items()}
    out["ENFORCED_CLASSES"] = list(govclass.ENFORCED)
    out["HARNESS_MARKERS"] = list(govclass.HARNESS_MARKERS)
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
    # --- added 2026-11-12: every hand-set value the hooks gained after 2026-10-19 ---
    out["CUE_MIN_WORDS"] = govclass.CUE_MIN_WORDS
    out["CUE_ACK_PATTERN"] = _h(govclass.ACK_RX.pattern)
    # --- 2026-11-15: the turn gates, read whole (see the module text) ---
    for filename in TURN_GATE_FILES + RECEIPT_GATE_FILES:
        out.update(module_constants(filename))
    out["WIRING_TURN_GATES_MATCHER"] = _turn_gate_matchers(os.path.join(REPO, ".claude", "settings.json"))
    out["PLUGIN_TURN_GATES_MATCHER"] = _turn_gate_matchers(os.path.join(REPO, "plugin", "core-governance", "hooks", "hooks.json"))
    trg = open(os.path.join(HOOKS, "governance-trigger.py"), encoding="utf-8").read()
    m = re.search(r'line = re\.compile\(r"(.*?)", re\.M\)', trg)
    out["CARD_REMINDER_LIST_PATTERN"] = _h(m.group(1)) if m else None
    return out


if __name__ == "__main__":
    print(json.dumps(live_values(), indent=1))
