"""Server-based computation backend."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.geometry.polygon_data import PolygonData

from ansys.edb.core.geometry.backends.base import PolygonBackend
from ansys.edb.core.inner import messages


class ServerBackend(PolygonBackend):
    """Server-based computation backend.

    This backend delegates all computations to the RPC server.
    """

    def __init__(self, stub):
        """Initialize the server backend.

        Parameters
        ----------
        stub : polygon_data_pb2_grpc.PolygonDataServiceStub
            The gRPC stub for polygon operations.
        """
        self._stub = stub

    def area(self, polygon: PolygonData) -> float:
        """Compute the area of a polygon using the server.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to compute area for.

        Returns
        -------
        float
            Area of the polygon.
        """
        return self._stub.GetArea(messages.polygon_data_message(polygon)).value

    def is_convex(self, polygon: PolygonData) -> bool:
        """Determine whether the polygon is convex using the server.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to check.

        Returns
        -------
        bool
            ``True`` when the polygon is convex, ``False`` otherwise.
        """
        return self._stub.IsConvex(messages.polygon_data_message(polygon)).value

    def is_inside(self, polygon: PolygonData, point: tuple[float, float]) -> bool:
        """Determine whether a point is inside the polygon using the server.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to check.
        point : tuple[float, float]
            Point coordinates (x, y).

        Returns
        -------
        bool
            ``True`` if the point is inside the polygon, ``False`` otherwise.
        """
        return self._stub.IsInside(messages.polygon_data_with_point_message(polygon, point)).value

    def bbox(self, polygon: PolygonData) -> tuple[tuple[float, float], tuple[float, float]]:
        """Compute the bounding box of a polygon using the server.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to compute bounding box for.

        Returns
        -------
        tuple[tuple[float, float], tuple[float, float]]
            Bounding box as ((min_x, min_y), (max_x, max_y)).
        """
        from ansys.edb.core.inner import parser

        result = self._stub.GetBBox(messages.polygon_data_list_message([polygon]))
        lower_left, upper_right = parser.to_box(result)
        return (
            (lower_left.x.double, lower_left.y.double),
            (upper_right.x.double, upper_right.y.double),
        )

    def bbox_of_polygons(
        self, polygons: list[PolygonData]
    ) -> tuple[tuple[float, float], tuple[float, float]]:
        """Compute the bounding box of a list of polygons using the server.

        Parameters
        ----------
        polygons : list[PolygonData]
            List of polygons to compute bounding box for.

        Returns
        -------
        tuple[tuple[float, float], tuple[float, float]]
            Bounding box as ((min_x, min_y), (max_x, max_y)).
        """
        from ansys.edb.core.inner import parser
        from ansys.edb.core.geometry.polygon_data import PolygonData

        result = self._stub.GetStreamedBBox(PolygonData._polygon_data_request_iterator(polygons))
        lower_left, upper_right = parser.to_box(result)
        return (
            (lower_left.x.double, lower_left.y.double),
            (upper_right.x.double, upper_right.y.double),
        )
