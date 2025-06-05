"""Point data."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.typing import ValueLike, PointLike
    from ansys.edb.core.utility.value import Value
    from typing import Iterable

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

    def __init__(self, *data: Iterable[ValueLike]):
        """Initialize point data from a list of coordinates.

        Parameters
        ----------
        data : :obj:`list` of :term:`ValueLike`
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

    def __eq__(self, other: PointData) -> bool:
        """Determine if two objects represent the same coordinates.

        Parameters
        ----------
        other : .PointData

        Returns
        -------
        bool
        """
        return self.equals(other)

    def __len__(self) -> int:
        """Return the number of coordinates present.

        Returns
        -------
        int
        """
        return len(self._matrix_values)

    def __add__(self, other: PointLike) -> PointData:
        """Perform matrix addition of two points.

        Parameters
        ----------
        other : :term:`Point2DLike`

        Returns
        -------
        .PointData
        """
        return self.__class__(self._map_reduce(other, operator.__add__))

    def __sub__(self, other: PointLike) -> PointData:
        """Perform matrix subtraction of two points.

        Parameters
        ----------
        other : :term:`Point2DLike`

        Returns
        -------
        .PointData
        """
        return self.__class__(self._map_reduce(other, operator.__sub__))

    def __str__(self) -> str:
        """Generate unique name for the point object.

        Returns
        -------
        str
        """
        coord = ",".join([str(v) for v in self._matrix_values])
        return f"<{coord}>" if self.is_arc else f"({coord})"

    def equals(self, other, tolerance: float = 0.0) -> bool:
        """Determine if two points are located at the same coordinates.

        Parameters
        ----------
        other : :term:`Point2DLike`
        tolerance : float, default: 0.0

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
    def _matrix_values(self) -> list[Value]:
        """
        :obj:`list` of :class:`.Value`: Coordinates of the point as a list of values.

        This property is read-only.
        """
        return [self.arc_height] if self.is_arc else [self.x, self.y]

    def _map_reduce(self, other, op):
        other = conversions.to_point(other)
        return [reduce(op, values) for values in zip(self._matrix_values, other._matrix_values)]

    @property
    def is_arc(self) -> bool:
        """
        :obj:`bool`: Flag indicating if the point represents an arc.

        This property is read-only.
        """
        return self._arc_h is not None

    @property
    def arc_height(self) -> Value:
        """
        :class:`.Value`: Height of the arc.

        This property is read-only.
        """
        return self._arc_h

    @property
    def x(self) -> Value:
        """
        :class:`.Value`: X coordinate.

        This property is read-only.
        """
        return self._x

    @property
    def y(self) -> Value:
        """
        :class:`.Value`: Y coordinate.

        This property is read-only.
        """
        return self._y

    @property
    def is_parametric(self) -> bool:
        """
        :obj:`bool`: Flag indicating if the point contains parametric values (variable expressions).

        This property is read-only.
        """
        return any(val.is_parametric for val in self._matrix_values)

    def magnitude(self) -> float:
        """Get the magnitude of the point vector.

        Returns
        -------
        float
            Magnitude of the point vector.
        """
        if self.is_arc:
            return 0
        return math.sqrt(sum([v**2 for v in self._matrix_values], value.Value(0)).value)

    def normalized(self) -> PointData:
        """Normalize the point vector.

        Returns
        -------
        PointData
        """
        mag = self.magnitude()
        n = [0] * len(self) if mag == 0 else [v / mag for v in self._matrix_values]
        return self.__class__(n)

    @parser.to_point_data
    def closest(self, start: PointLike, end: PointLike) -> PointData | None:
        """Get the closest point on a line segment from the point.

        Parameters
        ----------
        start : :term:`Point2DLike`
            Start point of the line segment.
        end : :term:`Point2DLike`
            End point of the line segment.

        Returns
        -------
        .PointData or :obj:`None`
            Closet PointData or :obj:`None` if either point is an arc.
        """
        if not self.is_arc:
            return self.__stub.ClosestPoint(messages.point_data_with_line_message(self, start, end))

    def distance(self, start: PointLike, end: PointLike = None) -> float:
        """Compute the shortest distance from the point to a line segment when an end point is given. \
        Otherwise, compute the distance between this point and another point.

        Parameters
        ----------
        start : :term:`Point2DLike`
            Start point of the line segment.
        end : :term:`Point2DLike`, default: None
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

    def cross(self, other: PointLike) -> Value | None:
        """Compute the cross product of the point vector with another point vector.

        Parameters
        ----------
        other : :term:`Point2DLike`
            Other point vector.

        Returns
        -------
        .Value or :obj:`None`
            Cross product value or :obj:`None` if either point is an arc.
        """
        other = conversions.to_point(other)
        if not self.is_arc and not other.is_arc:
            return self.x * other.y - self.y * other.x

    def move(self, vector: PointLike) -> PointData | None:
        """Move the point by a vector.

        Parameters
        ----------
        vector : :term:`Point2DLike`
           Vector.

        Returns
        -------
        .PointData or :obj:`None`
           PointData after moving or :obj:`None` if either point is an arc.
        """
        vector = conversions.to_point(vector)
        if not self.is_arc and not vector.is_arc:
            return self + vector

    @parser.to_point_data
    def rotate(self, angle: float, center: PointLike) -> PointData | None:
        """Rotate a point at a given center by a given angle.

        Parameters
        ----------
        angle : float
            Angle in radians.
        center : :term:`Point2DLike`
            Center.

        Returns
        -------
        .PointData or :obj:`None`
            PointData after rotating or :obj:`None` if either point is an arc.
        """
        if not self.is_arc:
            return self.__stub.Rotate(messages.point_data_rotate_message(self, center, angle))

    def dot(self, other: PointLike) -> float:
        """Perform per-component multiplication (dot product) of this point and another point.

        Parameters
        ----------
        other : :term:`Point2DLike`
            Other point.

        Returns
        -------
        float
            Dot product of the two points.
        """
        return sum(self._map_reduce(other, operator.__mul__), value.Value(0)).value

    def angle(self, other: PointLike) -> float:
        """Get the angle between this vector and another vector.

        Parameters
        ----------
        other : :term:`Point2DLike`
            Other vector.

        Returns
        -------
        float
            Angle in radians.
        """
        other = conversions.to_point(other)
        return math.acos(self.dot(other) / (self.magnitude() * other.magnitude()))
