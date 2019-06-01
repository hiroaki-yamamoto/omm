#!/usr/bin/env python
# coding=utf-8
"""Setup script."""

import sys
from os import path
from setuptools import setup, find_packages

dependencies = ["six==1.12.0"]
name = "OMM"
desc = "Object Model Mapper for Python-based web apps and/or APIs"
license = "MIT"
url = "https://github.com/hiroaki-yamamoto/omm.git"
keywords = "json OMM Object Model Mapper Relational Document"
version = "1.0.0"

category = [
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3"
]

version_file = path.join(path.abspath(path.dirname(__file__)), "VERSION")

if path.exists(version_file):
    with open(version_file) as v:
        version = v.read()

author = "Hiroaki Yamamoto"
author_email = "hiroaki@hysoftware.net"

if sys.version_info < (2, 7):
    raise RuntimeError("Not supported on earlier then python 2.7.")

try:
    with open('README.md') as readme:
        long_desc = readme.read()
except Exception:
    long_desc = None

setup(
    name=name,
    version=version,
    description=desc,
    long_description=long_desc,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=dependencies,
    zip_safe=False,
    author=author,
    author_email=author_email,
    license=license,
    keywords=keywords,
    url=url,
    classifiers=category
)
