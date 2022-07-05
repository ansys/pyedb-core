"""This module performs conversions from arbitrary user input to explicit types."""

import ansys.edb.core.models.geometries as geometries
import ansys.edb.core.utility.value as value


def to_value(val):
    """Take a value implicitly convertible to Value and return as Value.

    Parameters
    ----------
    val : ansys.edb.core.typing.ValueLike

    Returns
    -------
    ansys.edb.core.utility.value.Value
    """
    if isinstance(val, value.Value):
        return val
    elif type(val) in [int, float, complex, str]:
        return value.Value(val)
    else:
        raise TypeError("value-like objects must be either of type Value or int/float/complex/str.")


def to_point(val):
    """Take a value implicitly convertible to PointData and return as PointData.

    Parameters
    ----------
    val : ansys.edb.core.typing.PointLike

    Returns
    -------
    ansys.edb.core.models.geometries.point_data.PointData
    """
    if isinstance(val, geometries.point_data.PointData):
        return val
    try:
        if len(val) == 2:
            return geometries.point_data.PointData(val)
    except TypeError:
        return geometries.point_data.PointData(val)

    raise TypeError(
        "point-like objects must be either of type PointData or a list/tuple containing (start, end) or (arc_height)."
    )
