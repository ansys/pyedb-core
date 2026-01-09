"""Build123d-based computation backend for point operations."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.geometry.point_data import PointData
    from ansys.edb.core.typing import PointLike

from ansys.edb.core.geometry.backends.point_backend_base import PointBackend

try:
    import build123d  # noqa: F401

    BUILD123D_AVAILABLE = True
except ImportError:
    BUILD123D_AVAILABLE = False


class PointBuild123dBackend(PointBackend):
    """Build123d-based computation backend for point operations.

    This backend performs computations locally using the Build123d library,
    reducing the number of RPC calls to the server and improving performance.

    Raises
    ------
    ImportError
        If Build123d is not installed.
    """

    def __init__(self, stub=None):
        """Initialize the Build123d backend.

        Parameters
        ----------
        stub : point_data_pb2_grpc.PointDataServiceStub, optional
            The gRPC stub for point operations. May be required for operations
            that need to delegate to the server backend.

        Raises
        ------
        ImportError
            If Build123d is not installed.
        """
        if not BUILD123D_AVAILABLE:
            raise ImportError(
                "Build123d is required for PointBuild123dBackend but is not installed"
            )
        self._stub = stub

    def closest(self, point: PointData, start: PointLike, end: PointLike) -> PointData:
        """Get the closest point on a line segment from the point using Build123d.

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
        # TODO: Implement using Build123d
        raise NotImplementedError("closest method not yet implemented for Build123d backend")

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
        # TODO: Implement using Build123d
        raise NotImplementedError("distance method not yet implemented for Build123d backend")

    def rotate(self, point: PointData, angle: float, center: PointLike) -> PointData:
        """Rotate a point at a given center by a given angle using Build123d.

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
        # TODO: Implement using Build123d
        raise NotImplementedError("rotate method not yet implemented for Build123d backend")
