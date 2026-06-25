package uk.ac.york.cs.puml2emfatic.util;

import org.eclipse.emf.common.util.Diagnostic;
import org.eclipse.emf.ecore.EPackage;
import org.eclipse.emf.ecore.util.Diagnostician;

import java.util.Collections;
import java.util.List;

public class EPackageValidator {

  public List<String> validate(EPackage ePackage) {
    var diagnostician = new Diagnostician();
    var diagnostic = diagnostician.validate(ePackage);
    if (diagnostic.getSeverity() == Diagnostic.OK) {
      return Collections.emptyList();
    }

    return diagnostic.getChildren().stream()
        .map(d -> String.format("%s: %s", formatSeverity(d.getSeverity()), d.getMessage()))
        .toList();
  }

  protected String formatSeverity(int severity) {
    if (severity < Diagnostic.WARNING) {
      return "INFO";
    } else if (severity < Diagnostic.ERROR) {
      return "WARNING";
    } else {
      return "ERROR";
    }
  }

}
