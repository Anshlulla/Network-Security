from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]: 
    """
        This function returns list of requirements
    """
    try:
        requirements = []
        with open("requirements.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement != "-e .": # -e . in requirements.txt refers to setup.py
                    requirements.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found!")
    
    return requirements

setup(
    name="Network-Security",
    version="0.0.1",
    author="AnshLulla",
    packages=find_packages(),
    install_requires=get_requirements()
)