#!/usr/bin/env python
# coding=utf-8

"""Model Base."""

import json
import re
from functools import partial

from .fields import FieldBase
from .helper import reduce_with_index


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

    def __collect_fields(self):
        FieldList = partial(sorted, key=lambda cmp: cmp[0]) \
            if getattr(self, "$testing$", False) else list
        self.__fields = FieldList([
            (name, field) for (name, field) in type(self).__dict__.items()
            if isinstance(field, FieldBase)
        ])

    def validate(self):
        """Validate the model."""
        self.__errors = {}
        self.__collect_fields()
        self.__list = partial(sorted, key=self.__fields.index) \
            if getattr(self, "$testing$", False) else list
        rest_fields = self.__validate_each_field()
        rest_fields = self.__validate_consistency(rest_fields)
        return not bool(self.__errors)

    def __validate_each_field(self):
        """Validate each field."""
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
        fields = [
            field for field in fields or self.__fields
            if isinstance(getattr(field[1], "set_cast", None), list)
        ]
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

        def check_consistency_for_each_value(cur, attr, index,
                                             attrs, name, field):
            attr_set_cast = field.set_cast[index + 1]
            current_target_str = ("(root).{}").format(
                (".").join(attrs[:index + 1])
            )
            current = cur
            try:
                current = getattr(current, attr)
                current_type = getattr(current, "$$type$$", None)
                err = err_msg.format(
                    source=getattr(current, "$$source$$", None),
                    fldname=current_target_str
                )
                if current_type is not attr_set_cast:
                    error_fields.append((name, field))
                    self._register_error(name, err)
            except AttributeError:
                setattr(current, attr, AttributeInfo())
                current = getattr(current, attr)
                setattr(
                    current, "$$type$$",
                    field.set_cast[index + 1]
                )
                setattr(current, "$$source$$", name)
            return current

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
            reduce_with_index(
                check_consistency_for_each_value, parsed_attrs, current,
                attrs=parsed_attrs, name=name, field=field
            )
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

    def to_dict(self):
        """Convert the schema into dict."""
        self.__collect_fields()
        dct = {}
        for (name, fld) in self.__fields:
            try:
                value = getattr(self, name)
                try:
                    dct[name] = value.to_dict()
                except AttributeError:
                    dct[name] = value
            except AttributeError:
                pass
        return dct

    @classmethod
    def from_dict(cls, dct):
        """
        Convert the given dict into the schema.

        Parameters:
            dct: The dict to be deserialize.
        """
        ret = cls()
        for (name, value) in dct.items():
            if hasattr(cls, name):
                try:
                    set_cast = getattr(cls, name).set_cast
                    if isinstance(set_cast, list):
                        set_cast = set_cast[-1]
                    setattr(ret, name, set_cast.from_dict(
                        {name: value}
                    ))
                except AttributeError:
                    setattr(ret, name, value)
        return ret

    def to_json(self, **kwargs):
        """
        Generate JSON string.

        Parameters:
            **kwargs: Any keyword arguemnt to be passed to json.dumps
        """
        self.__collect_fields()
        dct = {}
        for (name, field) in self.__fields:
            try:
                dct[name] = getattr(self, name)
                dct[name] = json.loads(
                    dct[name].to_json(**kwargs)
                ) if hasattr(dct[name], "to_json") else dct[name].to_dict()
            except AttributeError:
                continue
        return json.dumps(dct)

    @classmethod
    def from_json(cls, json_str, **kwargs):
        """
        De-serialize JSON string into the object.

        Parameters:
            json_str: JSON string to be deserialized
            **kwargs: Any keyword arguments to be passed to json.loads
        """
        ret = cls()
        dct = json.loads(json_str, **kwargs)
        for (name, value) in dct.items():
            if hasattr(cls, name):
                try:
                    set_cast = getattr(cls, name).set_cast
                    if isinstance(set_cast, list):
                        set_cast = set_cast[-1]
                    setattr(
                        ret, name, set_cast.from_json(
                            json.dumps({name: value})
                        ) if hasattr(set_cast, "from_json")
                        else set_cast.from_dict({name: value})
                    )
                except AttributeError:
                    setattr(ret, name, value)
        return ret
