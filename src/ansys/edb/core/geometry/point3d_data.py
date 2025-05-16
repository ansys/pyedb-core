"""Point3D data."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.typing import ValueLike
    from builtins import NotImplementedType
    from ansys.edb.core.utility.value import Value

from ansys.edb.core.utility import conversions


class Point3DData:
    """Represents a point on a 3D coordinate system."""

    def __init__(self, x: ValueLike, y: ValueLike, z: ValueLike):
        """Initialize a 3D point.

        Parameters
        ----------
        x : :term:`ValueLike`
        y : :term:`ValueLike`
        z : :term:`ValueLike`
        """
        self.x, self.y, self.z = x, y, z

    def __eq__(self, other: Point3DData) -> bool:
        """Compare two points by exact coordinates."""
        if isinstance(other, Point3DData):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return False

    def __add__(self, other: Point3DData) -> Point3DData | NotImplementedType:
        """Add two points piecewise."""
        if isinstance(other, Point3DData):
            return Point3DData(self.x + other.x, self.y + other.y, self.z + other.z)
        return NotImplemented

    def __sub__(self, other: Point3DData) -> Point3DData | NotImplementedType:
        """Subtract a point piecewise."""
        if isinstance(other, Point3DData):
            return Point3DData(self.x - other.x, self.y - other.y, self.z - other.z)
        return NotImplemented

    def __mul__(self, other: Point3DData) -> Point3DData | NotImplementedType:
        """Compute a cross product if ``Point3DData`` is provided. Otherwise, perform scalar multiplication."""
        if isinstance(other, Point3DData):
            x = self.y * other.z - self.z * other.y
            y = self.z * other.x - self.x * other.y
            z = self.x * other.y - self.y * other.x
            return Point3DData(x, y, z)
        if isinstance(other, (int, float)):
            return Point3DData(self.x * other, self.y * other, self.z * other)
        return NotImplemented

    def __rmul__(self, other: Point3DData) -> Point3DData | NotImplementedType:
        """Perform scalar multiplication."""
        return self.__mul__(other)

    def __div__(self, other: Point3DData) -> Point3DData | NotImplementedType:
        """Perform scalar division."""
        if isinstance(other, (int, float)):
            return Point3DData(self.x / other, self.y / other, self.z / other)
        return NotImplemented

    def __neg__(self) -> Point3DData:
        """Negate the signs on the point coordinates."""
        return Point3DData(0, 0, 0) - self

    @property
    def x(self) -> Value:
        """:class:`.Value`: X coordinate."""
        return self._x

    @x.setter
    def x(self, x: ValueLike):
        self._x = conversions.to_value(x)

    @property
    def y(self) -> Value:
        """:class:`.Value`: Y coordinate."""
        return self._y

    @y.setter
    def y(self, y: ValueLike):
        self._y = conversions.to_value(y)

    @property
    def z(self) -> Value:
        """:class:`.Value`: Z coordinate."""
        return self._z

    @z.setter
    def z(self, z: ValueLike):
        self._z = conversions.to_value(z)

    @property
    def magnitude(self) -> float:
        """
        :obj:`float`: Magnitude or length of the point.

        This property is read-only.
        """
        return self.magnitude_sqr.sqrt.double

    @property
    def magnitude_sqr(self) -> float:
        """
        :obj:`float`: Magnitude-square of the point.

        This property is read-only.
        """
        return self.x * self.x + self.y * self.y + self.z * self.z

    def equals(self, other, tolerance: float = 1e-9) -> bool:
        """
        Compare the equality of two 3D points within a given tolerance.

        Parameters
        ----------
        other : .Point3DData
        tolerance : float, default: 1e-9
            Tolerance.

        Returns
        -------
        bool
            ``True`` if the 3D points are equal, ``False`` otherwise.
        """
        if isinstance(other, Point3DData):
            return (
                self.x.equals(other.x, tolerance)
                and self.y.equals(other.y, tolerance)
                and self.z.equals(other.z, tolerance)
            )
        return False

    def distance(self, other: Point3DData) -> float:
        """
        Compute the distance from this point to another point.

        Parameters
        ----------
        other : .Point3DData
            Other point

        Returns
        -------
        float
           Distance to the other point.
        """
        if isinstance(other, Point3DData):
            return (self - other).magnitude

    def midpoint(self, other: Point3DData) -> Point3DData:
        """
        Compute the midpoint of this point and another point.

        Parameters
        ----------
        other : .Point3DData
            Other point

        Returns
        -------
        .Point3DData
            Midpoint of the two points.
        """
        if isinstance(other, Point3DData):
            return 0.5 * (self + other)
