"""Shapely-based computation backend for arc operations (template).

This file provides a lightweight template containing the overall structure of
an Arc backend that uses Shapely for local computations. Implementations for
each method should be filled in later.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from ansys.edb.core.geometry.point_data import PointData

if TYPE_CHECKING:
    from ansys.edb.core.geometry.arc_data import ArcData
    from ansys.edb.core.typing import PointLike

from ansys.edb.core.geometry.backends.arc_backend_base import ArcBackend

try:
    # Import shapely modules you will need when implementing methods
    from shapely.geometry import Point  # noqa: F401

    SHAPELY_AVAILABLE = True
except ImportError:
    SHAPELY_AVAILABLE = False


class ArcShapelyBackend(ArcBackend):
    """Shapely-based computation backend for arc operations.

    This template exposes the public API that `ArcData` expects from a backend.
    Each method currently raises NotImplementedError and should be implemented
    using Shapely primitives when you populate the template.

    Raises
    ------
    ImportError
        If Shapely is not installed.
    """

    def __init__(self, stub=None):
        """Initialize the Shapely arc backend.

        Parameters
        ----------
        stub : optional
            gRPC stub to allow delegating to server-backed computations when
            necessary.
        """
        if not SHAPELY_AVAILABLE:
            raise ImportError("Shapely is required for ArcShapelyBackend but is not installed")
        self._stub = stub

    def center(self, arc: "ArcData") -> "PointLike":
        """Return the center point of the arc."""
        height = arc.height

        x1, y1 = arc.start.x.double, arc.start.y.double
        x2, y2 = arc.end.x.double, arc.end.y.double

        chord_dx = x2 - x1
        chord_dy = y2 - y1
        chord_length = math.sqrt(chord_dx * chord_dx + chord_dy * chord_dy)

        if math.isclose(height, 0.0, abs_tol=1e-12):
            if math.isclose(chord_length, 0.0, abs_tol=1e-12):
                return PointData(x2, y2)
            return PointData(math.nan, math.nan)

        h = abs(height)
        radius = (h**2 + (chord_length / 2) ** 2) / (2 * h)

        chord_mid_x = (x1 + x2) / 2
        chord_mid_y = (y1 + y2) / 2

        # If the chord_length is zero, assume the perpendicular vector as (-1.0, 0.0).
        perp_dx = -1.0
        perp_dy = 0.0
        if not math.isclose(chord_length, 0.0, abs_tol=1e-12):
            perp_dx = chord_dy / chord_length
            perp_dy = -chord_dx / chord_length

        if height < 0:
            center_x = chord_mid_x - perp_dx * (radius + height)
            center_y = chord_mid_y - perp_dy * (radius + height)
        else:
            center_x = chord_mid_x + perp_dx * (radius - height)
            center_y = chord_mid_y + perp_dy * (radius - height)

        return PointData(center_x, center_y)

    def midpoint(self, arc: "ArcData") -> "PointLike":
        """Return the midpoint of the arc."""
        height = arc.height

        x1, y1 = arc.start.x.double, arc.start.y.double
        x2, y2 = arc.end.x.double, arc.end.y.double

        if math.isclose(height, 0.0, abs_tol=1e-12):
            return PointData(0.5 * (x1 + x2), 0.5 * (y1 + y2))

        chord_dx = x2 - x1
        chord_dy = y2 - y1
        chord_length = math.sqrt(chord_dx * chord_dx + chord_dy * chord_dy)

        if math.isclose(chord_length, 0.0, abs_tol=1e-12):
            return PointData(x2, y2)

        chord_mid_x = (x1 + x2) / 2
        chord_mid_y = (y1 + y2) / 2

        perp_dx = chord_dy / chord_length
        perp_dy = -chord_dx / chord_length

        mid_x = chord_mid_x - perp_dx * height
        mid_y = chord_mid_y - perp_dy * height

        return PointData(mid_x, mid_y)

    def radius(self, arc: "ArcData") -> float:
        """Return the radius of the arc."""
        height = arc.height

        x1, y1 = arc.start.x.double, arc.start.y.double
        x2, y2 = arc.end.x.double, arc.end.y.double

        chord_dx = x2 - x1
        chord_dy = y2 - y1
        chord_length = math.sqrt(chord_dx * chord_dx + chord_dy * chord_dy)

        if math.isclose(height, 0.0, abs_tol=1e-12):
            if math.isclose(chord_length, 0.0, abs_tol=1e-12):
                return 0.0
            return math.inf

        h = abs(height)
        radius = (h**2 + (chord_length / 2) ** 2) / (2 * h)

        return radius

    def bbox(self, arc: "ArcData") -> object:
        """Return the bounding box / polygon representing arc bounds."""
        raise NotImplementedError("bbox is not implemented yet")

    def is_point(self, arc: "ArcData", tolerance: float = 0.0) -> bool:
        """Return True when the arc is effectively a point."""
        raise NotImplementedError("is_point is not implemented yet")

    def is_segment(self, arc: "ArcData", tolerance: float = 0.0) -> bool:
        """Return True when the arc is effectively a straight segment."""
        raise NotImplementedError("is_segment is not implemented yet")

    def angle(self, arc: "ArcData", other: "ArcData" | None = None) -> float:
        """Compute the angle for this arc or between two arcs."""
        raise NotImplementedError("angle is not implemented yet")

    def length(self, arc: "ArcData") -> float:
        """Return the length of the arc (circumference or segment length)."""
        raise NotImplementedError("length is not implemented yet")

    def points(self, arc: "ArcData") -> list["PointLike"]:
        """Return representative points for the arc (start, height, end)."""
        raise NotImplementedError("points is not implemented yet")

    def closest_points(self, arc1: "ArcData", arc2: "ArcData") -> tuple["PointLike", "PointLike"]:
        """Return the pair of closest points between two arcs."""
        raise NotImplementedError("closest_points is not implemented yet")
