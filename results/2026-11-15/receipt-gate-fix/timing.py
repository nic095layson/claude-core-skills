"""Run time of the receipt gate on a large record, and its answer to broken inputs. Run from the tree root:
    python3 <this file> <work dir>
Builds a synthetic record with hooks/selftest_rows.py (the recipe of results/2026-11-15/turn-gates-fix/timing.txt:
3,200 rounds of an owner message, two governor loads, a read-only shell call, a file read, a commit-and-push call,
an answer and a completed stop), then one more owner message and an answer that holds a bare claim."""
import json, os, subprocess, sys, time
sys.dont_write_bytecode = True
sys.path.insert(0, "hooks")
import selftest_rows as R
work = sys.argv[1]
os.makedirs(work, exist_ok=True)
HOOK = os.path.join("hooks", "receipt-law-stop-gate.sh")
PAD = "x" * 9000


def run(payload, env=None):
    began = time.time()
    p = subprocess.run(["bash", HOOK], input=payload if isinstance(payload, (str, bytes)) else json.dumps(payload),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=not isinstance(payload, bytes), env=env)
    out = p.stdout if isinstance(p.stdout, str) else p.stdout.decode("utf-8", "replace")
    verdict = "nothing printed" if not out.strip() else ("block" if '"decision": "block"' in out else "other output")
    return time.time() - began, p.returncode, verdict


rows = []
for n in range(3200):
    rows += R.flat(R.owner("Continue with step %d" % n), R.skill("plan-gate"), R.skill("adversarial-verify"),
                   R.bash("git status", "clean"), R.call("Read", PAD, file_path="/work/acme/lib/a.md"),
                   R.bash("git add -A && git commit -qm x && git push -u origin claude/x", "ok"),
                   R.say("Step %d done: read the file, committed and pushed. %s" % (n, "Details follow. " * 20)), R.stop())
big = R.write(rows + [R.owner("Is the service set up correctly?"), R.say("I couldn't verify the port.")], os.path.join(work, "big.jsonl"))
clean = R.write(rows + [R.owner("Is the service set up correctly?"), R.say("The port is 5432 (postgresql.conf line 64).")],
                os.path.join(work, "big-clean.jsonl"))
size = os.path.getsize(big) / 1e6
print("synthetic record: %.1f MB, %d rows" % (size, len(rows) + 2))
for label, path in (("answer with a bare claim", big), ("answer with no claim", clean)):
    best = min(run({"session_id": "t", "transcript_path": path, "hook_event_name": "Stop", "stop_hook_active": False})
               for _ in range(3))
    print("  Stop, %-26s %.2f s  (%s, exit %d)   best of 3" % (label + ":", best[0], best[2], best[1]))

print("broken inputs (each must end with exit status 0 and print nothing):")
missing = os.path.join(work, "does-not-exist.jsonl")
rnd = os.path.join(work, "random.bin")
with open(rnd, "wb") as fh:
    fh.write(bytes(bytearray((i * 197 + 31) % 256 for i in range(65536))))
line = os.path.join(work, "one-line.jsonl")
with open(line, "wb") as fh:
    fh.write(b"x" * (6 * 1024 * 1024) + b"\n")
cases = [("empty input", ""), ("input that is not JSON", "not json {"), ("input: random bytes", bytes(bytearray(range(256)) * 16)),
         ("input: one line of 6 MB", "x" * (6 * 1024 * 1024)),
         ("record missing", {"transcript_path": missing, "stop_hook_active": False}),
         ("record of random bytes", {"transcript_path": rnd, "stop_hook_active": False}),
         ("record that is one line of 6 MB", {"transcript_path": line, "stop_hook_active": False}),
         ("record path is a directory", {"transcript_path": work, "stop_hook_active": False}),
         ("no record path, answer in the input", {"transcript_path": "", "last_assistant_message": "I couldn't verify the port."})]
bad = 0
for label, payload in cases:
    secs, status, verdict = run(payload)
    ok = status == 0 and verdict == "nothing printed"
    bad += not ok
    print("  %-38s exit %d, %s, %.2f s%s" % (label, status, verdict, secs, "" if ok else "   <-- NOT AS REQUIRED"))
print("broken inputs not as required: %d of %d" % (bad, len(cases)))
