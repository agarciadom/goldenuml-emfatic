#!/bin/bash

set -e

BASEDIR="$(readlink -f "$(dirname "$0")")"
MODELSET="$(readlink -f "$BASEDIR/../modelset")"
source .env

# Ensure the application is built first
"$BASEDIR/gradlew" build

puml2emfatic() {
  java -jar "$BASEDIR"/build/libs/puml2emfatic-*-all.jar "$@"
}

for DESC in "$MODELSET"/*/description.md; do
  PUML_DIR="$(dirname "$DESC")"
  TARGET_DIR="$PUML_DIR/nl2ecore/$(basename "$MODEL_NAME")"
  mkdir -p "$TARGET_DIR"

  CONVERTED="$TARGET_DIR/generated.ecore"
  CONVERSION_STDOUT="$TARGET_DIR/nl2ecore-stdout.txt"
  CONVERSION_STDERR="$TARGET_DIR/nl2ecore-stderr.txt"

  echo -n "Converting ${DESC} to Ecore... "
  if puml2emfatic nl2ecore "$DESC" --xmi "$CONVERTED" --retries 2 > "$CONVERSION_STDOUT" 2> "$CONVERSION_STDERR"; then
    echo "success"
    # delete empty stderr files if successful
    if ! test -s "$CONVERSION_STDERR"; then
      rm "$CONVERSION_STDERR"
    fi
  else
    echo "failed (see $CONVERSION_STDERR)"
  fi
done