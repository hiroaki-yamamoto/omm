#!/usr/bin/env python
# coding=utf-8

"""
Object Model Mapping module.

This module helps transform models into other models.
"""

from .model import Mapper
from .fields import MapField
from .structures import ConDict

__all__ = ("Mapper", "MapField", "ConDict")
