#!/usr/bin/env python3
"""Generate a LaTeX booktabs table summarizing per-model results from a results CSV."""

import argparse
import csv
from pathlib import Path
from statistics import mean


def load_rows(csv_path: Path) -> list[dict]:
    with csv_path.open(newline="") as f:
        return list(csv.DictReader(f))


def token_field_names(fieldnames: list[str]) -> tuple[str, str]:
    if "total_input_tokens" in fieldnames:
        return "total_input_tokens", "total_output_tokens"
    return "input_tokens", "output_tokens"


def summarize(rows: list[dict]) -> dict[str, dict]:
    by_model: dict[str, list[dict]] = {}
    for row in rows:
        by_model.setdefault(row["model"], []).append(row)

    input_field, output_field = token_field_names(rows[0].keys() if rows else [])

    summary = {}
    for model, model_rows in by_model.items():
        input_tokens = [int(r[input_field]) for r in model_rows]
        output_tokens = [int(r[output_field]) for r in model_rows]
        jaccard_rows = [r for r in model_rows if r["set_jaccard"] != ""]
        set_jaccards = [float(r["set_jaccard"]) for r in jaccard_rows]
        multiset_jaccards = [float(r["multiset_jaccard"]) for r in jaccard_rows]

        summary[model] = {
            "avg_input_tokens": mean(input_tokens),
            "avg_output_tokens": mean(output_tokens),
            "num_successful": len(jaccard_rows),
            "avg_set_jaccard": mean(set_jaccards) if set_jaccards else None,
            "avg_multiset_jaccard": mean(multiset_jaccards) if multiset_jaccards else None,
        }
    return summary


def escape_latex(text: str) -> str:
    return text.replace("_", r"\_")


def format_jaccard(value: float | None) -> str:
    return "N/A" if value is None else f"{value:.4f}"


def to_latex(summary: dict[str, dict], dataset: str) -> str:
    lines = [
        r"\begin{table}",
        r"\centering",
        r"\begin{tabular}{lrrrrr}",
        r"\toprule",
        r"LLM & Input & Output & $C$ & $J$ & $J_{\text{multi}}$ \\",
        r"\midrule",
    ]
    for model in sorted(summary):
        s = summary[model]
        lines.append(
            f"{escape_latex(model)} & "
            f"{s['avg_input_tokens']:.2f} & "
            f"{s['avg_output_tokens']:.2f} & "
            f"{s['num_successful']} & "
            f"{format_jaccard(s['avg_set_jaccard'])} & "
            f"{format_jaccard(s['avg_multiset_jaccard'])} \\\\"
        )
    lines += [
        r"\bottomrule",
        r"\end{tabular}",
        rf"\caption{{Summary of \file{{{dataset}}} results by model: mean input and output tokens, number of outputs successfully converted to Emfatic ($C$), and mean Jaccard set ($J$) and multi-set ($J_{{multi}}$) scores.}}",
        rf"\label{{tab:{dataset}-summary}}",
        r"\end{table}",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "csv_path",
        type=Path,
        help="Path to the results CSV file (e.g. nl2ecore.csv or nl2flexmi.csv)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Write the LaTeX table to this file instead of stdout",
    )
    args = parser.parse_args()

    rows = load_rows(args.csv_path)
    summary = summarize(rows)
    table = to_latex(summary, dataset=args.csv_path.stem)

    if args.output:
        args.output.write_text(table + "\n")
    else:
        print(table)


if __name__ == "__main__":
    main()
