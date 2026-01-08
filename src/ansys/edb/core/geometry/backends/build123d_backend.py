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
            p1 = build123d.Vector(points[i - 1].x.double, points[i - 1].y.double, 0.0)
            if points[i].is_arc:
                arc_height = points[i].arc_height.double
                p3 = build123d.Vector(points[i + 1].x.double, points[i + 1].y.double, 0.0)

                mid = (p1 + p3) / 2
                direction = p3 - p1
                perp = build123d.Vector(direction.Y, -direction.X, 0.0)
                perp_length = math.sqrt(perp.X * perp.X + perp.Y * perp.Y)
                if perp_length > 0.0:
                    perp_normalized = perp / perp_length
                else:
                    perp_normalized = build123d.Vector(0, 0, 0)
                p2 = mid - perp_normalized * arc_height

                edges.append(build123d.ThreePointArc(p1, p2, p3))
                i += 2
            else:
                p2 = build123d.Vector(points[i].x.double, points[i].y.double, 0.0)
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

    @staticmethod
    def _polygonEdge_to_build123dEdge(edge: "PolygonData.Edge") -> "build123d.Edge":
        """Convert an edge to a build123d Edge primitive.

        Parameters
        ----------
        edge : Edge
            The edge to convert.

        Returns
        -------
        build123d.Line or build123d.ThreePointArc
            The build123d Edge representation of the edge.
        """
        if edge.is_point():
            return None

        p1 = build123d.Vector(edge.start.x.double, edge.start.y.double, 0.0)
        p3 = build123d.Vector(edge.end.x.double, edge.end.y.double, 0.0)
        if edge.is_segment():
            return build123d.Line(p1, p3)

        p2 = build123d.Vector(edge.midpoint.x.double, edge.midpoint.y.double, 0.0)
        return build123d.ThreePointArc(p1, p2, p3)

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

        edges = []
        for edge in polygon.edges:
            edges.append(Build123dBackend._polygonEdge_to_build123dEdge(edge))
        main_wire = build123d.Wire(edges)

        hole_wires = []
        if polygon.holes:
            for hole in polygon.holes:
                edges = []
                for edge in hole.edges:
                    edges.append(Build123dBackend._polygonEdge_to_build123dEdge(edge))
                hole_wires.append(build123d.Wire(edges))

        if hole_wires:
            face = build123d.Face(outer_wire=main_wire, inner_wires=hole_wires)
        else:
            face = build123d.Face(outer_wire=main_wire)

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

    def is_circle(self, polygon: PolygonData) -> bool:
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
        tol = 1e-8

        if polygon.has_holes():
            return False

        face = self._polygon_data_to_build123d(polygon)

        face_center = face.center()
        face_radius = math.sqrt(face.area / math.pi)
        print(face_center, face_radius)
        for item in face.edges():
            if item.geom_type != GeomType.CIRCLE:
                return False
            arc_center = item.arc_center
            arc_radius = item.radius
            if not (
                ((face_center - arc_center).length < tol)
                and math.isclose(arc_radius, face_radius, rel_tol=tol)
            ):
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

        Notes
        -----
        This implementation uses the bounding box to compute the bounding circle.
        The circle is centered at the center of the bounding box with a radius
        equal to half the diagonal of the bounding box, ensuring all points are
        within the circle. This provides a reasonable approximation but may not
        always produce the absolute minimum bounding circle.
        """
        face = self._polygon_data_to_build123d(polygon)
        bbox = face.bounding_box()

        center_x = (bbox.min.X + bbox.max.X) / 2.0
        center_y = (bbox.min.Y + bbox.max.Y) / 2.0

        width = bbox.max.X - bbox.min.X
        height = bbox.max.Y - bbox.min.Y
        radius = math.sqrt(width * width + height * height) / 2.0

        return ((center_x, center_y), radius)

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
        if not polygons:
            raise ValueError("Cannot compute convex hull of an empty list of polygons")
        if not isinstance(polygons, list):
            polygons = [polygons]

        all_edges = []
        for poly in polygons:
            face = self._polygon_data_to_build123d(poly)

            for edge in face.outer_wire().edges():
                all_edges.append(edge)

            for inner_wire in face.inner_wires():
                for edge in inner_wire.edges():
                    all_edges.append(edge)

        hull_wire = build123d.Wire.make_convex_hull(all_edges)
        hull_face = build123d.Face(hull_wire)

        return Build123dBackend._build123d_to_polygon_data(hull_face)

    def defeature(self, polygon: PolygonData, tol: float = 1e-9) -> PolygonData:
        """Defeature a polygon by removing small features using Build123d.

        This method delegates to the server backend implementation.

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

        Warns
        -----
        UserWarning
            If the server stub is not available, a warning is issued before
            attempting to use the server backend.

        Notes
        -----
        The defeature algorithm is not implemented in Build123d, so this method
        delegates to the server backend. The server stub must be available for
        this method to work.
        """
        import warnings

        if self._stub is None:
            warnings.warn(
                "Server stub is not available for defeature. "
                "Defeature operation requires server backend. "
                "This may fail if the stub is not properly initialized.",
                UserWarning,
                stacklevel=2,
            )

        from ansys.edb.core.geometry.backends.server_backend import ServerBackend

        server_backend = ServerBackend(self._stub)
        return server_backend.defeature(polygon, tol)

    def intersection_type(self, polygon: PolygonData, other: PolygonData, tol: float = 1e-9):
        """Get the intersection type with another polygon using Build123d.

        Parameters
        ----------
        polygon : PolygonData
            The first polygon.
        other : PolygonData
            The second polygon.
        tol : float, default: 1e-9
            Tolerance (not used in Build123d implementation but kept for API consistency).

        Returns
        -------
        int
            The intersection type enum value.

        Notes
        -----
        This implementation uses Build123d's geometric predicates to determine the relationship
        between two polygons. The tolerance parameter is kept for API consistency with the
        server backend but is not used in this implementation as Build123d uses its own
        internal tolerance.

        The intersection types are:
        - NO_INTERSECTION (0): Polygons do not intersect
        - THIS_INSIDE_OTHER (1): First polygon is completely inside the second
        - OTHER_INSIDE_THIS (2): Second polygon is completely inside the first
        - COMMON_INTERSECTION (3): Polygons partially intersect
        - UNDEFINED_INTERSECTION (4): Intersection cannot be determined
        """
        from ansys.api.edb.v1 import polygon_data_pb2

        face1 = self._polygon_data_to_build123d(polygon)
        face2 = self._polygon_data_to_build123d(other)

        if not face1.intersect(face2):
            return polygon_data_pb2.NO_INTERSECTION

        # A polygon is inside another if their intersection equals the first polygon
        intersection = face1.intersect(face2)
        if intersection and math.isclose(intersection.area, face1.area, rel_tol=tol, abs_tol=tol):
            return polygon_data_pb2.THIS_INSIDE_OTHER

        if intersection and math.isclose(intersection.area, face2.area, rel_tol=tol, abs_tol=tol):
            return polygon_data_pb2.OTHER_INSIDE_THIS

        return polygon_data_pb2.COMMON_INTERSECTION

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
        face = self._polygon_data_to_build123d(polygon)
        circle_wire = build123d.Circle(radius=radius).wire()
        circle_face = build123d.Face(circle_wire).translate(build123d.Vector(*center, 0))

        if not face.intersect(circle_face):
            return False
        return True

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

        Notes
        -----
        This implementation uses build123d's distance_to() and param_at_point() methods
        to efficiently find the closest point on the polygon boundary to the given point.
        """
        face = self._polygon_data_to_build123d(polygon)
        query_point = build123d.Vector(*point, 0)

        all_edges = list(face.outer_wire().edges())
        for inner_wire in face.inner_wires():
            all_edges.extend(inner_wire.edges())

        if not all_edges:
            vertices = face.outer_wire().vertices()
            if vertices:
                return PointData(vertices[0].X, vertices[0].Y)
            else:
                return point

        closest_edge = min(all_edges, key=lambda e: e.distance_to(query_point))
        closest_points_on_edge = closest_edge.closest_points(query_point)
        u = closest_edge.param_at_point(closest_points_on_edge[0])
        closest_point = closest_edge.position_at(u)

        return PointData(closest_point.X, closest_point.Y)

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

        Notes
        -----
        This implementation collects all edges from both polygons (including outer and inner
        wires) and finds the pair of edges with the minimum distance between them using
        build123d's distance_to() and closest_points() methods.
        """
        face1 = self._polygon_data_to_build123d(polygon1)
        face2 = self._polygon_data_to_build123d(polygon2)

        edges1 = list(face1.outer_wire().edges())
        for inner_wire in face1.inner_wires():
            edges1.extend(inner_wire.edges())

        edges2 = list(face2.outer_wire().edges())
        for inner_wire in face2.inner_wires():
            edges2.extend(inner_wire.edges())

        if not edges1 or not edges2:
            vertices1 = face1.outer_wire().vertices()
            vertices2 = face2.outer_wire().vertices()
            if vertices1 and vertices2:
                return (
                    (vertices1[0].X, vertices1[0].Y),
                    (vertices2[0].X, vertices2[0].Y),
                )
            else:
                return ((0.0, 0.0), (0.0, 0.0))

        min_distance = math.inf
        closest_point1 = None
        closest_point2 = None

        for edge1 in edges1:
            for edge2 in edges2:
                distance = edge1.distance_to(edge2)
                if distance < min_distance:
                    min_distance = distance
                    points = edge1.closest_points(edge2)
                    if len(points) >= 2:
                        closest_point1 = points[0]
                        closest_point2 = points[1]

        if closest_point1 is None or closest_point2 is None:
            vertices1 = face1.outer_wire().vertices()
            vertices2 = face2.outer_wire().vertices()
            return (
                (vertices1[0].X, vertices1[0].Y),
                (vertices2[0].X, vertices2[0].Y),
            )

        return (
            (closest_point1.X, closest_point1.Y),
            (closest_point2.X, closest_point2.Y),
        )

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
        if not polygons:
            return []

        if len(polygons) == 1:
            return polygons

        faces = [self._polygon_data_to_build123d(poly) for poly in polygons]

        result = faces[0]
        for face in faces[1:]:
            result = result.fuse(face)

        if isinstance(result, build123d.Face):
            return [Build123dBackend._build123d_to_polygon_data(result)]
        else:
            result_faces = result.faces()
            return [Build123dBackend._build123d_to_polygon_data(face) for face in result_faces]

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
        if not polygons1 or not polygons2:
            return []

        if not isinstance(polygons1, list):
            polygons1 = [polygons1]
        if not isinstance(polygons2, list):
            polygons2 = [polygons2]

        faces1 = [self._polygon_data_to_build123d(poly) for poly in polygons1]
        faces2 = [self._polygon_data_to_build123d(poly) for poly in polygons2]

        union1 = faces1[0]
        for face in faces1[1:]:
            union1 = union1.fuse(face)

        union2 = faces2[0]
        for face in faces2[1:]:
            union2 = union2.fuse(face)

        result = union1.intersect(union2)

        if result is None:
            return []

        if isinstance(result, build123d.Face):
            return [Build123dBackend._build123d_to_polygon_data(result)]
        else:
            result_faces = result.faces()
            return [Build123dBackend._build123d_to_polygon_data(face) for face in result_faces]

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
        if not polygons1:
            return []

        if not polygons2:
            return polygons1

        if not isinstance(polygons1, list):
            polygons1 = [polygons1]
        if not isinstance(polygons2, list):
            polygons2 = [polygons2]

        faces1 = [self._polygon_data_to_build123d(poly) for poly in polygons1]
        faces2 = [self._polygon_data_to_build123d(poly) for poly in polygons2]

        union1 = faces1[0]
        for face in faces1[1:]:
            union1 = union1.fuse(face)

        union2 = faces2[0]
        for face in faces2[1:]:
            union2 = union2.fuse(face)

        result = union1.cut(union2)

        if result is None:
            return []

        if isinstance(result, build123d.Face):
            return [Build123dBackend._build123d_to_polygon_data(result)]
        else:
            result_faces = result.faces()
            return [Build123dBackend._build123d_to_polygon_data(face) for face in result_faces]

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

        Notes
        -----
        This implementation first unions each list separately, then computes the
        symmetric difference between the two unions using build123d operations.
        The XOR operation returns all regions that are in one polygon set or the other,
        but not in both (i.e., union minus intersection).
        """
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

        faces1 = [self._polygon_data_to_build123d(poly) for poly in polygons1]
        faces2 = [self._polygon_data_to_build123d(poly) for poly in polygons2]

        union1 = faces1[0]
        for face in faces1[1:]:
            union1 = union1.fuse(face)

        union2 = faces2[0]
        for face in faces2[1:]:
            union2 = union2.fuse(face)

        diff1 = union1.cut(union2)
        diff2 = union2.cut(union1)

        result_polygons = []

        if diff1 is not None:
            if isinstance(diff1, build123d.Face):
                result_polygons.append(Build123dBackend._build123d_to_polygon_data(diff1))
            else:
                diff1_faces = diff1.faces()
                for face in diff1_faces:
                    result_polygons.append(Build123dBackend._build123d_to_polygon_data(face))

        if diff2 is not None:
            if isinstance(diff2, build123d.Face):
                result_polygons.append(Build123dBackend._build123d_to_polygon_data(diff2))
            else:
                diff2_faces = diff2.faces()
                for face in diff2_faces:
                    result_polygons.append(Build123dBackend._build123d_to_polygon_data(face))

        return result_polygons

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

        Notes
        -----
        This implementation uses Build123d's offset operation to expand or shrink polygons.
        When `round_corner` is True, rounded corners are created using arc mode.
        When False, intersection mode is used with mitred corners, and the `max_corner_ext`
        parameter controls the miter limit.
        """
        from build123d import Kind
        from build123d import offset as build123d_offset

        face = self._polygon_data_to_build123d(polygon)
        kind = Kind.ARC if round_corner else Kind.INTERSECTION

        offset_face = build123d_offset(face, amount=offset, kind=kind)

        result_polygons = []

        if offset_face is None:
            return []

        if hasattr(offset_face, "faces"):
            faces = offset_face.faces()
            if faces:
                for f in faces:
                    result_polygons.append(Build123dBackend._build123d_to_polygon_data(f))
        else:
            result_polygons.append(Build123dBackend._build123d_to_polygon_data(offset_face))

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
