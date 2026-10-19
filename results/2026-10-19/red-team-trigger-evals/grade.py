#!/usr/bin/env python3
"""Grade the red-team trigger-eval transcripts (2026-10-19).

FIRED := a Skill tool_use whose `skill` ends with "red-team" appears in the stream-json transcript
(evals/red-team.json `_grading.operationalization`). Nothing else counts: text that talks about red-teaming
without loading the skill is SILENT. Also recorded per run: the model the init event names, other skills
invoked, turn count, result subtype and cost. A run whose result subtype is not `success` or `error_max_turns`
(a session-limit refusal, a network error) is a NON-RUN (ledger INC-2026-08-26-01) and is listed, not graded.

Gate, as pre-registered in experiments/hypothesis-2026-10-19-red-team.md: ids 1-3 fire in >=5 of 6 runs;
ids 4-5 silent in 4 of 4. The evals file's own `_grading.gate` reads >=3/4 silent; both readings are printed.
id 6 is a should-fire case recorded beside the gate, as the hypothesis lists it.

    python3 grade.py <transcripts_dir> <model_tag> [--json OUT]
Transcripts are named <model_tag>-id<N>-r<R>.jsonl.
"""
import collections
import glob
import json
import os
import re
import sys

EVALS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "evals", "red-team.json")
GATE_IDS = (1, 2, 3)
SILENT_IDS = (4, 5)
EXTRA_FIRE_IDS = (6,)


def read_run(path):
    invoked, model, turns, subtype, cost = [], None, None, None, None
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if ev.get("type") == "system" and ev.get("subtype") == "init":
                model = ev.get("model")
            if ev.get("type") == "result":
                turns, subtype, cost = ev.get("num_turns"), ev.get("subtype"), ev.get("total_cost_usd")
            msg = ev.get("message")
            if not isinstance(msg, dict):
                continue
            content = msg.get("content")
            if not isinstance(content, list):
                continue
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_use" and block.get("name") == "Skill":
                    invoked.append(str((block.get("input") or {}).get("skill") or "?"))
    return dict(invoked=invoked, model=model, turns=turns, subtype=subtype, cost=cost)


def fired(invoked):
    return any(s.split(":")[-1] == "red-team" for s in invoked)


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    tdir, tag = argv[1], argv[2]
    out = argv[argv.index("--json") + 1] if "--json" in argv else None
    spec = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), EVALS) if not os.path.isabs(EVALS) else EVALS))
    rows, nonruns = [], []
    for case in spec["evals"]:
        cid = case["id"]
        expect_fire = case["expected_output"].startswith("FIRES")
        for path in sorted(glob.glob(os.path.join(tdir, f"{tag}-id{cid}-r*.jsonl"))):
            r = int(re.search(r"-r(\d+)\.jsonl$", path).group(1))
            run = read_run(path)
            if run["subtype"] not in ("success", "error_max_turns"):
                nonruns.append(dict(id=cid, run=r, subtype=run["subtype"], file=os.path.basename(path)))
                continue
            f = fired(run["invoked"])
            rows.append(dict(id=cid, run=r, expect="FIRE" if expect_fire else "SILENT", fired=f,
                             grade="PASS" if f == expect_fire else "FAIL", invoked=run["invoked"],
                             model=run["model"], turns=run["turns"], subtype=run["subtype"], cost=run["cost"]))
    print(f"{'id':<4}{'run':<5}{'expect':<8}{'fired':<7}{'grade':<6}{'turns':<7}{'end':<17}{'cost':<8}invoked")
    for x in rows:
        print(f"{x['id']:<4}{x['run']:<5}{x['expect']:<8}{str(x['fired']):<7}{x['grade']:<6}{str(x['turns']):<7}"
              f"{str(x['subtype']):<17}{(x['cost'] or 0):<8.2f}{','.join(x['invoked']) or '-'}")
    for n in nonruns:
        print(f"NON-RUN id{n['id']} r{n['run']}: {n['subtype']} ({n['file']})")
    models = collections.Counter(x["model"] for x in rows)
    gate_f = [x for x in rows if x["id"] in GATE_IDS]
    extra_f = [x for x in rows if x["id"] in EXTRA_FIRE_IDS]
    sil = [x for x in rows if x["id"] in SILENT_IDS]
    gf, gt = sum(x["fired"] for x in gate_f), len(gate_f)
    ef, et = sum(x["fired"] for x in extra_f), len(extra_f)
    ss, st = sum(not x["fired"] for x in sil), len(sil)
    strict = gt and gf / gt >= 5 / 6 and st and ss == st
    lenient = gt and gf / gt >= 5 / 6 and st and ss / st >= 3 / 4
    summary = dict(model_tag=tag, models_observed=dict(models), should_fire_ids_1_3=f"{gf}/{gt}",
                   should_fire_id_6=f"{ef}/{et}", should_not_ids_4_5_silent=f"{ss}/{st}",
                   gate_hypothesis_5of6_and_4of4="PASS" if strict else "FAIL",
                   gate_evalsfile_5of6_and_3of4="PASS" if lenient else "FAIL",
                   total_cost_usd=round(sum(x["cost"] or 0 for x in rows), 2), nonruns=nonruns, rows=rows)
    print()
    print(f"models observed: {dict(models)}")
    print(f"should-fire ids 1-3: {gf}/{gt}   id 6: {ef}/{et}   should-not ids 4-5 silent: {ss}/{st}")
    print(f"gate (hypothesis: >=5/6 fire, 4/4 silent): {summary['gate_hypothesis_5of6_and_4of4']}")
    print(f"gate (evals file: >=5/6 fire, >=3/4 silent): {summary['gate_evalsfile_5of6_and_3of4']}")
    print(f"cost: ${summary['total_cost_usd']}")
    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=1)
            f.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
