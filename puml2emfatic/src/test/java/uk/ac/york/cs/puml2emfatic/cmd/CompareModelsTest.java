package uk.ac.york.cs.puml2emfatic.cmd;

import org.eclipse.emf.common.util.URI;
import org.eclipse.emf.compare.CompareFactory;
import org.eclipse.emf.compare.DifferenceKind;
import org.eclipse.emf.compare.DifferenceSource;
import org.eclipse.emf.ecore.EClass;
import org.eclipse.emf.ecore.EPackage;
import org.eclipse.emf.ecore.EcoreFactory;
import org.eclipse.emf.ecore.EcorePackage;
import org.eclipse.emf.ecore.resource.Resource;
import org.eclipse.emf.ecore.resource.impl.ResourceSetImpl;
import org.eclipse.emf.ecore.xmi.impl.EcoreResourceFactoryImpl;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class CompareModelsTest {

  @Test
  void compareProducesHumanFriendlyAttributeDescriptions() throws Exception {
    var resourceSet = new ResourceSetImpl();
    resourceSet.getResourceFactoryRegistry().getExtensionToFactoryMap()
        .put("ecore", new EcoreResourceFactoryImpl());

    Resource left = resourceSet.createResource(URI.createURI("left.ecore"));
    Resource right = resourceSet.createResource(URI.createURI("right.ecore"));
    left.getContents().add(createPackage(false));
    right.getContents().add(createPackage(true));

    var results = new CompareModels().compare(left, right);
    List<String> changes = results.diffsByType().get(DifferenceKind.CHANGE);

    assertNotNull(changes);
    assertTrue(changes.stream().anyMatch(change ->
        change.equals("Changed attribute 'abstract' on EClass 'Customer' to false (source: left model)")));
    assertTrue(changes.stream().noneMatch(change -> change.contains("AttributeChange")));
  }

  @Test
  void identicalCompareProducesNoDifferences() throws Exception {
    var resourceSet = new ResourceSetImpl();
    resourceSet.getResourceFactoryRegistry().getExtensionToFactoryMap()
        .put("ecore", new EcoreResourceFactoryImpl());

    Resource left = resourceSet.createResource(URI.createURI("left.ecore"));
    Resource right = resourceSet.createResource(URI.createURI("right.ecore"));
    left.getContents().add(createPackage(false));
    right.getContents().add(createPackage(false));

    var results = new CompareModels().compare(left, right);
    assertEquals(0, results.diffsByType().size());
  }

  private EPackage createPackage(boolean customerAbstract) {
    EPackage ePackage = EcoreFactory.eINSTANCE.createEPackage();
    ePackage.setName("shop");
    ePackage.setNsPrefix("shop");
    ePackage.setNsURI("http://example.com/shop");

    EClass customer = EcoreFactory.eINSTANCE.createEClass();
    customer.setName("Customer");
    customer.setAbstract(customerAbstract);
    ePackage.getEClassifiers().add(customer);

    return ePackage;
  }
}
