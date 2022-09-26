"""Polygon Data."""

from enum import Enum
import itertools
import math

from ansys.api.edb.v1 import point_data_pb2, polygon_data_pb2_grpc

from ansys.edb import session
from ansys.edb.core import messages, parser
from ansys.edb.geometry.arc_data import ArcData
from ansys.edb.utility import conversions


class PolygonSenseType(Enum):
    """Direction of polygon sense."""

    SENSE_UNKNOWN = point_data_pb2.SENSE_UNKNOWN
    SENSE_CW = point_data_pb2.SENSE_CW
    SENSE_CCW = point_data_pb2.SENSE_CCW


class PolygonData:
    """Class representing a polygon data object."""

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
        closed=None,
    ):
        """Create a polygon.

        Parameters
        ----------
        points : list[ansys.edb.typing.PointLike], optional
        arcs : list[ArcData], optional
        lower_left : ansys.edb.typing.PointLike, optional
        upper_right : ansys.edb.typing.PointLike, optional
        holes : ansys.edb.geometry.PointData, optional
        sense : ansys.edb.geometry.PolygonSenseType, optional
        closed : bool, optional
        """
        self._holes, self._sense, self._is_closed = (
            [] if holes is None else holes,
            PolygonSenseType(sense),
            True if closed is None else closed,
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
        """Get the list of coordinates.

        Returns
        -------
        list[ansys.edb.geometry.PointData]
        """
        return self._points

    @property
    def holes(self):
        """Get the list of holes.

        Returns
        -------
        list[PolygonData]
        """
        return self._holes

    @property
    def arc_data(self):
        """Return a list of segments that represent the arc data of a polygon.

        Returns
        -------
        bool
        """
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
        """Return whether a polygon is closed between first and last points.

        Returns
        -------
        bool
        """
        return self._is_closed

    @property
    def sense(self):
        """Return the polygon sense type.

        Returns
        -------
        PolygonSenseType
        """
        return self._sense

    def is_hole(self):
        """Return whether a polygon is a hole.

        Returns
        -------
        bool
        """
        return self.is_closed and not self._is_ccw()

    def is_parametric(self):
        """Return whether a polygon contains any parametrized points.

        Returns
        -------
        bool
        """
        return any(pt.is_parametric for pt in self.points)

    def has_arcs(self):
        """Return whether a polygon contains any arcs.

        Returns
        -------
        bool
        """
        return any(pt.is_arc for pt in self.points)

    def has_holes(self):
        """Return whether a polygon contains any holes.

        Returns
        -------
        bool
        """
        return len(self.holes) > 0

    def is_circle(self):
        """Return whether the outer contour of a polygon is a circle.

        Returns
        -------
        bool
        """
        return self.__stub.IsCircle(messages.polygon_data_message(self)).value

    def is_box(self):
        """Return whether the outer contour of a polygon is a box.

        Returns
        -------
        bool
        """
        return self.__stub.IsBox(messages.polygon_data_message(self)).value

    def is_convex(self):
        """Return whether a polygon is a convex hull.

        Returns
        -------
        bool
        """
        return self.__stub.IsConvex(messages.polygon_data_message(self)).value

    def area(self):
        """Compute the area of polygon.

        Returns
        -------
        float
        """
        return self.__stub.GetArea(messages.polygon_data_message(self)).value

    def has_self_intersections(self, tol=1e-9):
        """Return whether this polygon contains self-intersections.

        Parameters
        ----------
        tol : float, optional

        Returns
        -------
        bool
        """
        return self.__stub.HasSelfIntersections(
            messages.polygon_data_with_tol_message(self, tol)
        ).value

    @parser.to_polygon_data
    def remove_self_intersections(self, tol=1e-9):
        """Create new polygon with all self-intersections removed.

        Parameters
        ----------
        tol : float, optional

        Returns
        -------
        PolygonData
        """
        return self.__stub.RemoveSelfIntersections(
            messages.polygon_data_with_tol_message(self, tol)
        )

    @parser.to_point_data_list
    def normalized(self):
        """Return normalized points of a polygon.

        Returns
        -------
        list[ansys.edb.geometry.PointData]
        """
        return self.__stub.GetNormalizedPoints(messages.polygon_data_message(self))

    @parser.to_polygon_data
    def move(self, vector):
        """Move a polygon by a (x, y) vector.

        Parameters
        ----------
        vector : ansys.edb.typing.PointLikeT

        Returns
        -------
        PolygonData
        """
        return self.__stub.Transform(messages.polygon_data_transform_message("move", self, vector))

    @parser.to_polygon_data
    def rotate(self, angle, center):
        """Rotate a polygon at a center by an angle.

        Parameters
        ----------
        angle : float
            in radian.
        center : ansys.edb.typing.PoinyLikeT

        Returns
        -------
        PolygonData
        """
        return self.__stub.Transform(
            messages.polygon_data_transform_message("rotate", self, angle, center)
        )

    @parser.to_polygon_data
    def scale(self, factor, center):
        """Scale a polygon by a linear factor from a center.

        Parameters
        ----------
        factor : float
        center : ansys.edb.typing.PointLikeT

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

        Returns
        -------
        PolygonData
        """
        return self.__stub.Transform(messages.polygon_data_transform_message("mirror_x", x))

    @parser.to_box
    def bbox(self, *others):
        """Compute the bounding box of polygon(s).

        Parameters
        ----------
        others : list[PolygonData]

        Returns
        -------
        tuple[ansys.edb.geometry.PointData, ansys.edb.geometry.PointData]
        """
        return self.__stub.GetBBox(messages.polygon_data_list_message([self, *others]))

    @parser.to_circle
    def bounding_circle(self):
        """Compute the bounding circle of a polygon.

        Returns
        -------
        tuple[ansys.edb.geometry.PointData, ansys.edb.utility.Value]
        """
        return self.__stub.GetBoundingCircle(messages.polygon_data_message(self))

    @parser.to_polygon_data
    def convex_hull(self, *others):
        """Compute the convex hull of a polygon union-ed with any extra polygons.

        Parameters
        ----------
        others : list[PolygonData], optional

        Returns
        -------
        PolygonData
        """
        return self.__stub.GetConvexHull(messages.polygon_data_list_message([self, *others]))

    @parser.to_polygon_data
    def without_arcs(self, max_chord_error=0, max_arc_angle=math.pi / 6, max_points=8):
        """Return a polygon data with all arcs removed.

        Parameters
        ----------
        max_chord_error : float, optional
        max_arc_angle : float, optional
        max_points : int, optional

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
        tol : float, optional

        Returns
        -------
        PolygonData
        """
        return self.__stub.Defeature(messages.polygon_data_with_tol_message(self, tol))

    def is_inside(self, point):
        """Return whether the point is inside a polygon.

        Parameters
        ----------
        point : ansys.edb.typing.PointLikeT

        Returns
        -------
        bool
        """
        return self.__stub.IsInside(messages.polygon_data_with_point_message(self, point)).value

    def intersection_type(self, other, tol=1e-9):
        """Return the intersection type with another polygon.

        Parameters
        ----------
        other : PolygonData
        tol : float, optional

        Returns
        -------
        bool
        """
        return self.__stub.GetIntersectionType(
            messages.polygon_data_pair_with_tolerance_message(self, other, tol)
        )

    def circle_intersect(self, center, radius):
        """Return whether a circle intersects with a polygon.

        Parameters
        ----------
        center : ansys.edb.typing.PointLikeT
        radius : float

        Returns
        -------
        bool
        """
        return self.__stub.DoesIntersect(
            messages.polygon_data_does_intersect_message(self, center, radius)
        ).value

    @parser.to_point_data
    def closest_point(self, point):
        """Compute a point on a polygon that is closest to another point.

        Parameters
        ----------
        point : ansys.edb.typing.PointLikeT

        Returns
        -------
        ansys.edb.geometry.PointData
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
        tuple[ansys.edb.geometry.PointData, ansys.edb.geometry.PointData]
        """
        return self.__stub.GetClosestPoints(
            messages.polygon_data_with_points_message(self, polygon=polygon)
        ).points

    @parser.to_polygon_data
    def unite(self, *others):
        """Compute the union of a polygon with arbitrary number of polygons.

        Parameters
        ----------
        others : list[PolygonData]

        Returns
        -------
        PolygonData
        """
        return self.__stub.GetUnion(messages.polygon_data_list_message([self, *others]))

    @parser.to_polygon_data_list
    def intersect(self, other_polygons):
        """Compute an intersection of polygons.

        Intersection between this polygon and another set of polygons.

        Parameters
        ----------
        other_polygons : list[PolygonData] or PolygonData

        Returns
        -------
        list[PolygonData]
        """
        return PolygonData.intersect(self, other_polygons)

    @classmethod
    @parser.to_polygon_data_list
    def intersect(cls, polygons1, polygons2):
        """Compute an intersection of polygons.

        Intersection between a set of polygons and another set of polygons.

        Parameters
        ----------
        polygons1 : list[PolygonData] or PolygonData
        polygons2 : list[PolygonData] or PolygonData

        Returns
        -------
        list[PolygonData]
        """
        return cls.__stub.GetIntersection(messages.polygon_data_pair_message(polygons1, polygons2))

    @parser.to_polygon_data_list
    def subtract(self, other_polygons):
        """Compute geometric subtraction of polygons.

        Subtract a set of polygons from this polygon.

        Parameters
        ----------
        other_polygons : list[PolygonData], PolygonData
            base polygons.

        Returns
        -------
        list[PolygonData]
        """
        return PolygonData.Subtract(self, other_polygons)

    @classmethod
    @parser.to_polygon_data_list
    def subtract(cls, polygons1, polygons2):
        """Compute geometric subtraction of polygons.

        Subtract a set of polygons from another set of polygons.

        Parameters
        ----------
        polygons1 : list[PolygonData], PolygonData
            base polygons.
        polygons2 : list[PolygonData], PolygonData
            polygons to subtract.

        Returns
        -------
        list[PolygonData]
        """
        return cls.__stub.Subtract(messages.polygon_data_pair_message(polygons1, polygons2))

    @parser.to_polygon_data_list
    def xor(self, other_polygons):
        """Compute an exclusive OR of polygons.

        Exclusive OR between this polygon and another set of polygons.

        Parameters
        ----------
        other_polygons : list[PolygonData], PolygonData

        Returns
        -------
        list[PolygonData]
        """
        return PolygonData.Xor(self, other_polygons)

    @classmethod
    @parser.to_polygon_data_list
    def xor(cls, polygons1, polygons2):
        """Compute an exclusive OR of polygons.

        Exclusive OR between a set of polygons and another set of polygons.

        Parameters
        ----------
        polygons1 : list[PolygonData], PolygonData
        polygons2 : list[PolygonData], PolygonData

        Returns
        -------
        list[PolygonData]
        """
        return cls.__stub.Xor(messages.polygon_data_pair_message(polygons1, polygons2))

    @parser.to_polygon_data_list
    def expand(self, offset, round_corner, max_corner_ext, tol=1e-9):
        """Expand a polygon by an offset.

        Parameters
        ----------
        offset : float
            Expansion offset. negative value to shrink.
        round_corner : bool
            True for rounded corners, straight edge otherwise.
        max_corner_ext : float
            Max corner extension at which point the corner is clipped.
        tol : float, optional

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
        points : list[ansys.edb.typing.PointLikeT]
        alpha : float

        Returns
        -------
        list[PolygonData]
        """
        return cls.__stub.Get2DAlphaShape(
            messages.polygon_data_get_alpha_shape_message(points, alpha)
        )
