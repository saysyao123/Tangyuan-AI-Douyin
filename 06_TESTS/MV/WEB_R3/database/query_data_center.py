#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

DB_DIR = Path(__file__).resolve().parent
CENTER = DB_DIR / "data_center"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def read_json(path: Path, default: Any):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def lower(value: Any) -> str:
    return str(value or "").strip().lower()


def emit(data: Any, as_json: bool) -> None:
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{key}: {value}")
        return
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                print(" | ".join(f"{k}={v}" for k, v in item.items()))
            else:
                print(item)
        return
    print(data)


def load():
    manifest = read_json(CENTER / "manifest.json", {})
    accounts = read_csv(DB_DIR / "accounts.csv")
    works = read_csv(CENTER / "observed_works.csv")
    metrics = read_csv(CENTER / "observed_metrics.csv")
    norms = read_csv(CENTER / "song_normalization.csv")
    candidates = read_csv(CENTER / "song_repeat_candidates.csv")
    evidence = read_json(CENTER / "direct_douyin_evidence.json", [])
    snapshots = read_csv(CENTER / "snapshots.csv")
    coverage = read_csv(CENTER / "coverage_latest.csv")
    return manifest, accounts, works, metrics, norms, candidates, evidence, snapshots, coverage


def latest_metrics(metrics: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    by_aweme: dict[str, dict[str, str]] = {}
    for row in metrics:
        aid = row.get("aweme_id", "")
        current = by_aweme.get(aid)
        if current is None or row.get("observed_at", "") > current.get("observed_at", ""):
            by_aweme[aid] = row
    return by_aweme


def resolve_account(query: str, accounts: list[dict[str, str]]) -> list[dict[str, str]]:
    q = lower(query)
    exact = []
    partial = []
    for row in accounts:
        values = [row.get("account_id"), row.get("case_id"), row.get("sec_uid"), row.get("douyin_id"), row.get("current_nickname")]
        values_lower = [lower(x) for x in values if x]
        if q in values_lower:
            exact.append(row)
        elif any(q in value for value in values_lower):
            partial.append(row)
    return exact or partial


def command_status(manifest, accounts, works, norms, candidates, snapshots):
    status_counts: dict[str, int] = defaultdict(int)
    for row in norms:
        status_counts[row.get("normalization_status", "UNKNOWN")] += 1
    return {
        "version": manifest.get("version"),
        "mode": manifest.get("mode"),
        "semantics": manifest.get("semantics"),
        "observed_at": manifest.get("observed_at"),
        "anchor_latest_observed": manifest.get("anchor_latest_observed"),
        "rolling_window_start": manifest.get("rolling_window_start"),
        "rolling_window_end_exclusive": manifest.get("rolling_window_end_exclusive"),
        "core_accounts": len(accounts),
        "cumulative_unique_works": len(works),
        "normalization_status_counts": dict(status_counts),
        "repeated_song_families": len(candidates),
        "snapshots": len(snapshots),
        "refresh_cadence_days": manifest.get("refresh_cadence_days"),
        "next_refresh_due_approx": manifest.get("next_refresh_due_approx"),
        "hg01_evidence_ready": manifest.get("hg01_evidence_ready"),
    }


def command_health(manifest, accounts, works, metrics, norms, candidates, evidence, snapshots, coverage):
    required = [
        CENTER / "manifest.json", CENTER / "observed_works.csv", CENTER / "observed_metrics.csv",
        CENTER / "snapshots.csv", CENTER / "coverage_latest.csv", CENTER / "song_normalization.csv",
        CENTER / "song_repeat_candidates.csv", CENTER / "direct_douyin_evidence.json",
    ]
    account_ids = {row.get("account_id", "") for row in accounts}
    work_ids = [row.get("aweme_id", "") for row in works]
    work_set = set(work_ids)
    norm_ids = {row.get("aweme_id", "") for row in norms}
    metric_ids = {row.get("aweme_id", "") for row in metrics}
    evidence_ids = {
        work.get("aweme_id", "")
        for group in evidence if isinstance(group, dict)
        for work in group.get("works", []) if isinstance(work, dict)
    }
    checks = {
        "required_files_present": all(path.exists() for path in required),
        "core_account_count_is_9": len(accounts) == 9,
        "work_ids_unique": len(work_ids) == len(work_set) and "" not in work_set,
        "works_reference_known_accounts": all(row.get("account_id", "") in account_ids for row in works),
        "normalization_references_known_works": norm_ids.issubset(work_set),
        "metrics_reference_known_works": metric_ids.issubset(work_set),
        "direct_evidence_references_known_works": evidence_ids.issubset(work_set),
        "manifest_version_present": bool(manifest.get("version")),
        "snapshot_history_present": len(snapshots) >= 1,
        "coverage_has_9_rows": len(coverage) == 9,
        "candidate_evidence_present": all(row.get("song_family") for row in candidates),
    }
    return {"pass": all(checks.values()), "checks": checks}


def command_accounts(accounts, works):
    times: dict[str, list[str]] = defaultdict(list)
    counts: dict[str, int] = defaultdict(int)
    for work in works:
        aid = work.get("account_id", "")
        counts[aid] += 1
        if work.get("create_time"):
            times[aid].append(work["create_time"])
    rows = []
    for account in accounts:
        aid = account["account_id"]
        rows.append({
            "account_id": aid,
            "case_id": account.get("case_id", ""),
            "nickname": account.get("current_nickname", ""),
            "douyin_id": account.get("douyin_id", ""),
            "role_category": account.get("role_category", ""),
            "trend_weight": account.get("trend_weight", ""),
            "visual_weight": account.get("visual_weight", ""),
            "observed_works": counts[aid],
            "latest_observed_work": max(times[aid]) if times[aid] else "",
        })
    return rows


def command_account(query, limit, accounts, works, norms, metrics):
    matched = resolve_account(query, accounts)
    if not matched:
        return {"error": f"account not found: {query}"}
    norm_by_id = {row.get("aweme_id", ""): row for row in norms}
    metric_by_id = latest_metrics(metrics)
    results = []
    for account in matched:
        aid = account["account_id"]
        account_works = sorted(
            [row for row in works if row.get("account_id") == aid],
            key=lambda row: row.get("create_time", ""), reverse=True,
        )[:limit]
        work_rows = []
        for row in account_works:
            wid = row["aweme_id"]
            n = norm_by_id.get(wid, {})
            m = metric_by_id.get(wid, {})
            work_rows.append({
                "create_time": row.get("create_time", ""),
                "aweme_id": wid,
                "song_family": n.get("song_family", ""),
                "normalization_status": n.get("normalization_status", ""),
                "caption": row.get("caption", ""),
                "work_url": row.get("work_url", ""),
                "digg_count": m.get("digg_count", ""),
                "collect_count": m.get("collect_count", ""),
            })
        results.append({
            "account": {
                "account_id": aid,
                "case_id": account.get("case_id", ""),
                "nickname": account.get("current_nickname", ""),
                "douyin_id": account.get("douyin_id", ""),
                "sec_uid": account.get("sec_uid", ""),
                "role": account.get("role", ""),
                "role_category": account.get("role_category", ""),
                "trend_weight": account.get("trend_weight", ""),
                "visual_weight": account.get("visual_weight", ""),
                "profile_short_url": account.get("profile_short_url", ""),
            },
            "works": work_rows,
        })
    return results


def command_repeats(limit, candidates):
    return candidates[:limit]


def command_song(query, candidates, evidence, works, norms):
    q = lower(query)
    candidate_matches = [row for row in candidates if q in lower(row.get("song_family"))]
    evidence_matches = [group for group in evidence if isinstance(group, dict) and q in lower(group.get("song_family"))]
    if candidate_matches or evidence_matches:
        return {"candidates": candidate_matches, "direct_evidence": evidence_matches}

    norm_by_id = {row.get("aweme_id", ""): row for row in norms}
    hits = []
    for work in works:
        n = norm_by_id.get(work.get("aweme_id", ""), {})
        hay = " ".join([
            work.get("caption", ""), work.get("music_title_raw", ""), work.get("music_author_raw", ""),
            work.get("hashtags", ""), n.get("song_family", ""), n.get("audio_version", ""),
        ]).lower()
        if q in hay:
            hits.append({
                "aweme_id": work.get("aweme_id", ""),
                "create_time": work.get("create_time", ""),
                "song_family": n.get("song_family", ""),
                "audio_version": n.get("audio_version", ""),
                "caption": work.get("caption", ""),
                "work_url": work.get("work_url", ""),
            })
    return {"candidates": [], "direct_evidence": [], "observed_work_hits": hits}


def command_work(aweme_id, works, norms, metrics):
    work = next((row for row in works if row.get("aweme_id") == aweme_id), None)
    if not work:
        return {"error": f"work not found: {aweme_id}"}
    norm = next((row for row in norms if row.get("aweme_id") == aweme_id), {})
    metric = latest_metrics(metrics).get(aweme_id, {})
    return {"work": work, "normalization": norm, "latest_metrics": metric}


def command_search(query, limit, accounts, works, norms):
    q = lower(query)
    account_by_id = {row.get("account_id", ""): row for row in accounts}
    norm_by_id = {row.get("aweme_id", ""): row for row in norms}
    hits = []
    for work in works:
        n = norm_by_id.get(work.get("aweme_id", ""), {})
        account = account_by_id.get(work.get("account_id", ""), {})
        fields = [
            work.get("caption", ""), work.get("music_title_raw", ""), work.get("music_author_raw", ""),
            work.get("hashtags", ""), n.get("song_family", ""), n.get("audio_version", ""),
            account.get("current_nickname", ""), account.get("douyin_id", ""),
        ]
        if q in " ".join(fields).lower():
            hits.append({
                "create_time": work.get("create_time", ""),
                "nickname": account.get("current_nickname", ""),
                "aweme_id": work.get("aweme_id", ""),
                "song_family": n.get("song_family", ""),
                "caption": work.get("caption", ""),
                "work_url": work.get("work_url", ""),
            })
    hits.sort(key=lambda row: row.get("create_time", ""), reverse=True)
    return hits[:limit]


def main() -> int:
    parser = argparse.ArgumentParser(description="Stable query interface for WEB R3 Douyin Data Center v1")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    sub.add_parser("health")
    sub.add_parser("accounts")

    p = sub.add_parser("account")
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=20)

    p = sub.add_parser("repeats")
    p.add_argument("--limit", type=int, default=20)

    p = sub.add_parser("song")
    p.add_argument("query")

    p = sub.add_parser("work")
    p.add_argument("aweme_id")

    p = sub.add_parser("search")
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=30)

    args = parser.parse_args()
    manifest, accounts, works, metrics, norms, candidates, evidence, snapshots, coverage = load()

    if args.command == "status":
        data = command_status(manifest, accounts, works, norms, candidates, snapshots)
    elif args.command == "health":
        data = command_health(manifest, accounts, works, metrics, norms, candidates, evidence, snapshots, coverage)
    elif args.command == "accounts":
        data = command_accounts(accounts, works)
    elif args.command == "account":
        data = command_account(args.query, args.limit, accounts, works, norms, metrics)
    elif args.command == "repeats":
        data = command_repeats(args.limit, candidates)
    elif args.command == "song":
        data = command_song(args.query, candidates, evidence, works, norms)
    elif args.command == "work":
        data = command_work(args.aweme_id, works, norms, metrics)
    elif args.command == "search":
        data = command_search(args.query, args.limit, accounts, works, norms)
    else:
        raise RuntimeError(args.command)

    emit(data, args.json)
    if args.command == "health" and not data.get("pass"):
        return 2
    if isinstance(data, dict) and data.get("error"):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
