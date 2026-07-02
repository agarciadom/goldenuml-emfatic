package uk.ac.york.cs.puml2emfatic.cmd;

import org.a2aproject.sdk.A2A;
import org.a2aproject.sdk.client.Client;
import org.a2aproject.sdk.client.MessageEvent;
import org.a2aproject.sdk.client.TaskEvent;
import org.a2aproject.sdk.client.TaskUpdateEvent;
import org.a2aproject.sdk.client.http.A2ACardResolver;
import org.a2aproject.sdk.client.transport.jsonrpc.JSONRPCTransport;
import org.a2aproject.sdk.client.transport.jsonrpc.JSONRPCTransportConfig;
import org.a2aproject.sdk.spec.Message;
import org.a2aproject.sdk.spec.TaskArtifactUpdateEvent;
import org.a2aproject.sdk.spec.TaskStatusUpdateEvent;
import picocli.CommandLine;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.util.concurrent.Callable;
import java.util.concurrent.CompletableFuture;
import java.util.stream.Collectors;

@CommandLine.Command(name="a2a-stream", description="Sends a text part to an A2A agent and " +
    "streams the updates")
public class A2AStream implements Callable<Integer> {

  @CommandLine.Option(names={"-b", "--base-url"}, defaultValue = "http://localhost:3000")
  private String baseUrl;

  @CommandLine.Parameters(index = "0")
  private String textOrHyphen;

  @CommandLine.Spec
  private CommandLine.Model.CommandSpec spec;

  @Override
  public Integer call() throws Exception {
    if (textOrHyphen == null) {
      throw new CommandLine.ParameterException(spec.commandLine(),
          "Text or - (for stdin) is required");
    }

    var card = A2ACardResolver.builder()
        .baseUrl(baseUrl)
        .build().getAgentCard();

    var completable = new CompletableFuture<String>();
    var client = Client.builder(card)
        .withTransport(JSONRPCTransport.class, new JSONRPCTransportConfig())
        .addConsumer((event, _card) -> {
          if (event instanceof TaskEvent taskEvent) {
            System.out.println("Received task event: " + taskEvent.getTask());
          }
          else if (event instanceof TaskUpdateEvent taskUpdate) {
            if (taskUpdate.getUpdateEvent() instanceof TaskStatusUpdateEvent taskStatusUpdate) {
              if (taskStatusUpdate.isFinal()) {
                completable.complete("task finalised with status " + taskStatusUpdate.status());
              } else {
                System.out.println("task status: " + taskStatusUpdate.status());
              }
            } else if (taskUpdate.getUpdateEvent() instanceof TaskArtifactUpdateEvent taskArtifactUpdate) {
              System.out.println("artifact update: " + taskArtifactUpdate.artifact());
            }
          } else if (event instanceof MessageEvent message) {
            completable.complete("completed with message: " + message.getMessage().toString());
          }
        })
        .streamingErrorHandler(error -> {
          System.err.println("Error receiving JSON RPC event: " + error);
        })
        .build();

    String text;
    if ("-".equals(textOrHyphen)) {
      text = getStdin();
    } else {
      text = textOrHyphen;
    }

    Message message = A2A.toUserMessage(text);
    client.sendMessage(message);
    System.out.println(completable.get());

    return 0;
  }

  private static String getStdin() {
    BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
    return reader.lines().collect(Collectors.joining("\n"));
  }
}
