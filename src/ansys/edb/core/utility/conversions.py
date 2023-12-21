"""This module performs conversions from arbitrary user input to explicit types."""
from ansys.api.edb.v1.edb_messages_pb2 import ValueMessage

from ansys.edb.core import geometry, utility


def to_value(val):
    """Take a value implicitly convertible to a ``Value``type and return as a ``Value`` type.

    Parameters
    ----------
    val : ansys.edb.core.typing.ValueLike

    Returns
    -------
    utility.Value
    """
    if isinstance(val, utility.Value):
        return val
    elif type(val) in [int, float, complex, str, ValueMessage]:
        return utility.Value(val)
    else:
        raise TypeError(
            f"Value-like objects must be either of type Value or int/float/complex/str. - Received '{val}'"
        )


def to_point(val):
    """Take a value implicitly convertible to a ``PointData`` type and return as a ``PointData`` type.

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
        "Point-like objects must be either of type PointData or a list/tuple containing (start, end) or (arc_height)."
    )


def to_point3d(val):
    """Convert a value to a ``Point3DData`` object.

    Parameters
    ----------
    val : geometry.Point3DData, tuple[:term:`ValueLike`,:term:`ValueLike`,:term:`ValueLike`]
        Value to convert.

    Returns
    -------
    geometry.Point3DData
    """
    if isinstance(val, geometry.Point3DData):
        return val
    if len(val) == 3:
        return geometry.Point3DData(val[0], val[1], val[2])
