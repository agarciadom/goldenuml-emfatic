# goldenuml-emfatic

This repository extends the Golden UML ModelSet with Ecore metamodels and their [Emfatic](https://eclipse.dev/emfatic/) equivalents.

The Golden UML ModelSet is available from Zenodo:

* C. Verbruggen et al., “Golden UML Modelset”. Zenodo, Aug. 28, 2025. doi: [10.5281/zenodo.16985873](https://doi.org/10.5281/zenodo.16985873).

## Repository structure

* `modelset`: Local copy of the ModelSet, extended with Ecore metamodels initially derived from the PlantUML descriptions using an LLM (currently, Claude Sonnet 4.6) and then manually checked and cleaned up.
* `puml2emfatic`: Java application automating the LLM-driven conversion of PlantUML to Ecore, and the deterministic conversion of Ecore to Emfatic.

## Building and running puml2emfatic

First, build the all-in-one JAR:

```shell
cd puml2emfatic
./gradlew build
```

You can then list available subcommands for the tool with:

```shell
java -jar build/libs/puml2emfatic-*-all.jar
```

To see specific help on a subcommand, use `--help`.
For example, for the `ecore` subcommand:

```shell
java -jar build/libs/puml2emfatic-*-all.jar ecore --help
```

Note that if you use a command that is based on an LLM, you will need to copy and customise the `.env.template` file:

```shell
cd puml2emfatic
cp .env.template .env
# customise .env as appropriate
```

## Batch rerun the conversion

First, delete the `converted.ecore` files.
The following command deletes them all - you can delete only some (conversion will be skipped for existing files):

```shell
find modelset -name converted.ecore -delete
```

Then, run the convenience script inside `puml2emfatic`:

```shell
cd puml2emfatic
./convert-ecore-all.sh
```
