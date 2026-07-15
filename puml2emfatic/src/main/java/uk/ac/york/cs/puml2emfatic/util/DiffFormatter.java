package uk.ac.york.cs.puml2emfatic.util;

import org.eclipse.emf.compare.*;
import org.eclipse.emf.ecore.EAttribute;
import org.eclipse.emf.ecore.ENamedElement;
import org.eclipse.emf.ecore.EObject;

public class DiffFormatter {

  private DiffFormatter() { }

  public static String format(Diff diff) {
    return switch (diff) {
      case AttributeChange attributeChange -> describeAttributeChange(attributeChange);
      case ReferenceChange referenceChange -> describeReferenceChange(referenceChange);
      case ResourceAttachmentChange attachmentChange ->
          describeResourceAttachmentChange(attachmentChange);
      default -> String.format("%s %s on %s%s",
          capitalize(diff.getKind().getLiteral()),
          diff.eClass().getName(),
          describeMatchObject(diff.getMatch(), diff.getSource()),
          describeSourceSuffix(diff.getSource()));
    };
  }

  private static String describeAttributeChange(AttributeChange diff) {
    String owner = describeMatchObject(diff.getMatch(), diff.getSource());
    String attributeName = diff.getAttribute().getName();
    String value = describeValue(diff.getValue());

    return switch (diff.getKind()) {
      case ADD -> String.format("Added %s to attribute '%s' on %s%s",
          value, attributeName, owner, describeSourceSuffix(diff.getSource()));
      case DELETE -> String.format("Removed %s from attribute '%s' on %s%s",
          value, attributeName, owner, describeSourceSuffix(diff.getSource()));
      case CHANGE -> String.format("Changed attribute '%s' on %s to %s%s",
          attributeName, owner, value, describeSourceSuffix(diff.getSource()));
      case MOVE -> String.format("Moved %s within attribute '%s' on %s%s",
          value, attributeName, owner, describeSourceSuffix(diff.getSource()));
    };
  }

  private static String describeReferenceChange(ReferenceChange diff) {
    String owner = describeMatchObject(diff.getMatch(), diff.getSource());
    String referenceName = diff.getReference().getName();
    String value = describeValue(diff.getValue());

    return switch (diff.getKind()) {
      case ADD -> String.format("Added %s to reference '%s' on %s%s",
          value, referenceName, owner, describeSourceSuffix(diff.getSource()));
      case DELETE -> String.format("Removed %s from reference '%s' on %s%s",
          value, referenceName, owner, describeSourceSuffix(diff.getSource()));
      case CHANGE -> String.format("Changed reference '%s' on %s to %s%s",
          referenceName, owner, value, describeSourceSuffix(diff.getSource()));
      case MOVE -> String.format("Moved %s within reference '%s' on %s%s",
          value, referenceName, owner, describeSourceSuffix(diff.getSource()));
    };
  }

  private static String describeResourceAttachmentChange(ResourceAttachmentChange diff) {
    String owner = describeMatchObject(diff.getMatch(), diff.getSource());
    String resourceUri = quote(diff.getResourceURI());

    return switch (diff.getKind()) {
      case ADD -> String.format("Attached %s to resource %s%s",
          owner, resourceUri, describeSourceSuffix(diff.getSource()));
      case DELETE -> String.format("Detached %s from resource %s%s",
          owner, resourceUri, describeSourceSuffix(diff.getSource()));
      case CHANGE, MOVE -> String.format("Moved %s to resource %s%s",
          owner, resourceUri, describeSourceSuffix(diff.getSource()));
    };
  }

  private static String describeMatchObject(Match match, DifferenceSource preferredSource) {
    if (match == null) {
      return "unknown element";
    }

    EObject preferredObject = preferredSource == DifferenceSource.RIGHT ? match.getRight() : match.getLeft();
    if (preferredObject == null) {
      preferredObject = match.getLeft();
    }
    if (preferredObject == null) {
      preferredObject = match.getRight();
    }
    if (preferredObject == null) {
      preferredObject = match.getOrigin();
    }
    return describeEObject(preferredObject);
  }

  private static String describeEObject(EObject eObject) {
    if (eObject == null) {
      return "unknown element";
    }

    String typeName = eObject.eClass().getName();
    String elementName = extractElementName(eObject);
    if (elementName != null) {
      return String.format("%s '%s'", typeName, elementName);
    }
    return typeName;
  }

  private static String extractElementName(EObject eObject) {
    if (eObject instanceof ENamedElement namedElement && namedElement.getName() != null &&
        !namedElement.getName().isBlank()) {
      return namedElement.getName();
    }

    var nameFeature = eObject.eClass().getEStructuralFeature("name");
    if (nameFeature instanceof EAttribute && eObject.eIsSet(nameFeature)) {
      Object value = eObject.eGet(nameFeature);
      if (value instanceof String name && !name.isBlank()) {
        return name;
      }
    }

    return null;
  }

  private static String describeValue(Object value) {
    return switch (value) {
      case null -> "null";
      case EObject eObject -> describeEObject(eObject);
      case String s -> quote(s);
      default -> String.valueOf(value);
    };
  }

  private static String describeSourceSuffix(DifferenceSource source) {
    return String.format(" (source: %s model)", source.getLiteral().toLowerCase());
  }

  private static String capitalize(String text) {
    if (text == null || text.isEmpty()) {
      return "";
    }
    return Character.toUpperCase(text.charAt(0)) + text.substring(1);
  }

  private static String quote(String text) {
    return text == null ? "null" : "'" + text + "'";
  }
}
