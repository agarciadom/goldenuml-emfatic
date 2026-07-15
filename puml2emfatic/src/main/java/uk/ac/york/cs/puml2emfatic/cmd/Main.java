package uk.ac.york.cs.puml2emfatic.cmd;

import picocli.CommandLine;

@CommandLine.Command(
    name="puml2emfatic",
    subcommands={
        A2AStream.class,
        PlantUMLToEcore.class,
        EcoreToEmfatic.class,
        CompareModels.class,
        NaturalLanguageToEcore.class,
    }
)
public class Main {
  public static void main(String[] args) {
    int exitCode = new CommandLine(new Main()).execute(args);
    System.exit(exitCode);
  }
}
