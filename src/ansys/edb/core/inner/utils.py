"""This module contains utility functions for API development work."""


def map_list(iterable_to_operate_on, operator=None):
    """Apply the given operator to each member of an iterable and return the modified list.

    Parameters
    ---------
    iterable_to_operate on
    operator
    """
    return list(
        iterable_to_operate_on if operator is None else map(operator, iterable_to_operate_on)
    )
