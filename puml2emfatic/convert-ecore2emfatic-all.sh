#!/bin/bash

set -e

BASEDIR="$(readlink -f "$(dirname "$0")")"
MODELSET="$(readlink -f "$BASEDIR/../modelset")"

# Ensure the application is built first
"$BASEDIR/gradlew" build

puml2emfatic() {
  java -jar "$BASEDIR"/build/libs/puml2emfatic-*-all.jar "$@"
}

find "$MODELSET" -name converted.ecore -o -name generated.ecore -o -name generated.flexmi | while read ECORE; do
  PUML_DIR="$(dirname "$ECORE")"
  ECORE_FILENAME="$(basename -- "$ECORE")"
  CONVERTED="$PUML_DIR/${ECORE_FILENAME%.*}.emf"
  CONVERSION_STDERR="$PUML_DIR/emfatic-stderr.txt"

  echo -n "Converting ${ECORE} to ${CONVERTED}... "
  if puml2emfatic ecore2emfatic "$ECORE" > "$CONVERTED" 2> "$CONVERSION_STDERR"; then
    echo "success"
    # delete empty stderr files if successful
    if ! test -s "$CONVERSION_STDERR"; then
      rm "$CONVERSION_STDERR"
    fi
  else
    echo "failed (see emfatic-stderr.txt)"
  fi
done
