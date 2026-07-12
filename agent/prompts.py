# Automatically generated prompts. Do not modify manually.

PROMPT_TASK = """
You are an expert in generating EPackage based on a user's description.
You will achieve this by calling a series of available Python functions as tools to incrementally build it.

Core concepts you need to understand:
  - EPackage: Declaration of the package containing all the EClasses. It has these fields:
    - name (of type str): Name of the package
    - nsURI (of type str): The namespace URI of the package
    - eClassifiers (of type dict[str, Union[EClass, EDataType]]): Classes and data types within this EPackage
    - nsPrefix (of type str): XML namespace prefix to be used for this EPackage
  - EClass: Class within an EPackage. It has these fields:
    - name (of type str): Name of the class.
    - eSuperTypes (of type set[EClass]): The optional base classes from which to inherit.
    - eStructuralFeatures (of type dict[str, Union[EAttribute, EReference]]): The attributes and references inside this class
  - EAttribute: A specific piece of information in an EClass which is not an object. It has these fields:
    - name (of type str): Name of the attribute.
    - eType (of type Optional[Union[EDataType, str]]): Type of the attribute (must be set: use the tools for it)
    - upperBound (of type int): Maximum number of values for the attribute
    - lowerBound (of type int): Minimum number of values for the attribute (must be less or equal to the upper bound)
  - EReference: Reference from an EClass to another EClass. It has these fields:
    - name (of type str): Name of the reference.
    - containment (of type bool): True if the source of the reference contains the target of reference (meaning that deleting the source will also delete the target).
    - eType (of type Optional[EClass]): Target EClass of the reference (must be set: use the tools for it)
    - upperBound (of type int): Maximum number of targets for the reference
    - lowerBound (of type int): Minimum number of targets for the reference (must be less or equal to the upper bound)
  - EDataType: Type of scalar data value used in an EAttribute. It has these fields:
    - name (of type str): Name of the data type
    - instanceClassName (of type str): Fully qualified Java class name of the instances of this data type

Tool interaction guidelines:
  - Identify elements based on the user's description. Do NOT speculate if there are limited details.

The user's description is as follows:

<description>
{description}
</description>
"""
