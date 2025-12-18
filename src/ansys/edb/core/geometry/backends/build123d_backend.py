"""Build123d-based computation backend for client-side operations."""

from __future__ import annotations

import math

from ansys.edb.core.geometry.backends.base import PolygonBackend
from ansys.edb.core.geometry.point_data import PointData
from ansys.edb.core.geometry.polygon_data import PolygonData

try:
    import build123d

    BUILD123D_AVAILABLE = True
except ImportError:
    BUILD123D_AVAILABLE = False


class Build123dBackend(PolygonBackend):
    """Build123d-based computation backend.

    This backend performs computations locally using the Build123d library,
    reducing the number of RPC calls to the server and improving performance
    for geometry-intensive operations.

    Raises
    ------
    ImportError
        If Build123d is not installed.
    """

    def __init__(self, stub=None):
        """Initialize the Build123d backend.

        Parameters
        ----------
        stub : polygon_data_pb2_grpc.PolygonDataServiceStub, optional
            The gRPC stub for polygon operations. Required for operations that
            may need to delegate to the server backend.

        Raises
        ------
        ImportError
            If Build123d is not installed.
        """
        if not BUILD123D_AVAILABLE:
            raise ImportError(
                "Build123d is not installed. Install it with: pip install build123d "
                "(check the pyproject.toml for the correct version)\n"
                "Or set PYEDB_COMPUTATION_BACKEND=server to use the server backend."
            )
        self._stub = stub

    def _polygon_data_to_build123d(self, polygon: PolygonData) -> "build123d.Face":
        """Convert a PolygonData object to a build123d Face.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to convert.

        Returns
        -------
        build123d.Face
            The build123d Face representation of the polygon.

        Notes
        -----
        This method converts the outer contour and holes of a PolygonData to build123d.
        Arcs in the polygon are currently tessellated into line segments.
        The result is cached on the PolygonData instance to avoid repeated conversions.
        """
        # Check if we have a cached build123d face
        if hasattr(polygon, "_build123d_cache"):
            return polygon._build123d_cache

        # Extract outer contour points
        outer_points = []
        for point in polygon.points:
            if point.is_arc:
                # For now, arcs need to be tessellated
                # This is a simplified approach - arc handling would need refinement
                continue
            outer_points.append((point.x.double, point.y.double))

        # Create the outer wire from points
        outer_wire = build123d.Wire.make_polygon(
            [build123d.Vector(x, y) for x, y in outer_points], close=polygon.is_closed
        )

        # Handle holes if present
        hole_wires = []
        if polygon.holes:
            for hole_polygon in polygon.holes:
                hole_points = []
                for point in hole_polygon.points:
                    if point.is_arc:
                        continue
                    hole_points.append((point.x.double, point.y.double))

                hole_wire = build123d.Wire.make_polygon(
                    [build123d.Vector(x, y) for x, y in hole_points], close=hole_polygon.is_closed
                )
                hole_wires.append(hole_wire)

        # Create face with outer contour and holes
        if hole_wires:
            face = build123d.Face(outer_wire, hole_wires)
        else:
            face = build123d.Face(outer_wire)

        # Cache the result for future use
        polygon._build123d_cache = face
        return face

    def _build123d_to_polygon_data(self, face: "build123d.Face") -> PolygonData:
        """Convert a build123d Face to a PolygonData object.

        Parameters
        ----------
        face : build123d.Face
            The build123d Face to convert.

        Returns
        -------
        PolygonData
            The PolygonData representation of the face.

        Notes
        -----
        This method converts build123d faces back to PolygonData format.
        Curved edges are tessellated into line segments.
        """
        # Get the outer wire
        outer_wire = face.outer_wire()

        # Extract points from outer wire
        outer_points = []
        for vertex in outer_wire.vertices():
            outer_points.append(PointData(vertex.X, vertex.Y))

        # Handle inner wires (holes)
        holes = []
        inner_wires = face.inner_wires()
        for wire in inner_wires:
            hole_points = []
            for vertex in wire.vertices():
                hole_points.append(PointData(vertex.X, vertex.Y))
            holes.append(PolygonData(points=hole_points, closed=True))

        # Create and return the PolygonData
        return PolygonData(points=outer_points, holes=holes if holes else None, closed=True)

    def area(self, polygon: PolygonData) -> float:
        """Compute the area of a polygon using Build123d.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to compute area for.

        Returns
        -------
        float
            Area of the polygon.
        """
        face = self._polygon_data_to_build123d(polygon)
        return face.area

    def is_convex(self, polygon: PolygonData) -> bool:
        """Determine whether the polygon is convex using Build123d.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to check.

        Returns
        -------
        bool
            ``True`` when the polygon is convex, ``False`` otherwise.
        """
        raise NotImplementedError("Build123d backend: is_convex method not yet implemented")

    def is_circle(self, polygon: PolygonData, tol: float = 1e-9) -> bool:
        """Determine whether the outer contour of the polygon is a circle using Build123d.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to check.
        tol : float, default: 1e-9
            Tolerance for circle detection.

        Returns
        -------
        bool
            ``True`` when the outer contour of the polygon is a circle, ``False`` otherwise.
        """
        raise NotImplementedError("Build123d backend: is_circle method not yet implemented")

    def is_box(self, polygon: PolygonData, tol: float = 1e-9) -> bool:
        """Determine whether the outer contour of the polygon is a box using Build123d.

        A box is defined as a rectangle (quadrilateral with 4 right angles).

        Parameters
        ----------
        polygon : PolygonData
            The polygon to check.
        tol : float, default: 1e-9
            Tolerance for box detection.

        Returns
        -------
        bool
            ``True`` when the outer contour of the polygon is a box, ``False`` otherwise.
        """
        raise NotImplementedError("Build123d backend: is_box method not yet implemented")

    def is_inside(self, polygon: PolygonData, point: tuple[float, float]) -> bool:
        """Determine whether a point is inside the polygon using Build123d.

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
        raise NotImplementedError("Build123d backend: is_inside method not yet implemented")

    def bbox(self, polygon: PolygonData) -> tuple[tuple[float, float], tuple[float, float]]:
        """Compute the bounding box of a polygon using Build123d.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to compute bounding box for.

        Returns
        -------
        tuple[tuple[float, float], tuple[float, float]]
            Bounding box as ((min_x, min_y), (max_x, max_y)).
        """
        raise NotImplementedError("Build123d backend: bbox method not yet implemented")

    def bbox_of_polygons(
        self, polygons: list[PolygonData]
    ) -> tuple[tuple[float, float], tuple[float, float]]:
        """Compute the bounding box of a list of polygons using Build123d.

        Parameters
        ----------
        polygons : list[PolygonData]
            List of polygons to compute bounding box for.

        Returns
        -------
        tuple[tuple[float, float], tuple[float, float]]
            Bounding box as ((min_x, min_y), (max_x, max_y)).
        """
        raise NotImplementedError("Build123d backend: bbox_of_polygons method not yet implemented")

    def without_arcs(
        self,
        polygon: PolygonData,
        max_chord_error: float = 0,
        max_arc_angle: float = math.pi / 6,
        max_points: int = 8,
    ) -> PolygonData:
        """Get polygon data with all arcs removed using Build123d.

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
        raise NotImplementedError("Build123d backend: without_arcs method not yet implemented")

    def has_self_intersections(self, polygon: PolygonData, tol: float = 1e-9) -> bool:
        """Determine whether the polygon contains any self-intersections using Build123d.

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
        raise NotImplementedError(
            "Build123d backend: has_self_intersections method not yet implemented"
        )

    def remove_self_intersections(
        self, polygon: PolygonData, tol: float = 1e-9
    ) -> list[PolygonData]:
        """Remove self-intersections from a polygon using Build123d.

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
        raise NotImplementedError(
            "Build123d backend: remove_self_intersections method not yet implemented"
        )

    def normalized(self, polygon: PolygonData) -> list:
        """Get the normalized points of the polygon using Build123d.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to process.

        Returns
        -------
        list[PointData]
            List of normalized points where outer contours are CCW and holes are CW.
        """
        raise NotImplementedError("Build123d backend: normalized method not yet implemented")

    def move(self, polygon: PolygonData, vector: tuple[float, float]) -> PolygonData:
        """Move the polygon by a vector using Build123d.

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
        raise NotImplementedError("Build123d backend: move method not yet implemented")

    def rotate(
        self, polygon: PolygonData, angle: float, center: tuple[float, float]
    ) -> PolygonData:
        """Rotate the polygon at a center by an angle using Build123d.

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
        raise NotImplementedError("Build123d backend: rotate method not yet implemented")

    def scale(
        self, polygon: PolygonData, factor: float, center: tuple[float, float]
    ) -> PolygonData:
        """Scale the polygon by a linear factor from a center using Build123d.

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
        raise NotImplementedError("Build123d backend: scale method not yet implemented")

    def mirror_x(self, polygon: PolygonData, x: float) -> PolygonData:
        """Mirror the polygon across a vertical line at x using Build123d.

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
        raise NotImplementedError("Build123d backend: mirror_x method not yet implemented")

    def bounding_circle(self, polygon: PolygonData) -> tuple[tuple[float, float], float]:
        """Compute the bounding circle of the polygon using Build123d.

        Parameters
        ----------
        polygon : PolygonData
            The polygon to compute bounding circle for.

        Returns
        -------
        tuple[tuple[float, float], float]
            Bounding circle as ((center_x, center_y), radius).
        """
        raise NotImplementedError("Build123d backend: bounding_circle method not yet implemented")

    def convex_hull(self, polygons: list[PolygonData]) -> PolygonData:
        """Compute the convex hull of the union of a list of polygons using Build123d.

        Parameters
        ----------
        polygons : list[PolygonData]
            List of polygons.

        Returns
        -------
        PolygonData
            The convex hull polygon.
        """
        raise NotImplementedError("Build123d backend: convex_hull method not yet implemented")

    def defeature(self, polygon: PolygonData, tol: float = 1e-9) -> PolygonData:
        """Defeature a polygon by removing small features using Build123d.

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
        """
        raise NotImplementedError("Build123d backend: defeature method not yet implemented")

    def intersection_type(self, polygon: PolygonData, other: PolygonData, tol: float = 1e-9):
        """Get the intersection type with another polygon using Build123d.

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
        raise NotImplementedError("Build123d backend: intersection_type method not yet implemented")

    def circle_intersect(
        self, polygon: PolygonData, center: tuple[float, float], radius: float
    ) -> bool:
        """Determine whether a circle intersects with a polygon using Build123d.

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
        raise NotImplementedError("Build123d backend: circle_intersect method not yet implemented")

    def closest_point(
        self, polygon: PolygonData, point: tuple[float, float]
    ) -> tuple[float, float]:
        """Compute a point on the polygon that is closest to another point using Build123d.

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
        raise NotImplementedError("Build123d backend: closest_point method not yet implemented")

    def closest_points(
        self, polygon1: PolygonData, polygon2: PolygonData
    ) -> tuple[tuple[float, float], tuple[float, float]]:
        """Compute points on two polygons that are closest to each other using Build123d.

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
        raise NotImplementedError("Build123d backend: closest_points method not yet implemented")

    def unite(self, polygons: list[PolygonData]) -> list[PolygonData]:
        """Compute the union of a list of polygons using Build123d.

        Parameters
        ----------
        polygons : list[PolygonData]
            List of polygons to unite.

        Returns
        -------
        list[PolygonData]
            List of polygons resulting from the union.
        """
        raise NotImplementedError("Build123d backend: unite method not yet implemented")

    def intersect(
        self, polygons1: list[PolygonData], polygons2: list[PolygonData]
    ) -> list[PolygonData]:
        """Compute the intersection of two lists of polygons using Build123d.

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
        raise NotImplementedError("Build123d backend: intersect method not yet implemented")

    def subtract(
        self, polygons1: list[PolygonData], polygons2: list[PolygonData]
    ) -> list[PolygonData]:
        """Subtract a set of polygons from another set of polygons using Build123d.

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
        raise NotImplementedError("Build123d backend: subtract method not yet implemented")

    def xor(self, polygons1: list[PolygonData], polygons2: list[PolygonData]) -> list[PolygonData]:
        """Compute an exclusive OR between two sets of polygons using Build123d.

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
        raise NotImplementedError("Build123d backend: xor method not yet implemented")

    def expand(
        self,
        polygon: PolygonData,
        offset: float,
        round_corner: bool,
        max_corner_ext: float,
        tol: float = 1e-9,
    ) -> list[PolygonData]:
        """Expand the polygon by an offset using Build123d.

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
        raise NotImplementedError("Build123d backend: expand method not yet implemented")

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
        The alpha shape algorithm is not implemented in Build123d, so this method
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
