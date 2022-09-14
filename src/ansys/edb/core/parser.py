"""This module parses message back to client data types."""

import functools

from ansys.edb import geometry, utility


def to_point_data(fn):
    """Decorate a function that returns a message to return as PointData."""
    return _wraps(fn, _to_point_data)


def to_point_data_list(fn):
    """Decorate a function that returns a message to return as list[PointData]."""
    return _wraps(fn, _to_point_data_list)


def to_polygon_data(fn):
    """Decorate a function that returns a message to return as PolygonData."""
    return _wraps(fn, _to_polygon_data)


def to_polygon_data_list(fn):
    """Decorate a function that returns a message to return as list[PolygonData]."""
    return _wraps(fn, _to_polygon_data_list)


def to_box(fn):
    """Decorate a function that returns a message to return as (lower_left, upper_right)."""
    return _wraps(fn, _to_box)


def to_circle(fn):
    """Decorate a function that returns a message to return as (center, radius)."""
    return _wraps(fn, _to_circle)


def _wraps(fn, wrapper_fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return wrapper_fn(fn(*args, **kwargs))

    return wrapper


def _to_point_data(message):
    """Convert PointMessage to PointData.

    Parameters
    ----------
    message : ansys.api.edb.v1.point_data_pb2.PointMessage

    Returns
    -------
    geometry.PointData
    """
    return geometry.PointData([utility.Value(message.x), utility.Value(message.y)])


def _to_point_data_list(message):
    """Convert a message to list of PointData.

    Parameters
    ----------
    message : list[ansys.api.edb.v1.point_data_pb2.PointMessage]

    Returns
    -------
    list[geometry.PointData]
    """
    return [_to_point_data(m) for m in message]


def _to_polygon_data(message):
    """Convert arbitrary message to PolygonData if possible.

    Parameters
    ----------
    message : ansys.api.edb.v1.point_data_pb2.BoxMessage

    Returns
    -------
    geometry.PolygonData
    """
    b = _to_box(message)
    if b is not None:
        return geometry.PolygonData(lower_left=b[0], upper_right=b[1])
    else:
        raise TypeError(
            "message must respond to 'lower_left/upper_right' to be able to convert to PolygonData."
            f"A message of type {type(message)} received."
        )


def _to_polygon_data_list(message):
    """Convert arbitrary messages to list of PolygonData if possible.

    Returns
    -------
    list[geometry.PolygonData]
    """
    if hasattr(message, "polygons"):
        return [_to_polygon_data(m) for m in message.polygons]
    elif hasattr(message, "points"):
        return [_to_polygon_data(m) for m in message.points]
    else:
        return [_to_polygon_data(m) for m in message]


def _to_box(message):
    """Convert message to box.

    Parameters
    ----------
    message : ansys.api.edb.v1.point_data_pb2.BoxMessage

    Returns
    -------
    tuple[geometry.PointData, geometry.PointData]
    """
    if hasattr(message, "lower_left") and hasattr(message, "upper_right"):
        return _to_point_data(message.lower_left), _to_point_data(message.upper_right)


def _to_circle(message):
    """Convert message to circle containing center point and radius.

    Parameters
    ----------
    message : ansys.api.edb.v1.point_data_pb2.CircleMessage

    Returns
    -------
    tuple[geometry.PointData, utility.Value]
    """
    if hasattr(message, "center") and hasattr(message, "radius"):
        return _to_point_data(message.center), utility.Value(message.radius)


def _to_rlc(message):
    """Convert message to rlc containing values related to resistance inductance capacitance.

    Parameters
    ----------
    message : ansys.api.edb.v1.rlc_pb2.RlcMessage

    Returns
    -------
    Rlc
    """
    if "msg" in message:
        rlc_msg = message["msg"]
        return utility.Rlc(
            utility.Value(rlc_msg.r),
            bool(rlc_msg.r_enabled.value),
            utility.Value(rlc_msg.l),
            bool(rlc_msg.l_enabled.value),
            utility.Value(rlc_msg.c),
            bool(rlc_msg.c_enabled.value),
            bool(rlc_msg.is_parallel.value),
        )
