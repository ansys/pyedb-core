"""This module performs conversions from arbitrary user input to explicit types."""
from ansys.api.edb.v1.edb_messages_pb2 import ValueMessage


def to_value(val):
    """Take a value implicitly convertible to Value and return as Value.

    Parameters
    ----------
    val : ansys.edb.core.typing.ValueLike

    Returns
    -------
    utility.Value
    """
    from ansys.edb.core.utility.value import Value

    if isinstance(val, Value):
        return val
    elif type(val) in [int, float, complex, str, ValueMessage]:
        return Value(val)
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
    from ansys.edb.core.geometry.point_data import PointData

    if isinstance(val, PointData):
        return val
    try:
        if len(val) == 2:
            return PointData(val)
    except TypeError:
        return PointData(val)

    raise TypeError(
        "point-like objects must be either of type PointData or a list/tuple containing (start, end) or (arc_height)."
    )


def to_point3d(val):
    """Convert a value to Point3DData object.

    Parameters
    ----------
    val : geometry.Point3DData, tuple[:term:`ValueLike`,:term:`ValueLike`,:term:`ValueLike`]

    Returns
    -------
    geometry.Point3DData
    """
    from ansys.edb.core.geometry.point3d_data import Point3DData

    if isinstance(val, Point3DData):
        return val
    if len(val) == 3:
        return Point3DData(val[0], val[1], val[2])
