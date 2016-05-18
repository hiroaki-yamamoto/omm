#!/usr/bin/env python
# coding=utf-8

"""Model Base."""

import re
from functools import partial

from .fields import FieldBase


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

    def __init__(self, target=None, **kwargs):
        """
        Initialize the object.

        Parameters:
            target: The target object. By default, None is set.
            **kwargs: Any attributes or meta-data.
        """
        if target is not None:
            self.connect(target)
        for (attr, value) in kwargs.items():
            setattr(self, attr, value)
        super(Mapper, self).__init__()

    def validate(self):
        """Validate the model."""
        self.__errors = {}
        FieldList = partial(sorted, key=lambda cmp: cmp[0]) \
            if getattr(self, "$testing$", False) else list
        self.__fields = FieldList([
            (name, field) for (name, field) in type(self).__dict__.items()
            if isinstance(field, FieldBase) and isinstance(
                getattr(field, "set_cast", None), list
            )
        ])
        self.__list = partial(sorted, key=self.__fields.index) \
            if getattr(self, "$testing$", False) else list
        rest_fields = self.__validate_setattr_num()
        rest_fields = self.__validate_consistency(rest_fields)
        return not bool(self.__errors)

    def __validate_setattr_num(self):
        """Validate the # of setattr."""
        fields = self.__fields
        error_fields = []
        for (name, field) in fields:
            try:
                field.validate()
            except ValueError as e:
                error_fields.append((name, field))
                self._register_error(name, str(e))
        return self.__list(set(fields) - set(error_fields))

    def _register_error(self, fldname, err):
        """
        Register an error message.

        Parameters:
            fldname: The name of the field.
            err: The message
        """
        if isinstance(self.__errors.get(fldname), list):
            self.__errors[fldname].append(err)
        else:
            self.__errors[fldname] = [err]

    def __validate_consistency(self, fields=None):
        """Check consistency of the class."""
        fields = fields or self.__fields
        error_fields = []
        if not fields:
            return {}
        AttributeInfo = type("__AttrInfo__", (object, ), {})
        root = AttributeInfo()
        setattr(root, "$$type$$", fields[0][1].set_cast[0])
        setattr(root, "$$source$$", fields[0][0])
        err_msg = (
            "This field partially references the same path of {source}, "
            "but set_cast corresponding to \"{fldname}\" is not the same."
        )
        parse_pattern = re.compile("([^\.\[\]0-9]+)|\[([0-9]+)\]+")
        for (name, field) in fields:
            parsed_attrs = [
                el for pa in parse_pattern.findall(field.target)
                for el in pa if el
            ]
            current = root
            current_type = getattr(current, "$$type$$", None)
            err = err_msg.format(
                source=getattr(current, "$$source$$", None),
                fldname="(root)"
            )
            root_set_cast = field.set_cast[0]
            if current_type is not root_set_cast:
                error_fields.append((name, field))
                self._register_error(name, err)
            for (attr_index, parsed_attr) in enumerate(parsed_attrs):
                attr_set_cast = field.set_cast[attr_index + 1]
                current_target_str = ("(root).{}").format(
                    (".").join(parsed_attrs[:attr_index + 1])
                )
                try:
                    current = getattr(current, parsed_attr)
                    current_type = getattr(current, "$$type$$", None)
                    err = err_msg.format(
                        source=getattr(current, "$$source$$", None),
                        fldname=current_target_str
                    )
                    if current_type is not attr_set_cast:
                        error_fields.append((name, field))
                        self._register_error(name, err)
                except AttributeError:
                    setattr(current, parsed_attr, AttributeInfo())
                    current = getattr(current, parsed_attr)
                    setattr(
                        current, "$$type$$",
                        field.set_cast[attr_index + 1]
                    )
                    setattr(current, "$$source$$", name)
        return self.__list(set(fields) - set(error_fields))

    @property
    def errors(self):
        """
        Return error-dict.

        The format of this property is compatible with [WTForms]. For example,
        if there are errors, this property returns a dict like this:

        ```JSON
        {
            "age": [
                "This field refernces partially the same path of name"
            ]
        }
        ```

        If there aren't any errors, None is returned.

        [WTForms]: https://wtforms.readthedocs.io/en/latest/
        """
        try:
            return self.__errors
        except AttributeError:
            raise NotImplementedError("Execute validate method.")

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
