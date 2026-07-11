package uk.ac.york.agentgen;

import java.io.File;

import org.eclipse.emf.common.util.URI;
import org.eclipse.emf.ecore.EPackage;
import org.eclipse.emf.ecore.resource.Resource;
import org.eclipse.emf.ecore.resource.ResourceSet;
import org.eclipse.emf.ecore.resource.impl.ResourceSetImpl;
import org.eclipse.emf.emfatic.core.EmfaticResourceFactory;
import org.eclipse.epsilon.egl.EgxModule;
import org.eclipse.epsilon.emc.emf.EmfModel;
import org.eclipse.epsilon.flexmi.FlexmiResourceFactory;

public class AgentGenerator {

    public void generateAgentTools(File inputModel, File outputFolder) throws Exception {
      // Register the Flexmi and Emfatic parsers with EMF
      Resource.Factory.Registry.INSTANCE.getExtensionToFactoryMap().put("flexmi", new FlexmiResourceFactory());
      Resource.Factory.Registry.INSTANCE.getExtensionToFactoryMap().put("emf", new EmfaticResourceFactory());

      // Load the EPackage from the Emfatic metamodel
      ResourceSet rsMetamodel = new ResourceSetImpl();
      URI metamodelResourceURI = URI.createURI(AgentGenerator.class.getResource(
          "metamodel.emf").toURI().toString());
      Resource rMetamodel = rsMetamodel.getResource(metamodelResourceURI, true);
      EPackage ePackage = (EPackage)rMetamodel.getContents().get(0);
      EPackage.Registry.INSTANCE.put(ePackage.getNsURI(), ePackage);

      // Parse the EGX transformation and configure it to produce
      // its output files in the target directory
      EgxModule module = new EgxModule(outputFolder.getCanonicalPath());
      module.parse(AgentGenerator.class.getResource("program.egx"));

      // Load the model from model.flexmi using metamodel.emf as its metamodel
      EmfModel model = new EmfModel();
      model.setName("M");
      model.setModelFile(inputModel.getCanonicalPath());
      model.setMetamodelUri(ePackage.getNsURI());
      model.setReadOnLoad(true);
      model.setStoredOnDisposal(false);
      model.load();

      // Make the model available to the transformation
      module.getContext().getModelRepository().addModel(model);

      // Execute the EGX transformation
      module.execute();

      // Dispose of the model
      module.getContext().getModelRepository().dispose();
    }

    public static void main(String[] args) throws Exception {
      if (args.length != 2) {
        System.err.println("Usage: AgentGenerator <input-model> <output-folder>");
        System.exit(1);
      }

      File fInputModel = new File(args[0]);
      if (!fInputModel.exists() || !fInputModel.canRead()) {
        System.err.println("Input model does not exist or cannot be read: " + fInputModel.getAbsolutePath());
        System.exit(2);
      } else if (!fInputModel.isFile()) {
        System.err.println("Input model must be a file: " + fInputModel.getAbsolutePath());
        System.exit(3);
      }

      File outputFolder = new File(args[1]);
      if (!outputFolder.exists()) {
        outputFolder.mkdirs();
      } else if (!outputFolder.isDirectory()) {
        System.err.println("Output folder must be a directory: " + outputFolder.getAbsolutePath());
        System.exit(4);
      }

      new AgentGenerator().generateAgentTools(fInputModel, outputFolder);
    }
}