# Automatically generated Pydantic models. Do not modify manually.

# Needed to avoid errors due to circular dependencies between Pydantic models
from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Union, Optional


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

