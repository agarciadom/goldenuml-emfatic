package uk.ac.york.cs.puml2emfatic.util;

import org.eclipse.emf.common.util.Diagnostic;
import org.eclipse.emf.common.util.URI;
import org.eclipse.emf.ecore.EPackage;
import org.eclipse.emf.ecore.resource.Resource;
import org.eclipse.emf.ecore.resource.ResourceSet;
import org.eclipse.emf.ecore.resource.impl.ResourceSetImpl;
import org.eclipse.emf.ecore.util.Diagnostician;
import org.eclipse.emf.ecore.xmi.impl.EcoreResourceFactoryImpl;
import org.eclipse.emf.emfatic.core.EmfaticResourceFactory;

import java.io.File;
import java.util.Collections;
import java.util.List;
import java.util.Map;

public class EPackageValidator {

  public List<String> validate(File ecoreFile) {
      ResourceSet resourceSet = new ResourceSetImpl();
      Map<String, Object> extMap = resourceSet.getResourceFactoryRegistry().getExtensionToFactoryMap();
      extMap.put("*", new EcoreResourceFactoryImpl());
      extMap.put("emf", new EmfaticResourceFactory());
      Resource ecoreResource = resourceSet.getResource(URI.createFileURI(ecoreFile.getAbsolutePath()), true);
      return validate((EPackage) ecoreResource.getContents().get(0));
  }

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
