#!/usr/bin/env python
# coding=utf-8

"""Model Base."""


class Mapper(object):
    """
    Mapper Base Classs.

    Every class that uses this mapper should inherit this class.

    Useful Attributes:
        asdict: Set True if you put value as dict. By default, this value is
            Falsy value that means "put value as attribute."

    Use of asdict:
        Suppose that there is a mapper like this:
        ```Python
        class Test(Mapper):
            test = MapField("test.a.b.c")
        ```
        Then, putting the value "this is a test" there, you can get an instance
        of object via connected_object property, like this:
        ```Python
        class B(object):
            def __init__(self, c):
                self.c = c

        class A(object):
            def __init__(self):
                self.b = B("this is a test")

        class Test(object):
            def __init__(self):
                self.a = A()

        # connected_object = Test()
        ```
        However, setting self.asdict = True, connected_object become
        multi-dimentional dict like this:
        ```Python
        connected_object = {"test": {"a": {"b": {"c": "this is a test"}}}}
        ```
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
        return getattr(self, "_target", None)

    def connect(self, target):
        """
        Connect the object/dict to the mapper.

        Parameters:
            target: The target object.
        """
        self._target = target
