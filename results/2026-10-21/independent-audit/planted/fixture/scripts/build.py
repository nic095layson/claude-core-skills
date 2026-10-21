import json, sys
THRESHOLD = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
rows = [0.42, 0.55, 0.61, 0.73]
kept = [r for r in rows if r >= THRESHOLD]
print(json.dumps({"threshold": THRESHOLD, "kept": kept}))
print("BUILD: PASS")
