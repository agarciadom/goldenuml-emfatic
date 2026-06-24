package uk.ac.york.cs.puml2emfatic.cmd;

import dev.langchain4j.model.chat.ChatModel;
import dev.langchain4j.model.openai.OpenAiChatModel;
import io.github.cdimascio.dotenv.Dotenv;

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
        .maxRetries(Integer.parseInt(dotenv.get("MAX_RETRIES", "3")))
        .modelName(dotenv.get("MODEL_NAME"))
        .build();

    return chatModel;
  }
}
