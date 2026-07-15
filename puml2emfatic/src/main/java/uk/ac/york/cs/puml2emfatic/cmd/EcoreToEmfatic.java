package uk.ac.york.cs.puml2emfatic.cmd;

import org.eclipse.emf.common.util.URI;
import org.eclipse.emf.ecore.EPackage;
import org.eclipse.emf.ecore.EcorePackage;
import org.eclipse.emf.ecore.resource.Resource;
import org.eclipse.emf.ecore.resource.ResourceSet;
import org.eclipse.emf.ecore.resource.impl.ResourceSetImpl;
import org.eclipse.emf.ecore.xmi.impl.EcoreResourceFactoryImpl;
import org.eclipse.emf.ecore.xmi.impl.XMIResourceFactoryImpl;
import org.eclipse.emf.emfatic.core.EmfaticResourceFactory;
import org.eclipse.epsilon.flexmi.FlexmiResourceFactory;
import picocli.CommandLine;
import uk.ac.york.cs.puml2emfatic.util.EPackageValidator;
import uk.ac.york.cs.puml2emfatic.util.EmfUtilities;

import java.io.File;
import java.util.Map;
import java.util.concurrent.Callable;

@CommandLine.Command(name="ecore2emfatic", description="Validates and converts an Ecore file to " +
    "Emfatic")
public class EcoreToEmfatic implements Callable<Integer> {

  @CommandLine.Parameters(index = "0")
  private File ecoreFile;

  @CommandLine.Option(names={ "-V", "--run-evl" }, description="If specified, also runs the " +
      "additional LLM-oriented EVL rules on the input metamodel before doing the conversion")
  private boolean runEvl;

  @Override
  public Integer call() {
    EmfUtilities.registerResourceFactories();
    Resource ecoreResource = EmfUtilities.loadModel(ecoreFile);

    var validator = new EPackageValidator(runEvl);
    var diagnostics = validator.validate((EPackage) ecoreResource.getContents().getFirst());
    if (diagnostics.isEmpty()) {
      System.out.println(generateEmfatic(ecoreResource));
      return 0;
    } else {
      diagnostics.forEach(System.err::println);
      return 1;
    }
  }

  protected String generateEmfatic(Resource ecoreResource) {
    var emfaticWriter = new org.eclipse.emf.emfatic.core.generator.emfatic.Writer();
    return emfaticWriter.write(ecoreResource, null, null);
  }


}
