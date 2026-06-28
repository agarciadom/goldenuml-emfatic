package uk.ac.york.cs.puml2emfatic.cmd;

import dev.langchain4j.memory.chat.MessageWindowChatMemory;
import dev.langchain4j.model.chat.ChatModel;
import dev.langchain4j.model.chat.request.ChatRequestParameters;
import dev.langchain4j.service.AiServices;
import picocli.CommandLine;
import picocli.CommandLine.Command;
import picocli.CommandLine.Parameters;
import uk.ac.york.cs.puml2emfatic.llm.ConverterAssistant;
import uk.ac.york.cs.puml2emfatic.util.EPackageValidator;

import java.io.File;
import java.nio.file.Files;
import java.util.List;

@Command(name="puml2ecore", mixinStandardHelpOptions = true,
    description="Converts PlantUML source code to Ecore XMI using an LLM")
public class PlantUMLToEcore extends LLMCommand {

  @CommandLine.Spec
  CommandLine.Model.CommandSpec spec;

  @Parameters(index="0", description="The PlantUML file to convert.")
  private File plantUmlFile;

  @CommandLine.Option(names={ "-x", "--xmi" }, description="If specified, separates the XMI " +
      "output to this file")
  private File xmiFile;

  @CommandLine.Option(names={ "-r", "--retries"}, description="If greater than 0, retries " +
      "generation that many times using validation feedback")
  private int retries;

  @CommandLine.Option(names={ "--max-output-tokens" }, defaultValue = "32000")
  private int maximumOutputTokens;

  @Override
  public Integer call() throws Exception {
    if (retries < 0) {
      throw new CommandLine.ParameterException(spec.commandLine(), String.format("Invalid value %d for " +
          "retries: must be >= 0", retries));
    }
    if (xmiFile == null) {
      // Use a temporary file instead (for validation)
      xmiFile = File.createTempFile("puml2ecore-", ".xmi");
      xmiFile.deleteOnExit();
    }

    String fileContents = Files.readString(plantUmlFile.toPath());
    ChatModel chatModel = getChatModel();
    ConverterAssistant assistant = AiServices.builder(ConverterAssistant.class)
        .chatModel(chatModel)
        .chatMemory(MessageWindowChatMemory.withMaxMessages(2 * (1 + retries)))
        .build();

    System.out.println("Using model: " + chatModel.defaultRequestParameters().modelName());
    String llmOutput, feedback = null;
    for (int attempt = 0; attempt <= retries; attempt++) {
      if (attempt > 0) {
        System.out.println();
        System.out.printf("# Retry %d%n", 1 + attempt);
        System.out.println();
      } else {
        System.out.printf("# First response%n%n");
      }

      ChatRequestParameters params = ChatRequestParameters.builder()
          .maxOutputTokens(maximumOutputTokens)
          .build();
      if (attempt == 0) {
        llmOutput = assistant.toEcore(fileContents, params);
      } else {
        llmOutput = assistant.retryToEcore(feedback, params);
        feedback = null;
      }
      System.out.println(llmOutput);

      String xmiOutput = extractFirstFencedBlock(llmOutput);
      if (xmiOutput.isEmpty()) {
        feedback = "Could not find a fenced block";
      } else {
        Files.write(xmiFile.toPath(), xmiOutput.getBytes());

        try {
          List<String> diagnostics = new EPackageValidator().validate(xmiFile);
          if (!diagnostics.isEmpty()) {
            feedback = String.join("\n", diagnostics);
          } else {
            System.out.println();
            System.out.println("INFO: XMI output is a valid EPackage");
            break;
          }
        } catch (Exception ex) {
          feedback = String.format("%s: %s", ex.getClass().getName(), ex.getMessage());
        }
      }

      System.out.println();
      System.out.println("Found problems in output:");
      System.out.println(feedback);
    }

    return feedback == null ? 0 : 1;
  }

  public static void main(String... args) {
    int exitCode = new CommandLine(new PlantUMLToEcore()).execute(args);
    System.exit(exitCode);
  }
}
