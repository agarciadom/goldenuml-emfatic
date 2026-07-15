package uk.ac.york.cs.puml2emfatic.util;

import org.eclipse.emf.common.util.Diagnostic;
import org.eclipse.emf.common.util.URI;
import org.eclipse.emf.ecore.EPackage;
import org.eclipse.emf.ecore.EcorePackage;
import org.eclipse.emf.ecore.resource.Resource;
import org.eclipse.emf.ecore.resource.ResourceSet;
import org.eclipse.emf.ecore.resource.impl.ResourceSetImpl;
import org.eclipse.emf.ecore.util.Diagnostician;
import org.eclipse.emf.ecore.xmi.impl.EcoreResourceFactoryImpl;
import org.eclipse.emf.emfatic.core.EmfaticResourceFactory;
import org.eclipse.epsilon.emc.emf.InMemoryEmfModel;
import org.eclipse.epsilon.evl.EvlModule;
import org.eclipse.epsilon.evl.execute.UnsatisfiedConstraint;
import org.eclipse.epsilon.flexmi.FlexmiResourceFactory;

import java.io.File;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;

public class EPackageValidator {

  private final boolean runEVL;

  public EPackageValidator(boolean runEVL) {
    this.runEVL = runEVL;
  }
  
  public List<String> validate(File ecoreFile) {
      Resource ecoreResource = EmfUtilities.loadModel(ecoreFile);
      return validate((EPackage) ecoreResource.getContents().get(0));
  }

  public List<String> validate(EPackage ePackage) {
    List<String> results = new ArrayList<>(validateBuiltIn(ePackage));
    if (runEVL) {
      results.addAll(validateEVL(ePackage));
    }
    return results;
  }

  protected List<String> validateBuiltIn(EPackage ePackage) {
    var diagnostician = new Diagnostician();
    var diagnostic = diagnostician.validate(ePackage);
    if (diagnostic.getSeverity() == Diagnostic.OK) {
      return Collections.emptyList();
    }
    return diagnostic.getChildren().stream()
        .map(d -> String.format("%s: %s", formatSeverity(d.getSeverity()), d.getMessage()))
        .toList();
  }

  protected List<String> validateEVL(EPackage ePackage) {
    var inMemory = new InMemoryEmfModel("Model", ePackage.eResource(), EcorePackage.eINSTANCE);

    var evlProgram = new EvlModule();
    try {
      evlProgram.parse(getClass().getResource("/evl/ecore.evl"));
      evlProgram.getContext().getModelRepository().addModel(inMemory);
      evlProgram.execute();

      var results = new ArrayList<String>();
      for (UnsatisfiedConstraint unsatisfiedConstraint : evlProgram.getContext().getUnsatisfiedConstraints()) {
        results.add(String.format("%s: %s",
            unsatisfiedConstraint.getConstraint().isCritique() ? "WARNING" : "ERROR",
            unsatisfiedConstraint.getMessage()));
      }
      return results;
    } catch (Exception e) {
      throw new RuntimeException(e);
    } finally {
      evlProgram.getContext().getModelRepository().dispose();
      evlProgram.getContext().dispose();
    }
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
