#!/usr/bin/env python
# coding=utf-8

"""Helper functions."""


def reduce_with_index(fn, iterable, start=None, *args, **kwargs):
    """
    A wrapper of functools.reduce, but this function puts index to fn.

    Parameters:
        fn: The function that should be called. fn requires the following
            parameters in the order: [target, element, index]. For details,
            see "Required parameters for fn" section
        it: The iteratable object.
        start: The same of "initializer" at reduce on the official
            python document.
        *args, **kwargs: Any arguments to be passed into fn

    Required Parameters for fn:
        target: target object to manipulate. This is the same maning of x at
        reduce on the official python document.
        element: An element in the iteratable object.
        index: The position of element in the iteratable object.
    """
    it = iter(iterable)
    if start is None:
        try:
            start = next(it)
        except StopIteration:
            raise TypeError(
                'reduce_with_index() of empty sequence with no initial value'
            )
    accum_value = start
    for index, x in enumerate(it):
        accum_value = fn(accum_value, x, index, *args, **kwargs)
    return accum_value


def shrink_list(lst, value=None):
    """
    Shrink list by specified value. By default, the value is None.

    Parameters:
        value: When this variable is specified, The element is removed if
            it is the same of this variable. By default, None is specified.
            (The point is that None doesn't mean "Unspecified".)

    CAUTION:
        This function is destroyable operation.

    Example:
        [None, None, None, None] -- (shrink_list:value=None) --> []
        [1, 0, 0, 1, 0, 1] -- (shrink_list:value=1) --> [1, 0, 0, 1, 0]
    """
    while lst and lst[-1] == value:
        lst.pop()
    return lst
