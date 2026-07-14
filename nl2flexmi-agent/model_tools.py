# Automatically generated model creation tools. Do not modify manually.

from model_types import *
from smolagents import Tool

# Root update tool

class UpdateEPackage(Tool):
  name = "update_EPackage"
  description = """
  Updates declaration of the package containing all the EClasses, and returns it.
  """
  inputs = {
    "name": {
      "type": "string",
      "description": "Name of the package (without spaces)"
    },
    "nsURI": {
      "type": "string",
      "description": "The namespace URI of the package"
    },
    "nsPrefix": {
      "type": "string",
      "description": "XML namespace prefix to be used for this EPackage"
    },
  }
  output_type = "object"

  def __init__(self, root: EPackage, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.root = root

  def forward(self, name: str, nsURI: str, nsPrefix: str) -> EPackage:
    self.root.name = name
    self.root.nsURI = nsURI
    self.root.nsPrefix = nsPrefix
    return self.root

# Subobject creation tools (for containment references)

class AddEClassToEPackageEClassifiers(Tool):
  name = "add_EClass_to_EPackage_eClassifiers"
  description = """
  Creates and adds a EClass to the eClassifiers in a EPackage, and returns the EClass.
  """
  inputs = {
    "name": {
      "type": "string",
      "description": "Name of the class"
    },
  }
  output_type = "object"

  def __init__(self, root: EPackage, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.root = root

  def forward(self, name: str) -> EClass:
    _fields = {
      "name": name,
    }
    if name in self.root.eClassifiers and isinstance(self.root.eClassifiers[name], EClass):
      _existing = self.root.eClassifiers[name]
      for field, value in _fields.items():
        setattr(_existing, field, value)
    else:
      self.root.eClassifiers[name] = EClass(**_fields)
    return self.root.eClassifiers[name]


class AddEDataTypeToEPackageEClassifiers(Tool):
  name = "add_EDataType_to_EPackage_eClassifiers"
  description = """
  Creates and adds a EDataType to the eClassifiers in a EPackage, and returns the EDataType.
  """
  inputs = {
    "name": {
      "type": "string",
      "description": "Name of the data type"
    },
    "instanceClassName": {
      "type": "string",
      "description": "Fully qualified Java class name of the instances of this data type"
    },
  }
  output_type = "object"

  def __init__(self, root: EPackage, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.root = root

  def forward(self, name: str, instanceClassName: str) -> EDataType:
    _fields = {
      "name": name,
      "instanceClassName": instanceClassName,
    }
    if name in self.root.eClassifiers and isinstance(self.root.eClassifiers[name], EDataType):
      _existing = self.root.eClassifiers[name]
      for field, value in _fields.items():
        setattr(_existing, field, value)
    else:
      self.root.eClassifiers[name] = EDataType(**_fields)
    return self.root.eClassifiers[name]


class AddEAttributeToEClassEStructuralFeatures(Tool):
  name = "add_EAttribute_to_EClass_eStructuralFeatures"
  description = """
  Creates and adds a EAttribute to the eStructuralFeatures in a EClass, and returns the EAttribute.
  """
  inputs = {
    "eClass": {
      "type": "object",
      "description": "EClass that this EAttribute belongs to"
    },
    "name": {
      "type": "string",
      "description": "Name of the attribute."
    },
    "lowerBound": {
      "type": "integer",
      "description": "Minimum number of values for the attribute (must be less or equal to the upper bound)"
    },
    "upperBound": {
      "type": "integer",
      "description": "Maximum number of values for the attribute"
    },
  }
  output_type = "object"


  def forward(self, eClass: EClass, name: str, lowerBound: int, upperBound: int) -> EAttribute:
    _fields = {
      "name": name,
      "lowerBound": lowerBound,
      "upperBound": upperBound,
    }
    if name in eClass.eStructuralFeatures and isinstance(eClass.eStructuralFeatures[name], EAttribute):
      _existing = eClass.eStructuralFeatures[name]
      for field, value in _fields.items():
        setattr(_existing, field, value)
    else:
      eClass.eStructuralFeatures[name] = EAttribute(**_fields)
    return eClass.eStructuralFeatures[name]


class AddEReferenceToEClassEStructuralFeatures(Tool):
  name = "add_EReference_to_EClass_eStructuralFeatures"
  description = """
  Creates and adds a EReference to the eStructuralFeatures in a EClass, and returns the EReference.
  """
  inputs = {
    "eClass": {
      "type": "object",
      "description": "EClass that this EReference belongs to"
    },
    "name": {
      "type": "string",
      "description": "Name of the reference."
    },
    "containment": {
      "type": "boolean",
      "description": "True if the source of the reference contains the target of reference (meaning that deleting the source will also delete the target)."
    },
    "lowerBound": {
      "type": "integer",
      "description": "Minimum number of targets for the reference (must be less or equal to the upper bound)"
    },
    "upperBound": {
      "type": "integer",
      "description": "Maximum number of targets for the reference"
    },
  }
  output_type = "object"


  def forward(self, eClass: EClass, name: str, containment: bool, lowerBound: int, upperBound: int) -> EReference:
    _fields = {
      "name": name,
      "containment": containment,
      "lowerBound": lowerBound,
      "upperBound": upperBound,
    }
    if name in eClass.eStructuralFeatures and isinstance(eClass.eStructuralFeatures[name], EReference):
      _existing = eClass.eStructuralFeatures[name]
      for field, value in _fields.items():
        setattr(_existing, field, value)
    else:
      eClass.eStructuralFeatures[name] = EReference(**_fields)
    return eClass.eStructuralFeatures[name]


# Non-containment reference tools

class AddEClassToEClassESuperTypes(Tool):
  name = "add_EClass_to_EClass_ESuperTypes"
  description = """
  Adds a EClass to the eSuperTypes of a EClass, and returns it.
  """
  inputs = {
    "eClass": {
      "type": "object",
      "description": "The EClass holding the eSuperTypes"
    },
    "addition": {
      "type": "object",
      "description": "The EClass to be added"
    }
  }
  output_type = "object"

  def forward(self, eClass: EClass, addition: EClass) -> EClass:
    eClass.eSuperTypes.add(addition)
    return addition


class AddEDataTypeToEAttributeEType(Tool):
  name = "add_EDataType_to_EAttribute_EType"
  description = """
  Adds a EDataType to the eType of a EAttribute, and returns it.
  """
  inputs = {
    "eAttribute": {
      "type": "object",
      "description": "The EAttribute holding the eType"
    },
    "addition": {
      "type": "object",
      "description": "The EDataType to be added"
    }
  }
  output_type = "object"

  def forward(self, eAttribute: EAttribute, addition: EDataType) -> EDataType:
    eAttribute.eType = addition
    return addition


class AddNamedToEAttributeEType(Tool):
  name = "add_named_to_EAttribute_EType"
  description = """
  Adds a named object to the eType of a EAttribute, and returns its name.
  """
  inputs = {
    "eAttribute": {
      "type": "object",
      "description": "The EAttribute holding the eType"
    },
    "addition": {
      "type": "string",
      "description": "The name of the object to be added. Possible options: BigDecimal, String, BigInteger, Boolean, Byte, Date, Double, Float, Integer, Long, Short, BooleanObject, ByteObject, CharacterObject, DoubleObject, FloatObject, IntegerObject, LongObject, ShortObject."
    }
  }
  output_type = "object"

  def forward(self, eAttribute: EAttribute, addition: str) -> str:
    options = {
      "BigDecimal": "//EBigDecimal",
      "String": "//EString",
      "BigInteger": "//EBigInteger",
      "Boolean": "//EBoolean",
      "Byte": "//EByte",
      "Date": "//EDate",
      "Double": "//EDouble",
      "Float": "//EFloat",
      "Integer": "//EInt",
      "Long": "//ELong",
      "Short": "//EShort",
      "BooleanObject": "//EBooleanObject",
      "ByteObject": "//EByteObject",
      "CharacterObject": "//ECharacterObject",
      "DoubleObject": "//EDoubleObject",
      "FloatObject": "//EFloatObject",
      "IntegerObject": "//EIntegerObject",
      "LongObject": "//ELongObject",
      "ShortObject": "//EShortObject",
    }
    eAttribute.eType = options[addition]
    return addition


class AddEClassToEReferenceEType(Tool):
  name = "add_EClass_to_EReference_EType"
  description = """
  Adds a EClass to the eType of a EReference, and returns it.
  """
  inputs = {
    "eReference": {
      "type": "object",
      "description": "The EReference holding the eType"
    },
    "addition": {
      "type": "object",
      "description": "The EClass to be added"
    }
  }
  output_type = "object"

  def forward(self, eReference: EReference, addition: EClass) -> EClass:
    eReference.eType = addition
    return addition


def createTools(root: EPackage) -> list[Tool]:
  return [
    UpdateEPackage(root),
    AddEClassToEPackageEClassifiers(root),
    AddEDataTypeToEPackageEClassifiers(root),
    AddEAttributeToEClassEStructuralFeatures(),
    AddEReferenceToEClassEStructuralFeatures(),
    AddEClassToEClassESuperTypes(),
    AddEDataTypeToEAttributeEType(),
    AddNamedToEAttributeEType(),
    AddEClassToEReferenceEType(),
  ]

