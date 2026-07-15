#!/bin/bash

set -e

BASEDIR="$(readlink -f "$(dirname "$0")")"
MODELSET="$(readlink -f "$BASEDIR/../modelset")"

# Ensure the application is built first
"$BASEDIR/gradlew" build

puml2emfatic() {
  java -jar "$BASEDIR"/build/libs/puml2emfatic-*-all.jar "$@"
}

find ../modelset -type f ! -empty -name generated.emf | while read GENERATED_MODEL; do
  GMODEL_DIR="$(dirname "$GENERATED_MODEL")"
  RMODEL="$(readlink -f "$GMODEL_DIR/../../converted.ecore")"

  STATS_CMODEL="$GMODEL_DIR/compare-models.csv"
  if test -f "$STATS_CMODEL"; then
    echo "$STATS_CMODEL already exists, skipping"
  else
    echo -n "Model comparison between $GENERATED_MODEL and $RMODEL... "
    CMODEL_STDOUT="$GMODEL_DIR/compare-models-stdout.txt"
    CMODEL_STDERR="$GMODEL_DIR/compare-models-stderr.txt"
    if puml2emfatic compareModels -n -x eOpposite -s "$STATS_CMODEL" "$RMODEL" "$GENERATED_MODEL" 2>"$CMODEL_STDERR" >"$CMODEL_STDOUT"; then
      echo "success"
      if ! test -s "$CMODEL_STDERR"; then
        rm "$CMODEL_STDERR"
      fi
    else
      echo "failed (see $CMODEL_STDERR)"
    fi
  fi

  STATS_CNAMES="$GMODEL_DIR/compare-names.csv"
  if test -f "$STATS_CNAMES"; then
    echo "$STATS_CNAMES already exists, skipping"
  else
    echo -n "Name comparison between $GENERATED_MODEL and $RMODEL... "
    CNAMES_STDOUT="$GMODEL_DIR/compare-names-stdout.txt"
    CNAMES_STDERR="$GMODEL_DIR/compare-names-stderr.txt"
    if puml2emfatic compareNames -s "$STATS_CNAMES" "$RMODEL" "$GENERATED_MODEL" 2>"$CNAMES_STDERR" >"$CNAMES_STDOUT"; then
      echo "success"
      if ! test -s "$CNAMES_STDERR"; then
        rm "$CNAMES_STDERR"
      fi
    else
      echo "failed (see $CNAMES_STDERR)"
    fi
  fi

done