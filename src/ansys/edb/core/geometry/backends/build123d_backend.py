"""Build123d-based computation backend for client-side operations."""

from __future__ import annotations

import math

from ansys.edb.core.geometry.arc_data import ArcData
from ansys.edb.core.geometry.backends.base import PolygonBackend
from ansys.edb.core.geometry.point_data import PointData
from ansys.edb.core.geometry.polygon_data import PolygonData

try:
    import build123d
    from build123d import GeomType

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

    @staticmethod
    def _points_to_wire(points: list[PointData]) -> "build123d.Wire":
        """Convert a list of PointData objects to a build123d Wire.

        Parameters
        ----------
        points : list[PointData]
            The list of points defining the wire. Arc points must be followed by
            an endpoint to complete the arc definition.

        Returns
        -------
        build123d.Wire
            A wire constructed from line segments and arcs based on the point data.

        Notes
        -----
        This method constructs a wire by iterating through the points and creating
        either line segments or three-point arcs. When an arc point is encountered,
        it uses the previous point as the start, calculates a midpoint based on the
        arc height, and uses the next point as the end of the arc.
        """
        edges = []
        i = 1
        while i < len(points):
            p1 = build123d.Vector(points[i - 1].x.double, points[i - 1].y.double)
            if points[i].is_arc:
                arc_height = points[i].arc_height.double
                p3 = build123d.Vector(points[i + 1].x.double, points[i + 1].y.double)

                mid = (p1 + p3) / 2
                direction = p3 - p1
                perp = build123d.Vector(direction.Y, -direction.X)
                perp_length = math.sqrt(perp.X**2 + perp.Y**2)
                if perp_length > 0:
                    perp_normalized = perp / perp_length
                else:
                    perp_normalized = build123d.Vector(0, 0)
                p2 = mid - perp_normalized * arc_height

                edges.append(build123d.ThreePointArc(p1, p2, p3))
                i += 2
            else:
                p2 = build123d.Vector(points[i].x.double, points[i].y.double)
                edges.append(build123d.Line(p1, p2))
                i += 1

        return build123d.Wire(edges)

    @staticmethod
    def _edge_to_arc_data(edge: "build123d.Edge") -> ArcData:
        """Convert a build123d Edge to an ArcData object.

        Parameters
        ----------
        edge : build123d.Edge
            The edge to convert.

        Returns
        -------
        ArcData
            The ArcData representation of the edge.
        """
        start_point = edge.start_point()
        end_point = edge.end_point()
        arc_height = 0.0

        if edge.geom_type == GeomType.CIRCLE:
            mid_point = 0.5 * (start_point + end_point)
            edge_center = edge.center()
            arc_height = (mid_point - edge_center).length
            v1 = end_point - start_point
            v2 = edge_center - start_point
            cross_product = v1.cross(v2)
            if cross_product.Z < 0:
                arc_height = -arc_height

        return ArcData(
            (start_point.X, start_point.Y), (end_point.X, end_point.Y), height=arc_height
        )

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
        The result is cached on the PolygonData instance to avoid repeated conversions.
        """
        if hasattr(polygon, "_build123d_cache"):
            return polygon._build123d_cache

        points = PolygonBackend._sanitize_points(polygon.points)
        main_wire = Build123dBackend._points_to_wire(points)

        hole_wires = []
        if polygon.holes:
            for hole_polygon in polygon.holes:
                hole_points = PolygonBackend._sanitize_points(hole_polygon.points)
                hole_wires.append(Build123dBackend._points_to_wire(hole_points))

        if hole_wires:
            face = build123d.Face(main_wire, hole_wires)
        else:
            face = build123d.Face(main_wire)

        polygon._build123d_cache = face
        return face

    @staticmethod
    def _build123d_to_polygon_data(face: "build123d.Face") -> PolygonData:
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
        """
        params = {"arcs": [], "holes": []}

        outer_wire = face.outer_wire()
        for edge in outer_wire.edges():
            params["arcs"].append(Build123dBackend._edge_to_arc_data(edge))

        inner_wires = face.inner_wires()
        for wire in inner_wires:
            hole = []
            for edge in wire.edges():
                hole.append(Build123dBackend._edge_to_arc_data(edge))
            params["holes"].append(PolygonData(arcs=hole))

        return PolygonData(**params)

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
        if polygon.has_holes():
            return False

        face = self._polygon_data_to_build123d(polygon)

        outer_wire = build123d.Wire(face.edges())
        hull_wire = outer_wire.make_convex_hull(outer_wire.edges())
        hull_face = build123d.Face(hull_wire)

        return math.isclose(face.area, hull_face.area, rel_tol=1e-9)

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
        if polygon.has_holes():
            return False

        face = self._polygon_data_to_build123d(polygon)

        face_center = tuple(face.center())
        face_radius = math.sqrt(face.area / math.pi)
        for item in face.edges():
            try:
                arc_center = item.arc_center
                arc_radius = item.radius
                if not (
                    math.isclose(math.dist(face_center, arc_center), 0.0, abs_tol=tol)
                    and math.isclose(arc_radius, face_radius, rel_tol=tol)
                ):
                    return False
            except Exception:
                return False

        return True

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
        # A box cannot have holes or arcs
        if (
            polygon.has_holes() or polygon.has_arcs()
        ):  # If the polygon was set up with arcs of zero height, the has_arcs() will return False.
            return False

        return PolygonBackend._is_box(polygon, tol)

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
        face = self._polygon_data_to_build123d(polygon)
        point = build123d.Vector(point[0], point[1], 0)
        return face.is_inside(point)

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
        face = self._polygon_data_to_build123d(polygon)
        bbox = face.bounding_box()
        return ((bbox.min.X, bbox.min.Y), (bbox.max.X, bbox.max.Y))

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
        if not polygons:
            return ((0.0, 0.0), (0.0, 0.0))

        min_x, min_y = math.inf, math.inf
        max_x, max_y = -math.inf, -math.inf

        # Expand to include all other polygons
        for polygon in polygons:
            face = self._polygon_data_to_build123d(polygon)
            bbox = face.bounding_box()
            min_x = min(min_x, bbox.min.X)
            min_y = min(min_y, bbox.min.Y)
            max_x = max(max_x, bbox.max.X)
            max_y = max(max_y, bbox.max.Y)

        return ((min_x, min_y), (max_x, max_y))

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
        return PolygonBackend._without_arcs(polygon, max_chord_error, max_arc_angle, max_points)

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
        import warnings

        if self._stub is None:
            warnings.warn(
                "Server stub is not available for has_self_intersections. "
                "Self-intersection detection requires server backend. "
                "This may fail if the stub is not properly initialized.",
                UserWarning,
                stacklevel=2,
            )

        from ansys.edb.core.geometry.backends.server_backend import ServerBackend

        server_backend = ServerBackend(self._stub)
        return server_backend.has_self_intersections(polygon, tol)

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

        Notes
        -----
        This method normalizes the polygon orientation:
        - Outer contours (shell) are returned in counter-clockwise (CCW) order
        - Holes are returned in clockwise (CW) order

        Build123d's faces can have their wires oriented, and we extract the
        outer wire to ensure CCW orientation for the normalized points.
        """
        face = self._polygon_data_to_build123d(polygon)
        outer_wire = face.outer_wire()

        return [PointData(vertex.X, vertex.Y) for vertex in outer_wire.vertices()]

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
        face = self._polygon_data_to_build123d(polygon)
        moved_face = face.translate(build123d.Vector(*vector, 0))

        return Build123dBackend._build123d_to_polygon_data(moved_face)

    def rotate(
        self, polygon: PolygonData, angle: float, center: tuple[float, float], use_radians: bool
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
        # Build123d expects angle in degrees.
        if use_radians:
            angle = math.degrees(angle)

        face = self._polygon_data_to_build123d(polygon)
        rotated_face = face.rotate(
            axis=build123d.Axis(
                origin=build123d.Vector(*center, 0), direction=build123d.Vector(0, 0, 1)
            ),
            angle=angle,
        )

        return Build123dBackend._build123d_to_polygon_data(rotated_face)

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
        face = self._polygon_data_to_build123d(polygon)
        scaled_face = face.scale(factor=factor)
        scaled_face = scaled_face.translate(
            build123d.Vector(center[0] * (1 - factor), center[1] * (1 - factor), 0)
        )

        return Build123dBackend._build123d_to_polygon_data(scaled_face)

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
        face = self._polygon_data_to_build123d(polygon)
        mirror_plane = build123d.Plane(
            origin=build123d.Vector(x, 0, 0), z_dir=build123d.Vector(1, 0, 0)
        )
        mirrored_face = face.mirror(mirror_plane)

        return Build123dBackend._build123d_to_polygon_data(mirrored_face)

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
