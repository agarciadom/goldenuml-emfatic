# Automatically generated Pydantic models. Do not modify manually.

# Needed to avoid errors due to circular dependencies between Pydantic models
from __future__ import annotations

import xml.etree.ElementTree as ET
from pydantic import BaseModel, Field
from typing import Union, Optional

XMI_NS = "http://www.omg.org/XMI"
XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"
ECORE_NS = "http://www.eclipse.org/emf/2002/Ecore"

ET.register_namespace("xmi", XMI_NS)
ET.register_namespace("xsi", XSI_NS)
ET.register_namespace("ecore", ECORE_NS)


def _qualified(name: str, namespace: str) -> str:
  return f"{{{namespace}}}{name}"


def _local_reference(name: str) -> str:
  return f"#//{name}"


def _builtin_ecore_reference(name: str) -> str:
  if name.startswith("ecore:EDataType "):
    return name
  if name.startswith("//"):
    return f"ecore:EDataType {ECORE_NS}#{name}"
  return name


class EPackage(BaseModel):
  name: str
  nsURI: str
  eClassifiers: dict[str, Union[EClass, EDataType]] = Field(default_factory=dict)

  def to_xmi_element(self) -> ET.Element:
    element = ET.Element(
      _qualified("EPackage", ECORE_NS),
      {
        _qualified("version", XMI_NS): "2.0",
        "name": self.name,
        "nsURI": self.nsURI,
        "nsPrefix": self.name,
      },
    )
    for classifier in self.eClassifiers.values():
      element.append(classifier.to_xmi_element())
    return element

  def to_xmi(self) -> str:
    element = self.to_xmi_element()
    ET.indent(element, space="  ")
    return ET.tostring(element, encoding="unicode", xml_declaration=True)

class EClass(BaseModel):
  name: str
  eSuperTypes: set[EClass] = Field(default_factory=set)
  eStructuralFeatures: dict[str, Union[EAttribute, EReference]] = Field(default_factory=dict)

  __hash__ = object.__hash__

  def to_xmi_element(self) -> ET.Element:
    attributes = {
      _qualified("type", XSI_NS): "ecore:EClass",
      "name": self.name,
    }
    if self.eSuperTypes:
      attributes["eSuperTypes"] = " ".join(
        _local_reference(super_type.name)
        for super_type in sorted(self.eSuperTypes, key=lambda e_class: e_class.name)
      )
    element = ET.Element("eClassifiers", attributes)
    for feature in self.eStructuralFeatures.values():
      element.append(feature.to_xmi_element())
    return element

class EAttribute(BaseModel):
  name: str
  eType: Optional[Union[EDataType, str]] = None
  upperBound: int
  lowerBound: int

  def to_xmi_element(self) -> ET.Element:
    attributes = {
      _qualified("type", XSI_NS): "ecore:EAttribute",
      "name": self.name,
      "upperBound": str(self.upperBound),
      "lowerBound": str(self.lowerBound),
    }
    if self.eType is not None:
      attributes["eType"] = self._serialize_etype()
    return ET.Element("eStructuralFeatures", attributes)

  def _serialize_etype(self) -> str:
    if isinstance(self.eType, EDataType):
      return _local_reference(self.eType.name)
    return _builtin_ecore_reference(self.eType)

class EReference(BaseModel):
  name: str
  containment: bool
  eType: Optional[EClass] = None
  upperBound: int
  lowerBound: int

  def to_xmi_element(self) -> ET.Element:
    attributes = {
      _qualified("type", XSI_NS): "ecore:EReference",
      "name": self.name,
      "containment": str(self.containment).lower(),
      "upperBound": str(self.upperBound),
      "lowerBound": str(self.lowerBound),
    }
    if self.eType is not None:
      attributes["eType"] = _local_reference(self.eType.name)
    return ET.Element("eStructuralFeatures", attributes)

class EDataType(BaseModel):
  name: str
  instanceClassName: str

  def to_xmi_element(self) -> ET.Element:
    return ET.Element(
      "eClassifiers",
      {
        _qualified("type", XSI_NS): "ecore:EDataType",
        "name": self.name,
        "instanceClassName": self.instanceClassName,
      },
    )
