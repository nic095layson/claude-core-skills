import json,sys,os,re
for d in sys.argv[1:]:
    ev=[]
    for l in open(os.path.join(d,"out.jsonl")):
        try: r=json.loads(l)
        except: continue
        t=r.get("type")
        if t=="assistant":
            for b in r["message"].get("content") or []:
                if b.get("type")=="tool_use":
                    nm=b["name"]; x=(b["input"].get("skill") if nm=="Skill" else (b["input"].get("command") or b["input"].get("file_path") or ""))
                    ev.append(f"T:{nm}:{str(x)[:40]}")
                elif b.get("type")=="text" and b["text"].strip():
                    ev.append("X:"+("GOAL " if re.search(r"\bGoal\b",b["text"]) else "")+b["text"][:40].replace("\n"," "))
        elif t=="system" and r.get("subtype") in ("hook_response","hook_started"):
            o=json.dumps(r)
            if r.get("subtype")=="hook_response" and ("GOV-ENFORCE" in o or "TURN-GATE" in o):
                ev.append("HOOK:"+("F1-BLOCK" if "outward action" in o else "STOP-BLOCK" if "GOV-ENFORCE" in o else "F3-ADVISE" if "plan shown" in o else "F2" ))
        elif t=="result": ev.append("RESULT:"+str(r.get("subtype")))
    print(os.path.basename(d)); [print("   ",e) for e in ev]
