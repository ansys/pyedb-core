"""Abstract base class for point computation backends."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.geometry.point_data import PointData
    from ansys.edb.core.typing import PointLike


class PointBackend(ABC):
    """Abstract base class for point computation backends.

    This class defines the interface that all computation backends must implement.
    Backends handle geometry operations that can be performed either on the server
    or locally using libraries like Shapely or Build123d.
    """

    @abstractmethod
    def closest(self, point: PointData, start: PointLike, end: PointLike) -> PointData:
        """Get the closest point on a line segment from the point.

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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def rotate(self, point: PointData, angle: float, center: PointLike) -> PointData:
        """Rotate a point at a given center by a given angle.

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
        pass
