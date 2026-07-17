#!/usr/bin/env python3
"""Aggregate token counts from nl2ecore-stdout.txt files and other CSVs into the same folder into a joint CSV across all cases."""

import argparse
import csv
import re
from pathlib import Path

TOKEN_RE = re.compile(r"Result after (\d+) input \+ (\d+) output tokens")
COMPARISON_CSVS = ["compare-names.csv", "compare-models.csv"]


def parse_renames(pairs):
    """Parse a list of "old=new" strings into a {old: new} dict."""
    renames = {}
    for pair in pairs or []:
        old, sep, new = pair.partition("=")
        if not sep:
            raise argparse.ArgumentTypeError(f"invalid rename {pair!r}, expected OLD=NEW")
        renames[old] = new
    return renames


def read_comparison_columns(folder):
    """Read the header/value row of each comparison CSV in folder, if present."""
    columns = {}
    for csv_name in COMPARISON_CSVS:
        csv_file = folder / csv_name
        if not csv_file.exists():
            continue
        with csv_file.open(newline="") as f:
            reader = csv.DictReader(f)
            row = next(reader, None)
            if row:
                columns.update(row)
    return columns

def aggregate_results(root, output_csv, renames=None):
    renames = renames or {}
    rows = []
    fieldnames = ["case", "model", "input_tokens", "output_tokens"]
    for txt_file in sorted(root.rglob("nl2ecore-stdout.txt")):
        # Expected layout: <root>/<case>/nl2ecore/<model>/nl2ecore-stdout.txt
        parts = txt_file.relative_to(root).parts
        case = parts[0] if len(parts) >= 1 else "unknown"
        model = parts[2] if len(parts) >= 3 else "unknown"
        model = renames.get(model, model)

        total_input = total_output = 0
        for line in txt_file.read_text(errors="replace").splitlines():
            m = TOKEN_RE.search(line)
            if m:
                total_input += int(m.group(1))
                total_output += int(m.group(2))

        row = {"case": case, "model": model,
            "input_tokens": total_input, "output_tokens": total_output}
        row.update(read_comparison_columns(txt_file.parent))
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
        rows.append(row)

    with output_csv.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows ({len(fieldnames)} columns) to {output_csv}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", type=Path,
                         help="Directory to search for nl2ecore-stdout.txt files (default: current directory)")
    parser.add_argument("-o", "--output", default="nl2ecore-combined.csv", help="Output CSV path", type=Path)
    parser.add_argument("--rename-model", action="append", metavar="OLD=NEW",
                         help="Rename a model in the output (can be repeated), e.g. --rename-model claude-sonnet-latest=claude-sonnet-4.6")
    args = parser.parse_args()
    if args.output is None:
        args.output = args.root / "token_counts.csv"

    aggregate_results(args.root, args.output, renames=parse_renames(args.rename_model))
