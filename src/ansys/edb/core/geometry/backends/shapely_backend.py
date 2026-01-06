"""Shapely-based computation backend for client-side operations."""

from __future__ import annotations

import math

from ansys.edb.core.geometry.backends.base import PolygonBackend
from ansys.edb.core.geometry.point_data import PointData
from ansys.edb.core.geometry.polygon_data import PolygonData

try:
    from shapely.geometry import Point as ShapelyPoint
    from shapely.geometry import Polygon as ShapelyPolygon

    SHAPELY_AVAILABLE = True
except ImportError:
    SHAPELY_AVAILABLE = False


class ShapelyBackend(PolygonBackend):
    """Shapely-based computation backend.

    This backend performs computations locally using the Shapely library,
    reducing the number of RPC calls to the server and improving performance
    for geometry-intensive operations.

    Raises
    ------
    ImportError
        If Shapely is not installed.
    """

    def __init__(self, stub=None):
        """Initialize the Shapely backend.

        Parameters
        ----------
        stub : polygon_data_pb2_grpc.PolygonDataServiceStub, optional
            The gRPC stub for polygon operations. Required for alpha_shape method
            which delegates to the server backend.

        Raises
        ------
        ImportError
            If Shapely is not installed.
        """
        if not SHAPELY_AVAILABLE:
            raise ImportError(
                "Shapely is not installed. Install it with: pip install shapely "
                "(check the pyproject.toml for the correct version)\n"
                "Or set PYEDB_COMPUTATION_BACKEND=server to use the server backend."
            )
        self._stub = stub

    @staticmethod
    def _to_tuple(point: tuple[float, float] | PointData) -> tuple[float, float]:
        """Convert a point to a tuple of (x, y) coordinates.

        Parameters
        ----------
        point : tuple[float, float] | PointData
            Point as either a tuple of coordinates or a PointData object.

        Returns
        -------
        tuple[float, float]
            Point coordinates as (x, y) tuple.

        Raises
        ------
        ValueError
            If the point is not a valid tuple or PointData object.
        """
        if isinstance(point, PointData):
            return (point.x.double, point.y.double)
        if isinstance(point, tuple) and len(point) == 2:
            return point
        raise ValueError("Point must be a tuple of (x, y) coordinates or a PointData object.")

    def _to_shapely_polygon(
        self,
        polygon: PolygonData,
        max_chord_error: float = 0,
        max_arc_angle: float = math.pi / 6,
        max_points: int = 8,
    ) -> ShapelyPolygon:
        """Convert a PolygonData object to a Shapely Polygon.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to convert.
        max_chord_error : float, default: 0
            Maximum allowed chord error for arc tessellation.
        max_arc_angle : float, default: math.pi / 6
            Maximum angle (in radians) for each arc segment.
        max_points : int, default: 8
            Maximum number of points per arc.

        Returns
        -------
        ShapelyPolygon
            Shapely polygon object.

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
        # Check if we have a cached Shapely polygon
        if hasattr(polygon, "_shapely_cache"):
            return polygon._shapely_cache

        # Extract coordinates, tessellating arcs locally
        exterior_coords = PolygonBackend._extract_coordinates_with_arcs(
            polygon.points, max_chord_error, max_arc_angle, max_points
        )

        # Handle holes
        holes = []
        for hole in polygon.holes:
            hole_coords = PolygonBackend._extract_coordinates_with_arcs(
                hole.points, max_chord_error, max_arc_angle, max_points
            )
            if hole_coords:
                holes.append(hole_coords)

        # Create Shapely polygon
        if holes:
            shapely_poly = ShapelyPolygon(shell=exterior_coords, holes=holes)
        else:
            shapely_poly = ShapelyPolygon(shell=exterior_coords)

        # Cache the result for future use
        polygon._shapely_cache = shapely_poly
        return shapely_poly

    @staticmethod
    def _shapely_to_polygon_data(shapely_poly: ShapelyPolygon) -> PolygonData:
        """Convert a Shapely polygon to PolygonData.

        Parameters
        ----------
        shapely_poly : ShapelyPolygon
            The Shapely polygon to convert.

        Returns
        -------
        PolygonData
            The converted polygon data.
        """
        # Extract exterior coordinates
        exterior_coords = list(shapely_poly.exterior.coords[:-1])  # Exclude closing point
        points = [PointData(x, y) for x, y in exterior_coords]

        # Extract holes if any
        holes = []
        for interior in shapely_poly.interiors:
            hole_coords = list(interior.coords[:-1])  # Exclude closing point
            hole_points = [PointData(x, y) for x, y in hole_coords]
            holes.append(PolygonData(points=hole_points, closed=True))

        return PolygonData(points=points, holes=holes, closed=True)

    def area(self, polygon: PolygonData) -> float:
        """Compute the area of a polygon using Shapely.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to compute area for.

        Returns
        -------
        float
            Area of the polygon.
        """
        shapely_polygon = self._to_shapely_polygon(polygon)
        return shapely_polygon.area

    def is_convex(self, polygon: PolygonData) -> bool:
        """Determine whether the polygon is convex using Shapely.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to check.

        Returns
        -------
        bool
            ``True`` when the polygon is convex, ``False`` otherwise.
        """
        shapely_polygon = self._to_shapely_polygon(polygon)
        # A polygon is convex if it equals its convex hull
        return shapely_polygon.equals(shapely_polygon.convex_hull)

    def is_circle(self, polygon: PolygonData, tol: float = 1e-9) -> bool:
        """Determine whether the outer contour of the polygon is a circle using Shapely.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to check.

        Returns
        -------
        bool
            ``True`` when the outer contour of the polygon is a circle, ``False`` otherwise.
        """
        # Check if polygon has holes - a circle cannot have holes
        if polygon.has_holes():
            return False

        points = PolygonBackend._sanitize_points(polygon.points.copy())

        if not points[1].is_arc:
            return False

        _, center, radius = self._tessellate_arc(points[0], points[2], points[1].arc_height.double)

        i = 0
        n = len(points)
        while i < n:
            pt = points[i]
            if i + 1 < n and points[i + 1].is_arc:
                if i + 2 < n:
                    start = pt
                    arc_pt = points[i + 1]
                    end = points[i + 2]
                    height = arc_pt.arc_height.double
                    _, c, r = ShapelyBackend._tessellate_arc(start, end, height)
                    if not (
                        math.isclose(c[0], center[0], rel_tol=tol)
                        and math.isclose(c[1], center[1], rel_tol=tol)
                        and math.isclose(r, radius, rel_tol=tol)
                    ):
                        return False
                    i += 2
                else:
                    RuntimeError("Invalid arc definition: arc point without an end point.")
            else:
                if not (
                    math.isclose(
                        (pt.x.double - center[0]) * (pt.x.double - center[0])
                        + (pt.y.double - center[1]) * (pt.y.double - center[1]),
                        radius * radius,
                        rel_tol=tol,
                    )
                ):
                    return False
                i += 1

        return True

    def is_box(self, polygon: PolygonData, tol: float = 1e-9) -> bool:
        """Determine whether the outer contour of the polygon is a box using Shapely.

        A box is defined as a rectangle (quadrilateral with 4 right angles).

        Parameters
        ----------
        polygon : PolygonData
            The polygon to check.

        Returns
        -------
        bool
            ``True`` when the outer contour of the polygon is a box, ``False`` otherwise.
        """
        # A box cannot have holes or arcs
        if (
            polygon.has_holes() or polygon.has_arcs()
        ):  # If the polygon was set up with arcs of zero height, the has_arcs() will return False.
            return False

        return PolygonBackend._is_box(polygon, tol)

    def is_inside(self, polygon: PolygonData, point: tuple[float, float]) -> bool:
        """Determine whether a point is inside the polygon using Shapely.

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
        point = self._to_tuple(point)
        shapely_polygon = self._to_shapely_polygon(polygon)
        shapely_point = ShapelyPoint(point)
        return shapely_polygon.intersects(shapely_point)

    def bbox(self, polygon: PolygonData) -> tuple[tuple[float, float], tuple[float, float]]:
        """Compute the bounding box of a polygon using Shapely.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to compute bounding box for.

        Returns
        -------
        tuple[tuple[float, float], tuple[float, float]]
            Bounding box as ((min_x, min_y), (max_x, max_y)).
        """
        shapely_polygon = self._to_shapely_polygon(polygon)
        min_x, min_y, max_x, max_y = shapely_polygon.bounds
        return ((min_x, min_y), (max_x, max_y))

    def bbox_of_polygons(
        self, polygons: list[PolygonData]
    ) -> tuple[tuple[float, float], tuple[float, float]]:
        """Compute the bounding box of a list of polygons using Shapely.

        Parameters
        ----------
        polygons : list[PolygonData]
            List of polygons to compute bounding box for.

        Returns
        -------
        tuple[tuple[float, float], tuple[float, float]]
            Bounding box as ((min_x, min_y), (max_x, max_y)).
        """
        if not polygons:
            return ((0.0, 0.0), (0.0, 0.0))

        min_x, min_y = math.inf, math.inf
        max_x, max_y = -math.inf, -math.inf

        # Expand to include all other polygons
        for polygon in polygons:
            shapely_poly = self._to_shapely_polygon(polygon)
            p_min_x, p_min_y, p_max_x, p_max_y = shapely_poly.bounds
            min_x = min(min_x, p_min_x)
            min_y = min(min_y, p_min_y)
            max_x = max(max_x, p_max_x)
            max_y = max(max_y, p_max_y)

        return ((min_x, min_y), (max_x, max_y))

    def without_arcs(
        self,
        polygon: PolygonData,
        max_chord_error: float = 0,
        max_arc_angle: float = math.pi / 6,
        max_points: int = 8,
    ) -> PolygonData:
        """Get polygon data with all arcs removed using Shapely.

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
        return PolygonBackend._without_arcs(polygon, max_chord_error, max_arc_angle, max_points)

    def has_self_intersections(self, polygon: PolygonData, tol: float = 1e-9) -> bool:
        """Determine whether the polygon contains any self-intersections using Shapely.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to check.
        tol : float, default: 1e-9
            Tolerance (not used in Shapely implementation but kept for API consistency).

        Returns
        -------
        bool
            ``True`` when the polygon contains self-intersections, ``False`` otherwise.

        Notes
        -----
        This implementation uses Shapely's `is_valid` property. A polygon is considered
        valid if it does not have self-intersections. The tolerance parameter is kept
        for API consistency with the server backend but is not used in this implementation
        as Shapely uses its own internal tolerance.
        """
        shapely_polygon = self._to_shapely_polygon(polygon)
        # A polygon with self-intersections is invalid in Shapely
        return not shapely_polygon.is_valid

    def remove_self_intersections(
        self, polygon: PolygonData, tol: float = 1e-9
    ) -> list[PolygonData]:
        """Remove self-intersections from a polygon using Shapely.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to process.
        tol : float, default: 1e-9
            Tolerance (not used in Shapely implementation but kept for API consistency).

        Returns
        -------
        list[PolygonData]
            A list of non self-intersecting polygons.

        Notes
        -----
        This implementation uses Shapely's `make_valid` operation to fix self-intersections.
        The make_valid function converts invalid geometries into valid ones by splitting
        or modifying them as needed. The result may be a single polygon, multiple polygons
        (MultiPolygon), or an empty geometry depending on the nature of the self-intersections.
        The tolerance parameter is kept for API consistency with the server backend but is
        not used in this implementation as Shapely uses its own internal tolerance.
        """
        from shapely import make_valid
        from shapely.geometry import MultiPolygon

        shapely_polygon = self._to_shapely_polygon(polygon)

        # If the polygon is already valid, return it as-is
        if shapely_polygon.is_valid:
            return [polygon]

        # Use make_valid to fix self-intersections
        fixed_geom = make_valid(shapely_polygon)

        # Handle different result types
        result_polygons = []

        if fixed_geom.is_empty:
            # If the result is empty, return an empty list
            return []

        # Check if result is a MultiPolygon
        if isinstance(fixed_geom, MultiPolygon):
            # Convert each polygon in the MultiPolygon to PolygonData
            for poly in fixed_geom.geoms:
                result_polygons.append(self._shapely_to_polygon_data(poly))
        else:
            # Single polygon result
            result_polygons.append(self._shapely_to_polygon_data(fixed_geom))

        return result_polygons

    def normalized(self, polygon: PolygonData) -> list:
        """Get the normalized points of the polygon using Shapely.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to process.

        Returns
        -------
        list[PointData]
            List of normalized points where outer contours are CCW and holes are CW.

        Notes
        -----
        This method normalizes the polygon orientation:
        - Outer contours (shell) are returned in counter-clockwise (CCW) order
        - Holes are returned in clockwise (CW) order

        Shapely's exterior coordinates are always in CCW order by default,
        and interior coordinates (holes) are in CW order.
        """
        from shapely.geometry.polygon import orient

        shapely_polygon = self._to_shapely_polygon(polygon)
        shapely_polygon = orient(shapely_polygon, sign=1.0)
        exterior_coords = list(shapely_polygon.exterior.coords[:-1])
        normalized_points = [PointData(x, y) for x, y in exterior_coords]

        return normalized_points

    def move(self, polygon: PolygonData, vector: tuple[float, float]) -> PolygonData:
        """Move the polygon by a vector using Shapely.

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
        from shapely.affinity import translate

        shape = self._to_shapely_polygon(polygon)
        shape = translate(shape, xoff=vector[0], yoff=vector[1])

        return ShapelyBackend._shapely_to_polygon_data(shape)

    def rotate(
        self, polygon: PolygonData, angle: float, center: tuple[float, float], use_radians: bool
    ) -> PolygonData:
        """Rotate the polygon at a center by an angle using Shapely.

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
        from shapely.affinity import rotate

        shape = self._to_shapely_polygon(polygon)
        shape = rotate(shape, angle, origin=center, use_radians=use_radians)

        return ShapelyBackend._shapely_to_polygon_data(shape)

    def scale(
        self, polygon: PolygonData, factor: float, center: tuple[float, float]
    ) -> PolygonData:
        """Scale the polygon by a linear factor from a center using Shapely.

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
        from shapely.affinity import scale

        shape = self._to_shapely_polygon(polygon)
        shape = scale(shape, xfact=factor, yfact=factor, origin=center)

        return ShapelyBackend._shapely_to_polygon_data(shape)

    def mirror_x(self, polygon: PolygonData, x: float) -> PolygonData:
        """Mirror the polygon across a vertical line at x using Shapely.

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
        from shapely.affinity import scale, translate

        shape = self._to_shapely_polygon(polygon)
        shape = translate(shape, xoff=-x)
        shape = scale(shape, xfact=-1, yfact=1, origin=(0, 0))
        shape = translate(shape, xoff=x)

        return ShapelyBackend._shapely_to_polygon_data(shape)

    def bounding_circle(self, polygon: PolygonData) -> tuple[tuple[float, float], float]:
        """Compute the bounding circle of the polygon using Shapely.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to compute bounding circle for.

        Returns
        -------
        tuple[tuple[float, float], float]
            Bounding circle as ((center_x, center_y), radius).

        Notes
        -----
        This implementation uses the minimum bounding circle algorithm.
        For simple cases (like rectangles), it uses the circumcircle of the bounding box.
        This is a simplified implementation that may not always produce the absolute
        minimum bounding circle but provides a reasonable approximation.
        """
        shapely_polygon = self._to_shapely_polygon(polygon)

        # Get the bounding box
        min_x, min_y, max_x, max_y = shapely_polygon.bounds

        # Calculate center as the center of the bounding box
        center_x = (min_x + max_x) / 2.0
        center_y = (min_y + max_y) / 2.0

        # Calculate radius as half the diagonal of the bounding box
        # This ensures all points are within the circle
        width = max_x - min_x
        height = max_y - min_y
        radius = math.sqrt(width**2 + height**2) / 2.0

        return ((center_x, center_y), radius)

    def convex_hull(self, polygons: list[PolygonData]) -> PolygonData:
        """Compute the convex hull of the union of a list of polygons using Shapely.

        Parameters
        ----------
        polygons : list[PolygonData]
            List of polygons.

        Returns
        -------
        PolygonData
            The convex hull polygon.
        """
        from shapely.geometry import MultiPoint

        if not polygons:
            raise ValueError("Cannot compute convex hull of an empty list of polygons")

        # Collect all points from all polygons (including tessellated arc points)
        all_points = []
        for poly in polygons:
            # Convert to shapely polygon to get tessellated coordinates
            shapely_poly = self._to_shapely_polygon(poly)
            # Extract all exterior coordinates
            all_points.extend(shapely_poly.exterior.coords[:-1])  # Exclude closing point
            # Also add points from holes if any
            for interior in shapely_poly.interiors:
                all_points.extend(interior.coords[:-1])

        # Create a MultiPoint geometry from all collected points
        multi_point = MultiPoint(all_points)

        # Compute the convex hull of all points
        hull_geom = multi_point.convex_hull

        # Convert back to PolygonData
        return self._shapely_to_polygon_data(hull_geom)

    def defeature(self, polygon: PolygonData, tol: float = 1e-9) -> PolygonData:
        """Defeature a polygon by removing small features using Shapely.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to defeature.
        tol : float, default: 1e-9
            Tolerance for defeaturing. Points closer than this distance may be simplified.

        Returns
        -------
        PolygonData
            Defeatured polygon.

        Notes
        -----
        This implementation uses Shapely's `simplify` method with the Douglas-Peucker algorithm.
        The tolerance represents the maximum distance from the original geometry to the simplified one.
        Small features smaller than the tolerance will be removed. The operation preserves topology
        to ensure the result is valid.
        """
        shapely_polygon = self._to_shapely_polygon(polygon)

        # Simplify the polygon using Douglas-Peucker algorithm
        # preserve_topology=True ensures the result remains valid
        simplified_polygon = shapely_polygon.simplify(tolerance=tol, preserve_topology=True)

        # Convert back to PolygonData
        return self._shapely_to_polygon_data(simplified_polygon)

    def intersection_type(self, polygon: PolygonData, other: PolygonData, tol: float = 1e-9):
        """Get the intersection type with another polygon using Shapely.

        Parameters
        ----------
        polygon : PolygonData
            The first polygon.
        other : PolygonData
            The second polygon.
        tol : float, default: 1e-9
            Tolerance (not used in Shapely implementation but kept for API consistency).

        Returns
        -------
        int
            The intersection type enum value.

        Notes
        -----
        This implementation uses Shapely's geometric predicates to determine the relationship
        between two polygons. The tolerance parameter is kept for API consistency with the
        server backend but is not used in this implementation as Shapely uses its own
        internal tolerance.

        The intersection types are:
        - NO_INTERSECTION (0): Polygons do not intersect
        - THIS_INSIDE_OTHER (1): First polygon is completely inside the second
        - OTHER_INSIDE_THIS (2): Second polygon is completely inside the first
        - COMMON_INTERSECTION (3): Polygons partially intersect
        - UNDEFINED_INTERSECTION (4): Intersection cannot be determined
        """
        from ansys.api.edb.v1 import polygon_data_pb2

        shapely_poly1 = self._to_shapely_polygon(polygon)
        shapely_poly2 = self._to_shapely_polygon(other)

        # Check if polygons don't intersect
        if not shapely_poly1.intersects(shapely_poly2):
            return polygon_data_pb2.NO_INTERSECTION

        # Check if polygon is inside other
        if shapely_poly1.within(shapely_poly2):
            return polygon_data_pb2.THIS_INSIDE_OTHER

        # Check if other is inside polygon
        if shapely_poly2.within(shapely_poly1):
            return polygon_data_pb2.OTHER_INSIDE_THIS

        # If they intersect but neither is inside the other, they have common intersection
        return polygon_data_pb2.COMMON_INTERSECTION

    def circle_intersect(
        self, polygon: PolygonData, center: tuple[float, float], radius: float
    ) -> bool:
        """Determine whether a circle intersects with a polygon using Shapely.

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

        Notes
        -----
        This implementation creates a Shapely Point for the circle center and uses
        the buffer operation to create a circular polygon, then checks for intersection.
        """
        center = self._to_tuple(center)
        shapely_polygon = self._to_shapely_polygon(polygon)

        # Create a circle as a buffered point
        circle_center = ShapelyPoint(center)
        circle = circle_center.buffer(radius)

        # Check if the circle intersects with the polygon
        return shapely_polygon.intersects(circle)

    def closest_point(
        self, polygon: PolygonData, point: tuple[float, float]
    ) -> tuple[float, float]:
        """Compute a point on the polygon that is closest to another point using Shapely.

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

        Notes
        -----
        This implementation uses Shapely's nearest_points function to find the closest
        point on the polygon boundary to the given point. If the polygon has arcs,
        they are tessellated first.
        """
        from shapely.ops import nearest_points

        point = self._to_tuple(point)
        shapely_polygon = self._to_shapely_polygon(polygon)
        shapely_point = ShapelyPoint(point)

        # Find the nearest points between the polygon boundary and the given point
        # nearest_points returns a tuple of (nearest point on geom1, nearest point on geom2)
        nearest_on_polygon, _ = nearest_points(shapely_polygon.boundary, shapely_point)

        return PointData(nearest_on_polygon.x, nearest_on_polygon.y)

    def closest_points(
        self, polygon1: PolygonData, polygon2: PolygonData
    ) -> tuple[tuple[float, float], tuple[float, float]]:
        """Compute points on two polygons that are closest to each other using Shapely.

        Parameters
        ----------
        polygon1 : PolygonData
            The first polygon.
        polygon2 : PolygonData
            The second polygon.

        Returns
        -------
        tuple[tuple[float, float], tuple[float, float]]
            A tuple of two points ((x1, y1), (x2, y2)) where the first point is on polygon1
            and the second point is on polygon2.

        Notes
        -----
        This implementation uses Shapely's nearest_points function to find the closest
        points between the boundaries of two polygons. If the polygons have arcs,
        they are tessellated first.
        """
        from shapely.ops import nearest_points

        shapely_polygon1 = self._to_shapely_polygon(polygon1)
        shapely_polygon2 = self._to_shapely_polygon(polygon2)

        # Find the nearest points between the two polygon boundaries
        # nearest_points returns a tuple of (nearest point on geom1, nearest point on geom2)
        nearest_on_polygon1, nearest_on_polygon2 = nearest_points(
            shapely_polygon1.boundary, shapely_polygon2.boundary
        )

        return (
            (nearest_on_polygon1.x, nearest_on_polygon1.y),
            (nearest_on_polygon2.x, nearest_on_polygon2.y),
        )

    def unite(self, polygons: list[PolygonData]) -> list[PolygonData]:
        """Compute the union of a list of polygons using Shapely.

        Parameters
        ----------
        polygons : list[PolygonData]
            List of polygons to unite.

        Returns
        -------
        list[PolygonData]
            List of polygons resulting from the union.

        Notes
        -----
        This implementation uses Shapely's unary_union operation to efficiently
        compute the union of multiple polygons. The result may be a single polygon
        or multiple disjoint polygons (MultiPolygon).
        """
        from shapely.geometry import MultiPolygon
        from shapely.ops import unary_union

        if not polygons:
            return []

        # Convert all polygons to Shapely format
        shapely_polygons = [self._to_shapely_polygon(p) for p in polygons]

        # Compute the union
        result = unary_union(shapely_polygons)

        # Convert the result back to PolygonData
        result_polygons = []

        if result.is_empty:
            return []

        if isinstance(result, MultiPolygon):
            for geom in result.geoms:
                result_polygons.append(self._shapely_to_polygon_data(geom))
        else:
            result_polygons.append(self._shapely_to_polygon_data(result))

        return result_polygons

    def intersect(
        self, polygons1: list[PolygonData], polygons2: list[PolygonData]
    ) -> list[PolygonData]:
        """Compute the intersection of two lists of polygons using Shapely.

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

        Notes
        -----
        This implementation first unions each list separately, then computes the
        intersection between the two unions. The result may be a single polygon,
        multiple disjoint polygons (MultiPolygon), or empty if there's no intersection.
        """
        from shapely.geometry import MultiPolygon
        from shapely.ops import unary_union

        if not polygons1 or not polygons2:
            return []

        if not isinstance(polygons1, list):
            polygons1 = [polygons1]
        if not isinstance(polygons2, list):
            polygons2 = [polygons2]

        shapely_polygons1 = [self._to_shapely_polygon(p) for p in polygons1]
        shapely_polygons2 = [self._to_shapely_polygon(p) for p in polygons2]

        union1 = unary_union(shapely_polygons1)
        union2 = unary_union(shapely_polygons2)

        result = union1.intersection(union2)

        result_polygons = []

        if result.is_empty:
            return []

        if isinstance(result, MultiPolygon):
            for geom in result.geoms:
                result_polygons.append(self._shapely_to_polygon_data(geom))
        else:
            result_polygons.append(self._shapely_to_polygon_data(result))

        return result_polygons

    def subtract(
        self, polygons1: list[PolygonData], polygons2: list[PolygonData]
    ) -> list[PolygonData]:
        """Subtract a set of polygons from another set of polygons using Shapely.

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

        Notes
        -----
        This implementation first unions each list separately, then computes the
        difference between the two unions. The result may be a single polygon,
        multiple disjoint polygons (MultiPolygon), or empty if nothing remains.
        """
        from shapely.geometry import MultiPolygon
        from shapely.ops import unary_union

        if not polygons1:
            return []
        if not polygons2:
            return polygons1

        if not isinstance(polygons1, list):
            polygons1 = [polygons1]
        if not isinstance(polygons2, list):
            polygons2 = [polygons2]

        # Convert all polygons to Shapely format and union each set
        shapely_polygons1 = [self._to_shapely_polygon(p) for p in polygons1]
        shapely_polygons2 = [self._to_shapely_polygon(p) for p in polygons2]

        # Union each set
        union1 = unary_union(shapely_polygons1)
        union2 = unary_union(shapely_polygons2)

        # Compute the difference
        result = union1.difference(union2)

        # Convert the result back to PolygonData
        result_polygons = []

        if result.is_empty:
            return []

        if isinstance(result, MultiPolygon):
            for geom in result.geoms:
                result_polygons.append(self._shapely_to_polygon_data(geom))
        else:
            result_polygons.append(self._shapely_to_polygon_data(result))

        return result_polygons

    def xor(self, polygons1: list[PolygonData], polygons2: list[PolygonData]) -> list[PolygonData]:
        """Compute an exclusive OR between two sets of polygons using Shapely.

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

        Notes
        -----
        This implementation first unions each list separately, then computes the
        symmetric difference between the two unions. The result may be a single polygon,
        multiple disjoint polygons (MultiPolygon), or empty.
        """
        from shapely.geometry import MultiPolygon
        from shapely.ops import unary_union

        if not polygons1 and not polygons2:
            return []
        if not polygons1:
            return polygons2
        if not polygons2:
            return polygons1

        if not isinstance(polygons1, list):
            polygons1 = [polygons1]
        if not isinstance(polygons2, list):
            polygons2 = [polygons2]

        # Convert all polygons to Shapely format and union each set
        shapely_polygons1 = [self._to_shapely_polygon(p) for p in polygons1]
        shapely_polygons2 = [self._to_shapely_polygon(p) for p in polygons2]

        # Union each set
        union1 = unary_union(shapely_polygons1)
        union2 = unary_union(shapely_polygons2)

        # Compute the symmetric difference (XOR)
        result = union1.symmetric_difference(union2)

        # Convert the result back to PolygonData
        result_polygons = []

        if result.is_empty:
            return []

        if isinstance(result, MultiPolygon):
            for geom in result.geoms:
                result_polygons.append(self._shapely_to_polygon_data(geom))
        else:
            result_polygons.append(self._shapely_to_polygon_data(result))

        return result_polygons

    def expand(
        self,
        polygon: PolygonData,
        offset: float,
        round_corner: bool,
        max_corner_ext: float,
        tol: float = 1e-9,
    ) -> list[PolygonData]:
        """Expand the polygon by an offset using Shapely.

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

        Notes
        -----
        This implementation uses Shapely's buffer operation to expand or shrink polygons.
        When `round_corner` is True, rounded corners are created. When False, mitered
        corners are used with the `max_corner_ext` parameter controlling the miter limit.
        The miter limit is calculated as the ratio of max_corner_ext to offset.
        """
        from shapely.geometry import MultiPolygon

        shapely_polygon = self._to_shapely_polygon(polygon)

        # Determine join style based on round_corner parameter
        # JOIN_STYLE: 1 = round, 2 = mitre, 3 = bevel
        if round_corner:
            join_style = 1  # Round
            mitre_limit = 5.0  # Default for round joins (not used)
        else:
            join_style = 2  # Mitre (sharp corners)
            # Calculate mitre limit as the ratio of max extension to offset
            # Shapely's mitre_limit is the ratio of the maximum corner extension to the buffer distance
            if offset != 0:
                mitre_limit = max_corner_ext / abs(offset)
            else:
                mitre_limit = 5.0  # Default value

            # Ensure mitre_limit is at least 1.0 to avoid errors
            mitre_limit = max(1.0, mitre_limit)

        # Apply buffer operation
        # Positive offset expands, negative offset shrinks
        buffered = shapely_polygon.buffer(offset, join_style=join_style, mitre_limit=mitre_limit)

        # Convert result back to PolygonData
        result_polygons = []

        if buffered.is_empty:
            return []

        if isinstance(buffered, MultiPolygon):
            # Multiple polygons resulted from the operation
            for geom in buffered.geoms:
                result_polygons.append(self._shapely_to_polygon_data(geom))
        else:
            # Single polygon result
            result_polygons.append(self._shapely_to_polygon_data(buffered))

        return result_polygons

    def alpha_shape(self, points: list[tuple[float, float]], alpha: float) -> list[PolygonData]:
        """Compute the outline of a 2D point cloud using alpha shapes.

        This method delegates to the server backend implementation.

        Parameters
        ----------
        points : list[tuple[float, float]]
            List of point coordinates.
        alpha : float
            Alpha parameter controlling the shape's tightness.

        Returns
        -------
        list[PolygonData]
            List of polygons representing the alpha shape.

        Warns
        -----
        UserWarning
            If the server stub is not available, a warning is issued before
            attempting to use the server backend.

        Notes
        -----
        The alpha shape algorithm is not implemented in Shapely, so this method
        delegates to the server backend. The server stub must be available for
        this method to work.
        """
        import warnings

        if self._stub is None:
            warnings.warn(
                "Server stub is not available for alpha_shape. "
                "Alpha shape algorithm requires server backend. "
                "This may fail if the stub is not properly initialized.",
                UserWarning,
                stacklevel=2,
            )

        from ansys.edb.core.geometry.backends.server_backend import ServerBackend

        server_backend = ServerBackend(self._stub)
        return server_backend.alpha_shape(points, alpha)
