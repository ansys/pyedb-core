"""This module parses message back to client data types."""
import ansys.edb.core.models.geometries as geometries


def to_point_data(point_message):
    """Convert PointMessage to PointData.

    Parameters
    ----------
    point_message : ansys.api.edb.v1.point_data_pb2.PointMessage

    Returns
    -------
    ansys.edb.core.models.geometries.point_data.PointData
    """
    return geometries.point_data.PointData([point_message.x, point_message.y])
