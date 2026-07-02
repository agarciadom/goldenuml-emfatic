#!/bin/bash

set -e

BASEDIR="$(readlink -f "$(dirname "$0")")"
MODELSET="$(readlink -f "$BASEDIR/../modelset")"

# Ensure the application is built first
"$BASEDIR/gradlew" build

puml2emfatic() {
  java -jar "$BASEDIR"/build/libs/puml2emfatic-*-all.jar "$@"
}

for DESC in "$MODELSET"/*/description.md; do
  PUML_DIR="$(dirname "$DESC")"
  TARGET_DIR="$PUML_DIR/a2a-stream/"
  mkdir -p "$TARGET_DIR"

  CONVERTED="$TARGET_DIR/generated.emf"
  CONVERSION_STDOUT="$TARGET_DIR/a2a-stream-stdout.txt"
  CONVERSION_STDERR="$TARGET_DIR/a2a-stream-stderr.txt"

  if test -f "$CONVERTED"; then
    echo "$CONVERTED already exists, skipping"
  else
    echo -n "Converting ${DESC} to Emfatic via MOSAICO agent... "
    if echo -e "Generate an Emfatic metamodel from the domain description below:\n" | cat - "${DESC}" | puml2emfatic a2a-stream --base-url http://localhost:12000 -d "$TARGET_DIR" - > "$CONVERSION_STDOUT" 2> "$CONVERSION_STDERR"; then
      echo "success"
      # delete empty stderr files if successful
      if ! test -s "$CONVERSION_STDERR"; then
        rm "$CONVERSION_STDERR"
      fi
    else
      echo "failed (see $CONVERSION_STDERR)"
    fi
  fi
done