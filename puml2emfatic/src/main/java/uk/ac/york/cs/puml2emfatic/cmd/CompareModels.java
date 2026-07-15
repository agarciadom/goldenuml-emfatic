package uk.ac.york.cs.puml2emfatic.cmd;

import org.eclipse.emf.compare.*;
import org.eclipse.emf.compare.scope.DefaultComparisonScope;
import org.eclipse.emf.ecore.resource.Resource;
import picocli.CommandLine;
import uk.ac.york.cs.puml2emfatic.util.DiffFormatter;
import uk.ac.york.cs.puml2emfatic.util.EmfUtilities;

import java.io.*;
import java.util.*;
import java.util.concurrent.Callable;
import java.util.stream.Collectors;

@CommandLine.Command(name="compareModels", description="Compares two models via EMF Compare and " +
    "reports diff counts by type")
public class CompareModels implements Callable<Integer> {

  @CommandLine.Parameters(index="0")
  private File leftModel;

  @CommandLine.Parameters(index="1")
  private File rightModel;

  @CommandLine.Option(names={"-n", "--sort-by-name"},
      description="Sort containment tree by name prior to comparison")
  private boolean sortByName;

  @CommandLine.Option(names={"-x", "--exclude-feature"},
      description="Exclude differences around a specific feature")
  private List<String> excludeFeatures = new ArrayList<>();

  @CommandLine.Option(names={"-s", "--stats"},
      description="Path to the CSV file to be generated with difference counts per kind")
  private File csvFile;

  protected record ComparisonResults(Map<DifferenceKind, List<String>> diffsByType) {
    @Override
    public String toString() {
      if (diffsByType.isEmpty()) {
        return "No differences found.";
      }

      var sb = new StringBuilder();
      for (var entry : diffsByType.entrySet()) {
        if (!sb.isEmpty()) {
          sb.append(System.lineSeparator());
          sb.append(System.lineSeparator());
        }

        sb.append(entry.getKey());
        sb.append(" (");
        sb.append(entry.getValue().size());
        sb.append("):");
        for (String diffDescription : entry.getValue()) {
          sb.append(System.lineSeparator());
          sb.append("  - ");
          sb.append(diffDescription);
        }
      }
      return sb.toString();
    }
  }

  public ComparisonResults compare(Resource rLeft, Resource rRight) throws Exception {
    if (sortByName) {
      EmfUtilities.sortByName(rLeft);
      EmfUtilities.sortByName(rRight);
    }

    var emfCompare = EMFCompare.builder().build();
    var diffScope = new DefaultComparisonScope(rLeft, rRight, null);
    var cmp = emfCompare.compare(diffScope);

    var diffsByType = new EnumMap<DifferenceKind, List<String>>(DifferenceKind.class);
    for (Diff diff : cmp.getDifferences()) {
      var diffsInType = diffsByType.computeIfAbsent(diff.getKind(), (k) -> new ArrayList<String>());
      var included = switch (diff) {
        case AttributeChange attrChange -> !excludeFeatures.contains(attrChange.getAttribute().getName());
        case ReferenceChange refChange -> !excludeFeatures.contains(refChange.getReference().getName());
        default -> true;
      };
      if (included) {
        diffsInType.add(DiffFormatter.format(diff));
      }
    }

    return new ComparisonResults(diffsByType);
  }

  @Override
  public Integer call() throws Exception {
    EmfUtilities.registerResourceFactories();

    Resource leftResource = EmfUtilities.loadModel(leftModel);
    Resource rightResource = EmfUtilities.loadModel(rightModel);

    ComparisonResults results = compare(leftResource, rightResource);
    System.out.println(results);

    if (csvFile != null) {
      writeCSV(results);
    }

    return 0;
  }

  protected void writeCSV(ComparisonResults results) throws IOException {
    try (FileWriter fw = new FileWriter(csvFile); PrintWriter pw = new PrintWriter(fw)) {
      pw.println(Arrays.stream(DifferenceKind.values())
          .map(DifferenceKind::getName)
          .collect(Collectors.joining(",")));
      pw.println(Arrays.stream(DifferenceKind.values())
          .map(k -> results.diffsByType.getOrDefault(k, Collections.emptyList()).size() + "")
          .collect(Collectors.joining(",")));
    }
  }

}
