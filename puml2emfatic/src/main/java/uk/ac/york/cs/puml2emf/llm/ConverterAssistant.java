package uk.ac.york.cs.puml2emf.llm;

import dev.langchain4j.service.UserMessage;
import dev.langchain4j.service.V;

public interface ConverterAssistant {

  @UserMessage(fromResource = "prompts/plantuml-to-ecore.txt")
  String toEcore(@V("plantUmlCode") String plantUmlCode);

}
