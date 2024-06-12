"""Point data."""
from functools import reduce
import math
import operator
import sys

from ansys.api.edb.v1 import point_data_pb2_grpc

from ansys.edb.core import session
from ansys.edb.core.inner import messages, parser
from ansys.edb.core.utility import conversions, value


class PointData:
    """Represents arbitrary (x, y) coordinates that exist on a 2D space."""

    __stub: point_data_pb2_grpc.PointDataServiceStub = session.StubAccessor(
        session.StubType.point_data
    )

    def __init__(self, *data):
        """Initialize point data from a list of coordinates.

        Parameters
        ----------
        data : Iterable[Iterable[ansys.edb.core.typing.ValueLike], ansys.edb.core.typing.ValueLike]
        """
        self._x = self._y = self._arc_h = None

        if len(data) == 1:
            # try to expand the argument.
            try:
                iter(data[0])
                data = data[0]
            except TypeError:
                pass

        if len(data) == 1:
            self._x = self._arc_h = conversions.to_value(data[0])
            self._y = sys.float_info.max
        elif len(data) == 2:
            self._x = conversions.to_value(data[0])
            self._y = conversions.to_value(data[1])
            if not self._y.is_parametric and self._y == sys.float_info.max:
                self._arc_h = self._x
        else:
            raise TypeError(
                "`PointData` must receive either one value representing arc height or "
                f"two values representing x and y coordinates. - Received '{data}'"
            )

    def __eq__(self, other):
        """Determine if two objects represent the same coordinates.

        Parameters
        ----------
        other : PointData

        Returns
        -------
        bool
        """
        return self.equals(other)

    def __len__(self):
        """Return the number of coordinates present.

        Returns
        -------
        int
        """
        return len(self._matrix_values)

    def __add__(self, other):
        """Perform matrix addition of two points.

        Parameters
        ----------
        other : ansys.edb.core.typing.PointLike

        Returns
        -------
        PointData
        """
        return self.__class__(self._map_reduce(other, operator.__add__))

    def __sub__(self, other):
        """Perform matrix subtraction of two points.

        Parameters
        ----------
        other : ansys.edb.core.typing.PointLike

        Returns
        -------
        PointData
        """
        return self.__class__(self._map_reduce(other, operator.__sub__))

    def __str__(self):
        """Generate unique name for the point object.

        Returns
        -------
        str
        """
        coord = ",".join([str(v) for v in self._matrix_values])
        return f"<{coord}>" if self.is_arc else f"({coord})"

    def equals(self, other, tolerance=0.0):
        """Determine if two points are located at the same coordinates.

        Parameters
        ----------
        other : ansys.edb.core.typing.PointLike
        tolerance : float, optional

        Returns
        -------
        bool
            ``True`` if the two points are located at the same coordinates,
            ``False`` otherwise.
        """

        def value_equals(a, b):
            return a.equals(b, tolerance)

        try:
            return all(self._map_reduce(other, value_equals))
        except TypeError:
            return False

    @property
    def _matrix_values(self):
        """:obj:`list` of :class:`.Value`: Coordinates of the point as a list of values."""
        return [self.arc_height] if self.is_arc else [self.x, self.y]

    def _map_reduce(self, other, op):
        other = conversions.to_point(other)
        return [reduce(op, values) for values in zip(self._matrix_values, other._matrix_values)]

    @property
    def is_arc(self):
        """:obj:`bool`: Flag indicating if the point represents an arc."""
        return self._arc_h is not None

    @property
    def arc_height(self):
        """:class:`.Value`: Height of the arc."""
        return self._arc_h

    @property
    def x(self):
        """:class:`.Value`: X coordinate."""
        return self._x

    @property
    def y(self):
        """:class:`.Value`: Y coordinate."""
        return self._y

    @property
    def is_parametric(self):
        """:obj:`bool`: Flag indicating if the point contains parametric values (variable expressions)."""
        return any(val.is_parametric for val in self._matrix_values)

    def magnitude(self):
        """Get the magnitude of the point vector.

        Returns
        -------
        float
            Magnitude of the point vector.
        """
        if self.is_arc:
            return 0
        return math.sqrt(sum([v**2 for v in self._matrix_values], value.Value(0)).value)

    def normalized(self):
        """Normalize the point vector.

        Returns
        -------
        PointData
        """
        mag = self.magnitude()
        n = [0] * len(self) if mag == 0 else [v / mag for v in self._matrix_values]
        return self.__class__(n)

    @parser.to_point_data
    def closest(self, start, end):
        """Get the closest point on a line segment from the point.

        Parameters
        ----------
        start : ansys.edb.core.typing.PointLike
            Start point of the line segment.
        end : ansys.edb.core.typing.PointLike
            End point of the line segment.

        Returns
        -------
        typing.Optional[PointData] or ``None`` if either point is an arc.
        """
        if not self.is_arc:
            return self.__stub.ClosestPoint(messages.point_data_with_line_message(self, start, end))

    def distance(self, start, end=None):
        """Compute the shortest distance from the point to a line segment when an end point is given. \
        Otherwise, compute the distance between this point and another point.

        Parameters
        ----------
        start : ansys.edb.core.typing.PointLike
            Start point of the line segment.
        end : ansys.edb.core.typing.PointLike, default: None
            End point of the line segment.

        Returns
        -------
        float
        """
        if end is None:
            return (self - start).magnitude()
        else:
            return self.__stub.Distance(
                messages.point_data_with_line_message(self, start, end)
            ).value

    def cross(self, other):
        """Compute the cross product of the point vector with another point vector.

        Parameters
        ----------
        other : ansys.edb.core.typing.PointLike
            Other point vector.

        Returns
        -------
        typing.Optional[.Value] or ``None`` if either point is an arc.
        """
        other = conversions.to_point(other)
        if not self.is_arc and not other.is_arc:
            return self.x * other.y - self.y * other.x

    def move(self, vector):
        """Move the point by a vector.

        Parameters
        ----------
        vector : ansys.edb.core.typing.PointLike
           Vector.

        Returns
        -------
        typing.Optional[PointData] or ``None`` if either point is an arc.
        """
        vector = conversions.to_point(vector)
        if not self.is_arc and not vector.is_arc:
            return self + vector

    @parser.to_point_data
    def rotate(self, angle, center):
        """Rotate a point at a given center by a given angle.

        Parameters
        ----------
        angle : float
            Angle in radians.
        center : ansys.edb.core.typing.PointLike
            Center.

        Returns
        -------
        typing.Optional[PointData] or ``None`` if either point is an arc.
        """
        if not self.is_arc:
            return self.__stub.Rotate(messages.point_data_rotate_message(self, center, angle))

    def dot(self, other):
        """Perform per-component multiplication (dot product) of this point and another point.

        Parameters
        ----------
        other : ansys.edb.core.typing.PointLike
            Other point.

        Returns
        -------
        float
            Dot product of the two points.
        """
        return sum(self._map_reduce(other, operator.__mul__), value.Value(0)).value

    def angle(self, other):
        """Get the angle between this vector and another vector.

        Parameters
        ----------
        other : ansys.edb.core.typing.PointLike
            Other vector.

        Returns
        -------
        float
            Angle in radians.
        """
        other = conversions.to_point(other)
        return math.acos(self.dot(other) / (self.magnitude() * other.magnitude()))
