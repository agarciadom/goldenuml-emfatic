#!/bin/bash

set -e

BASEDIR="$(readlink -f "$(dirname "$0")")"
MODELSET="$(readlink -f "$BASEDIR/../modelset")"

# Ensure the application is built first
"$BASEDIR/gradlew" build

puml2emfatic() {
  java -jar "$BASEDIR"/build/libs/puml2emfatic-*-all.jar "$@"
}

for PUML in "$MODELSET"/*/plantuml.txt; do
  PUML_DIR="$(dirname "$PUML")"
  CONVERTED="$PUML_DIR/converted.ecore"
  RAW_STDOUT="$PUML_DIR/raw-llm-stdout.txt"
  RAW_STDERR="$PUML_DIR/raw-llm-stderr.txt"

  if test -f "$CONVERTED"; then
    echo "$CONVERTED already exists, skipping"
  else
    echo -n "Converting $(basename "$PUML_DIR")... "
    if puml2emfatic ecore --retries 2 --xmi "${CONVERTED}" "${PUML}" >"$RAW_STDOUT" 2>"$RAW_STDERR"; then
      echo "success"
    else
      echo "failed (see raw-llm-stderr.txt)"
    fi
  fi
done