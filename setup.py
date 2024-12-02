from setuptools import setup, find_packages
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open(os.path.join("rangy", "__version__.py")) as f:
    exec(f.read())

setup(
    name="rangy",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "humanize==4.11.0",
        "PyYAML==6.0.2",
    ],
    extras_require={
        "testing": ["pytest"],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A brief description of your package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/rangy",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
