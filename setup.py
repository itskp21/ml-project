from setuptools import find_packages, setup
from typing import List

def get_requirements(file_path: str) -> List[str]:
    """Reads requirements.txt and returns a list of dependencies"""
    hypen_e_dot = '-e .'
    requirements = []
    
    with open(file_path, "r", encoding="utf-8") as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.strip() for req in requirements]  # ✅ Corrected newline handling

        if hypen_e_dot in requirements:
            requirements.remove(hypen_e_dot)
    
    return requirements

setup(
    name='mlproject',
    version='0.0.1',
    author='Kush',
    author_email='itskp2106@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
)
