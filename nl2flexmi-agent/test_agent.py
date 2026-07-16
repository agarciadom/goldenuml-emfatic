from smolagents import LiteLLMModel

from agent import ModelAgent
from model_types import EAttribute, EClass, EDataType, EReference


def test_remove_duplicated_fields():
    agent = ModelAgent(LiteLLMModel(model_id="dummy"))

    ec_super = EClass(name="Supertype")
    ec_super.eStructuralFeatures["x"] = EAttribute(name="x", lowerBound=0, upperBound=1)
    ec_sub = EClass(name="Subtype")
    ec_sub.eStructuralFeatures["x"] = EAttribute(name="x", lowerBound=0, upperBound=1)
    ec_sub.eSuperTypes.add(ec_super)

    agent.epackage.eClassifiers["Supertype"] = ec_super
    agent.epackage.eClassifiers["Subtype"] = ec_sub
    agent.run_post_repair()
    assert "x" not in ec_sub.eStructuralFeatures

def test_keep_nonduplicated_fields():
    agent = ModelAgent(LiteLLMModel(model_id="dummy"))
    ec = EClass(name="Supertype")
    ec.eStructuralFeatures["x"] = EAttribute(name="x", lowerBound=0, upperBound=1)
    agent.epackage.eClassifiers["Supertype"] = ec
    agent.run_post_repair()
    assert "x" in ec.eStructuralFeatures

def test_repair_with_edatatype():
    agent = ModelAgent(LiteLLMModel(model_id="dummy"))
    dt = EDataType(name="Date", instanceClassName="java.time.LocalDate")
    agent.epackage.eClassifiers["Date"] = dt
    agent.run_post_repair()

def test_swap_eattr_with_eref_repair():
    agent = ModelAgent(LiteLLMModel(model_id="dummy"))
    ec_image = EClass(name="Image")
    agent.epackage.eClassifiers["Image"] = ec_image
    ec_profile = EClass(name="Profile")
    agent.epackage.eClassifiers["Profile"] = ec_profile

    # Simulate scenario where LLM incorrectly uses non-EDataType name as eType
    eattr_profile_img = EAttribute(name="profileImage", lowerBound=0, upperBound=1)
    ec_profile.eStructuralFeatures["profileImage"] = eattr_profile_img
    eattr_profile_img.eType = "Image"

    # Repair should swap the EAttribute for an EReference to the right class
    agent.run_post_repair()
    assert isinstance(ec_profile.eStructuralFeatures["profileImage"], EReference)
    assert ec_profile.eStructuralFeatures["profileImage"].eType is ec_image
