#!/bin/bash

set -e

BASEDIR="$(readlink -f "$(dirname "$0")")"
MODELSET="$(readlink -f "$BASEDIR/../modelset")"

# Ensure the application is built first
"$BASEDIR/gradlew" build

puml2emfatic() {
  java -jar "$BASEDIR"/build/libs/puml2emfatic-*-all.jar "$@"
}

for ECORE in "$MODELSET"/*/converted.ecore; do
  PUML_DIR="$(dirname "$ECORE")"
  CONVERTED="$PUML_DIR/converted.emf"
  CONVERSION_STDERR="$PUML_DIR/emfatic-stderr.txt"

  echo -n "Converting ${ECORE} to Emfatic... "
  if puml2emfatic emfatic "$ECORE" > "$CONVERTED" 2> "$CONVERSION_STDERR"; then
    echo "success"
    if ! test -s "$CONVERSION_STDERR"; then
      # delete empty stderr files if successful
      rm "$CONVERSION_STDERR"
    fi
  else
    echo "failed (see emfatic-stderr.txt)"
  fi
done