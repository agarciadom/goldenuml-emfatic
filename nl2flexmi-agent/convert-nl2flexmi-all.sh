#!/bin/bash

set -e

BASEDIR="$(readlink -f "$(dirname "$0")")"
MODELSET="$(readlink -f "$BASEDIR/../modelset")"
source .env

# Ensure dependencies are downloaded first
uv sync

nl2flexmi() {
  uv run main.py "$@"
}

for DESC in "$MODELSET"/*/description.md; do
  PUML_DIR="$(dirname "$DESC")"
  TARGET_DIR="$PUML_DIR/nl2flexmi/$(basename "$MODEL_NAME")"
  mkdir -p "$TARGET_DIR"

  CONVERTED="$TARGET_DIR/generated.flexmi"
  CONVERSION_STATS="$TARGET_DIR/generated.csv"
  CONVERSION_STDOUT="$TARGET_DIR/nl2flexmi-stdout.txt"
  CONVERSION_STDERR="$TARGET_DIR/nl2flexmi-stderr.txt"

  if test -f "$CONVERTED"; then
    echo "$CONVERTED already exists, skipping"
  else
    echo -n "Converting ${DESC} to Ecore Flexmi... "
    if nl2flexmi --stats "$CONVERSION_STATS" "$DESC" "$CONVERTED" > "$CONVERSION_STDOUT" 2> "$CONVERSION_STDERR"; then
      echo "success"
    else
      echo "failed (see $CONVERSION_STDERR)"
    fi
  fi
done