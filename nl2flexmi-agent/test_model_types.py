from model_tools import *
from model_types import EPackage

def test_recreate_preserves_existing():
    epkg = EPackage(nsPrefix="p", nsURI="myuri", name="Example")
    tool = AddEClassToEPackageEClassifiers(epkg)
    c1 = tool.forward("MyClass")
    c2 = tool.forward("MyClass")
    assert c1 is c2