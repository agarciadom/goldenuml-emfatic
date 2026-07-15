package uk.ac.york.cs.puml2emfatic.util;

import org.eclipse.emf.common.util.ECollections;
import org.eclipse.emf.common.util.EList;
import org.eclipse.emf.common.util.URI;
import org.eclipse.emf.ecore.EObject;
import org.eclipse.emf.ecore.EStructuralFeature;
import org.eclipse.emf.ecore.resource.Resource;
import org.eclipse.emf.ecore.resource.ResourceSet;
import org.eclipse.emf.ecore.resource.impl.ResourceSetImpl;
import org.eclipse.emf.ecore.xmi.impl.EcoreResourceFactoryImpl;
import org.eclipse.emf.ecore.xmi.impl.XMIResourceFactoryImpl;
import org.eclipse.emf.emfatic.core.EmfaticResourceFactory;
import org.eclipse.epsilon.flexmi.FlexmiResourceFactory;

import java.io.File;
import java.util.Map;

public class EmfUtilities {
  private EmfUtilities() {}

  public static void registerResourceFactories() {
    Map<String, Object> extMap = Resource.Factory.Registry.INSTANCE.getExtensionToFactoryMap();
    extMap.put("*", new XMIResourceFactoryImpl());
    extMap.put("ecore", new EcoreResourceFactoryImpl());
    extMap.put("flexmi", new FlexmiResourceFactory());
    extMap.put("emf", new EmfaticResourceFactory());
  }

  public static Resource loadModel(File fModel) {
    ResourceSet resourceSet = new ResourceSetImpl();
    return resourceSet.getResource(URI.createFileURI(fModel.getAbsolutePath()), true);
  }

  public static void sortByName(Resource r) {
    var cmp = new NameComparator();
    ECollections.sort(r.getContents(), cmp);
    for (EObject child : r.getContents()) {
      sortByName(child, cmp);
    }
  }

  @SuppressWarnings("unchecked")
  protected static void sortByName(EObject child, NameComparator cmp) {
    for (EStructuralFeature feature : child.eClass().getEStructuralFeatures()) {
      if (feature.isMany()) {
        ECollections.sort((EList<EObject>) child.eGet(feature), cmp);
      }
    }
  }
}
