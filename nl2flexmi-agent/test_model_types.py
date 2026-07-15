from model_tools import *
from model_types import EPackage, EAttribute

def test_recreate_preserves_existing():
    epkg = EPackage(nsPrefix="p", nsURI="myuri", name="Example")
    tool = AddEClassToEPackageEClassifiers(epkg)
    c1 = tool.forward("MyClass")
    c2 = tool.forward("MyClass")
    assert c1 is c2

def test_assign_eattr_etype_by_name():
    eattr = EAttribute(name="name", lowerBound=1, upperBound=1)
    eattr.eType = "String"
    assert eattr.eType == "//EString"

def test_assign_eattr_etype_by_uri_fragment():
    eattr = EAttribute(name="name", lowerBound=1, upperBound=1)
    eattr.eType = "//EString"
    assert eattr.eType == "//EString"