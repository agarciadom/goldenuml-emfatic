package uk.ac.york.cs.puml2emfatic.cmd;

import org.eclipse.emf.common.util.URI;
import org.eclipse.emf.ecore.EcorePackage;
import org.eclipse.emf.ecore.resource.Resource;
import org.eclipse.emf.ecore.resource.ResourceSet;
import org.eclipse.emf.ecore.resource.impl.ResourceSetImpl;
import org.eclipse.emf.ecore.xmi.impl.EcoreResourceFactoryImpl;
import org.eclipse.emf.emfatic.core.EmfaticResourceFactory;
import picocli.CommandLine;

import java.io.File;
import java.util.Map;
import java.util.concurrent.Callable;

@CommandLine.Command(name="emfatic", description="Converts an Ecore file to Emfatic")
public class EcoreToEmfatic implements Callable<Integer> {

  @CommandLine.Parameters(index = "0")
  private File ecoreFile;

  @Override
  public Integer call() throws Exception {
    EcorePackage.eINSTANCE.getEPackage();

    ResourceSet resourceSet = new ResourceSetImpl();
    Map<String, Object> extMap = resourceSet.getResourceFactoryRegistry().getExtensionToFactoryMap();
    extMap.put("*", new EcoreResourceFactoryImpl());
    extMap.put("emf", new EmfaticResourceFactory());
    Resource ecoreResource = resourceSet.getResource(URI.createFileURI(ecoreFile.getAbsolutePath()), true);

    var emfaticWriter = new org.eclipse.emf.emfatic.core.generator.emfatic.Writer();
    String emfaticSource = emfaticWriter.write(ecoreResource, null, null);
    System.out.println(emfaticSource);

    return 0;
  }

}
