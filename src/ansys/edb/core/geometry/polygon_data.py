"""Polygon Data."""

from enum import Enum
import itertools
import math

from ansys.api.edb.v1 import edb_defs_pb2, point_data_pb2, polygon_data_pb2_grpc

from ansys.edb.core.geometry.arc_data import ArcData
from ansys.edb.core.inner.messages import (
    polygon_data_expand_message,
    polygon_data_get_alpha_shape_message,
    polygon_data_list_message,
    polygon_data_message,
    polygon_data_pair_message,
    polygon_data_pair_with_tolerance_message,
    polygon_data_remove_arc_message,
    polygon_data_transform_message,
    polygon_data_with_circle_message,
    polygon_data_with_point_message,
    polygon_data_with_points_message,
    polygon_data_with_tol_message,
)
from ansys.edb.core.inner.parser import (
    to_box,
    to_circle,
    to_point_data,
    to_point_data_list,
    to_polygon_data,
    to_polygon_data_list,
)
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.conversions import to_point


class PolygonSenseType(Enum):
    """Direction of polygon sense.

    - SENSE_UNKNOWN
    - SENSE_CW
    - SENSE_CCW
    """

    SENSE_UNKNOWN = point_data_pb2.SENSE_UNKNOWN
    SENSE_CW = point_data_pb2.SENSE_CW
    SENSE_CCW = point_data_pb2.SENSE_CCW


class ExtentType(Enum):
    """Extent types for geometries.

    - CONFORMING
    - BOUNDING_BOX
    """

    CONFORMING = edb_defs_pb2.CONFORMING
    BOUNDING_BOX = edb_defs_pb2.BOUNDING_BOX


class PolygonData:
    """Class representing a polygon data object."""

    __stub: polygon_data_pb2_grpc.PolygonDataServiceStub = StubAccessor(StubType.polygon_data)

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
        points : list[ansys.edb.core.typing.PointLike], optional
        arcs : list[ArcData], optional
        lower_left : ansys.edb.core.typing.PointLike, optional
        upper_right : ansys.edb.core.typing.PointLike, optional
        holes : List[ansys.edb.core.geometry.PolygonData]
        sense : ansys.edb.core.geometry.PolygonSenseType, optional
        closed : bool, optional
        """
        self._holes, self._sense, self._is_closed = (
            [] if holes is None else holes,
            PolygonSenseType(sense),
            closed,
        )

        if points is not None:
            self._points = [to_point(pt) for pt in points]
        elif arcs is not None:
            self._points = list(
                itertools.chain.from_iterable(
                    [[arc.start, arc.end] if arc.is_segment() else arc.points for arc in arcs]
                )
            )
        elif lower_left is not None and upper_right is not None:
            ll, ur = [to_point(pt) for pt in [lower_left, upper_right]]
            self._points = [
                to_point(pt) for pt in [(ll.x, ll.y), (ur.x, ll.y), (ur.x, ur.y), (ll.x, ur.y)]
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
        list[ansys.edb.core.geometry.PointData]
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
        return self.__stub.IsCircle(polygon_data_message(self)).value

    def is_box(self):
        """Return whether the outer contour of a polygon is a box.

        Returns
        -------
        bool
        """
        return self.__stub.IsBox(polygon_data_message(self)).value

    def is_convex(self):
        """Return whether a polygon is a convex hull.

        Returns
        -------
        bool
        """
        return self.__stub.IsConvex(polygon_data_message(self)).value

    def area(self):
        """Compute the area of polygon.

        Returns
        -------
        float
        """
        return self.__stub.GetArea(polygon_data_message(self)).value

    def has_self_intersections(self, tol=1e-9):
        """Return whether this polygon contains self-intersections.

        Parameters
        ----------
        tol : float, optional

        Returns
        -------
        bool
        """
        return self.__stub.HasSelfIntersections(polygon_data_with_tol_message(self, tol)).value

    @to_polygon_data
    def remove_self_intersections(self, tol=1e-9):
        """Create new polygon with all self-intersections removed.

        Parameters
        ----------
        tol : float, optional

        Returns
        -------
        PolygonData
        """
        return self.__stub.RemoveSelfIntersections(polygon_data_with_tol_message(self, tol))

    @to_point_data_list
    def normalized(self):
        """Return normalized points of a polygon.

        Returns
        -------
        list[ansys.edb.core.geometry.PointData]
        """
        return self.__stub.GetNormalizedPoints(polygon_data_message(self))

    @to_polygon_data
    def move(self, vector):
        """Move a polygon by a (x, y) vector.

        Parameters
        ----------
        vector : ansys.edb.core.typing.PointLikeT

        Returns
        -------
        PolygonData
        """
        return self.__stub.Transform(polygon_data_transform_message("move", self, vector))

    @to_polygon_data
    def rotate(self, angle, center):
        """Rotate a polygon at a center by an angle.

        Parameters
        ----------
        angle : float
            in radian.
        center : ansys.edb.core.typing.PoinyLikeT

        Returns
        -------
        PolygonData
        """
        return self.__stub.Transform(polygon_data_transform_message("rotate", self, angle, center))

    @to_polygon_data
    def scale(self, factor, center):
        """Scale a polygon by a linear factor from a center.

        Parameters
        ----------
        factor : float
        center : ansys.edb.core.typing.PointLikeT

        Returns
        -------
        PolygonData
        """
        return self.__stub.Transform(polygon_data_transform_message("scale", factor, center))

    @to_polygon_data
    def mirror_x(self, x):
        """Mirror a polygon by x line.

        Parameters
        ----------
        x : float

        Returns
        -------
        PolygonData
        """
        return self.__stub.Transform(polygon_data_transform_message("mirror_x", x))

    @to_box
    def bbox(self):
        """Compute the bounding box.

        Returns
        -------
        tuple[ansys.edb.core.geometry.PointData, ansys.edb.core.geometry.PointData]
        """
        return self.__stub.GetBBox(polygon_data_list_message([self]))

    @classmethod
    @to_box
    def bbox_of_polygons(cls, polygons):
        """Compute the bounding box of polygons.

        Parameters
        ----------
        polygons: list[PolygonData]

        Returns
        -------
        tuple[ansys.edb.core.geometry.PointData, ansys.edb.core.geometry.PointData]
        """
        return cls.__stub.GetBBox(polygon_data_list_message(polygons))

    @to_circle
    def bounding_circle(self):
        """Compute the bounding circle of a polygon.

        Returns
        -------
        tuple[ansys.edb.core.geometry.PointData, ansys.edb.core.utility.Value]
        """
        return self.__stub.GetBoundingCircle(polygon_data_message(self))

    @classmethod
    @to_polygon_data
    def convex_hull(cls, polygons):
        """Compute the convex hull of the union of polygons.

        Parameters
        ----------
        others : list[PolygonData]

        Returns
        -------
        PolygonData
        """
        return cls.__stub.GetConvexHull(polygon_data_list_message(polygons))

    @to_polygon_data
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
            polygon_data_remove_arc_message(self, max_chord_error, max_arc_angle, max_points)
        )

    @to_polygon_data
    def defeature(self, tol=1e-9):
        """Defeature a polygon.

        Parameters
        ----------
        tol : float, optional

        Returns
        -------
        PolygonData
        """
        return self.__stub.Defeature(polygon_data_with_tol_message(self, tol))

    def is_inside(self, point):
        """Return whether the point is inside a polygon.

        Parameters
        ----------
        point : ansys.edb.core.typing.PointLikeT

        Returns
        -------
        bool
        """
        return self.__stub.IsInside(polygon_data_with_point_message(self, point)).value

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
            polygon_data_pair_with_tolerance_message(self, other, tol)
        )

    def circle_intersect(self, center, radius):
        """Return whether a circle intersects with a polygon.

        Parameters
        ----------
        center : ansys.edb.core.typing.PointLikeT
        radius : float

        Returns
        -------
        bool
        """
        return self.__stub.CircleIntersectsPolygon(
            polygon_data_with_circle_message(self, center, radius)
        ).value

    @to_point_data
    def closest_point(self, point):
        """Compute a point on a polygon that is closest to another point.

        Parameters
        ----------
        point : ansys.edb.core.typing.PointLikeT

        Returns
        -------
        ansys.edb.core.geometry.PointData
        """
        return self.__stub.GetClosestPoints(
            polygon_data_with_points_message(self, point=point)
        ).points[0]

    @to_point_data_list
    def closest_points(self, polygon):
        """Compute points on this and another polygon that are closest to the other polygon.

        Parameters
        ----------
        polygon : PolygonData

        Returns
        -------
        tuple[ansys.edb.core.geometry.PointData, ansys.edb.core.geometry.PointData]
        """
        return self.__stub.GetClosestPoints(
            polygon_data_with_points_message(self, polygon=polygon)
        ).points

    @classmethod
    @to_polygon_data_list
    def unite(cls, polygons):
        """Compute union of polygons.

        Parameters
        ----------
        polygons: list[PolygonData]

        Returns
        -------
        list[PolygonData]
        """
        return cls.__stub.GetUnion(polygon_data_list_message(polygons))

    @classmethod
    @to_polygon_data_list
    def intersect(cls, polygons1, polygons2):
        """Compute intersection of polygons.

        Parameters
        ----------
        polygons1: list[PolygonData] or PolygonData
        polygons2: list[PolygonData] or PolygonData, optional

        Returns
        -------
        list[PolygonData]
        """
        return cls.__stub.GetIntersection(polygon_data_pair_message(polygons1, polygons2))

    @classmethod
    @to_polygon_data_list
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
        return cls.__stub.Subtract(polygon_data_pair_message(polygons1, polygons2))

    @classmethod
    @to_polygon_data_list
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
        return cls.__stub.Xor(polygon_data_pair_message(polygons1, polygons2))

    @to_polygon_data_list
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
            polygon_data_expand_message(self, offset, tol, round_corner, max_corner_ext)
        )

    @classmethod
    @to_polygon_data_list
    def alpha_shape(cls, points, alpha):
        """Compute the outline of a 2D point cloud using alpha shapes.

        Parameters
        ----------
        points : list[ansys.edb.core.typing.PointLikeT]
        alpha : float

        Returns
        -------
        list[PolygonData]
        """
        return cls.__stub.Get2DAlphaShape(polygon_data_get_alpha_shape_message(points, alpha))
