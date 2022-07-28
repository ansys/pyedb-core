"""Arc Data."""
import enum
import math

from ansys.api.edb.v1 import arc_data_pb2_grpc

from ansys.edb import geometry, session
from ansys.edb.core import messages, parser
from ansys.edb.utility import conversions


class RotationDirection(enum.Enum):
    """Represents possible directions of arc."""

    CW = "cw"
    CCW = "ccw"
    CO_LINEAR = "colinear"


class ArcData:
    """Class representing arc data."""

    __stub: arc_data_pb2_grpc.ArcDataServiceStub = session.StubAccessor(session.StubType.arc_data)

    def __init__(self, start, end, **kwargs):
        """Create an arc.

        Parameters
        ----------
        start : ansys.edb.typing.PointLike
        end : ansys.edb.typing.PointLike
        height: float, int, optional
        thru : ansys.edb.typing.PointLike, optional
        direction : Literal["cw", "ccw", "colinear"], optional
        radius : float, optional
        center : ansys.edb.typing.PointLike, optional
        is_big : bool, optional
        """
        self._start = conversions.to_point(start)
        self._end = conversions.to_point(end)
        self._height = None
        self._height_options = kwargs

        if "height" in kwargs or len(kwargs) == 0:
            self._height = kwargs.get("height", 0.0)
        if "direction" in kwargs:
            self._height_options["direction"] = RotationDirection(kwargs["direction"])

    def __str__(self):
        """Generate a readable string for arc.

        Returns
        -------
        str
        """
        if self.height == 0:
            return f"{self.start} {self.end}"
        else:
            arc = geometry.PointData(self.height)
            return f"{self.start} {arc} {self.end}"

    @property
    def start(self):
        """Get the start point of arc.

        Returns
        -------
        geometry.PointData
        """
        return self._start

    @property
    def end(self):
        """Get the end point of arc.

        Returns
        -------
        geometry.PointData
        """
        return self._end

    @property
    def height(self):
        """Get the height of arc.

        Returns
        -------
        float
        """
        if self._height is None:
            self._height = self.__stub.GetHeight(messages.arc_message(self)).value

        return self._height

    def is_point(self, tolerance=0.0):
        """Get if an arc is a point (i.e. start and end points are the same).

        Parameters
        ----------
        tolerance : float, optional

        Returns
        -------
        bool
        """
        return self.is_segment(tolerance) and self.start.equals(self.end, tolerance)

    def is_segment(self, tolerance=0.0):
        """Get if an arc is a straight line segment.

        Parameters
        ----------
        tolerance : float, optional

        Returns
        -------
        bool
        """
        return math.fabs(self.height) <= tolerance

    @property
    def center(self):
        """Get the center point of arc.

        Returns
        -------
        geometry.PointData
        """
        c = self.__stub.GetCenter(messages.arc_message(self))
        return parser.to_point_data(c)

    @property
    def midpoint(self):
        """Get the midpoint of arc.

        Returns
        -------
        geometry.PointData
        """
        mid = self.__stub.GetMidpoint(messages.arc_message(self))
        return parser.to_point_data(mid)

    @property
    def radius(self):
        """Get the radius of arc.

        Returns
        -------
        float
        """
        return self.__stub.GetRadius(messages.arc_message(self)).value

    @property
    def bbox(self):
        """Get the rectangular bounding box of arc.

        Returns
        -------
        geometry.PolygonData
        """
        box = self.__stub.GetBoundingBox(messages.arc_message(self))
        return parser.to_polygon_data(box)

    def is_big(self):
        """Get if the arc is big.

        Returns
        -------
        bool
        """
        dist = self.start.distance(self.end)
        return 2 * math.fabs(self.height) > dist

    def is_left(self):
        """Get if arc rotates clockwise. Same as is_cw.

        Returns
        -------
        bool
        """
        return self.is_cw()

    def is_cw(self):
        """Get if arc rotates clockwise.

        Returns
        -------
        bool
        """
        return self.height > 0.0

    def is_ccw(self):
        """Get if arc rotates counter-clockwise.

        Returns
        -------
        bool
        """
        return self.height < 0.0

    @property
    def direction(self):
        """Get the rotational direction of arc.

        Returns
        -------
        Literal["cw", "ccw", "colinear"]
        """
        if self.is_cw():
            return "cw"
        elif self.is_ccw():
            return "ccw"
        else:
            return "colinear"

    def angle(self, arc=None):
        """Get the angle between another arc when provided, otherwise the angle of the arc itself.

        Parameters
        ----------
        arc : ArcData

        Returns
        -------
        float
            angle in radian
        """
        if arc is None:
            return self.__stub.GetAngle(messages.arc_message(self)).value

        if self.is_segment() and arc.is_segment():
            vec1 = self.end - self.start
            vec2 = arc.end - arc.start
        else:
            point1, point2 = self.closest_points(arc)
            vec1, vec2 = self.tangent_at(point1), self.tangent_at(point2)

        return vec1.angle(vec2)

    @property
    def length(self):
        """Get the circumference length of arc.

        Returns
        -------
        float
        """
        if self.is_segment():
            return self.start.distance(self.end)
        else:
            return math.fabs(self.angle() * self.radius)

    @property
    def points(self):
        """Get geometric points representing the arc.

        Returns
        -------
        list[geometry.PointData]
        """
        return [self._start, geometry.PointData(self.height), self._end]

    def tangent_at(self, point):
        """Get the tangent vector of arc at a point.

        Parameters
        ----------
        point : ansys.edb.typing.PointLike

        Returns
        -------
        geometry.PointData
        """
        if self.is_segment():
            return self.end - self.start

        point = conversions.to_point(point)
        vec = point - self.center

        if self.is_ccw():
            return geometry.PointData(-vec.y, vec.x)
        else:
            return geometry.PointData(vec.y, -vec.x)

    def closest_points(self, other):
        """Get the closest point from one arc to another, and vice versa.

        Parameters
        ----------
        other : ArcData

        Returns
        -------
        tuple[geometry.PointData, geometry.PointData]
        """
        points = self.__stub.ClosestPoints(messages.arc_data_two_points(self, other))
        point1 = parser.to_point_data(points.lower_left)
        point2 = parser.to_point_data(points.upper_right)
        return point1, point2
