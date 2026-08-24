#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parent
ANALYSIS_DIR = DATA_DIR / "analysis"
ELIGIBLE_STATUSES = {"AUTO_HIGH", "MANUAL_CONFIRMED"}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def parse_dt(value: str) -> datetime | None:
    text = str(value or "").strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S"):
        try:
            dt = datetime.strptime(text, fmt)
            return dt.replace(tzinfo=None)
        except ValueError:
            pass
    return None


def fnum(value: Any) -> float:
    try:
        return float(value or 0)
    except Exception:
        return 0.0


def inum(value: Any) -> int:
    try:
        return int(float(value or 0))
    except Exception:
        return 0


def best_72h_distinct_accounts(rows: list[dict[str, Any]]) -> int:
    events = sorted((row["dt"], row["account_id"]) for row in rows if row.get("dt"))
    best = 0
    for i, (start, _) in enumerate(events):
        end = start + timedelta(hours=72)
        accounts = {account for dt, account in events[i:] if dt <= end}
        best = max(best, len(accounts))
    return best


def main() -> int:
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    accounts = read_csv(DATA_DIR / "accounts.csv")
    works = read_csv(DATA_DIR / "works.csv")
    norm = read_csv(DATA_DIR / "song_normalization.csv")
    manifest = json.loads((DATA_DIR / "manifest.json").read_text(encoding="utf-8"))

    account_by_id = {row["account_id"]: row for row in accounts}
    norm_by_aweme = {row["aweme_id"]: row for row in norm if row.get("aweme_id")}

    # Correct freshness semantics: account inactivity is not collection staleness.
    # HG01 data readiness comes only from a successful authenticated live run + closed windows.
    all_complete = len(accounts) == 9 and all(inum(row.get("window_15d_complete")) == 1 for row in accounts)
    authenticated_manifest_pass = bool(manifest.get("authenticated_gate_pass"))
    hg01_data_gate = bool(all_complete and authenticated_manifest_pass)

    end_dt = parse_dt(str(manifest.get("window_end_exclusive") or ""))
    if not end_dt:
        raise RuntimeError("manifest window_end_exclusive is missing or invalid")
    start_7d = end_dt - timedelta(days=7)

    eligible = []
    unresolved = 0
    for work in works:
        n = norm_by_aweme.get(work["aweme_id"])
        if not n or n.get("normalization_status") not in ELIGIBLE_STATUSES or not n.get("song_family"):
            unresolved += 1
            continue
        dt = parse_dt(work.get("create_time", ""))
        if not dt:
            continue
        eligible.append({
            **work,
            "dt": dt,
            "song_family": n["song_family"].strip(),
            "audio_version": n.get("audio_version", ""),
            "confidence": fnum(n.get("confidence")),
        })

    by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in eligible:
        by_family[row["song_family"]].append(row)

    candidate_rows = []
    evidence = []
    for family, rows in by_family.items():
        account_ids_15 = sorted({row["account_id"] for row in rows})
        if len(account_ids_15) < 2:
            continue
        rows_7 = [row for row in rows if start_7d <= row["dt"] < end_dt]
        account_ids_7 = sorted({row["account_id"] for row in rows_7})
        trend_weight_15 = sum(fnum(account_by_id[aid].get("trend_weight")) for aid in account_ids_15)
        trend_weight_7 = sum(fnum(account_by_id[aid].get("trend_weight")) for aid in account_ids_7)
        visual_overlap = sum(1 for aid in account_ids_15 if fnum(account_by_id[aid].get("visual_weight")) >= 0.80)
        versions = sorted({row.get("audio_version", "") for row in rows if row.get("audio_version")})
        latest = max(row["dt"] for row in rows)
        first = min(row["dt"] for row in rows)
        concentration = best_72h_distinct_accounts(rows)

        candidate_rows.append({
            "song_family": family,
            "distinct_accounts_15d": len(account_ids_15),
            "distinct_accounts_7d": len(account_ids_7),
            "weighted_trend_15d": round(trend_weight_15, 3),
            "weighted_trend_7d": round(trend_weight_7, 3),
            "visual_overlap_accounts": visual_overlap,
            "best_72h_distinct_accounts": concentration,
            "audio_version_count": len(versions),
            "first_observed_work_time": first.strftime("%Y-%m-%d %H:%M:%S"),
            "latest_observed_work_time": latest.strftime("%Y-%m-%d %H:%M:%S"),
            "hg01_data_gate": "PASS" if hg01_data_gate else "BLOCKED",
        })

        family_evidence = []
        for row in sorted(rows, key=lambda x: x["dt"], reverse=True):
            account = account_by_id[row["account_id"]]
            family_evidence.append({
                "song_family": family,
                "account_id": row["account_id"],
                "nickname": account.get("current_nickname", ""),
                "douyin_id": account.get("douyin_id", ""),
                "create_time": row.get("create_time", ""),
                "aweme_id": row["aweme_id"],
                "work_url": row.get("work_url", ""),
                "caption": row.get("caption", ""),
                "audio_version": row.get("audio_version", ""),
            })
        evidence.append({"song_family": family, "works": family_evidence})

    candidate_rows.sort(
        key=lambda row: (
            row["distinct_accounts_7d"], row["weighted_trend_7d"],
            row["distinct_accounts_15d"], row["best_72h_distinct_accounts"],
            row["weighted_trend_15d"],
        ),
        reverse=True,
    )

    fields = [
        "song_family","distinct_accounts_15d","distinct_accounts_7d","weighted_trend_15d",
        "weighted_trend_7d","visual_overlap_accounts","best_72h_distinct_accounts",
        "audio_version_count","first_observed_work_time","latest_observed_work_time","hg01_data_gate",
    ]
    with (ANALYSIS_DIR / "song_repeat_candidates.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader(); w.writerows(candidate_rows)
    (ANALYSIS_DIR / "direct_douyin_evidence.json").write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    by_account_works: dict[str, list[datetime]] = defaultdict(list)
    for work in works:
        dt = parse_dt(work.get("create_time", ""))
        if dt:
            by_account_works[work["account_id"]].append(dt)

    lines = [
        "# WEB R3｜Database Song Analysis v2", "",
        f"- observed_at: `{manifest.get('observed_at', '')}`",
        f"- collector: `{manifest.get('collector', '')}`",
        f"- 9-account authenticated completeness: `{'PASS' if hg01_data_gate else 'BLOCKED'}`",
        f"- normalized eligible works: `{len(eligible)}` / `{len(works)}`",
        f"- unresolved/review-required works: `{unresolved}`",
        f"- repeated SONG_FAMILY (2+ accounts): `{len(candidate_rows)}`", "",
        "## Gate semantics", "",
        "Account posting age is **not** a data-freshness gate. A creator may legitimately publish nothing for days.",
        "HG01 data readiness requires authenticated live collection + identity/ownership verification + complete window closure for all 9 locked accounts.", "",
        "## Core account activity snapshot", "",
        "| account | works/15d | latest work | window gate |",
        "|---|---:|---|---|",
    ]
    for account in accounts:
        times = by_account_works.get(account["account_id"], [])
        latest = max(times).strftime("%Y-%m-%d %H:%M:%S") if times else "NO_WORK_IN_WINDOW"
        lines.append(
            f"| {account.get('current_nickname') or account['account_id']} | {len(times)} | {latest} | "
            f"{'PASS' if inum(account.get('window_15d_complete')) else 'BLOCKED'} |"
        )

    lines += ["", "## Repeated song families", "",
              "| SONG_FAMILY | acc/7d | acc/15d | weighted/7d | best72h | visual overlap | versions | latest |",
              "|---|---:|---:|---:|---:|---:|---:|---|"]
    for row in candidate_rows:
        lines.append(
            f"| {row['song_family']} | {row['distinct_accounts_7d']} | {row['distinct_accounts_15d']} | "
            f"{row['weighted_trend_7d']} | {row['best_72h_distinct_accounts']} | "
            f"{row['visual_overlap_accounts']} | {row['audio_version_count']} | {row['latest_observed_work_time']} |"
        )
    lines += ["", "## HG01", "", f"`HG01_DATA_READY = {'YES' if hg01_data_gate else 'NO'}`", "",
              "Candidates may be inspected internally while this Gate is NO, but they must not be delivered as the final current R3 shortlist."]
    (ANALYSIS_DIR / "R3_DATABASE_SONG_ANALYSIS_v2.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    summary = {
        "hg01_data_ready": hg01_data_gate,
        "eligible_works": len(eligible),
        "total_works": len(works),
        "repeat_families": len(candidate_rows),
        "top_candidates": candidate_rows[:10],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if hg01_data_gate else 2


if __name__ == "__main__":
    raise SystemExit(main())
