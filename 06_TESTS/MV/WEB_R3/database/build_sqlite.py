#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import sqlite3
from pathlib import Path

TABLES = ["accounts", "works", "work_metrics", "ingestion_runs", "song_normalization"]


def load_csv(conn: sqlite3.Connection, table: str, csv_path: Path) -> int:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        cols = reader.fieldnames or []
    if not rows:
        return 0
    placeholders = ",".join("?" for _ in cols)
    conn.executemany(
        f"INSERT OR REPLACE INTO {table} ({','.join(cols)}) VALUES ({placeholders})",
        [[row.get(col, "") for col in cols] for row in rows],
    )
    return len(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build R3 Douyin SQLite database from Git-tracked CSV tables.")
    parser.add_argument("--data-dir", default=str(Path(__file__).resolve().parent))
    parser.add_argument("--out", default="r3_douyin.sqlite3")
    args = parser.parse_args()
    data_dir = Path(args.data_dir).resolve()
    out = Path(args.out).resolve()
    if out.exists():
        out.unlink()
    conn = sqlite3.connect(out)
    try:
        conn.executescript((data_dir / "schema.sql").read_text(encoding="utf-8"))
        counts = {table: load_csv(conn, table, data_dir / f"{table}.csv") for table in TABLES}
        conn.commit()
        fk_errors = conn.execute("PRAGMA foreign_key_check").fetchall()
        if fk_errors:
            raise RuntimeError(f"foreign key check failed: {fk_errors}")
        print({"db": str(out), "rows": counts, "foreign_key_check": "PASS"})
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
