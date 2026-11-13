#!/usr/bin/env python3
"""Every tool name in pack/session-tools.txt through the merged turngate.is_outward (read-only import)."""
import re, sys
PACK = "/tmp/claude-0/-home-user/ff01f16c-7b3f-5ea5-8051-7a95ac7cd1d1/scratchpad/merge-audit"
sys.dont_write_bytecode = True
sys.path.insert(0, PACK + "/lib/hooks")
import turngate
L = open(PACK + "/pack/session-tools.txt").read().splitlines()
def words(a, b):  # 1-based inclusive line range -> names
    return [w for w in re.split(r"[,\s]+", " ".join(L[a - 1:b]).replace("Loaded on demand:", " ")) if re.fullmatch(r"[A-Za-z_]\w*\*?", w)]
tools = words(4, 11)
tools += ["mcp__claude-code-remote__" + w for w in words(14, 19)]
for w in words(23, 32):
    tools.append("mcp__github__" + w.rstrip("*"))
    if w.endswith("*"):
        tools.append("mcp__GH__" + w.rstrip("*"))
tools += ["mcp__GH__" + w for w in words(33, 34) if w not in ("Only", "under", "mcp__GH__")]
for a, b, pre in ((37, 42, "mcp__Gmail__"), (43, 45, "mcp__Google_Drive__"), (46, 46, "mcp__Claude_Docs__")):
    tools += [pre + w for w in words(a, b) if not w.startswith("mcp__")]
counted = [t for t in tools if turngate.is_outward({"name": t, "input": {}})]
print("session tool names parsed: %d; counted as outward by the merged turngate.is_outward: %d" % (len(tools), len(counted)))
print("COUNTED: " + ", ".join(counted))
STATE = re.compile(r"(create|update|delete|merge|push|write|send|reply|forward|fork|fire_|run_trigger|share_file|trash|archive|enable_pr|disable_pr|resolve|add_|request_copilot|switch|interrupt|Cron(Create|Delete)|ScheduleWakeup|^Artifact$|^Agent$|^Workflow$|batch|^Monitor$|PushNotification|SendMessage|SendUserFile)")
rest = [t for t in tools if t not in counted and STATE.search(t)]
print("NOT COUNTED although the name says it changes or sends something (%d):" % len(rest))
print(", ".join(rest))
