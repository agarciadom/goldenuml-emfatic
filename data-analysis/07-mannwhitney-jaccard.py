#!/usr/bin/env python3
"""Mann-Whitney U tests comparing Claude Sonnet's Jaccard scores (nl2ecore.csv)
against each local LLM's Jaccard scores (nl2flexmi.csv)."""

import argparse
import csv
import sys
import typing

from pathlib import Path
from statistics import median

from scipy.stats import mannwhitneyu

CLAUDE_MODEL = "claude-sonnet-4.6"
METRICS = ["set_jaccard", "multiset_jaccard"]


def load_rows(csv_path: Path) -> list[dict]:
    with csv_path.open(newline="") as f:
        return list(csv.DictReader(f))


def jaccard_scores(rows: list[dict], model: str, metric: str) -> list[float]:
    return [float(r[metric]) for r in rows if r["model"] == model and r[metric] != ""]


def local_models(rows: list[dict]) -> list[str]:
    return sorted({r["model"] for r in rows})


def run_tests(ecore_rows: list[dict], flexmi_rows: list[dict]) -> list[dict]:
    results = []
    for metric in METRICS:
        claude_scores = jaccard_scores(ecore_rows, CLAUDE_MODEL, metric)
        for model in local_models(flexmi_rows):
            local_scores = jaccard_scores(flexmi_rows, model, metric)
            u_stat, p_value = mannwhitneyu(
                claude_scores, local_scores, alternative="two-sided"
            )
            results.append(
                {
                    "metric": metric,
                    "model": model,
                    "n_claude": len(claude_scores),
                    "n_local": len(local_scores),
                    "median_claude": median(claude_scores),
                    "median_local": median(local_scores),
                    "u_statistic": u_stat,
                    "p_value": p_value,
                }
            )
    return results


def print_results(results: list[dict], alpha: float, out_file: typing.TextIO = sys.stdout) -> None:
    header = (
        f"{'metric':<16} {'model':<16} {'n_claude':>8} {'n_local':>8} "
        f"{'med_claude':>10} {'med_local':>10} {'U':>10} {'p_value':>10}  significant"
    )
    print(header, file=out_file)
    print("-" * len(header), file=out_file)
    for r in results:
        sig = "yes" if r["p_value"] < alpha else "no"
        print(
            f"{r['metric']:<16} {r['model']:<16} {r['n_claude']:>8} {r['n_local']:>8} "
            f"{r['median_claude']:>10.4f} {r['median_local']:>10.4f} "
            f"{r['u_statistic']:>10.1f} {r['p_value']:>10.4f}  {sig} (alpha={alpha})",
            file=out_file
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--nl2ecore", type=Path, default=Path("nl2ecore.csv"),
        help="Path to nl2ecore.csv (default: nl2ecore.csv)",
    )
    parser.add_argument(
        "--nl2flexmi", type=Path, default=Path("nl2flexmi.csv"),
        help="Path to nl2flexmi.csv (default: nl2flexmi.csv)",
    )
    parser.add_argument(
        "--alpha", type=float, default=0.05,
        help="Significance level (default: 0.05)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Write the table to this file instead of stdout"
    )
    args = parser.parse_args()

    ecore_rows = load_rows(args.nl2ecore)
    flexmi_rows = load_rows(args.nl2flexmi)

    results = run_tests(ecore_rows, flexmi_rows)
    if args.output:
        with args.output.open('w') as f:
            print_results(results, args.alpha, out_file=f)
    else:
        print_results(results, args.alpha)


if __name__ == "__main__":
    main()
