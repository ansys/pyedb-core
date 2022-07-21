"""This module parses message back to client data types."""

from ansys.edb.core import geometry, utility


def to_point_data(point_message):
    """Convert PointMessage to PointData.

    Parameters
    ----------
    point_message : ansys.api.edb.v1.point_data_pb2.PointMessage

    Returns
    -------
    geometry.PointData
    """
    return geometry.PointData([utility.Value(point_message.x), utility.Value(point_message.y)])


def to_polygon_data(message):
    """Convert arbitrary message to PolygonData if possible.

    Parameters
    ----------
    message : ansys.api.edb.v1.point_data.BoxMessage

    Returns
    -------
    PolygonData
    """
    if hasattr(message, "lower_left") and hasattr(message, "upper_right"):
        return geometry.PolygonData(
            lower_left=to_point_data(message.lower_left),
            upper_right=to_point_data(message.upper_right),
        )
    else:
        raise TypeError(
            "message must respond to 'lower_left/upper_right' to be able to convert to PolygonData."
            f"A message of type {type(message)} received."
        )
