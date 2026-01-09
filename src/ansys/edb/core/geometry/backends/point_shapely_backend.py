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

    @staticmethod
    def _to_shapely_point(point_data: PointData) -> Point:
        """Convert a PointData to a Shapely Point with caching.

        Parameters
        ----------
        point_data : PointData
            The point to convert.

        Returns
        -------
        Point
            Shapely Point object.

        Notes
        -----
        The Shapely Point is cached on the PointData instance to avoid
        repeated conversions.
        """
        if hasattr(point_data, "_shapely_cache"):
            return point_data._shapely_cache

        shapely_point = Point(point_data.x.double, point_data.y.double)

        point_data._shapely_cache = shapely_point
        return shapely_point

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
        from ansys.edb.core.geometry.point_data import PointData

        if isinstance(start, PointData):
            start = [start.x.double, start.y.double]
        if isinstance(end, PointData):
            end = [end.x.double, end.y.double]

        p = self._to_shapely_point(point)
        line = LineString([start, end])

        distance_along_line = line.project(p)
        closest_point = line.interpolate(distance_along_line)

        return PointData(closest_point.x, closest_point.y)

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
