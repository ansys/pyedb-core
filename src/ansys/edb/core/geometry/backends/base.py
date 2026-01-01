"""Abstract base class for polygon computation backends."""

from __future__ import annotations

from abc import ABC, abstractmethod
import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.geometry.point_data import PointData
    from ansys.edb.core.geometry.polygon_data import PolygonData


class PolygonBackend(ABC):
    """Abstract base class for polygon computation backends.

    This class defines the interface that all computation backends must implement.
    Backends handle geometry operations that can be performed either on the server
    or locally using libraries like Shapely.
    """

    @staticmethod
    def _sanitize_points(points: list[PointData], tol: float = 1e-9) -> list[PointData]:
        """Remove duplicate points and fix arc points at the start/end of the point list.

        Parameters
        ----------
        points : list[PointData]
            The list of points to sanitize.
        tol : float, default: 1e-9
            Tolerance for detecting duplicate points.

        Returns
        -------
        list[PointData]
            Sanitized list of points with duplicates removed and arc endpoints fixed.

        Notes
        -----
        Arc points require a preceding regular point to define the arc start.
        This method ensures that if the first or last point is an arc, an appropriate
        regular point is added before/after it.
        """
        if not points:
            return []

        sanitized = points.copy()

        if sanitized[0].is_arc:
            prev_point = sanitized[-2] if sanitized[-1].is_arc else sanitized[-1]
            sanitized.insert(0, PointData(prev_point.x.double, prev_point.y.double))

        if sanitized[-1].is_arc:
            next_point = sanitized[1] if sanitized[0].is_arc else sanitized[0]
            sanitized.append(PointData(next_point.x.double, next_point.y.double))

        unique_points = [sanitized[0]]
        for point in sanitized[1:]:
            last_point = unique_points[-1]
            if not (
                math.isclose(point.x.double, last_point.x.double, rel_tol=tol, abs_tol=tol)
                and math.isclose(point.y.double, last_point.y.double, rel_tol=tol, abs_tol=tol)
            ):
                unique_points.append(point)
        if not (
            math.isclose(
                unique_points[0].x.double, unique_points[-1].x.double, rel_tol=tol, abs_tol=tol
            )
            and math.isclose(
                unique_points[0].y.double, unique_points[-1].y.double, rel_tol=tol, abs_tol=tol
            )
        ):
            unique_points.append(unique_points[0])

        return unique_points

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
        if height < 0:
            center_x = chord_mid_x - perp_dx * (radius + height)
            center_y = chord_mid_y - perp_dy * (radius + height)
        else:
            center_x = chord_mid_x + perp_dx * (radius - height)
            center_y = chord_mid_y + perp_dy * (radius - height)

        dot_product = (x1 - center_x) * (x2 - center_x) + (y1 - center_y) * (y2 - center_y)
        temp = dot_product / (radius * radius)
        if abs(temp) > 1.0 + 1e-10:
            raise ValueError("Numerical error in arc tessellation: acos argument out of range.")
        if abs(temp) > 1.0:
            temp = max(-1.0, min(1.0, temp))
        temp_angle = math.acos(temp)
        angle1 = math.atan2(y1 - center_y, x1 - center_x)

        if radius <= abs(height):
            temp_angle = 2 * math.pi - temp_angle

        if height < 0:
            arc_angle = temp_angle
        elif height >= 0:
            arc_angle = -temp_angle

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

        return points, (center_x, center_y), radius

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

        points = PolygonBackend._sanitize_points(points)

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
                    arc_coords, _, _ = PolygonBackend._tessellate_arc(
                        start, end, height, max_chord_error, max_arc_angle, max_points
                    )
                    # arc_coords includes the end point, so add all of them
                    coords.extend(arc_coords[:-1])  # Exclude end point for now

                    # Move to the end point (i+2), which will be processed in next iteration
                    i += 2
                else:
                    RuntimeError("Invalid arc definition: arc point without an end point.")
            else:
                # Regular point - just add it
                coords.append((pt.x.double, pt.y.double))
                i += 1

        # Remove consecutive duplicate points that may have arisen from tessellation
        i = 0
        while i < len(coords) - 1:
            if math.isclose(coords[i][0], coords[i + 1][0], rel_tol=1e-9) and math.isclose(
                coords[i][1], coords[i + 1][1], rel_tol=1e-9
            ):
                coords.pop(i + 1)
            i += 1

        return coords

    @staticmethod
    def _is_box(polygon: PolygonData, tol: float = 1e-9) -> bool:
        """Check if points form a box (rectangle).

        A box is defined as a rectangle (quadrilateral with 4 right angles).
        This shared implementation is used by all backends to ensure consistency.

        Parameters
        ----------
        points : list[PointData]
            The list of points to check. Should be preprocessed (sanitized and
            optionally deduplicated) by the calling backend.
        tol : float, default: 1e-9
            Tolerance for box detection.

        Returns
        -------
        bool
            ``True`` when the points form a box, ``False`` otherwise.

        Notes
        -----
        This method expects that the calling backend has already:
        1. Checked for holes and arcs (boxes cannot have either)
        2. Sanitized the points
        3. Optionally removed consecutive duplicates
        4. Extended the points list to close the loop on both ends
        """

        def extract_next_vector(
            pts: list[PointData], i: int
        ) -> tuple[tuple[float, float] | None, int]:
            n = len(pts)
            pt = pts[i]
            if i + 1 < n:
                start = pt
                end = pts[i + 1]
                i += 1
            else:
                return None, i

            return (end.x.double - start.x.double, end.y.double - start.y.double), i

        points = PolygonBackend._sanitize_points(polygon.points.copy())

        points = [
            points[-2],
            points[-1],
            *points,
            points[0],
            points[1],
        ]  # Close the loop on both ends

        index = 0
        while index < len(points):
            vec1, index = extract_next_vector(points, index)
            if vec1 is None:
                break

            vec2, index = extract_next_vector(points, index)
            if vec2 is None:
                break

            dot_product = vec1[0] * vec2[0] + vec1[1] * vec2[1]
            if not math.isclose(math.hypot(*vec1), 0.0, rel_tol=tol):
                dot_product /= math.hypot(*vec1)
            if not math.isclose(math.hypot(*vec2), 0.0, rel_tol=tol):
                dot_product /= math.hypot(*vec2)

            if not (
                math.isclose(dot_product, 0.0, rel_tol=tol)
                or math.isclose(dot_product, 1.0, rel_tol=tol)
            ):
                return False

            index -= 1

        return True

    @staticmethod
    def _without_arcs(
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
        exterior_coords = PolygonBackend._extract_coordinates_with_arcs(
            polygon.points, max_chord_error, max_arc_angle, max_points
        )

        # Convert coordinates back to PointData objects (non-arc points)
        new_points = [PointData(x, y) for x, y in exterior_coords]

        # Process holes
        new_holes = []
        for hole in polygon.holes:
            hole_coords = PolygonBackend._extract_coordinates_with_arcs(
                hole.points, max_chord_error, max_arc_angle, max_points
            )
            hole_points = [PointData(x, y) for x, y in hole_coords]
            # Create a new PolygonData for the hole without arcs

            new_hole = PolygonData(points=hole_points, sense=hole.sense, closed=hole.is_closed)
            new_holes.append(new_hole)

        # Create and return new PolygonData without arcs
        return PolygonData(
            points=new_points, holes=new_holes, sense=polygon.sense, closed=polygon.is_closed
        )

    @abstractmethod
    def area(self, polygon: PolygonData) -> float:
        """Compute the area of a polygon.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to compute area for.

        Returns
        -------
        float
            Area of the polygon.
        """
        pass

    @abstractmethod
    def is_convex(self, polygon: PolygonData) -> bool:
        """Determine whether the polygon is convex.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to check.

        Returns
        -------
        bool
            ``True`` when the polygon is convex, ``False`` otherwise.
        """
        pass

    @abstractmethod
    def is_circle(self, polygon: PolygonData) -> bool:
        """Determine whether the outer contour of the polygon is a circle.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to check.

        Returns
        -------
        bool
            ``True`` when the outer contour of the polygon is a circle, ``False`` otherwise.
        """
        pass

    @abstractmethod
    def is_box(self, polygon: PolygonData) -> bool:
        """Determine whether the outer contour of the polygon is a box.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to check.

        Returns
        -------
        bool
            ``True`` when the outer contour of the polygon is a box, ``False`` otherwise.
        """
        pass

    @abstractmethod
    def is_inside(self, polygon: PolygonData, point: tuple[float, float]) -> bool:
        """Determine whether a point is inside the polygon.

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
        pass

    @abstractmethod
    def bbox(self, polygon: PolygonData) -> tuple[tuple[float, float], tuple[float, float]]:
        """Compute the bounding box of a polygon.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to compute bounding box for.

        Returns
        -------
        tuple[tuple[float, float], tuple[float, float]]
            Bounding box as ((min_x, min_y), (max_x, max_y)).
        """
        pass

    @abstractmethod
    def bbox_of_polygons(
        self, polygons: list[PolygonData]
    ) -> tuple[tuple[float, float], tuple[float, float]]:
        """Compute the bounding box of a list of polygons.

        Parameters
        ----------
        polygons : list[PolygonData]
            List of polygons to compute bounding box for.

        Returns
        -------
        tuple[tuple[float, float], tuple[float, float]]
            Bounding box as ((min_x, min_y), (max_x, max_y)).
        """
        pass

    @abstractmethod
    def without_arcs(
        self,
        polygon: PolygonData,
        max_chord_error: float = 0,
        max_arc_angle: float = math.pi / 6,
        max_points: int = 8,
    ) -> PolygonData:
        """Get polygon data with all arcs removed.

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
        pass

    @abstractmethod
    def has_self_intersections(self, polygon: PolygonData, tol: float = 1e-9) -> bool:
        """Determine whether the polygon contains any self-intersections.

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
        pass

    @abstractmethod
    def remove_self_intersections(
        self, polygon: PolygonData, tol: float = 1e-9
    ) -> list[PolygonData]:
        """Remove self-intersections from a polygon.

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
        pass

    @abstractmethod
    def normalized(self, polygon: PolygonData) -> list:
        """Get the normalized points of the polygon.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to process.

        Returns
        -------
        list[PointData]
            List of normalized points.
        """
        pass

    @abstractmethod
    def move(self, polygon: PolygonData, vector: tuple[float, float]) -> PolygonData:
        """Move the polygon by a vector.

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
        pass

    @abstractmethod
    def rotate(
        self,
        polygon: PolygonData,
        angle: float,
        center: tuple[float, float],
        use_radians: bool = True,
    ) -> PolygonData:
        """Rotate the polygon at a center by an angle.

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
        pass

    @abstractmethod
    def scale(
        self, polygon: PolygonData, factor: float, center: tuple[float, float]
    ) -> PolygonData:
        """Scale the polygon by a linear factor from a center.

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
        pass

    @abstractmethod
    def mirror_x(self, polygon: PolygonData, x: float) -> PolygonData:
        """Mirror the polygon across a vertical line at x.

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
        pass

    @abstractmethod
    def bounding_circle(self, polygon: PolygonData) -> tuple[tuple[float, float], float]:
        """Compute the bounding circle of the polygon.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to compute bounding circle for.

        Returns
        -------
        tuple[tuple[float, float], float]
            Bounding circle as ((center_x, center_y), radius).
        """
        pass

    @abstractmethod
    def convex_hull(self, polygons: list[PolygonData]) -> PolygonData:
        """Compute the convex hull of the union of a list of polygons.

        Parameters
        ----------
        polygons : list[PolygonData]
            List of polygons.

        Returns
        -------
        PolygonData
            The convex hull polygon.
        """
        pass

    @abstractmethod
    def defeature(self, polygon: PolygonData, tol: float = 1e-9) -> PolygonData:
        """Defeature a polygon by removing small features.

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
        pass

    @abstractmethod
    def intersection_type(self, polygon: PolygonData, other: PolygonData, tol: float = 1e-9):
        """Get the intersection type with another polygon.

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
        pass

    @abstractmethod
    def circle_intersect(
        self, polygon: PolygonData, center: tuple[float, float], radius: float
    ) -> bool:
        """Determine whether a circle intersects with a polygon.

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
        pass

    @abstractmethod
    def closest_point(
        self, polygon: PolygonData, point: tuple[float, float]
    ) -> tuple[float, float]:
        """Compute a point on the polygon that is closest to another point.

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
        pass

    @abstractmethod
    def closest_points(
        self, polygon1: PolygonData, polygon2: PolygonData
    ) -> tuple[tuple[float, float], tuple[float, float]]:
        """Compute points on two polygons that are closest to each other.

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
        """
        pass

    @abstractmethod
    def unite(self, polygons: list[PolygonData]) -> list[PolygonData]:
        """Compute the union of a list of polygons.

        Parameters
        ----------
        polygons : list[PolygonData]
            List of polygons to unite.

        Returns
        -------
        list[PolygonData]
            List of polygons resulting from the union.
        """
        pass

    @abstractmethod
    def intersect(
        self, polygons1: list[PolygonData], polygons2: list[PolygonData]
    ) -> list[PolygonData]:
        """Compute the intersection of two lists of polygons.

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
        pass

    @abstractmethod
    def subtract(
        self, polygons1: list[PolygonData], polygons2: list[PolygonData]
    ) -> list[PolygonData]:
        """Subtract a set of polygons from another set of polygons.

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
        pass

    @abstractmethod
    def xor(self, polygons1: list[PolygonData], polygons2: list[PolygonData]) -> list[PolygonData]:
        """Compute an exclusive OR between two sets of polygons.

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
        pass

    @abstractmethod
    def expand(
        self,
        polygon: PolygonData,
        offset: float,
        round_corner: bool,
        max_corner_ext: float,
        tol: float = 1e-9,
    ) -> list[PolygonData]:
        """Expand the polygon by an offset.

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
        pass

    @abstractmethod
    def alpha_shape(self, points: list[tuple[float, float]], alpha: float) -> list[PolygonData]:
        """Compute the outline of a 2D point cloud using alpha shapes.

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
        """
        pass
