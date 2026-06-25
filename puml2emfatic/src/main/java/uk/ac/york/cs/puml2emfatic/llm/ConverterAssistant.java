package uk.ac.york.cs.puml2emfatic.llm;

import dev.langchain4j.service.UserMessage;
import dev.langchain4j.service.V;

public interface ConverterAssistant {

  @UserMessage(fromResource = "prompts/plantuml-to-ecore.txt")
  String toEcore(@V("plantUmlCode") String plantUmlCode);

  @UserMessage(fromResource = "prompts/plantuml-to-ecore-retry.txt")
  String retryToEcore(@V("feedback") String feedback);

}
