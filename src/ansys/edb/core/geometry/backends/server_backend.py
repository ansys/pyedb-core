"""Server-based computation backend."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.geometry.polygon_data import PolygonData

from ansys.edb.core.geometry.backends.base import PolygonBackend
from ansys.edb.core.inner import messages, parser


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
        from ansys.edb.core.geometry.polygon_data import PolygonData

        result = self._stub.GetStreamedBBox(PolygonData._polygon_data_request_iterator(polygons))
        lower_left, upper_right = parser.to_box(result)
        return (
            (lower_left.x.double, lower_left.y.double),
            (upper_right.x.double, upper_right.y.double),
        )

    @parser.to_polygon_data
    def without_arcs(
        self,
        polygon: PolygonData,
        max_chord_error: float = 0,
        max_arc_angle: float = math.pi / 6,
        max_points: int = 8,
    ) -> PolygonData:
        """Get polygon data with all arcs removed using the server.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to process.
        max_chord_error : float, default: 0
            Maximum allowed chord error for arc tessellation.
        max_arc_angle : float, default: math.pi / 6
            Maximum angle (in radians) for each arc segment.
        max_points : int, default: 8
            Maximum number of points per arc.

        Returns
        -------
        PolygonData
            Polygon with all arcs tessellated into line segments.
        """

        result = self._stub.RemoveArcs(
            messages.polygon_data_remove_arc_message(
                polygon, max_chord_error, max_arc_angle, max_points
            )
        )
        return result

    def has_self_intersections(self, polygon: PolygonData, tol: float = 1e-9) -> bool:
        """Determine whether the polygon contains any self-intersections using the server.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to check.
        tol : float, default: 1e-9
            Tolerance.

        Returns
        -------
        bool
            ``True`` when the polygon contains self-intersections, ``False`` otherwise.
        """
        return self._stub.HasSelfIntersections(
            messages.polygon_data_with_tol_message(polygon, tol)
        ).value

    @parser.to_polygon_data_list
    def remove_self_intersections(self, polygon: PolygonData, tol: float = 1e-9) -> list[PolygonData]:
        """Remove self-intersections from a polygon using the server.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to process.
        tol : float, default: 1e-9
            Tolerance.

        Returns
        -------
        list[PolygonData]
            A list of non self-intersecting polygons.
        """

        result = self._stub.RemoveSelfIntersections(
            messages.polygon_data_with_tol_message(polygon, tol)
        )
        return result

    @parser.to_point_data_list
    def normalized(self, polygon: PolygonData) -> list:
        """Get the normalized points of the polygon using the server.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to process.

        Returns
        -------
        list[PointData]
            List of normalized points.
        """

        # return self._stub.GetNormalizedPoints(messages.polygon_data_message(polygon)).points  # The server implementation does not look correct.

        from ansys.edb.core.geometry.point_data import PointData
        
        # Note: The server's GetNormalizedPoints currently returns the original points,
        # not the normalized ones. As a workaround, we normalize the points client-side.
        normalized_points = []
        for point in polygon.points:
            # Normalize each point using the PointData.normalized() method
            normalized_points.append(point.normalized())
        
        return normalized_points

    @parser.to_polygon_data
    def move(self, polygon: PolygonData, vector: tuple[float, float]) -> PolygonData:
        """Move the polygon by a vector using the server.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to move.
        vector : tuple[float, float]
            Vector coordinates (x, y).

        Returns
        -------
        PolygonData
            Moved polygon.
        """

        result = self._stub.Transform(messages.polygon_data_transform_message("move", polygon, vector))
        return result

    @parser.to_polygon_data
    def rotate(self, polygon: PolygonData, angle: float, center: tuple[float, float]) -> PolygonData:
        """Rotate the polygon at a center by an angle using the server.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to rotate.
        angle : float
            Angle in radians.
        center : tuple[float, float]
            Center coordinates (x, y).

        Returns
        -------
        PolygonData
            Rotated polygon.
        """

        result = self._stub.Transform(messages.polygon_data_transform_message("rotate", polygon, angle, center))
        return result
