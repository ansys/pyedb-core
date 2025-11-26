"""Shapely-based computation backend for client-side operations."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.geometry.point_data import PointData

from ansys.edb.core.geometry.backends.base import PolygonBackend

try:
    from shapely.geometry import Polygon as ShapelyPolygon
    from shapely.geometry import Point as ShapelyPoint

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

    def __init__(self):
        """Initialize the Shapely backend.

        Raises
        ------
        ImportError
            If Shapely is not installed.
        """
        if not SHAPELY_AVAILABLE:
            raise ImportError(
                "Shapely is not installed. Install it with: pip install shapely (check the pyproject.toml for the correct version)\nOr set PYEDB_COMPUTATION_BACKEND=server to use the server backend."
            )

    @staticmethod
    def _tessellate_arc(
        start: PointData,
        end: PointData,
        height: float,
        max_chord_error: float = 0,
        max_arc_angle: float = math.pi / 6,
        max_points: int = 8,
    ) -> list[tuple[float, float]]:
        """Tessellate an arc into line segments locally.

        Parameters
        ----------
        start : PointData
            Start point of the arc.
        end : PointData
            End point of the arc.
        height : float
            Arc height (sagitta). Positive for clockwise, negative for counter-clockwise.
        max_chord_error : float, default: 0
            Maximum allowed chord error (distance from arc to chord).
        max_arc_angle : float, default: math.pi / 6
            Maximum angle (in radians) for each arc segment.
        max_points : int, default: 8
            Maximum number of points to generate.

        Returns
        -------
        list[tuple[float, float]]
            List of intermediate points (excluding start, including end).

        Notes
        -----
        Arc is defined by three points: start, arc point (with height), and end.
        The height (sagitta) is the perpendicular distance from the chord midpoint to the arc.
        """
        # If height is zero or very small, it's a straight line
        if abs(height) < 1e-12:
            return [(end.x.double, end.y.double)]

        # Extract coordinates
        x1, y1 = start.x.double, start.y.double
        x2, y2 = end.x.double, end.y.double

        # Calculate chord properties
        chord_dx = x2 - x1
        chord_dy = y2 - y1
        chord_length = math.sqrt(chord_dx**2 + chord_dy**2)

        # If chord length is zero, start and end are the same point
        if chord_length < 1e-12:
            return [(x2, y2)]

        # Calculate arc properties
        # For a circular arc, radius r and sagitta h are related by:
        # r = (h^2 + (c/2)^2) / (2*h) where c is chord length
        h = abs(height)
        radius = (h**2 + (chord_length / 2) ** 2) / (2 * h)

        # Calculate the center of the arc
        # The center is perpendicular to the chord at its midpoint
        chord_mid_x = (x1 + x2) / 2
        chord_mid_y = (y1 + y2) / 2

        # Perpendicular direction (rotated 90 degrees from chord)
        perp_dx = -chord_dy / chord_length
        perp_dy = chord_dx / chord_length

        # Distance from chord midpoint to center
        center_dist = radius - h

        # Adjust direction based on arc orientation (height sign)
        if height > 0:  # Clockwise
            center_x = chord_mid_x + perp_dx * center_dist
            center_y = chord_mid_y + perp_dy * center_dist
        else:  # Counter-clockwise
            center_x = chord_mid_x - perp_dx * center_dist
            center_y = chord_mid_y - perp_dy * center_dist

        # Calculate total angle subtended by the arc
        angle1 = math.atan2(y1 - center_y, x1 - center_x)
        angle2 = math.atan2(y2 - center_y, x2 - center_x)

        # Determine the arc angle considering direction
        if height > 0:  # Clockwise
            if angle2 > angle1:
                arc_angle = angle2 - angle1 - 2 * math.pi
            else:
                arc_angle = angle2 - angle1
        else:  # Counter-clockwise
            if angle2 < angle1:
                arc_angle = angle2 - angle1 + 2 * math.pi
            else:
                arc_angle = angle2 - angle1

        total_angle = abs(arc_angle)

        # Determine number of segments
        # Method 1: Based on max_arc_angle
        num_segments_angle = max(1, int(math.ceil(total_angle / max_arc_angle)))

        # Method 2: Based on max_chord_error (if specified)
        if max_chord_error > 0:
            # Chord error for a segment: e = r * (1 - cos(θ/2))
            # Solving for θ: θ = 2 * acos(1 - e/r)
            max_segment_angle = 2 * math.acos(max(0, min(1, 1 - max_chord_error / radius)))
            num_segments_error = max(1, int(math.ceil(total_angle / max_segment_angle)))
        else:
            num_segments_error = 1

        # Take the maximum to satisfy both constraints, but limit to max_points
        num_segments = min(max(num_segments_angle, num_segments_error), max_points)

        # Generate intermediate points
        points = []
        angle_step = arc_angle / num_segments

        for i in range(1, num_segments + 1):
            angle = angle1 + angle_step * i
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))

        return points

    @staticmethod
    def _extract_coordinates_with_arcs(
        points: list[PointData],
        max_chord_error: float = 0,
        max_arc_angle: float = math.pi / 6,
        max_points: int = 8,
    ) -> list[tuple[float, float]]:
        """Extract coordinates from points, tessellating arcs into line segments.

        Parameters
        ----------
        points : list[PointData]
            List of points, where arc points have is_arc=True and contain arc height.
        max_chord_error : float, default: 0
            Maximum allowed chord error for arc tessellation.
        max_arc_angle : float, default: math.pi / 6
            Maximum angle for each arc segment.
        max_points : int, default: 8
            Maximum number of points per arc.

        Returns
        -------
        list[tuple[float, float]]
            List of coordinate tuples.

        Notes
        -----
        The arc representation in PolygonData works as follows:
        - Point at index i is the start of an arc
        - Point at index i+1 has is_arc=True and contains the arc height
        - Point at index i+2 is the end of the arc
        Then we skip to i+2 for the next segment.
        """
        if not points:
            return []

        coords = []
        i = 0
        n = len(points)

        while i < n:
            pt = points[i]

            # Check if the next point (if it exists) is an arc point
            if i + 1 < n and points[i + 1].is_arc:
                # This is the start of an arc segment
                if i + 2 < n:
                    start = pt
                    arc_pt = points[i + 1]
                    end = points[i + 2]
                    height = arc_pt.arc_height.double

                    # Add the start point
                    coords.append((start.x.double, start.y.double))

                    # Tessellate the arc and add intermediate points (excluding start)
                    arc_coords = ShapelyBackend._tessellate_arc(
                        start, end, height, max_chord_error, max_arc_angle, max_points
                    )
                    # arc_coords includes the end point, so add all of them
                    coords.extend(arc_coords[:-1])  # Exclude end point for now

                    # Move to the end point (i+2), which will be processed in next iteration
                    i += 2
                else:
                    # Incomplete arc at the end - just add the current point
                    coords.append((pt.x.double, pt.y.double))
                    i += 1
            else:
                # Regular point - just add it
                coords.append((pt.x.double, pt.y.double))
                i += 1

        return coords

    @staticmethod
    def _to_shapely_polygon(
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
        exterior_coords = ShapelyBackend._extract_coordinates_with_arcs(
            polygon.points, max_chord_error, max_arc_angle, max_points
        )

        # Handle holes
        holes = []
        for hole in polygon.holes:
            hole_coords = ShapelyBackend._extract_coordinates_with_arcs(
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
        shapely_poly = self._to_shapely_polygon(polygon)
        return shapely_poly.area

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
        shapely_poly = self._to_shapely_polygon(polygon)
        # A polygon is convex if it equals its convex hull
        return shapely_poly.equals(shapely_poly.convex_hull)

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
        shapely_poly = self._to_shapely_polygon(polygon)
        shapely_point = ShapelyPoint(point)
        return shapely_poly.intersects(shapely_point)

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
        shapely_poly = self._to_shapely_polygon(polygon)
        min_x, min_y, max_x, max_y = shapely_poly.bounds
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

        # Initialize with the first polygon's bounds
        first_poly = self._to_shapely_polygon(polygons[0])
        min_x, min_y, max_x, max_y = first_poly.bounds

        # Expand to include all other polygons
        for polygon in polygons[1:]:
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
        from ansys.edb.core.geometry.point_data import PointData
        from ansys.edb.core.geometry.polygon_data import PolygonData

        # Extract coordinates with arcs tessellated
        exterior_coords = self._extract_coordinates_with_arcs(
            polygon.points, max_chord_error, max_arc_angle, max_points
        )

        # Convert coordinates back to PointData objects (non-arc points)
        new_points = [PointData(x, y) for x, y in exterior_coords]

        # Process holes
        new_holes = []
        for hole in polygon.holes:
            hole_coords = self._extract_coordinates_with_arcs(
                hole.points, max_chord_error, max_arc_angle, max_points
            )
            hole_points = [PointData(x, y) for x, y in hole_coords]
            # Create a new PolygonData for the hole without arcs

            new_hole = PolygonData(points=hole_points, sense=hole.sense, closed=hole.is_closed)
            new_holes.append(new_hole)

        # Create and return new PolygonData without arcs
        return PolygonData(points=new_points, holes=new_holes, sense=polygon.sense, closed=polygon.is_closed)
