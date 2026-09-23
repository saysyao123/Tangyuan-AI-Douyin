#!/usr/bin/env python3
"""
Deterministic scorer for Motion Gate v0.1.

Usage:
  python score_baseline.py \
    CONTRASTIVE_ANSWER_KEY_v0.1.jsonl \
    BLIND_PREDICTIONS_RUN01.jsonl

This script performs no model inference.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path


def read_jsonl(path: str):
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def flatten_answers(rows):
    out = {}
    for row in rows:
        pid = row["pair_id"]
        crit = row["criterion"]
        for suffix, key in (("A", "case_a"), ("B", "case_b")):
            cid = f"{pid}_{suffix}"
            out[cid] = {
                "criterion": crit,
                "expected": row[key]["expected"],
                "route": row[key]["route"],
                "pair_id": pid,
            }
    return out


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: score_baseline.py ANSWER_KEY.jsonl PREDICTIONS.jsonl")

    answers = flatten_answers(read_jsonl(sys.argv[1]))
    preds_rows = read_jsonl(sys.argv[2])
    preds = {r["case_id"]: r for r in preds_rows}

    missing = sorted(set(answers) - set(preds))
    extra = sorted(set(preds) - set(answers))
    if missing or extra:
        raise SystemExit(f"case mismatch: missing={missing} extra={extra}")

    n = len(answers)
    correct = 0
    route_correct = 0
    false_pass = 0
    false_reject = 0
    criterion_errors = defaultdict(int)
    pair_ok = defaultdict(lambda: True)

    for cid, ans in answers.items():
        pred = preds[cid]
        pred_ok = pred["prediction"] == ans["expected"]
        route_ok = pred["route"] == ans["route"]

        correct += int(pred_ok)
        route_correct += int(route_ok)

        if not pred_ok:
            criterion_errors[ans["criterion"]] += 1
            pair_ok[ans["pair_id"]] = False

        if ans["route"] in {"REVISE", "ESCALATE"} and pred["route"] == "PASS":
            false_pass += 1

        if ans["route"] == "PASS" and pred["route"] == "REVISE":
            false_reject += 1

    total_pairs = len({v["pair_id"] for v in answers.values()})
    correct_pairs = sum(1 for ok in pair_ok.values() if ok)
    # pairs with no errors never touched in defaultdict:
    error_pairs = {p for p, ok in pair_ok.items() if not ok}
    correct_pairs = total_pairs - len(error_pairs)

    insuff_ids = [
        cid for cid, ans in answers.items()
        if ans["route"] == "ESCALATE"
    ]
    insuff_correct = sum(
        1 for cid in insuff_ids
        if preds[cid]["route"] == "ESCALATE"
    )

    result = {
        "cases": n,
        "pairs": total_pairs,
        "case_accuracy": correct / n,
        "pair_accuracy": correct_pairs / total_pairs,
        "route_accuracy": route_correct / n,
        "critical_false_pass_count": false_pass,
        "critical_false_pass_rate": false_pass / n,
        "false_reject_count": false_reject,
        "false_reject_rate": false_reject / n,
        "insufficient_evidence_cases": len(insuff_ids),
        "insufficient_evidence_route_accuracy":
            (insuff_correct / len(insuff_ids)) if insuff_ids else None,
        "errors_by_criterion": dict(sorted(criterion_errors.items())),
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
