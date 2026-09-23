#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

LABELS = ["TRUE", "FALSE", "INSUFFICIENT_EVIDENCE", "NOT_APPLICABLE"]

def read_jsonl(path):
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]

def safe_div(a,b):
    return a/b if b else None

def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: score_run02.py ANSWER_KEY_v0.2.jsonl PREDICTIONS_RUN02.jsonl")

    answers = {x["case_id"]: x for x in read_jsonl(sys.argv[1])}
    preds = {x["case_id"]: x for x in read_jsonl(sys.argv[2])}

    missing = sorted(set(answers)-set(preds))
    extra = sorted(set(preds)-set(answers))
    if missing or extra:
        raise SystemExit(f"case mismatch missing={missing} extra={extra}")

    confusion = {a:{p:0 for p in LABELS} for a in LABELS}
    criterion_total=Counter()
    criterion_correct=Counter()
    label_total=Counter()
    label_correct=Counter()
    route_total=0
    route_correct=0
    false_pass=0
    false_reject=0
    expected_escalate=0
    predicted_escalate=0
    correct_escalate=0
    standalone_total=0
    standalone_correct=0
    relation_cases=defaultdict(list)

    for cid, ans in answers.items():
        pred=preds[cid]
        if pred["prediction"] not in LABELS:
            raise SystemExit(f"invalid label {cid}: {pred['prediction']}")
        correct = pred["prediction"] == ans["expected"]

        confusion[ans["expected"]][pred["prediction"]] += 1
        criterion_total[ans["criterion"]] += 1
        criterion_correct[ans["criterion"]] += int(correct)
        label_total[ans["expected"]] += 1
        label_correct[ans["expected"]] += int(correct)

        route_total += 1
        route_correct += int(pred["route"] == ans["route"])

        if ans["route"] in {"REVISE","ESCALATE"} and pred["route"] == "PASS":
            false_pass += 1
        if ans["route"] == "PASS" and pred["route"] == "REVISE":
            false_reject += 1

        expected_escalate += int(ans["route"] == "ESCALATE")
        predicted_escalate += int(pred["route"] == "ESCALATE")
        correct_escalate += int(ans["route"] == "ESCALATE" and pred["route"] == "ESCALATE")

        group=ans.get("relation_group")
        if group:
            relation_cases[group].append(correct)
        else:
            standalone_total += 1
            standalone_correct += int(correct)

    relation_total=len(relation_cases)
    relation_correct=sum(all(v) for v in relation_cases.values())

    n=len(answers)
    out={
        "cases":n,
        "case_accuracy":safe_div(sum(label_correct.values()),n),
        "route_accuracy":safe_div(route_correct,route_total),
        "accuracy_by_label":{k:{
            "correct":label_correct[k],
            "total":label_total[k],
            "accuracy":safe_div(label_correct[k],label_total[k])
        } for k in LABELS},
        "accuracy_by_criterion":{k:{
            "correct":criterion_correct[k],
            "total":criterion_total[k],
            "accuracy":safe_div(criterion_correct[k],criterion_total[k])
        } for k in sorted(criterion_total)},
        "hidden_relation_groups":{
            "correct":relation_correct,
            "total":relation_total,
            "accuracy":safe_div(relation_correct,relation_total)
        },
        "standalone_cases":{
            "correct":standalone_correct,
            "total":standalone_total,
            "accuracy":safe_div(standalone_correct,standalone_total)
        },
        "critical_false_pass_count":false_pass,
        "false_reject_count":false_reject,
        "escalate":{
            "expected":expected_escalate,
            "predicted":predicted_escalate,
            "correct":correct_escalate,
            "recall":safe_div(correct_escalate,expected_escalate),
            "precision":safe_div(correct_escalate,predicted_escalate)
        },
        "confusion_matrix":confusion
    }
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
