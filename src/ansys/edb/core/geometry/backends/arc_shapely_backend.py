"""Shapely-based computation backend for arc operations (template).

This file provides a lightweight template containing the overall structure of
an Arc backend that uses Shapely for local computations. Implementations for
each method should be filled in later.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.geometry.arc_data import ArcData
    from ansys.edb.core.typing import PointLike

from ansys.edb.core.geometry.backends.arc_backend_base import ArcBackend

try:
    from shapely.geometry import LineString as ShapelyLineString

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

    def _to_shapely_linestring(
        self,
        arc: ArcData,
        max_chord_error: float = 0,
        max_arc_angle: float = math.pi / 6,
        max_points: int = 8,
    ) -> ShapelyLineString:
        """Convert a ArcData object to a Shapely Wire.

        Parameters
        ----------
        arc : ArcData
            The arc to convert.
        max_chord_error : float, default: 0
            Maximum allowed chord error for arc tessellation.
        max_arc_angle : float, default: math.pi / 6
            Maximum angle (in radians) for each arc segment.
        max_points : int, default: 8
            Maximum number of points per arc.

        Returns
        -------
        ShapelyLineString
            Shapely line string object.

        Notes
        -----
        This method handles:
        - Converting points to coordinate tuples
        - Handling holes in polygons
        - Approximating arcs with line segments locally (no server calls)
        - Caching the result on the PolygonData instance to avoid repeated conversions

        Arc tessellation is performed locally using mathematical calculations
        based on the arc height (sagitta) which represents the perpendicular
        distance from the chord midpoint to the arc.
        """
        # Check if we have a cached Shapely wire
        if hasattr(arc, "_shapely_cache"):
            return arc._shapely_cache

        # Extract coordinates and arc metadata, tessellating arcs locally
        result, arc._center, arc._midpoint, arc._radius = ArcBackend._tessellate_arc(
            arc, max_chord_error, max_arc_angle, max_points
        )

        # Create Shapely line string
        shapely_linestring = ShapelyLineString(result)

        # Cache the result for future use
        arc._shapely_cache = shapely_linestring
        arc.test = "sidhfkljashdfljka hsjdhsdalj"
        return shapely_linestring

    def center(self, arc: "ArcData") -> "PointLike":
        """Return the center point of the arc."""
        self._to_shapely_linestring(arc)

        return arc._center

    def midpoint(self, arc: "ArcData") -> "PointLike":
        """Return the midpoint of the arc."""
        self._to_shapely_linestring(arc)

        return arc._midpoint

    def radius(self, arc: "ArcData") -> float:
        """Return the radius of the arc."""
        self._to_shapely_linestring(arc)

        return arc._radius

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
