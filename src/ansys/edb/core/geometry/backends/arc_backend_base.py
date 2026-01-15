"""Abstract base class for arc computation backends.

Defines the interface that all arc computation backends must implement.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.geometry.arc_data import ArcData
    from ansys.edb.core.geometry.point_data import PointData
    from ansys.edb.core.geometry.polygon_data import PolygonData


class ArcBackend(ABC):
    """Abstract base class for arc computation backends.

    Backends perform operations that can be executed either on the server or
    locally using libraries such as Shapely or Build123d. Implementations must
    provide the methods declared below.
    """

    @abstractmethod
    def center(self, arc: "ArcData") -> "PointData":
        """Return the center point of the arc."""
        pass

    @abstractmethod
    def midpoint(self, arc: "ArcData") -> "PointData":
        """Return the midpoint of the arc."""
        pass

    @abstractmethod
    def radius(self, arc: "ArcData") -> float:
        """Return the radius of the arc."""
        pass

    @abstractmethod
    def bbox(self, arc: "ArcData") -> "PolygonData":
        """Return the bounding box (polygon) of the arc."""
        pass

    @abstractmethod
    def closest_points(self, arc1: "ArcData", arc2: "ArcData") -> tuple["PointData", "PointData"]:
        """Return the pair of closest points between two arcs."""
        pass

    @abstractmethod
    def angle(self, arc: "ArcData", other: "ArcData" | None = None) -> float:
        """Return the angle of the arc or the angle between two arcs."""
        pass

    @abstractmethod
    def length(self, arc: "ArcData") -> float:
        """Return the length of the arc."""
        pass

    @abstractmethod
    def points(self, arc: "ArcData") -> list["PointData"]:
        """Return representative points for the arc (start, height, end)."""
        pass
