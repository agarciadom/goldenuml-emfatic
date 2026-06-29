package uk.ac.york.cs.puml2emfatic.cmd;

import dev.langchain4j.model.chat.ChatModel;
import dev.langchain4j.model.openai.OpenAiChatModel;
import io.github.cdimascio.dotenv.Dotenv;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.StringReader;
import java.time.Duration;
import java.util.concurrent.Callable;

public abstract class LLMCommand implements Callable<Integer> {
  protected ChatModel getChatModel() {
    Dotenv dotenv = Dotenv.configure()
        .ignoreIfMalformed()
        .ignoreIfMissing()
        .load();

    ChatModel chatModel = OpenAiChatModel.builder()
        .baseUrl(dotenv.get("API_BASE"))
        .apiKey(dotenv.get("API_KEY"))
        .modelName(dotenv.get("MODEL_NAME"))
        .maxRetries(Integer.parseInt(dotenv.get("MAX_RETRIES", "0")))
        .timeout(Duration.ofSeconds(Integer.parseInt(dotenv.get("TIMEOUT_SECONDS", "30"))))
        .build();

    return chatModel;
  }

  protected String extractFirstFencedBlock(String llmOutput) throws IOException {
    if (llmOutput == null || llmOutput.isEmpty()) return null;

    StringBuilder sb = new StringBuilder();
    try (BufferedReader br = new BufferedReader(new StringReader(llmOutput))) {
      String line;
      // Skip ahead until we reach the first fenced block
      while ((line = br.readLine()) != null && !line.startsWith("```")) {}
      // Append all lines until we reach the end of the fenced block
      while ((line = br.readLine()) != null && !line.startsWith("```")) {
        sb.append(line);
        sb.append(System.lineSeparator());
      }
    }
    return sb.toString();
  }
}
