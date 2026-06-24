package uk.ac.york.cs.puml2emfatic.cmd;

import dev.langchain4j.model.chat.ChatModel;
import dev.langchain4j.service.AiServices;
import picocli.CommandLine;
import picocli.CommandLine.Command;
import picocli.CommandLine.Parameters;
import uk.ac.york.cs.puml2emfatic.llm.ConverterAssistant;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.StringReader;
import java.nio.file.Files;

@Command(name="ecore", mixinStandardHelpOptions = true,
    description="Converts PlantUML source code to Ecore XMI using an LLM")
public class PlantUMLToEcore extends LLMCommand {

  @Parameters(index="0", description="The PlantUML file to convert.")
  private File plantUmlFile;

  @CommandLine.Option(names={ "-x", "--xmi" }, description="If specified, separates the XMI " +
      "output to this file")
  private File xmiFile;

  @Override
  public Integer call() throws Exception {
    String fileContents = Files.readString(plantUmlFile.toPath());
    ChatModel chatModel = getChatModel();

    ConverterAssistant assistant = AiServices.create(ConverterAssistant.class, chatModel);
    String llmOutput = assistant.toEcore(fileContents);

    if (xmiFile != null) {
      String xmiOutput = extractXMI(llmOutput);
      if (!xmiOutput.isEmpty()) {
        Files.write(xmiFile.toPath(), xmiOutput.getBytes());
      }
    }
    System.out.println(llmOutput);
    return 0;
  }

  private String extractXMI(String llmOutput) throws IOException {
    StringBuilder sb = new StringBuilder();
    try (BufferedReader br = new BufferedReader(new StringReader(llmOutput))) {
      String line;
      // Skip ahead until we reach the first fenced block
      while ((line = br.readLine()) != null && !line.startsWith("```"));
      // Append all lines until we reach the end of the fenced block
      while ((line = br.readLine()) != null && !line.startsWith("```")) {
        sb.append(line);
        sb.append(System.lineSeparator());
      }
    }
    return sb.toString();
  }

  public static void main(String... args) {
    int exitCode = new CommandLine(new PlantUMLToEcore()).execute(args);
    System.exit(exitCode);
  }
}
