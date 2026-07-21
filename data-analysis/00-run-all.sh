#!/bin/bash

# Runs all the data analysis scripts in sequence.

set -e

# Set up the local Python environment
uv sync

# Collate data from the modelset folders into CSVs
uv run 01-nl2ecore.py ../modelset -o nl2ecore.csv --rename-model claude-sonnet-latest=claude-sonnet-4.6
uv run 02-nl2flexmi.py ../modelset -o nl2flexmi.csv

# Extract figures and summary tables
uv run 03-violin-jaccard.py
uv run 04-violin-input_tokens.py
uv run 05-violin-output_tokens.py
uv run 06-summary-table.py nl2ecore.csv -o nl2ecore-summary.tex
uv run 06-summary-table.py nl2flexmi.csv -o nl2flexmi-summary.tex

# Statistical significance tests
uv run 07-mannwhitney-jaccard.py -o mann-whitney.txt
