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

    def is_circle(self, polygon: PolygonData) -> bool:
        """Determine whether the outer contour of the polygon is a circle using the server.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to check.

        Returns
        -------
        bool
            ``True`` when the outer contour of the polygon is a circle, ``False`` otherwise.
        """
        return self._stub.IsCircle(messages.polygon_data_message(polygon)).value

    def is_box(self, polygon: PolygonData) -> bool:
        """Determine whether the outer contour of the polygon is a box using the server.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to check.

        Returns
        -------
        bool
            ``True`` when the outer contour of the polygon is a box, ``False`` otherwise.
        """
        return self._stub.IsBox(messages.polygon_data_message(polygon)).value

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
        return self._stub.HasSelfIntersections(messages.polygon_data_with_tol_message(polygon, tol)).value

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

        return self._stub.RemoveSelfIntersections(messages.polygon_data_with_tol_message(polygon, tol))

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

        return self._stub.GetNormalizedPoints(messages.polygon_data_message(polygon)).points

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

        return self._stub.Transform(messages.polygon_data_transform_message("move", polygon, vector))

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

        return self._stub.Transform(messages.polygon_data_transform_message("rotate", polygon, angle, center))

    @parser.to_polygon_data
    def scale(self, polygon: PolygonData, factor: float, center: tuple[float, float]) -> PolygonData:
        """Scale the polygon by a linear factor from a center using the server.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to scale.
        factor : float
            Linear scaling factor.
        center : tuple[float, float]
            Center coordinates (x, y).

        Returns
        -------
        PolygonData
            Scaled polygon.
        """

        return self._stub.Transform(messages.polygon_data_transform_message("scale", polygon, factor, center))

    @parser.to_polygon_data
    def mirror_x(self, polygon: PolygonData, x: float) -> PolygonData:
        """Mirror the polygon across a vertical line at x using the server.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to mirror.
        x : float
            X-coordinate of the vertical line to mirror across.

        Returns
        -------
        PolygonData
            Mirrored polygon.
        """

        result = self._stub.Transform(messages.polygon_data_transform_message("mirror_x", polygon, x))
        return result

    def bounding_circle(self, polygon: PolygonData) -> tuple[tuple[float, float], float]:
        """Compute the bounding circle of the polygon using the server.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to compute bounding circle for.

        Returns
        -------
        tuple[tuple[float, float], float]
            Bounding circle as ((center_x, center_y), radius).
        """
        from ansys.edb.core.utility.value import Value

        result = self._stub.GetBoundingCircle(messages.polygon_data_message(polygon))
        center = parser.msg_to_point_data(result.center)
        radius = Value(result.radius)
        return ((center.x.double, center.y.double), radius.double)

    @parser.to_polygon_data
    def convex_hull(self, polygons: list[PolygonData]) -> PolygonData:
        """Compute the convex hull of the union of a list of polygons using the server.

        Parameters
        ----------
        polygons : list[PolygonData]
            List of polygons.

        Returns
        -------
        PolygonData
            The convex hull polygon.
        """
        return self._stub.GetConvexHull(messages.polygon_data_list_message(polygons))

    @parser.to_polygon_data
    def defeature(self, polygon: PolygonData, tol: float = 1e-9) -> PolygonData:
        """Defeature a polygon by removing small features using the server.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to defeature.
        tol : float, default: 1e-9
            Tolerance for defeaturing.

        Returns
        -------
        PolygonData
            Defeatured polygon.
        """
        return self._stub.Defeature(messages.polygon_data_with_tol_message(polygon, tol))

    def intersection_type(self, polygon: PolygonData, other: PolygonData, tol: float = 1e-9):
        """Get the intersection type with another polygon using the server.

        Parameters
        ----------
        polygon : PolygonData
            The first polygon.
        other : PolygonData
            The second polygon.
        tol : float, default: 1e-9
            Tolerance.

        Returns
        -------
        int
            The intersection type enum value.
        """
        return self._stub.GetIntersectionType(
            messages.polygon_data_pair_with_tolerance_message(polygon, other, tol)
        ).intersection_type

    def circle_intersect(self, polygon: PolygonData, center: tuple[float, float], radius: float) -> bool:
        """Determine whether a circle intersects with a polygon using the server.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to check.
        center : tuple[float, float]
            Center coordinates (x, y) of the circle.
        radius : float
            Radius of the circle.

        Returns
        -------
        bool
            ``True`` if the circle intersects with the polygon, ``False`` otherwise.
        """
        return self._stub.CircleIntersectsPolygon(
            messages.polygon_data_with_circle_message(polygon, center, radius)
        ).value

    @parser.to_point_data
    def closest_point(self, polygon: PolygonData, point: tuple[float, float]) -> tuple[float, float]:
        """Compute a point on the polygon that is closest to another point using the server.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to check.
        point : tuple[float, float]
            Point coordinates (x, y).

        Returns
        -------
        tuple[float, float]
            Coordinates (x, y) of the closest point on the polygon.
        """
        
        return self._stub.GetClosestPoints(messages.polygon_data_with_points_message(polygon, point=point)).points[0]

    @parser.to_polygon_data_list
    def unite(self, polygons: list[PolygonData]) -> list[PolygonData]:
        """Compute the union of a list of polygons using the server.

        Parameters
        ----------
        polygons : list[PolygonData]
            List of polygons to unite.

        Returns
        -------
        list[PolygonData]
            List of polygons resulting from the union.
        """
        return self._stub.GetUnion(messages.polygon_data_list_message(polygons))

    @parser.to_polygon_data_list
    def intersect(
        self, polygons1: list[PolygonData], polygons2: list[PolygonData]
    ) -> list[PolygonData]:
        """Compute the intersection of two lists of polygons using the server.

        Parameters
        ----------
        polygons1 : list[PolygonData]
            First list of polygons.
        polygons2 : list[PolygonData]
            Second list of polygons.

        Returns
        -------
        list[PolygonData]
            List of polygons resulting from the intersection.
        """
        return self._stub.GetIntersection(messages.polygon_data_pair_message(polygons1, polygons2))

    @parser.to_polygon_data_list
    def subtract(
        self, polygons1: list[PolygonData], polygons2: list[PolygonData]
    ) -> list[PolygonData]:
        """Subtract a set of polygons from another set of polygons using the server.

        Parameters
        ----------
        polygons1 : list[PolygonData]
            List of base polygons.
        polygons2 : list[PolygonData]
            List of polygons to subtract.

        Returns
        -------
        list[PolygonData]
            List of polygons resulting from the subtraction.
        """
        return self._stub.Subtract(messages.polygon_data_pair_message(polygons1, polygons2))

    @parser.to_polygon_data_list
    def xor(
        self, polygons1: list[PolygonData], polygons2: list[PolygonData]
    ) -> list[PolygonData]:
        """Compute an exclusive OR between two sets of polygons using the server.

        Parameters
        ----------
        polygons1 : list[PolygonData]
            First list of polygons.
        polygons2 : list[PolygonData]
            Second list of polygons.

        Returns
        -------
        list[PolygonData]
            List of polygons resulting from the XOR operation.
        """
        return self._stub.Xor(messages.polygon_data_pair_message(polygons1, polygons2))

    @parser.to_polygon_data_list
    def expand(
        self, polygon: PolygonData, offset: float, round_corner: bool, max_corner_ext: float, tol: float = 1e-9
    ) -> list[PolygonData]:
        """Expand the polygon by an offset using the server.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to expand.
        offset : float
            Expansion offset. Specify a negative value to shrink the polygon.
        round_corner : bool
            Whether the corners are rounded corners. If ``False``, the corners
            are straight edges.
        max_corner_ext : float
            Maximum corner extension to clip the corner at.
        tol : float, default: 1e-9
            Tolerance.

        Returns
        -------
        list[PolygonData]
            List of expanded polygons.
        """
        return self._stub.Expand(
            messages.polygon_data_expand_message(polygon, offset, tol, round_corner, max_corner_ext)
        )
