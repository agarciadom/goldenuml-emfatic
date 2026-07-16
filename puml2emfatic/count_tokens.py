#!/usr/bin/env python3
"""Aggregate token counts from nl2ecore-stdout.txt files into a CSV."""

import csv
import re
import sys
from pathlib import Path

TOKEN_RE = re.compile(r"Result after (\d+) input \+ (\d+) output tokens")

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
output_csv = Path(sys.argv[2]) if len(sys.argv) > 2 else root / "token_counts.csv"

rows = []
for txt_file in sorted(root.rglob("nl2ecore-stdout.txt")):
    # Expected layout: <root>/<case>/nl2ecore/<model>/nl2ecore-stdout.txt
    parts = txt_file.relative_to(root).parts
    case = parts[0] if len(parts) >= 1 else "unknown"
    model = parts[2] if len(parts) >= 3 else "unknown"

    total_input = total_output = 0
    for line in txt_file.read_text(errors="replace").splitlines():
        m = TOKEN_RE.search(line)
        if m:
            total_input += int(m.group(1))
            total_output += int(m.group(2))

    rows.append({"case": case, "model": model,
                 "input_tokens": total_input, "output_tokens": total_output})

with output_csv.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["case", "model", "input_tokens", "output_tokens"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Written {len(rows)} rows to {output_csv}")
