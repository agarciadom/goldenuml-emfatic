#!/usr/bin/env python3
"""Combine generated.csv, compare-names.csv, and compare-models.csv for each
nl2flexmi run (one row per case + model pair) into a single CSV file.

Each run lives at: <case>/nl2flexmi/<model>/{generated.csv,compare-names.csv,compare-models.csv}
generated.csv and compare-names.csv/compare-models.csv may be missing (e.g. when
generation or comparison failed) - missing files just leave their columns blank.

Usage:
    python combine_nl2flexmi_results.py [root_dir] [-o output.csv]
"""
import argparse
import csv
from pathlib import Path


def read_single_row_csv(path):
    """Read a one-data-row CSV and return {column: value}, or {} if missing/empty."""
    if not path.is_file():
        return {}
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    return rows[0] if rows else {}


def find_runs(root):
    return sorted(root.glob("*/nl2flexmi/*/generated.csv"))


def main():
    parser = argparse.ArgumentParser(description="Combine nl2flexmi CSV files for each run into a single CSV file.")
    parser.add_argument("root_dir", nargs="?", default=".", help="Directory containing the case folders")
    parser.add_argument("-o", "--output", default="nl2flexmi-combined.csv", help="Output CSV path")
    args = parser.parse_args()

    root = Path(args.root_dir).resolve()
    run_dirs = [p.parent for p in find_runs(root)]

    rows = []
    fieldnames = ["case", "model"]

    for run_dir in run_dirs:
        case = run_dir.parent.parent.name
        model = run_dir.name

        row = {"case": case, "model": model}
        for filename in ("generated.csv", "compare-names.csv", "compare-models.csv"):
            data = read_single_row_csv(run_dir / filename)
            for key in data:
                if key not in fieldnames:
                    fieldnames.append(key)
            row.update(data)

        rows.append(row)

    out_path = Path(args.output)
    with out_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, restval="")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows ({len(fieldnames)} columns) to {out_path}")


if __name__ == "__main__":
    main()
