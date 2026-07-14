# Automatically generated Pydantic models. Do not modify manually.

# Needed to avoid errors due to circular dependencies between Pydantic models
from __future__ import annotations

import xml.etree.ElementTree as ET
from pydantic import BaseModel, Field, model_validator, ConfigDict
from typing import Union, Optional, override


class EObjectBaseModel(BaseModel):
  model_config = ConfigDict(
    # Prevent Smolagents from directly assigning the wrong type of value to a field
    validate_assignment = True,
  )
  emf_uri_fragment: str = Field(default='/')

  def set_uri_fragments(self, own_fragment):
    self.emf_uri_fragment = own_fragment

  # Make instances hashable based on object identity
  __hash__ = object.__hash__


class EPackage(EObjectBaseModel):
  name: str = Field(pattern="[a-zA-Z]+")
  nsURI: str = Field(min_length=1)
  eClassifiers: dict[str, Union[EClass, EDataType]] = Field(default_factory=dict, repr=False)
  nsPrefix: str = Field(pattern="[a-zA-Z]+")

  def write_to_file(self, f):
    pis = [
      ET.ProcessingInstruction("nsuri", "http://www.eclipse.org/emf/2002/Ecore"),
      ET.ProcessingInstruction("import", "http://www.eclipse.org/emf/2002/Ecore"),
    ]
    root = self.to_flexmi()
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)

    for pi in pis:
      f.write(ET.tostring(pi, encoding="unicode"))
      f.write("\n")
    tree.write(f, encoding="unicode", short_empty_elements=True)
    f.write("\n")

  def to_flexmi(self) -> ET.Element:
    self.set_uri_fragments('/')
    element = ET.Element("ePackage", {
      "name": self.name,
      "nsURI": self.nsURI,
      "nsPrefix": self.nsPrefix,
    })
    feature_element = ET.SubElement(element, "eClassifiers")
    for child in self.eClassifiers.values():
      feature_element.append(child.to_flexmi())
    return element

  @override
  def set_uri_fragments(self, own_fragment):
    self.emf_uri_fragment = own_fragment
    for pos, child in enumerate(self.eClassifiers.values()):
      child.set_uri_fragments('{0}/@eClassifiers.{1:d}'.format(own_fragment, pos))

# protected region EPackage on begin
# add custom validation logic here
# protected region EPackage end


class EClass(EObjectBaseModel):
  name: str = Field(pattern="[_a-zA-Z][_a-ZA-Z0-9]*")
  eSuperTypes: set[EClass] = Field(default_factory=set, repr=False)
  eStructuralFeatures: dict[str, Union[EAttribute, EReference]] = Field(default_factory=dict, repr=False)

  def to_flexmi(self) -> ET.Element:
    element = ET.Element("eClass", {
      "name": self.name,
    })
    if self.eSuperTypes:
      element.set("eSuperTypes", ', '.join(v.emf_uri_fragment for v in self.eSuperTypes))
    feature_element = ET.SubElement(element, "eStructuralFeatures")
    for child in self.eStructuralFeatures.values():
      feature_element.append(child.to_flexmi())
    return element

  @override
  def set_uri_fragments(self, own_fragment):
    self.emf_uri_fragment = own_fragment
    for pos, child in enumerate(self.eStructuralFeatures.values()):
      child.set_uri_fragments('{0}/@eStructuralFeatures.{1:d}'.format(own_fragment, pos))

# protected region EClass on begin
# add custom validation logic here
# protected region EClass end


class EAttribute(EObjectBaseModel):
  name: str = Field(pattern="[_a-zA-Z][_a-ZA-Z0-9]*")
  eType: Optional[Union[EDataType, str]] = Field(default=None)
  lowerBound: int
  upperBound: int

  def to_flexmi(self) -> ET.Element:
    element = ET.Element("eAttribute", {
      "name": self.name,
      "lowerBound": str(self.lowerBound),
      "upperBound": str(self.upperBound),
    })
    if self.eType:
      element.set("eType", (self.eType.emf_uri_fragment if hasattr(self.eType, 'emf_uri_fragment') else self.eType))
    return element

# protected region EAttribute on begin
  @model_validator(mode="after")
  def validate_bounds(self) -> EAttribute:
      if self.upperBound != -1 and self.lowerBound > self.upperBound:
          raise ValueError(
              "lowerBound ({}) must be less than or equal to upperBound ({}), unless upperBound is -1".format(
                  self.lowerBound, self.upperBound))
      return self
# protected region EAttribute end


class EReference(EObjectBaseModel):
  name: str = Field(pattern="[_a-zA-Z][_a-ZA-Z0-9]*")
  containment: bool
  eType: Optional[EClass] = Field(default=None)
  lowerBound: int
  upperBound: int

  def to_flexmi(self) -> ET.Element:
    element = ET.Element("eReference", {
      "name": self.name,
      "containment": str(self.containment),
      "lowerBound": str(self.lowerBound),
      "upperBound": str(self.upperBound),
    })
    if self.eType:
      element.set("eType", self.eType.emf_uri_fragment)
    return element

# protected region EReference on begin
  @model_validator(mode="after")
  def validate_bounds(self) -> EReference:
    if self.upperBound != -1 and self.lowerBound > self.upperBound:
        raise ValueError(
            "lowerBound ({}) must be less than or equal to upperBound ({}), unless upperBound is -1".format(
                self.lowerBound, self.upperBound))
    return self
# protected region EReference end


class EDataType(EObjectBaseModel):
  name: str = Field(pattern="[_a-zA-Z][_a-ZA-Z0-9]*")
  instanceClassName: str = Field(min_length=1)

  def to_flexmi(self) -> ET.Element:
    element = ET.Element("eDataType", {
      "name": self.name,
      "instanceClassName": self.instanceClassName,
    })
    return element

# protected region EDataType on begin
# add custom validation logic here
# protected region EDataType end


