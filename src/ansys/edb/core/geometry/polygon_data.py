"""Polygon data."""

from enum import Enum
import itertools
import math

from ansys.api.edb.v1 import edb_defs_pb2, point_data_pb2, polygon_data_pb2_grpc

from ansys.edb.core import session
from ansys.edb.core.geometry.arc_data import ArcData
from ansys.edb.core.inner import messages, parser
from ansys.edb.core.utility import conversions


class PolygonSenseType(Enum):
    """Provides an enum representing the direction of polygon sense."""

    SENSE_UNKNOWN = point_data_pb2.SENSE_UNKNOWN
    SENSE_CW = point_data_pb2.SENSE_CW
    SENSE_CCW = point_data_pb2.SENSE_CCW


class ExtentType(Enum):
    """Provides an enum representing extent types for geometries."""

    CONFORMING = edb_defs_pb2.CONFORMING
    BOUNDING_BOX = edb_defs_pb2.BOUNDING_BOX


class PolygonData:
    """Represents a polygon data object."""

    __stub: polygon_data_pb2_grpc.PolygonDataServiceStub = session.StubAccessor(
        session.StubType.polygon_data
    )

    def __init__(
        self,
        points=None,
        arcs=None,
        lower_left=None,
        upper_right=None,
        holes=None,
        sense=PolygonSenseType.SENSE_CCW,
        closed=True,
    ):
        """Create a polygon.

        Parameters
        ----------
        points : list[ansys.edb.core.typing.PointLike], default: None
        arcs : list[ArcData], default: None
        lower_left : ansys.edb.core.typing.PointLike, default: None
        upper_right : ansys.edb.core.typing.PointLike, default: None
        holes : List[ansys.edb.core.geometry.polygon_data.PolygonData], default: None
        sense : ansys.edb.core.geometry.polygon_data.PolygonSenseType, default: SENSE_CCW
        closed : bool, default: True
        """
        self._holes, self._sense, self._is_closed = (
            [] if holes is None else holes,
            PolygonSenseType(sense),
            closed,
        )

        if points is not None:
            self._points = [conversions.to_point(pt) for pt in points]
        elif arcs is not None:
            self._points = list(
                itertools.chain.from_iterable(
                    [[arc.start, arc.end] if arc.is_segment() else arc.points for arc in arcs]
                )
            )
        elif lower_left is not None and upper_right is not None:
            ll, ur = [conversions.to_point(pt) for pt in [lower_left, upper_right]]
            self._points = [
                conversions.to_point(pt)
                for pt in [(ll.x, ll.y), (ur.x, ll.y), (ur.x, ur.y), (ll.x, ur.y)]
            ]
        else:
            raise TypeError("PolygonData must be initialized from a list of points/arcs or a box.")

    def __len__(self):
        """Get the number of coordinates.

        Returns
        -------
        int
        """
        return len(self.points)

    @property
    def points(self):
        """:obj:`list` of :class:`.PointData`: List of coordinates for the points."""
        return self._points

    @property
    def holes(self):
        """:obj:`list` of :class:`.PolygonData`: List of holes."""
        return self._holes

    @property
    def arc_data(self):
        """:obj:`list`: List of segments that represent the arc data of a polygon."""
        i, n = 0, len(self)
        i_max = n if self.is_closed else n - 1
        segments = []

        while i < i_max:
            h, incr = 0, 1
            p1, p2 = self.points[i], self.points[(i + incr) % n]
            if p2.is_arc:
                h, incr = p2.arc_height, 2
                p2 = self.points[(i + incr) % n]
            segments.append(ArcData(p1, p2, height=h))
            i += incr
        return segments

    def _is_ccw(self):
        return self._sense == PolygonSenseType.SENSE_CCW

    @property
    def is_closed(self):
        """:obj:`bool`: Flag indicating if a polygon is closed between the first and last points."""
        return self._is_closed

    @property
    def sense(self):
        """:class:`PolygonSenseType`: Polygon sense type."""
        return self._sense

    def is_hole(self):
        """Determine whether the polygon is a hole.

        Returns
        -------
        bool
            ``True`` when the polygon is a hole, ``False`` otherwise.
        """
        return self.is_closed and not self._is_ccw()

    def is_parametric(self):
        """Determine whether a polygon contains any parametrized points.

        Returns
        -------
        bool
            ``True`` when the polygon contains parametrized points, ``False`` otherwise.
        """
        return any(pt.is_parametric for pt in self.points)

    def has_arcs(self):
        """Determine whether the polygon contains any arcs.

        Returns
        -------
        bool
            ``True`` when the polygon contains arcs, ``False`` otherwise.
        """
        return any(pt.is_arc for pt in self.points)

    def has_holes(self):
        """Determine whether the polygon contains any holes.

        Returns
        -------
        bool
            ``True`` when the polygon contains holes, ``False`` otherwise.
        """
        return len(self.holes) > 0

    def is_circle(self):
        """Determine whether the outer contour of the polygon is a circle.

        Returns
        -------
        bool
            ``True`` when the outer contour of the polygon is a circle holes, ``False`` otherwise.
        """
        return self.__stub.IsCircle(messages.polygon_data_message(self)).value

    def is_box(self):
        """Determine whether the outer contour of the polygon is a box.

        Returns
        -------
        bool
            ``True`` when the outer corner of the polygon is a box, ``False`` otherwise.
        """
        return self.__stub.IsBox(messages.polygon_data_message(self)).value

    def is_convex(self):
        """Determine whether the polygon is a convex hull.

        Returns
        -------
        bool
            ``True`` when the polygon is a convex hull, ``False`` otherwise.
        """
        return self.__stub.IsConvex(messages.polygon_data_message(self)).value

    def area(self):
        """Compute the area of the polygon.

        Returns
        -------
        float
            Area of the polygon.
        """
        return self.__stub.GetArea(messages.polygon_data_message(self)).value

    def has_self_intersections(self, tol=1e-9):
        """Determine whether the polygon contains any self-intersections.

        Parameters
        ----------
        tol : float, default: 1e-9
            Tolerance.

        Returns
        -------
        bool
            ``True`` when the polygon contains self-intersections, ``False`` otherwise.
        """
        return self.__stub.HasSelfIntersections(
            messages.polygon_data_with_tol_message(self, tol)
        ).value

    @parser.to_polygon_data
    def remove_self_intersections(self, tol=1e-9):
        """Create a polygon with all self-intersections removed.

        Parameters
        ----------
        tol : float, default: 1e-9
            Tolerance.

        Returns
        -------
        PolygonData
        """
        return self.__stub.RemoveSelfIntersections(
            messages.polygon_data_with_tol_message(self, tol)
        )

    @parser.to_point_data_list
    def normalized(self):
        """Get the normalized points of the polygon.

        Returns
        -------
        list[.PointData]
        """
        return self.__stub.GetNormalizedPoints(messages.polygon_data_message(self))

    @parser.to_polygon_data
    def move(self, vector):
        """Move the polygon by a vector.

        Parameters
        ----------
        vector : ansys.edb.core.typing.PointLikeT
            Vector in the form: ``(x, y)``.

        Returns
        -------
        PolygonData
        """
        return self.__stub.Transform(messages.polygon_data_transform_message("move", self, vector))

    @parser.to_polygon_data
    def rotate(self, angle, center):
        """Rotate the polygon at a center by an angle.

        Parameters
        ----------
        angle : float
            Angle in radians.
        center : ansys.edb.core.typing.PoinyLikeT
            Center.

        Returns
        -------
        PolygonData
        """
        return self.__stub.Transform(
            messages.polygon_data_transform_message("rotate", self, angle, center)
        )

    @parser.to_polygon_data
    def scale(self, factor, center):
        """Scale the polygon by a linear factor from a center.

        Parameters
        ----------
        factor : float
            Linear factor.
        center : ansys.edb.core.typing.PointLikeT
            Center.

        Returns
        -------
        PolygonData
        """
        return self.__stub.Transform(
            messages.polygon_data_transform_message("scale", factor, center)
        )

    @parser.to_polygon_data
    def mirror_x(self, x):
        """Mirror a polygon by x line.

        Parameters
        ----------
        x : float
            X line.

        Returns
        -------
        PolygonData
        """
        return self.__stub.Transform(messages.polygon_data_transform_message("mirror_x", x))

    @parser.to_box
    def bbox(self):
        """Compute the bounding box.

        Returns
        -------
        tuple[.PointData, .PointData]
        """
        return self.__stub.GetBBox(messages.polygon_data_list_message([self]))

    @classmethod
    @parser.to_box
    def bbox_of_polygons(cls, polygons):
        """Compute the bounding box of a list of polygons.

        Parameters
        ----------
        polygons: list[PolygonData]
            List of polygons.

        Returns
        -------
        tuple[.PointData, .PointData]
        """
        return cls.__stub.GetBBox(messages.polygon_data_list_message(polygons))

    @parser.to_circle
    def bounding_circle(self):
        """Compute the bounding circle of the polygon.

        Returns
        -------
        tuple[.PointData, .Value]
        """
        return self.__stub.GetBoundingCircle(messages.polygon_data_message(self))

    @classmethod
    @parser.to_polygon_data
    def convex_hull(cls, polygons):
        """Compute the convex hull of the union of a list of polygons.

        Parameters
        ----------
        others : list[PolygonData]
            List of polygons.

        Returns
        -------
        PolygonData
        """
        return cls.__stub.GetConvexHull(messages.polygon_data_list_message(polygons))

    @parser.to_polygon_data
    def without_arcs(self, max_chord_error=0, max_arc_angle=math.pi / 6, max_points=8):
        """Get polygon data with all arcs removed.

        Parameters
        ----------
        max_chord_error : float, default: 0
        max_arc_angle : float, default: math.pi
        max_points : int, default: 8

        Returns
        -------
        PolygonData
        """
        return self.__stub.RemoveArcs(
            messages.polygon_data_remove_arc_message(
                self, max_chord_error, max_arc_angle, max_points
            )
        )

    @parser.to_polygon_data
    def defeature(self, tol=1e-9):
        """Defeature a polygon.

        Parameters
        ----------
        tol : float, default: 1e-9
            Tolerance.

        Returns
        -------
        PolygonData
        """
        return self.__stub.Defeature(messages.polygon_data_with_tol_message(self, tol))

    def is_inside(self, point):
        """Determine whether the point is inside the polygon.

        Parameters
        ----------
        point : ansys.edb.core.typing.PointLikeT

        Returns
        -------
        bool
            ``True`` if the point is inside the polygon, ``False`` otherwise.
        """
        return self.__stub.IsInside(messages.polygon_data_with_point_message(self, point)).value

    def intersection_type(self, other, tol=1e-9):
        """Get the intersection type with another polygon.

        Parameters
        ----------
        other : PolygonData
            Other polygon.
        tol : float, default: 1e-9
            Tolerance.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.
        """
        return self.__stub.GetIntersectionType(
            messages.polygon_data_pair_with_tolerance_message(self, other, tol)
        )

    def circle_intersect(self, center, radius):
        """Determine whether the circle intersects with a polygon.

        Parameters
        ----------
        center : ansys.edb.core.typing.PointLikeT
            Center.
        radius : float
            Radius.

        Returns
        -------
        bool
            ``True`` if the circle intersects with a polygon, ``False`` otherwise.
        """
        return self.__stub.CircleIntersectsPolygon(
            messages.polygon_data_with_circle_message(self, center, radius)
        ).value

    @parser.to_point_data
    def closest_point(self, point):
        """Compute a point on the polygon that is closest to another point.

        Parameters
        ----------
        point : ansys.edb.core.typing.PointLikeT
           Other point.

        Returns
        -------
        .PointData
            Point closest to the given point.
        """
        return self.__stub.GetClosestPoints(
            messages.polygon_data_with_points_message(self, point=point)
        ).points[0]

    @parser.to_point_data_list
    def closest_points(self, polygon):
        """Compute points on this and another polygon that are closest to the other polygon.

        Parameters
        ----------
        polygon : PolygonData

        Returns
        -------
        tuple[.PointData, .PointData]
        """
        return self.__stub.GetClosestPoints(
            messages.polygon_data_with_points_message(self, polygon=polygon)
        ).points

    @classmethod
    @parser.to_polygon_data_list
    def unite(cls, polygons):
        """Compute the union of a list of polygons.

        Parameters
        ----------
        polygons: list[PolygonData]
            List of polygons.

        Returns
        -------
        list[PolygonData]
        """
        return cls.__stub.GetUnion(messages.polygon_data_list_message(polygons))

    @classmethod
    @parser.to_polygon_data_list
    def intersect(cls, polygons1, polygons2):
        """Compute the intersection of one or more lists of polygons.

        Parameters
        ----------
        polygons1: `list` of :class:`.PolygonData` or :class:`.PolygonData`
            First list of polygons.
        polygons2: `list` of :class:`.PolygonData` or :class:`.PolygonData`
            Second optional list of polygons.

        Returns
        -------
        list[PolygonData]
        """
        return cls.__stub.GetIntersection(messages.polygon_data_pair_message(polygons1, polygons2))

    @classmethod
    @parser.to_polygon_data_list
    def subtract(cls, polygons1, polygons2):
        """Subtract a set of polygons from another set of polygons.

        Parameters
        ----------
        polygons1 : list[PolygonData], PolygonData
            List of base polygons.
        polygons2 : list[PolygonData], PolygonData
            List of polygons to subtract.

        Returns
        -------
        list[PolygonData]
        """
        return cls.__stub.Subtract(messages.polygon_data_pair_message(polygons1, polygons2))

    @classmethod
    @parser.to_polygon_data_list
    def xor(cls, polygons1, polygons2):
        """Compute an exclusive OR between a set of polygons and another set of polygons.

        Parameters
        ----------
        polygons1 : list[PolygonData], PolygonData
            First list of polygons.
        polygons2 : list[PolygonData], PolygonData
            Second list of polygons.

        Returns
        -------
        list[PolygonData]
        """
        return cls.__stub.Xor(messages.polygon_data_pair_message(polygons1, polygons2))

    @parser.to_polygon_data_list
    def expand(self, offset, round_corner, max_corner_ext, tol=1e-9):
        """Expand the polygon by an offset.

        Parameters
        ----------
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
        """
        return self.__stub.Expand(
            messages.polygon_data_expand_message(self, offset, tol, round_corner, max_corner_ext)
        )

    @classmethod
    @parser.to_polygon_data_list
    def alpha_shape(cls, points, alpha):
        """Compute the outline of a 2D point cloud using alpha shapes.

        Parameters
        ----------
        points : list[ansys.edb.core.typing.PointLikeT]
            List of points.
        alpha : float

        Returns
        -------
        list[PolygonData]
        """
        return cls.__stub.Get2DAlphaShape(
            messages.polygon_data_get_alpha_shape_message(points, alpha)
        )
