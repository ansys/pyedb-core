# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Module containing shared decorators."""
import functools


def _as_array(array_or_item):
    try:
        iter(array_or_item)
        return array_or_item
    except TypeError:
        return [array_or_item]


def _self_as_param_class_method(fn):
    @functools.wraps(fn)
    def wrapper(first, second):
        return fn(_as_array(first), _as_array(second))

    return wrapper


def _self_as_param_instance_method(fn, instance):
    @functools.wraps(fn)
    def wrapper(other):
        return fn(_as_array(instance), _as_array(other))

    return wrapper


class self_as_param(classmethod):  # noqa
    def __init__(self, func):
        """Initialize a decorator."""
        super().__init__(func)

    def __get__(self, instance, owner):
        """Fetch decorated function."""
        fn = super().__get__(instance, owner)
        if instance is None:
            return _self_as_param_class_method(fn)
        else:
            return _self_as_param_instance_method(fn, instance)
