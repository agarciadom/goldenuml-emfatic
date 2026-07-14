from model_types import EPackage
from model_tools import *

def test_string_eattribute():
    epkg = EPackage(nsURI="default", nsPrefix="d", name="dummy")
    tool_ec = AddEClassToEPackageEClassifiers(epkg)
    tool_ea = AddEAttributeToEClassEStructuralFeatures()
    tool_st = SetETypeOfEAttribute()

    person = tool_ec.forward("Person")
    name = tool_ea.forward(person, "name", lowerBound=1, upperBound=1)
    tool_st.forward(name, "String")

    assert name.eType == '//EString'

def test_custom_eattribute():
    epkg = EPackage(nsURI="default", nsPrefix="d", name="dummy")
    tool_ec = AddEClassToEPackageEClassifiers(epkg)
    tool_dt = AddEDataTypeToEPackageEClassifiers(epkg)
    tool_ea = AddEAttributeToEClassEStructuralFeatures()
    tool_st = SetETypeOfEAttribute()

    person = tool_ec.forward("Person")
    wakeup_time = tool_ea.forward(person, "wakeup_time", lowerBound=1, upperBound=1)
    local_time = tool_dt.forward("LocalTime", instanceClassName="java.time.LocalTime")
    tool_st.forward(wakeup_time, local_time)
    assert wakeup_time.eType.name == 'LocalTime'