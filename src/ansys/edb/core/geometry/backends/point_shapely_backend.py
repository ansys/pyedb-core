"""Shapely-based computation backend for point operations."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.geometry.point_data import PointData
    from ansys.edb.core.typing import PointLike

from ansys.edb.core.geometry.backends.point_backend_base import PointBackend

try:
    from shapely.geometry import LineString, Point  # noqa: F401

    SHAPELY_AVAILABLE = True
except ImportError:
    SHAPELY_AVAILABLE = False


class PointShapelyBackend(PointBackend):
    """Shapely-based computation backend for point operations.

    This backend performs computations locally using the Shapely library,
    reducing the number of RPC calls to the server and improving performance.

    Raises
    ------
    ImportError
        If Shapely is not installed.
    """

    def __init__(self, stub=None):
        """Initialize the Shapely backend.

        Parameters
        ----------
        stub : point_data_pb2_grpc.PointDataServiceStub, optional
            The gRPC stub for point operations. May be required for operations
            that need to delegate to the server backend.

        Raises
        ------
        ImportError
            If Shapely is not installed.
        """
        if not SHAPELY_AVAILABLE:
            raise ImportError("Shapely is required for PointShapelyBackend but is not installed")
        self._stub = stub

    def closest(self, point: PointData, start: PointLike, end: PointLike) -> PointData:
        """Get the closest point on a line segment from the point using Shapely.

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
        # TODO: Implement using Shapely
        raise NotImplementedError("closest method not yet implemented for Shapely backend")

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
        # TODO: Implement using Shapely
        raise NotImplementedError("distance method not yet implemented for Shapely backend")

    def rotate(self, point: PointData, angle: float, center: PointLike) -> PointData:
        """Rotate a point at a given center by a given angle using Shapely.

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
        # TODO: Implement using Shapely
        raise NotImplementedError("rotate method not yet implemented for Shapely backend")
