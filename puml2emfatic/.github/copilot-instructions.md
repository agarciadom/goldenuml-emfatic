# Copilot Instructions

## Build and test commands

- Use **Java 21** for Gradle work. The build declares a Java 21 toolchain in `build.gradle`, and the wrapper currently fails under JDK 25 during build-script compilation.
- Full build: `./gradlew build`
- Package the runnable uberjar used by the helper scripts: `./gradlew shadowJar`
- Run the test suite: `./gradlew test`
- Run one test class: `./gradlew test --tests 'fully.qualified.ClassName'`
- Run one test method: `./gradlew test --tests 'fully.qualified.ClassName.methodName'`
- There is no dedicated lint task configured in Gradle.

## High-level architecture

- This is a Picocli-based CLI application. `uk.ac.york.cs.puml2emfatic.cmd.Main` registers the subcommands and delegates all execution through command classes in `src/main/java/uk/ac/york/cs/puml2emfatic/cmd/`.
- There are two LLM-driven conversion paths:
  - `puml2ecore` reads PlantUML and asks the LangChain4j `ConverterAssistant` to generate Ecore XMI.
  - `nl2ecore` does the same from a Markdown domain description.
- Both LLM commands inherit from `LLMCommand`, which centralizes `.env`-driven model configuration (`API_BASE`, `API_KEY`, `MODEL_NAME`, `MAX_RETRIES`, `TIMEOUT_SECONDS`) and fenced-block extraction. They both use the same retry loop pattern: generate XMI, write it to a file, validate it, and if validation fails, feed the diagnostics back through the retry prompt.
- Validation is layered. `EPackageValidator` always runs EMF `Diagnostician` validation, and optionally runs the EVL rules from `src/main/resources/evl/ecore.evl` for extra metamodel constraints that are important to downstream LLM workflows.
- `ecore2emfatic` is the non-LLM conversion step: it loads an Ecore/XMI model, validates it, and renders Emfatic text with the EMFatic writer.
- `compareModels` uses EMF Compare to group model differences by `DifferenceKind`.
- `a2a-stream` is a separate integration path for external A2A agents. It streams task updates, prints text/data artifacts, and saves file artifacts into the requested base directory.
- `EmfUtilities` is the shared EMF bootstrap layer. Commands that load models are expected to register resource factories first so `.ecore`, `.emf`, `.flexmi`, and generic XMI resources all resolve consistently.
- The `convert-*.sh` scripts are batch wrappers around the shaded jar. They assume a sibling `../modelset` directory, build first, then run the CLI over files such as `description.md`, `plantuml.txt`, `generated.ecore`, and `converted.ecore`, writing outputs beside the source models.

## Key conventions

- Reuse the existing command split instead of mixing concerns: CLI parsing stays in `cmd/*`, LLM prompt contracts stay in `llm/ConverterAssistant`, and EMF/model helpers stay in `util/*`.
- For any command that loads EMF resources, call `EmfUtilities.registerResourceFactories()` before `loadModel(...)`. The code relies on that registration rather than per-command resource setup.
- Keep prompt text in `src/main/resources/prompts/*.txt` and bind it through `@UserMessage(fromResource = ...)` on `ConverterAssistant`; prompt content is not embedded inline in command classes.
- The retry flow is validator-driven, not heuristic. `puml2ecore` and `nl2ecore` only retry by passing concrete validation feedback through `retry-step.txt`.
- Prompt outputs are expected to contain the generated XMI inside the first fenced Markdown block. `LLMCommand.extractFirstFencedBlock(...)` is the shared contract that downstream code depends on.
- Validation rules are intentionally stricter than plain EMF loading. The prompt resources and EVL rules both enforce repository-specific metamodel expectations such as a single root container and containment consistency, so changes to prompts and validation should stay aligned.
