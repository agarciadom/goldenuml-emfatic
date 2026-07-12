# Automatically generated model creation tools. Do not modify manually.

# Needed to avoid errors due to circular dependencies between Pydantic models
from __future__ import annotations

from pydantic import BaseModel, Field
from smolagents import Tool
from typing import Union, Optional

# Pydantic models

class EPackage(BaseModel):
  name: str
  nsURI: str
  eClassifiers: dict[str, Union[EClass, EDataType]] = Field(default_factory=dict)

class EClass(BaseModel):
  name: str
  eSuperTypes: set[EClass] = Field(default_factory=set)
  eStructuralFeatures: dict[str, Union[EAttribute, EReference]] = Field(default_factory=dict)

class EAttribute(BaseModel):
  name: str
  eType: Optional[Union[EDataType, str]] = None
  upperBound: int
  lowerBound: int

class EReference(BaseModel):
  name: str
  containment: bool
  eType: Optional[EClass] = None
  upperBound: int
  lowerBound: int

class EDataType(BaseModel):
  name: str
  instanceClassName: str


# Tools for Smolagents

# Root update tool

class UpdateEPackage(Tool):
  name = "update_EPackage"
  description = """
  Updates declaration of the package containing all the EClasses, and returns it.
  """
  inputs = {
    "name": {
      "type": "string",
      "description": "Name of the package"
    },
    "nsURI": {
      "type": "string",
      "description": "The namespace URI of the package"
    },
  }
  output_type = "object"

  def __init__(self, root: EPackage, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.root = root

  def forward(self, name: str, nsURI: str) -> EPackage:
    self.root.name = name
    self.root.nsURI = nsURI
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
      "description": "Name of the class."
    },
  }
  output_type = "object"

  def __init__(self, root: EPackage, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.root = root

  def forward(self, name: str) -> EClass:
    _instance = EClass(
      name=name,
    )
    self.root.eClassifiers[name] = _instance
    return _instance


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
    _instance = EDataType(
      name=name,
      instanceClassName=instanceClassName,
    )
    self.root.eClassifiers[name] = _instance
    return _instance


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
    "upperBound": {
      "type": "integer",
      "description": "Maximum number of values for the attribute"
    },
    "lowerBound": {
      "type": "integer",
      "description": "Minimum number of values for the attribute (must be less or equal to the upper bound)"
    },
  }
  output_type = "object"


  def forward(self, eClass: EClass, name: str, upperBound: int, lowerBound: int) -> EAttribute:
    _instance = EAttribute(
      name=name,
      upperBound=upperBound,
      lowerBound=lowerBound,
    )
    eClass.eStructuralFeatures[name] = _instance
    return _instance


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
    "upperBound": {
      "type": "integer",
      "description": "Maximum number of targets for the reference"
    },
    "lowerBound": {
      "type": "integer",
      "description": "Minimum number of targets for the reference (must be less or equal to the upper bound)"
    },
  }
  output_type = "object"


  def forward(self, eClass: EClass, name: str, containment: bool, upperBound: int, lowerBound: int) -> EReference:
    _instance = EReference(
      name=name,
      containment=containment,
      upperBound=upperBound,
      lowerBound=lowerBound,
    )
    eClass.eStructuralFeatures[name] = _instance
    return _instance


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
      "description": "The name of the object to be added. Possible options: BigDecimal, String, BigInteger, Boolean, Byte, Date, Double, Float, Integer, Long, Short."
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

