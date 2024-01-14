import re
import sys
from setuptools import setup, find_packages

def find_version(file_path: str) -> str:
    version_file = open(file_path).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if not version_match:
        raise RuntimeError(f"Unable to find version string in {file_path}")
    return version_match.group(1)

VERSION = find_version("simsnake/_version.py")


setup(
    name = "simsnake",
    version = VERSION,
    packages=find_packages(exclude=('docs', 'tests', 'examples'))
)