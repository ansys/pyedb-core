"""This module performs conversions from arbitrary user input to explicit types."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.typing import ValueLike, PointLike, Point3DLike

from ansys.api.edb.v1.edb_messages_pb2 import ValueMessage

from ansys.edb.core.geometry import point3d_data, point_data
from ansys.edb.core.utility import value


def to_value(val: ValueLike) -> value.Value:
    """Take a value implicitly convertible to a :class:`.Value` type and return as a :class:`.Value` type.

    Parameters
    ----------
    val : :term:`ValueLike`

    Returns
    -------
    .Value
    """
    if isinstance(val, value.Value):
        return val
    elif type(val) in [int, float, complex, str, ValueMessage]:
        return value.Value(val)
    else:
        raise TypeError(
            f"Value-like objects must be either of type Value or int/float/complex/str. - Received '{val}'"
        )


def to_point(val: PointLike) -> point_data.PointData:
    """Take a value implicitly convertible to a :class:`.PointData` type and return as a :class:`.PointData` type.

    Parameters
    ----------
    val : :term:`Point2DLike`

    Returns
    -------
    .PointData
    """
    if isinstance(val, point_data.PointData):
        return val
    try:
        if len(val) == 2:
            return point_data.PointData(val)
    except TypeError:
        return point_data.PointData(val)

    raise TypeError(
        "Point-like objects must be either of type PointData or a list/tuple containing (start, end) or (arc_height)."
    )


def to_point3d(val: Point3DLike) -> point3d_data.Point3DData:
    """Take a value implicitly convertible to a :class:`.Point3DData` type and return as a :class:`.Point3DData` type.

    Parameters
    ----------
    val : :term:`Point3DLike`

    Returns
    -------
    .Point3DData
    """
    if isinstance(val, point3d_data.Point3DData):
        return val
    if len(val) == 3:
        return point3d_data.Point3DData(val[0], val[1], val[2])
