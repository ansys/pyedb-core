"""Build123d-based computation backend for arc operations (template).

This file provides a lightweight template containing the overall structure of
an Arc backend that uses Build123d for local computations. Implementations for
each method should be filled in later.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.geometry.arc_data import ArcData
    from ansys.edb.core.typing import PointLike

from ansys.edb.core.geometry.backends.arc_backend_base import ArcBackend
from ansys.edb.core.geometry.backends.arc_shapely_backend import ArcShapelyBackend

try:
    import build123d  # noqa: F401

    BUILD123D_AVAILABLE = True
except ImportError:
    BUILD123D_AVAILABLE = False


class ArcBuild123dBackend(ArcBackend):
    """Build123d-based computation backend for arc operations.

    This template exposes the public API that `ArcData` expects from a backend.
    Each method currently raises NotImplementedError and should be implemented
    using Build123d primitives when you populate the template.

    Raises
    ------
    ImportError
        If Build123d is not installed.
    """

    def __init__(self, stub=None, **kwargs):
        """Initialize the Build123d arc backend.

        Parameters
        ----------
        stub : optional
            gRPC stub to allow delegating to server-backed computations when
            necessary.
        **kwargs
            Additional parameters passed to Shapely backend.
        """
        if not BUILD123D_AVAILABLE:
            raise ImportError("Build123d is required for ArcBuild123dBackend but is not installed")
        self._stub = stub
        self._shapely_backend = ArcShapelyBackend(stub=stub, **kwargs)

    def center(self, arc: "ArcData") -> "PointLike":
        """Return the center point of the arc."""
        return self._shapely_backend.center(arc)

    def midpoint(self, arc: "ArcData") -> "PointLike":
        """Return the midpoint of the arc."""
        return self._shapely_backend.midpoint(arc)

    def radius(self, arc: "ArcData") -> float:
        """Return the radius of the arc."""
        return self._shapely_backend.radius(arc)

    def bbox(self, arc: "ArcData") -> object:
        """Return the bounding box / polygon representing arc bounds."""
        raise NotImplementedError("bbox is not implemented yet")

    def angle(self, arc: "ArcData", other: "ArcData" | None = None) -> float:
        """Compute the angle for this arc or between two arcs."""
        raise NotImplementedError("angle is not implemented yet")

    def length(self, arc: "ArcData") -> float:
        """Return the length of the arc (circumference or segment length)."""
        raise NotImplementedError("length is not implemented yet")

    def closest_points(self, arc1: "ArcData", arc2: "ArcData") -> tuple["PointLike", "PointLike"]:
        """Return the pair of closest points between two arcs."""
        raise NotImplementedError("closest_points is not implemented yet")
