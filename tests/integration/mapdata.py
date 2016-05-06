#!/usr/bin/env python
# coding=utf-8

"""Mapping data for integration tests."""

import omm


class SimpleTestMapper(omm.Mapper):
    """Simple mapper."""

    name = omm.MapField("test.name")
    age = omm.MapField("test.age")
    sex = omm.MapField("test.sex")

    @staticmethod
    def generate_test_data(type_dict=False):
        """
        Generate test data.

        Parameters:
            type_dict: Set True if the data is expected to be typed as dict.
        """
        User = type("User", (object, ), {
            "name": "Test Example",
            "age": 960,
            "sex": None
        })
        gen_obj = type("GenObj", (object, ), {
            "test": User()
        })()

        return {
            "test": {
                "name": gen_obj.test.name,
                "age": gen_obj.test.age,
                "sex": gen_obj.test.sex
            }
        } if type_dict else gen_obj


class DictSimpleTestSchema(SimpleTestMapper):
    """Dict-based test mapper."""

    asdict = True


class ArrayMapTestSchema(omm.Mapper):
    """Array Mapper."""

    array = omm.MapField("test.array[1][1].correct")

    @staticmethod
    def generate_test_data(type_dict=False):
        """
        Generate test data.

        Parameters:
            type_dict: Set True if the data is expected to be typed as dict.
        """
        class ObjectClass(object):

            class Test(object):

                class ArrayElement(object):

                    def __init__(self, correct):
                        self.correct = correct

                def __init__(self):
                    self.array = [
                        [
                            type(self).ArrayElement(False),
                            type(self).ArrayElement(False)
                        ], [
                            type(self).ArrayElement(False),
                            type(self).ArrayElement(True)
                        ]
                    ]

            def __init__(self):
                self.test = type(self).Test()
        return {
            "test": {"array": [
                [{"correct": False}, {"correct": False}],
                [{"correct": False}, {"correct": True}]
            ]}
        } if type_dict else ObjectClass()


class ArrayMapDictTestSchema(ArrayMapTestSchema):
    """Array mapper (asdict)."""

    asdict = True
