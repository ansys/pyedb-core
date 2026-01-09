"""Server-based computation backend for point operations."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.geometry.point_data import PointData
    from ansys.edb.core.typing import PointLike

from ansys.edb.core.geometry.backends.point_backend_base import PointBackend
from ansys.edb.core.inner import messages, parser


class PointServerBackend(PointBackend):
    """Server-based computation backend for point operations.

    This backend delegates all computations to the RPC server.
    """

    def __init__(self, stub):
        """Initialize the server backend.

        Parameters
        ----------
        stub : point_data_pb2_grpc.PointDataServiceStub
            The gRPC stub for point operations.
        """
        self._stub = stub

    @parser.to_point_data
    def closest(self, point: PointData, start: PointLike, end: PointLike) -> PointData:
        """Get the closest point on a line segment from the point using the server.

        Parameters
        ----------
        point : PointData
            The point to find the closest point from.
        start : PointLike
            Start point of the line segment.
        end : PointLike
            End point of the line segment.

        Returns
        -------
        PointData
            Closest point on the line segment.
        """
        return self._stub.ClosestPoint(messages.point_data_with_line_message(point, start, end))

    def distance(self, point: PointData, start: PointLike, end: PointLike = None) -> float:
        """Compute the shortest distance from the point to a line segment or another point.

        Parameters
        ----------
        point : PointData
            The point to compute distance from.
        start : PointLike
            Start point of the line segment or the other point.
        end : PointLike, default: None
            End point of the line segment. If None, compute distance between two points.

        Returns
        -------
        float
            Distance value.
        """
        if end is None:
            return (point - start).magnitude()
        else:
            return self._stub.Distance(
                messages.point_data_with_line_message(point, start, end)
            ).value

    @parser.to_point_data
    def rotate(self, point: PointData, angle: float, center: PointLike) -> PointData:
        """Rotate a point at a given center by a given angle using the server.

        Parameters
        ----------
        point : PointData
            The point to rotate.
        angle : float
            Angle in radians.
        center : PointLike
            Center of rotation.

        Returns
        -------
        PointData
            Rotated point.
        """
        return self._stub.Rotate(messages.point_data_rotate_message(point, center, angle))
