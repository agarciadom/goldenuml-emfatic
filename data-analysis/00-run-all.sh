#!/bin/bash

# Runs all the data analysis scripts in sequence.

set -e

uv sync
uv run 01-nl2ecore.py ../modelset -o nl2ecore.csv
uv run 02-nl2flexmi.py ../modelset -o nl2flexmi.csv
uv run 03-violin-jaccard.py
uv run 04-violin-input_tokens.py
uv run 05-violin-output_tokens.py
uv run 06-summary-table.py nl2ecore.csv -o nl2ecore-summary.tex
uv run 06-summary-table.py nl2flexmi.csv -o nl2flexmi-summary.tex
