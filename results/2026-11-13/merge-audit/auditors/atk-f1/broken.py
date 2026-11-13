#!/usr/bin/env python3
"""Angle 6: broken or unusual input, missing helper modules, a very large transcript.

Every case is the same ungoverned turn (owner "Continue" -> git commit -> "done"), which lib/hooks blocks (control
X00). What changes is one thing around it. Printed: verdict, exit code, last line of stderr.

Run: python3 <this file> [big]
"""
import json
import os
import shutil
import subprocess
import sys
import time

PACK = "/tmp/claude-0/-home-user/ff01f16c-7b3f-5ea5-8051-7a95ac7cd1d1/scratchpad/merge-audit"
SCRATCH = PACK + "/work/atk-f1"
LIB = PACK + "/lib/hooks"
OLD = PACK + "/account/plugin/core-governance/scripts"
sys.dont_write_bytecode = True
sys.path.insert(0, PACK + "/pack/tools")
import mk  # noqa: E402

FX = SCRATCH + "/fx"
TURN = [mk.owner("Continue"), mk.tool("Bash", command="git add -A && git commit -qm x"), mk.say("done")]
EARLIER = [mk.owner("What does this repo do?"), mk.say("It is a governance library.")]


def dump(rows):
    return "".join(json.dumps(r) + "\n" for r in rows)


def put(name, text, binary=False):
    os.makedirs(FX, exist_ok=True)
    p = os.path.join(FX, name)
    with open(p, "wb" if binary else "w") as fh:
        fh.write(text)
    return p


def stop(payload, hooks=LIB):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([sys.executable, os.path.join(hooks, "governance-enforce.py")],
                       input=payload if isinstance(payload, str) else json.dumps(payload), capture_output=True, text=True, env=env)
    out = r.stdout.strip()
    verdict = "allow"
    if out:
        try:
            j = json.loads(out)
            verdict = "block:F1" if "outward action" in j.get("reason", "") else "block:other"
        except Exception:
            verdict = "unparsed"
    err = (r.stderr.strip().splitlines() or [""])[-1][:90]
    return "%-9s exit %d  stderr: %s" % (verdict, r.returncode, err or "(empty)")


def hookset(name, drop=(), replace=None):
    d = os.path.join(SCRATCH, "hooksets", name)
    if os.path.isdir(d):
        shutil.rmtree(d)
    shutil.copytree(LIB, d, ignore=shutil.ignore_patterns("__pycache__"))
    for f in drop:
        os.remove(os.path.join(d, f))
    for f, src in (replace or {}).items():
        shutil.copyfile(src, os.path.join(d, f))
    return d


def pay(path):
    return {"transcript_path": path, "stop_hook_active": False, "session_id": "x"}


def main():
    rows = []
    good = put("x-good.jsonl", dump(EARLIER + TURN))
    rows.append(("X00", "control: the plain ungoverned commit turn", stop(pay(good))))
    rows.append(("X01", "transcript path does not exist", stop(pay(FX + "/no-such-file.jsonl"))))
    rows.append(("X02", "transcript path is a directory", stop(pay(FX))))
    rows.append(("X03", "one extra line holding the JSON value null (parses, is not an object)", stop(pay(put("x-null-line.jsonl", dump(EARLIER) + "null\n" + dump(TURN))))))
    rows.append(("X04", "one extra line holding [] at the very start of the file", stop(pay(put("x-list-line.jsonl", "[]\n" + dump(EARLIER + TURN))))))
    rows.append(("X05", "last line cut off mid-object (a write in progress)", stop(pay(put("x-truncated.jsonl", dump(EARLIER + TURN) + '{"type": "assistant", "message": {"role": "assi')))))
    bad_text = {"type": "user", "message": {"role": "user", "content": [{"type": "text", "text": None}]}}
    rows.append(("X06", "an EARLIER user row whose text block has text null", stop(pay(put("x-text-null.jsonl", dump([bad_text] + EARLIER + TURN))))))
    str_input = {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "tool_use", "id": "t1", "name": "Bash", "input": "git status"}]}}
    rows.append(("X07", "a Bash call in the turn whose input is a string, not an object", stop(pay(put("x-input-str.jsonl", dump(EARLIER + [TURN[0], str_input] + TURN[1:]))))))
    rows.append(("X08", "the same odd Bash call BEFORE the turn (control: must still block)", stop(pay(put("x-input-str-early.jsonl", dump([str_input] + EARLIER + TURN))))))
    num_result = {"type": "user", "message": {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "t0", "content": 5}]}}
    rows.append(("X09", "an EARLIER tool_result whose content is a number", stop(pay(put("x-result-num.jsonl", dump([num_result] + EARLIER + TURN))))))
    str_msg = {"type": "user", "message": "hello"}
    rows.append(("X10", "an EARLIER user row whose message is a bare string", stop(pay(put("x-msg-str.jsonl", dump([str_msg] + EARLIER + TURN))))))
    real_other = [{"type": "attachment", "attachment": {"type": "total_tokens_reminder"}}, {"type": "system", "subtype": "stop_hook_summary", "hookErrors": []},
                  {"type": "queue-operation", "operation": "enqueue", "content": "x", "sessionId": "s", "timestamp": "t"}, {"type": "last-prompt", "lastPrompt": "Continue", "leafUuid": "u", "sessionId": "s"},
                  {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "thinking", "thinking": "", "signature": "x"}]}}]
    rows.append(("X11", "real non-message rows mixed in (attachment, system, queue-operation, last-prompt, thinking): control", stop(pay(put("x-real-other.jsonl", dump(EARLIER + real_other + [TURN[0]] + real_other + TURN[1:] + real_other))))))
    rows.append(("X12", "invalid UTF-8 bytes inside an earlier row", stop(pay(put("x-bad-utf8.jsonl", dump(EARLIER).encode() + b'{"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": "caf\xe9 \xff"}]}}\n' + dump(TURN).encode(), binary=True)))))
    rows.append(("X13", "CRLF line endings", stop(pay(put("x-crlf.jsonl", dump(EARLIER + TURN).replace("\n", "\r\n"))))))
    rows.append(("X14", "stdin is a JSON list, not an object", stop("[1, 2]")))
    rows.append(("X15", "stdin is not JSON", stop("not json")))
    rows.append(("X16", "payload without transcript_path", stop({"stop_hook_active": False})))
    rows.append(("X17", "hooks directory WITHOUT turngate.py", stop(pay(good), hookset("no-turngate", drop=["turngate.py"]))))
    rows.append(("X18", "hooks directory WITHOUT govclass.py (F1 does not use it)", stop(pay(good), hookset("no-govclass", drop=["govclass.py"]))))
    rows.append(("X19", "merged governance-enforce.py beside the 0.1.4 turngate.py (a half-finished sync)", stop(pay(good), hookset("stale-turngate", replace={"turngate.py": OLD + "/turngate.py"}))))
    rows.append(("X20", "0.1.4 governance-enforce.py beside the merged turngate.py (the other half)", stop(pay(good), hookset("stale-enforce", replace={"governance-enforce.py": OLD + "/governance-enforce.py"}))))
    for cid, what, got in rows:
        print("%-4s %s | %s" % (cid, got, what))
    if "big" in sys.argv[1:]:
        filler = json.dumps({"type": "user", "message": {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "t", "content": "x" * 20000}]}}) + "\n"
        for mb in (60, 240):
            p = os.path.join(SCRATCH, "big-%d.jsonl" % mb)
            with open(p, "w") as fh:
                fh.write(dump(EARLIER))
                for _ in range(mb * 1024 * 1024 // len(filler)):
                    fh.write(filler)
                fh.write(dump(TURN))
            t0 = time.time()
            got = stop(pay(p))
            print("BIG  %s | %d MB transcript, %.2f s (Stop timeout in settings.json: 15 s)" % (got, os.path.getsize(p) // (1024 * 1024), time.time() - t0))
            os.remove(p)


if __name__ == "__main__":
    main()
