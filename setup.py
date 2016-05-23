#!/usr/bin/env python
# coding=utf-8
"""Setup script."""

import sys
from setuptools import setup, find_packages

dependencies = []
desc = "Object Model Mapper for Python-based web apps and/or APIs"
version = "0.5.0"
if sys.version_info < (2, 7):
    raise RuntimeError("Not supported on earlier then python 2.7.")

try:
    with open('README.rst') as readme:
        long_desc = readme.read()
except Exception:
    long_desc = None

setup(
    name="OMM",
    version=version,
    description=desc,
    long_description=long_desc,
    packages=find_packages(exclude=["tests"]),
    install_requires=dependencies,
    zip_safe=False,
    author="Hiroaki Yamamoto",
    author_email="hiroaki@hysoftware.net",
    license="MIT",
    keywords="json OMM Object Model Mapper Relational Document",
    url="https://github.com/hiroaki-yamamoto/omm.git",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5"
    ]
)
