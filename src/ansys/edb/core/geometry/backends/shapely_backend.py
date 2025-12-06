"""Shapely-based computation backend for client-side operations."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.geometry.polygon_data import PolygonData, PolygonSenseType
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
            Arc height (sagitta). 
            - Negative: center on LEFT side, small arc on RIGHT (< 180°)
            - Positive: center on RIGHT side, large arc on RIGHT (> 180°)
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
        When going from start to end:
        - Negative height: center on LEFT, arc on RIGHT (small arc, < 180°)
        - Positive height: center on RIGHT, arc on RIGHT (large arc, > 180°)
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
        chord_length = math.sqrt(chord_dx * chord_dx + chord_dy * chord_dy)

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

        # Perpendicular direction to the right when going from start to end
        perp_dx = chord_dy / chord_length
        perp_dy = -chord_dx / chord_length

        # Place center based on height sign:
        # - Negative height: center on LEFT side, arc on RIGHT (small portion)
        # - Positive height: center on RIGHT side, arc on RIGHT (large portion)
        if height < 0:  # Center on LEFT, small arc on RIGHT
            center_x = chord_mid_x - perp_dx * (radius + height)
            center_y = chord_mid_y - perp_dy * (radius + height)
        else:  # Center on RIGHT, large arc on RIGHT
            center_x = chord_mid_x + perp_dx * (radius - height)
            center_y = chord_mid_y + perp_dy * (radius - height)
        
        dot_product = (x1-center_x)*(x2-center_x) + (y1-center_y)*(y2-center_y)
        temp_angle = math.acos(dot_product/(radius*radius))
        angle1 = math.atan2(y1 - center_y, x1 - center_x)
        if height < 0 and radius > abs(height):
            arc_angle = temp_angle
        if height < 0 and radius <= abs(height):
            arc_angle = (2*math.pi - temp_angle)
        if height > 0 and radius > abs(height):
            arc_angle = (2*math.pi - temp_angle)
        if height > 0 and radius <= abs(height):
            arc_angle = temp_angle
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
        
        # Remove consecutive duplicate points that may have arisen from tessellation
        i = 0
        while i < len(coords) - 1:
            if math.isclose(coords[i][0], coords[i+1][0], rel_tol=1e-9) and math.isclose(coords[i][1], coords[i+1][1], rel_tol=1e-9):
                coords.pop(i+1)
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
    

    @staticmethod
    def _shapely_to_polygon_data(shapely_poly: ShapelyPolygon, sense: PolygonSenseType) -> PolygonData:
        """Convert a Shapely polygon to PolygonData.

        Parameters
        ----------
        shapely_poly : ShapelyPolygon
            The Shapely polygon to convert.
        sense : PolygonSenseType
            The sense to apply to the resulting polygon.

        Returns
        -------
        PolygonData
            The converted polygon data.
        """
        from ansys.edb.core.geometry.point_data import PointData
        from ansys.edb.core.geometry.polygon_data import PolygonData, PolygonSenseType

        # Extract exterior coordinates
        exterior_coords = list(shapely_poly.exterior.coords[:-1])  # Exclude closing point
        points = [PointData(x, y) for x, y in exterior_coords]

        # Extract holes if any
        holes = []
        for interior in shapely_poly.interiors:
            hole_coords = list(interior.coords[:-1])  # Exclude closing point
            hole_points = [PointData(x, y) for x, y in hole_coords]
            # Holes are typically CCW in Shapely, but we create them with opposite sense
            hole_sense = PolygonSenseType.SENSE_CW if sense == PolygonSenseType.SENSE_CCW else PolygonSenseType.SENSE_CCW
            holes.append(PolygonData(points=hole_points, sense=hole_sense, closed=True))
        
        return PolygonData(points=points, holes=holes, sense=sense, closed=True)


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


    def remove_self_intersections(self, polygon: PolygonData, tol: float = 1e-9) -> list[PolygonData]:
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
        from shapely.geometry import MultiPolygon
        from shapely import make_valid

        shapely_polygon = self._to_shapely_polygon(polygon)

        # If the polygon is already valid, return it as-is
        if shapely_polygon.is_valid:
            return [polygon]
        
        # Use buffer(0) to fix self-intersections
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
                result_polygons.append(self._shapely_to_polygon_data(poly, polygon.sense))
        else:
            # Single polygon result
            result_polygons.append(self._shapely_to_polygon_data(fixed_geom, polygon.sense))
        
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
        from ansys.edb.core.geometry.point_data import PointData
        
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

        Notes
        -----
        This implementation moves each point in the polygon by adding the vector to it.
        Arc points are preserved, and holes are also moved by the same vector.
        """
        from ansys.edb.core.geometry.polygon_data import PolygonData
        from ansys.edb.core.utility import conversions
        
        # Convert vector to PointData for easy addition
        vector_point = conversions.to_point(vector)
        
        # Move all points in the polygon
        moved_points = []
        for point in polygon.points:
            moved_point = point.move(vector_point)
            if moved_point is not None:
                moved_points.append(moved_point)
            else:
                # If move returns None (arc points), keep the original point
                moved_points.append(point)
        
        # Move holes
        moved_holes = []
        for hole in polygon.holes:
            moved_hole = self.move(hole, vector)
            moved_holes.append(moved_hole)
        
        # Create and return new PolygonData with moved points
        return PolygonData(
            points=moved_points,
            holes=moved_holes,
            sense=polygon.sense,
            closed=polygon.is_closed
        )

    def rotate(self, polygon: PolygonData, angle: float, center: tuple[float, float]) -> PolygonData:
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

        Notes
        -----
        This implementation rotates each point in the polygon around the given center.
        Arc points are preserved, and holes are also rotated around the same center.
        """
        from ansys.edb.core.geometry.point_data import PointData
        from ansys.edb.core.geometry.polygon_data import PolygonData
        from ansys.edb.core.utility import conversions
        
        # Convert center to PointData
        center_point = conversions.to_point(center)
        
        # Rotate all points in the polygon
        rotated_points = []
        for point in polygon.points:
            if point.is_arc:
                rotated_point = point  # Preserve arc points as-is
            else:
                rotated_point = point.rotate(angle, center_point)
            rotated_points.append(rotated_point)
                
        
        # Rotate holes
        rotated_holes = []
        for hole in polygon.holes:
            rotated_hole = self.rotate(hole, angle, center)
            rotated_holes.append(rotated_hole)
        
        # Create and return new PolygonData with rotated points
        return PolygonData(
            points=rotated_points,
            holes=rotated_holes,
            sense=polygon.sense,
            closed=polygon.is_closed
        )

    def scale(self, polygon: PolygonData, factor: float, center: tuple[float, float]) -> PolygonData:
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

        Notes
        -----
        This implementation scales each point in the polygon relative to the given center.
        The scaling is done by: new_point = center + factor * (point - center).
        Arc points are preserved with their heights scaled, and holes are also scaled from the same center.
        """
        from ansys.edb.core.geometry.point_data import PointData
        from ansys.edb.core.geometry.polygon_data import PolygonData
        from ansys.edb.core.utility import conversions
        
        # Convert center to PointData
        center_point = conversions.to_point(center)
        cx, cy = center_point.x.double, center_point.y.double
        
        # Scale all points in the polygon
        scaled_points = []
        for point in polygon.points:
            # Create new point, preserving arc information
            if point.is_arc:
                # For arc points, scale the height as well
                new_height = point.arc_height * factor
                scaled_point = PointData(new_height)
            else:
                # Get the point coordinates
                px, py = point.x.double, point.y.double
                
                # Calculate scaled position: new_point = center + factor * (point - center)
                new_x = cx + factor * (px - cx)
                new_y = cy + factor * (py - cy)

                scaled_point = PointData(new_x, new_y)
            
            scaled_points.append(scaled_point)
        
        # Scale holes
        scaled_holes = []
        for hole in polygon.holes:
            scaled_hole = self.scale(hole, factor, center)
            scaled_holes.append(scaled_hole)
        
        # Create and return new PolygonData with scaled points
        return PolygonData(
            points=scaled_points,
            holes=scaled_holes,
            sense=polygon.sense,
            closed=polygon.is_closed
        )

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

        Notes
        -----
        This implementation mirrors each point in the polygon across the vertical line x=constant.
        The mirroring is done by: new_x = 2*x - old_x, new_y = old_y.
        Arc points are preserved with their heights negated (to maintain arc direction),
        and holes are also mirrored across the same line.
        The polygon sense is also flipped (CCW becomes CW and vice versa) because mirroring
        reverses the orientation.
        """
        from ansys.edb.core.geometry.point_data import PointData
        from ansys.edb.core.geometry.polygon_data import PolygonData, PolygonSenseType
        
        # Mirror all points in the polygon
        mirrored_points = []
        for point in polygon.points:
            # Create new point, preserving arc information
            if point.is_arc:
                # For arc points, negate the height to maintain correct arc orientation
                new_height = -point.arc_height.double
                mirrored_point = PointData(new_height)
            else:
                # Get the point coordinates
                px, py = point.x.double, point.y.double
                
                # Calculate mirrored position: new_x = 2*x - old_x
                new_x = 2 * x - px
                new_y = py

                mirrored_point = PointData(new_x, new_y)
            
            mirrored_points.append(mirrored_point)
        
        # Mirror holes
        mirrored_holes = []
        for hole in polygon.holes:
            mirrored_hole = self.mirror_x(hole, x)
            mirrored_holes.append(mirrored_hole)
        
        # Flip the polygon sense (mirroring reverses orientation)
        new_sense = (
            PolygonSenseType.SENSE_CW 
            if polygon.sense == PolygonSenseType.SENSE_CCW 
            else PolygonSenseType.SENSE_CCW
        )
        
        # Create and return new PolygonData with mirrored points
        return PolygonData(
            points=mirrored_points,
            holes=mirrored_holes,
            sense=new_sense,
            closed=polygon.is_closed
        )

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
        from shapely.ops import unary_union
        from shapely.geometry import MultiPoint
        from ansys.edb.core.geometry.polygon_data import PolygonData, PolygonSenseType
        
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
        
        # Convert back to PolygonData (convex hull is always CCW)
        return self._shapely_to_polygon_data(hull_geom, PolygonSenseType.SENSE_CCW)

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
        return self._shapely_to_polygon_data(simplified_polygon, polygon.sense)

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

    def circle_intersect(self, polygon: PolygonData, center: tuple[float, float], radius: float) -> bool:
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
        shapely_polygon = self._to_shapely_polygon(polygon)
        
        # Create a circle as a buffered point
        circle_center = ShapelyPoint(center)
        circle = circle_center.buffer(radius)
        
        # Check if the circle intersects with the polygon
        return shapely_polygon.intersects(circle)

    def closest_point(self, polygon: PolygonData, point: tuple[float, float]) -> tuple[float, float]:
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
        from ansys.edb.core.geometry.point_data import PointData
        
        shapely_polygon = self._to_shapely_polygon(polygon)
        shapely_point = ShapelyPoint(point)
        
        # Find the nearest points between the polygon boundary and the given point
        # nearest_points returns a tuple of (nearest point on geom1, nearest point on geom2)
        nearest_on_polygon, _ = nearest_points(shapely_polygon.boundary, shapely_point)
        
        return PointData(nearest_on_polygon.x, nearest_on_polygon.y)
