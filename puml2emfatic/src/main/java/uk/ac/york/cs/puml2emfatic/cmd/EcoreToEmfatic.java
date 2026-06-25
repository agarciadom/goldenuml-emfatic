package uk.ac.york.cs.puml2emfatic.cmd;

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
import picocli.CommandLine;
import uk.ac.york.cs.puml2emfatic.util.EPackageValidator;

import java.io.File;
import java.util.Map;
import java.util.concurrent.Callable;

@CommandLine.Command(name="emfatic", description="Converts an Ecore file to Emfatic")
public class EcoreToEmfatic implements Callable<Integer> {

  @CommandLine.Parameters(index = "0")
  private File ecoreFile;

  @Override
  public Integer call() {
    EcorePackage.eINSTANCE.getEPackage();
    Resource ecoreResource = loadEcore();
    System.out.println(generateEmfatic(ecoreResource));

    var validator = new EPackageValidator();
    var diagnostics = validator.validate((EPackage) ecoreResource.getContents().get(0));
    if (diagnostics.isEmpty()) {
      return 0;
    } else {
      diagnostics.forEach(System.err::println);
      return 1;
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

  protected String generateEmfatic(Resource ecoreResource) {
    var emfaticWriter = new org.eclipse.emf.emfatic.core.generator.emfatic.Writer();
    String emfaticSource = emfaticWriter.write(ecoreResource, null, null);
    return emfaticSource;
  }

  protected Resource loadEcore() {
    ResourceSet resourceSet = new ResourceSetImpl();
    Map<String, Object> extMap = resourceSet.getResourceFactoryRegistry().getExtensionToFactoryMap();
    extMap.put("*", new EcoreResourceFactoryImpl());
    extMap.put("emf", new EmfaticResourceFactory());
    Resource ecoreResource = resourceSet.getResource(URI.createFileURI(ecoreFile.getAbsolutePath()), true);
    return ecoreResource;
  }

}
