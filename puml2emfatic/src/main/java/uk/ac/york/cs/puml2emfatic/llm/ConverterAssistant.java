package uk.ac.york.cs.puml2emfatic.llm;

import dev.langchain4j.model.chat.request.ChatRequestParameters;
import dev.langchain4j.service.Result;
import dev.langchain4j.service.UserMessage;
import dev.langchain4j.service.V;

public interface ConverterAssistant {

  @UserMessage(fromResource = "prompts/plantuml-to-ecore.txt")
  String plantUmlToEcore(@V("plantUmlCode") String plantUmlCode, ChatRequestParameters parameters);

  @UserMessage(fromResource = "prompts/domain-to-ecore.txt")
  Result<String> domainToEcore(@V("domainDescription") String domainDescription,
                               ChatRequestParameters parameters);

  @UserMessage(fromResource = "prompts/retry-step.txt")
  Result<String> retryStep(@V("feedback") String feedback, ChatRequestParameters parameters);

}
