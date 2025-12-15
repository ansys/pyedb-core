"""Abstract base class for polygon computation backends."""

from __future__ import annotations

from abc import ABC, abstractmethod
import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.geometry.polygon_data import PolygonData


class PolygonBackend(ABC):
    """Abstract base class for polygon computation backends.

    This class defines the interface that all computation backends must implement.
    Backends handle geometry operations that can be performed either on the server
    or locally using libraries like Shapely.
    """

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
    def remove_self_intersections(self, polygon: PolygonData, tol: float = 1e-9) -> list[PolygonData]:
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
    def rotate(self, polygon: PolygonData, angle: float, center: tuple[float, float]) -> PolygonData:
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
    def scale(self, polygon: PolygonData, factor: float, center: tuple[float, float]) -> PolygonData:
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
    def circle_intersect(self, polygon: PolygonData, center: tuple[float, float], radius: float) -> bool:
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
    def closest_point(self, polygon: PolygonData, point: tuple[float, float]) -> tuple[float, float]:
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
    def closest_points(self, polygon1: PolygonData, polygon2: PolygonData) -> tuple[tuple[float, float], tuple[float, float]]:
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
    def xor(
        self, polygons1: list[PolygonData], polygons2: list[PolygonData]
    ) -> list[PolygonData]:
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
        self, polygon: PolygonData, offset: float, round_corner: bool, max_corner_ext: float, tol: float = 1e-9
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
