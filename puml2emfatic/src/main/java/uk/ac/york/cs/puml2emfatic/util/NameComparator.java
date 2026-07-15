package uk.ac.york.cs.puml2emfatic.util;

import org.eclipse.emf.ecore.EObject;
import org.eclipse.emf.ecore.EStructuralFeature;

public class NameComparator implements java.util.Comparator<EObject> {

  @Override
  public int compare(EObject o1, EObject o2) {
    EStructuralFeature sfName1 = o1.eClass().getEStructuralFeature("name");
    EStructuralFeature sfName2 = o2.eClass().getEStructuralFeature("name");
    String name1 = sfName1 == null ? null : o1.eGet(sfName1) + "";
    String name2 = sfName2 == null ? null : o2.eGet(sfName2) + "";

    if (name1 != null && name2 != null) {
      return name1.compareTo(name2);
    } else if (name1 == null && name2 == null) {
      return 0;
    } else if (name1 != null) {
      return -1;
    } else {
      return 1;
    }
  }

}
