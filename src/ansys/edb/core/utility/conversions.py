"""This module performs conversions from arbitrary user input to explicit types."""

from ansys.edb.core import geometry, utility


def to_value(val):
    """Take a value implicitly convertible to Value and return as Value.

    Parameters
    ----------
    val : ansys.edb.core.typing.ValueLike

    Returns
    -------
    utility.Value
    """
    if isinstance(val, utility.Value):
        return val
    elif type(val) in [int, float, complex, str]:
        return utility.Value(val)
    else:
        raise TypeError(
            f"value-like objects must be either of type Value or int/float/complex/str. - Received '{val}'"
        )


def to_point(val):
    """Take a value implicitly convertible to PointData and return as PointData.

    Parameters
    ----------
    val : ansys.edb.core.typing.PointLike

    Returns
    -------
    geometry.PointData
    """
    if isinstance(val, geometry.PointData):
        return val
    try:
        if len(val) == 2:
            return geometry.PointData(val)
    except TypeError:
        return geometry.PointData(val)

    raise TypeError(
        "point-like objects must be either of type PointData or a list/tuple containing (start, end) or (arc_height)."
    )
