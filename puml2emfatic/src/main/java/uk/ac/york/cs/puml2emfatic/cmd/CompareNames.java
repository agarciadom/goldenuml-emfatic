package uk.ac.york.cs.puml2emfatic.cmd;

import org.eclipse.emf.ecore.ENamedElement;
import org.eclipse.emf.ecore.EObject;
import org.eclipse.emf.ecore.resource.Resource;
import picocli.CommandLine;
import uk.ac.york.cs.puml2emfatic.util.EmfUtilities;

import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;
import java.util.concurrent.Callable;

@CommandLine.Command(name = "compareNames",
    description = "Computes Jaccard distances between the sets and multisets of the names in the " +
        "model, ignoring case")
public class CompareNames implements Callable<Integer> {

  @CommandLine.Parameters(index = "0", description="Left model to be compared")
  private File leftModel;

  @CommandLine.Parameters(index = "1", description="Right model to be compared")
  private File rightModel;

  @CommandLine.Option(names={"-s", "--stats"}, description="CSV file to be generated with the " +
      "results")
  private File csvFile;

  protected static Map<String, Integer> getNameCounts(Resource r) {
    var namesByLevel = new TreeMap<String, Integer>();
    for (var eob : r.getContents()) {
      addNames(namesByLevel, eob);
    }
    return namesByLevel;
  }

  protected static void addNames(Map<String, Integer> nameCounts, EObject eob) {
    String name = null;
    if (eob instanceof ENamedElement named) {
      name = named.getName();
    } else {
      var sf = eob.eClass().getEStructuralFeature("name");
      if (sf != null && eob.eIsSet(sf)) {
        name = eob.eGet(sf) + "";
      }
    }

    if (name != null) {
      nameCounts.compute(name.toLowerCase(), (k, v) -> v == null ? 1 : v + 1);
    }
    for (EObject child : eob.eContents()) {
      addNames(nameCounts, child);
    }
  }

  protected double computeSetJaccard(Set<String> left, Set<String> right) {
    TreeSet<String> intersection = new TreeSet<>(left);
    intersection.retainAll(right);

    TreeSet<String> union = new TreeSet<>(left);
    union.addAll(right);

    return (double)intersection.size() / union.size();
  }

  protected double computeMultisetJaccard(Map<String, Integer> left, Map<String, Integer> right) {
    TreeSet<String> union = new TreeSet<>(left.keySet());
    union.addAll(right.keySet());

    int totalMin = 0, totalMax = 0;
    for (String name : union) {
      int leftCount = left.getOrDefault(name, 0);
      int rightCount = right.getOrDefault(name, 0);
      totalMin += Math.min(leftCount, rightCount);
      totalMax += Math.max(leftCount, rightCount);
    }

    return (double)totalMin / totalMax;
  }

  @Override
  public Integer call() throws Exception {
    EmfUtilities.registerResourceFactories();

    Resource rLeft = EmfUtilities.loadModel(this.leftModel);
    Resource rRight = EmfUtilities.loadModel(this.rightModel);

    var namesLeft = getNameCounts(rLeft);
    var namesRight = getNameCounts(rRight);

    double setJaccard = computeSetJaccard(namesLeft.keySet(), namesRight.keySet());
    double multiSetJaccard = computeMultisetJaccard(namesLeft, namesRight);

    System.out.println("Set Jaccard distance = " + setJaccard);
    System.out.println("Multiset Jaccard distance = " + multiSetJaccard);
    if (csvFile != null) {
      try (FileWriter fw = new FileWriter(csvFile); PrintWriter pw = new PrintWriter(fw)) {
        pw.println("set_jaccard,multiset_jaccard");
        pw.printf("%f,%f%n", setJaccard, multiSetJaccard);
      }
    }

    return 0;
  }
}
