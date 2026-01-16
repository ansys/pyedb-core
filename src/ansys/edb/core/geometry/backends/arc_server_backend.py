"""Server-based computation backend for arc operations (template).

This backend delegates arc-related computations to the RPC server via a stub.
The file is a minimal, ready-to-fill template consistent with the other server
backend implementations in this package.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.geometry.arc_data import ArcData
    from ansys.edb.core.geometry.point_data import PointData
    from ansys.edb.core.geometry.polygon_data import PolygonData

from ansys.edb.core.geometry.backends.arc_backend_base import ArcBackend
from ansys.edb.core.geometry.point_data import PointData
from ansys.edb.core.inner import messages, parser


class ArcServerBackend(ArcBackend):
    """Server-based computation backend for arc operations.

    This backend delegates computations to the RPC server using messages defined
    in `ansys.edb.core.inner.messages` and wraps responses using parser
    decorators to return local data objects.
    """

    def __init__(self, stub):
        """Initialize the server backend.

        Parameters
        ----------
        stub : arc_data_pb2_grpc.ArcDataServiceStub
            The gRPC stub for arc operations.
        """
        self._stub = stub

    def center(self, arc: "ArcData") -> "PointData":
        """Get the center point of the arc from the server."""
        return self._stub.GetCenter(messages.arc_message(arc))

    def midpoint(self, arc: "ArcData") -> "PointData":
        """Get the midpoint of the arc from the server."""
        return self._stub.GetMidpoint(messages.arc_message(arc))

    def radius(self, arc: "ArcData") -> float:
        """Get the radius of the arc from the server."""
        return self._stub.GetRadius(messages.arc_message(arc)).value

    def bbox(self, arc: "ArcData") -> "PolygonData":
        """Get the bounding box (polygon) of the arc from the server."""
        return self._stub.GetBoundingBox(messages.arc_message(arc))

    @parser.to_box
    def closest_points(self, arc1: "ArcData", arc2: "ArcData") -> tuple["PointData", "PointData"]:
        """Get closest points between two arcs from the server."""
        return self._stub.ClosestPoints(messages.arc_data_two_points(arc1, arc2))

    def angle(self, arc: "ArcData", other: "ArcData" | None = None) -> float:
        """Get the angle of the arc or between two arcs from the server."""
        if other is None:
            return self._stub.GetAngle(messages.arc_message(arc)).value
        return self._stub.GetAngleBetween(messages.arc_data_two_points(arc, other)).value

    def length(self, arc: "ArcData") -> float:
        """Get the length of the arc from the server."""
        if arc.is_segment():
            return arc.start.distance(arc.end)
        return abs(self._stub.GetAngle(messages.arc_message(arc)).value * self.radius(arc))

    def points(self, arc: "ArcData") -> list["PointData"]:
        """Return representative points for the arc using server data."""
        return [arc.start, PointData(arc.height), arc.end]
