"""Abstract base class for arc computation backends.

Defines the interface that all arc computation backends must implement.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.geometry.arc_data import ArcData
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.geometry.point_data import PointData

import math


class ArcBackend(ABC):
    """Abstract base class for arc computation backends.

    Backends perform operations that can be executed either on the server or
    locally using libraries such as Shapely or Build123d. Implementations must
    provide the methods declared below.
    """

    @staticmethod
    def _sanitize_points(points: list[PointData], tol: float = 1e-10) -> list[PointData]:
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
        from ansys.edb.core.geometry.point_data import PointData

        if not points:
            return []

        sanitized = points.copy()

        if sanitized[0].is_arc:
            prev_point = sanitized[-2] if sanitized[-1].is_arc else sanitized[-1]
            sanitized.insert(0, PointData(prev_point.x.double, prev_point.y.double))

        if sanitized[-1].is_arc:
            next_point = sanitized[1] if sanitized[0].is_arc else sanitized[0]
            sanitized.append(PointData(next_point.x.double, next_point.y.double))

        assert not sanitized[0].is_arc
        assert not sanitized[-1].is_arc
        for i in range(1, len(sanitized) - 1):
            assert not (sanitized[i].is_arc and sanitized[i - 1].is_arc)

        unique_points = [sanitized[0]]
        index = 1
        while index < len(sanitized):
            point = sanitized[index]

            if point.is_arc:
                unique_points.append(point)
                index += 1
                point = sanitized[index]
                last_point = unique_points[-2]
            else:
                last_point = unique_points[-1]

            if not (
                math.isclose(point.x.double, last_point.x.double, rel_tol=tol, abs_tol=tol)
                and math.isclose(point.y.double, last_point.y.double, rel_tol=tol, abs_tol=tol)
            ):
                unique_points.append(point)

            index += 1

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
        arc: ArcData,
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
        from ansys.edb.core.geometry.point_data import PointData

        start = arc.start
        end = arc.end
        height = arc.height

        x1, y1 = start.x.double, start.y.double
        x2, y2 = end.x.double, end.y.double

        chord_dx = x2 - x1
        chord_dy = y2 - y1
        chord_length = math.sqrt(chord_dx * chord_dx + chord_dy * chord_dy)

        if math.isclose(height, 0.0, abs_tol=1e-12):
            if math.isclose(chord_length, 0.0, abs_tol=1e-12):
                return ([(x1, y1), (x2, y2)], PointData(x2, y2), PointData(x2, y2), 0.0)
            return (
                [(x1, y1), (x2, y2)],
                PointData(math.nan, math.nan),
                PointData(0.5 * (x1 + x2), 0.5 * (y1 + y2)),
                math.inf,
            )

        h = abs(height)
        radius = (h**2 + (chord_length / 2.0) ** 2) / (2.0 * h)

        chord_mid_x = (x1 + x2) / 2.0
        chord_mid_y = (y1 + y2) / 2.0

        mid_x = chord_mid_x
        mid_y = chord_mid_y

        # If the chord_length is zero, assume the perpendicular vector as (-1.0, 0.0).
        perp_dx = -1.0
        perp_dy = 0.0
        if not math.isclose(chord_length, 0.0, abs_tol=1e-12):
            perp_dx = chord_dy / chord_length
            perp_dy = -chord_dx / chord_length

            mid_x = chord_mid_x - perp_dx * height
            mid_y = chord_mid_y - perp_dy * height

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

        points = []
        angle_step = arc_angle / num_segments

        for i in range(1, num_segments + 1):
            angle = angle1 + angle_step * i
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))

        return (points, PointData(center_x, center_y), PointData(mid_x, mid_y), radius)

    @abstractmethod
    def center(self, arc: "ArcData") -> "PointData":
        """Return the center point of the arc."""
        pass

    @abstractmethod
    def midpoint(self, arc: "ArcData") -> "PointData":
        """Return the midpoint of the arc."""
        pass

    @abstractmethod
    def radius(self, arc: "ArcData") -> float:
        """Return the radius of the arc."""
        pass

    @abstractmethod
    def bbox(self, arc: "ArcData") -> "PolygonData":
        """Return the bounding box (polygon) of the arc."""
        pass

    @abstractmethod
    def closest_points(self, arc1: "ArcData", arc2: "ArcData") -> tuple["PointData", "PointData"]:
        """Return the pair of closest points between two arcs."""
        pass

    @abstractmethod
    def angle(self, arc: "ArcData", other: "ArcData" | None = None) -> float:
        """Return the angle of the arc or the angle between two arcs."""
        pass

    @abstractmethod
    def length(self, arc: "ArcData") -> float:
        """Return the length of the arc."""
        pass

    @abstractmethod
    def points(self, arc: "ArcData") -> list["PointData"]:
        """Return representative points for the arc (start, height, end)."""
        pass
