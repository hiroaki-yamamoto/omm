#!/usr/bin/env python
# coding=utf-8

"""Model Base."""


class Mapper(object):
    """
    Mapper Base Classs.

    Every class that uses this mapper should inherit this class.
    """

    def __init__(self, target=None):
        """
        Initialize the object.

        Parameters:
            target: The target object. By default, None is set.
        """
        if target is not None:
            self.connect(target)

    @property
    def connected_object(self):
        """Get connected object."""
        return self._target

    def connect(self, target):
        """
        Connect the object/dict to the mapper.

        Parameters:
            target: The target object.
        """
        self._target = target
