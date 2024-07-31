"""Arc data."""
from enum import Enum
import math

from ansys.api.edb.v1 import arc_data_pb2_grpc

from ansys.edb.core import session
from ansys.edb.core.geometry.point_data import PointData
from ansys.edb.core.inner import messages, parser
from ansys.edb.core.utility import conversions


class RotationDirection(Enum):
    """Represents arc directions."""

    CW = "cw"
    CCW = "ccw"
    CO_LINEAR = "colinear"


class ArcData:
    """Represents arc data."""

    __stub: arc_data_pb2_grpc.ArcDataServiceStub = session.StubAccessor(session.StubType.arc_data)

    def __init__(self, start, end, **kwargs):
        """Create an arc.

        Parameters
        ----------
        start : ansys.edb.core.typing.PointLike
        end : ansys.edb.core.typing.PointLike
        height: float, int, optional
        thru : ansys.edb.core.typing.PointLike, optional
        direction : Literal["cw", "ccw", "colinear"], optional
        radius : float, optional
        center : ansys.edb.core.typing.PointLike, optional
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
        """Generate a readable string for the arc.

        Returns
        -------
        str
        """
        if self.height == 0:
            return f"{self.start} {self.end}"
        else:
            arc = PointData(self.height)
            return f"{self.start} {arc} {self.end}"

    @property
    def start(self):
        """:class:`.PointData`: Start point of the arc."""
        return self._start

    @property
    def end(self):
        """:class:`.PointData`: End point of the arc."""
        return self._end

    @property
    def height(self):
        """:obj:`float`: Height of the arc."""
        if self._height is None:
            self._height = self.__stub.GetHeight(messages.arc_message(self)).value

        return self._height

    def is_point(self, tolerance=0.0):
        """Determine if the arc is a point.

        An arc is a point when its start and end points are the same.

        Parameters
        ----------
        tolerance : float, optional
           Tolearance.

        Returns
        -------
        bool
            ``True`` when the arc is a point, ``False`` otherwise.
        """
        return self.is_segment(tolerance) and self.start.equals(self.end, tolerance)

    def is_segment(self, tolerance=0.0):
        """Determine if the arc is a straight line segment.

        Parameters
        ----------
        tolerance : float, optional
            Tolearance.

        Returns
        -------
        bool
            ``True`` when the arc is a straight line segment, ``False`` otherwise.
        """
        return math.fabs(self.height) <= tolerance

    @property
    @parser.to_point_data
    def center(self):
        """:class:`.PointData`: Center point of the arc."""
        return self.__stub.GetCenter(messages.arc_message(self))

    @property
    @parser.to_point_data
    def midpoint(self):
        """:class:`.PointData`: Midpoint of the arc."""
        return self.__stub.GetMidpoint(messages.arc_message(self))

    @property
    def radius(self):
        """:obj:`float`: Radius of the arc."""
        return self.__stub.GetRadius(messages.arc_message(self)).value

    @property
    @parser.to_polygon_data
    def bbox(self):
        """:class:`.PolygonData`: Rectangular bounding box of the arc."""
        return self.__stub.GetBoundingBox(messages.arc_message(self))

    def is_big(self):
        """Determine if the arc is big.

        Returns
        -------
        bool
            ``True`` when the arc is big, ``False`` otherwise.
        """
        dist = self.start.distance(self.end)
        return 2 * math.fabs(self.height) > dist

    def is_left(self):
        """Determine if the arc rotates clockwise.

        This method is the same as the ``is_cw`` method.

        Returns
        -------
        bool
            ``True`` when the arc rotates clockwise, ``False`` otherwise.
        """
        return self.is_cw()

    def is_cw(self):
        """Determine if the arc rotates clockwise.

        This method is the same as the ``is_left`` method.

        Returns
        -------
        bool
            ``True`` when the arc rotates clockwise, ``False`` otherwise.
        """
        return self.height > 0.0

    def is_ccw(self):
        """Determine if the arc rotates counter-clockwise.

        Returns
        -------
        bool
            ``True`` when the arc rotates counter-clockwise, ``False`` otherwise.
        """
        return self.height < 0.0

    @property
    def direction(self):
        """:obj:`Literal["cw", "ccw", "colinear"]`: Rotational direction of the arc."""
        if self.is_cw():
            return "cw"
        elif self.is_ccw():
            return "ccw"
        else:
            return "colinear"

    def angle(self, arc=None):
        """Get the angle between this arc and another arc if provided or the angle of this arc.

        Parameters
        ----------
        arc : ArcData, default: None
           Other arc.

        Returns
        -------
        float
            Angle in radians.
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
        """:obj:`str`: Circumference length of the arc."""
        if self.is_segment():
            return self.start.distance(self.end)
        else:
            return math.fabs(self.angle() * self.radius)

    @property
    def points(self):
        """:obj:`list` of :class:`.PointData`: Geometric points representing the arc."""
        return [self._start, PointData(self.height), self._end]

    def tangent_at(self, point):
        """Get the tangent vector of the arc at a given point.

        Parameters
        ----------
        point : ansys.edb.core.typing.PointLike
            Point.

        Returns
        -------
        .PointData
        """
        if self.is_segment():
            return self.end - self.start

        point = conversions.to_point(point)
        vec = point - self.center

        if self.is_ccw():
            return PointData(-vec.y, vec.x)
        else:
            return PointData(vec.y, -vec.x)

    @parser.to_box
    def closest_points(self, other):
        """Get the closest points from this arc to another arc, and vice versa.

        Parameters
        ----------
        other : ArcData
            Other arc.

        Returns
        -------
        tuple[.PointData, .PointData]
        """
        return self.__stub.ClosestPoints(messages.arc_data_two_points(self, other))
