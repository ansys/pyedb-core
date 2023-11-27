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
