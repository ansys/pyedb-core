"""Shapely-based computation backend for client-side operations."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.geometry.polygon_data import PolygonData

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
    def _to_shapely_polygon(polygon: PolygonData) -> ShapelyPolygon:
        """Convert a PolygonData object to a Shapely Polygon.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to convert.

        Returns
        -------
        ShapelyPolygon
            Shapely polygon object.

        Notes
        -----
        This method handles:
        - Converting points to coordinate tuples
        - Handling holes in polygons
        - Approximating arcs with line segments (if present)
        - Caching the result on the PolygonData instance to avoid repeated conversions
        """
        # Check if we have a cached Shapely polygon
        if hasattr(polygon, "_shapely_cache"):
            return polygon._shapely_cache

        # Get the outer boundary coordinates
        # Note: If polygon has arcs, we should use without_arcs() first
        if polygon.has_arcs():
            # Convert arcs to line segments using server
            polygon = polygon.without_arcs()
            # without_arcs() returns a new PolygonData, so recursively process it
            return ShapelyBackend._to_shapely_polygon(polygon)

        # Extract coordinates from points
        exterior_coords = [(pt.x.double, pt.y.double) for pt in polygon.points]

        # Handle holes
        holes = []
        for hole in polygon.holes:
            if hole.has_arcs():
                # Convert hole arcs to line segments using server
                hole = hole.without_arcs()
            hole_coords = [(pt.x.double, pt.y.double) for pt in hole.points]
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
        return shapely_poly.contains(shapely_point)

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
