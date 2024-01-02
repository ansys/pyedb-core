"""Point3D Data."""
from ansys.edb.core.utility.conversions import to_value


class Point3DData:
    """Represent a point on 3D coordinate system."""

    def __init__(self, x, y, z):
        """Initialize a 3D point.

        Parameters
        ----------
        x : :term:`ValueLike`
        y : :term:`ValueLike`
        z : :term:`ValueLike`
        """
        self.x, self.y, self.z = x, y, z

    def __eq__(self, other):
        """Compare two points by exact coordinates."""
        if isinstance(other, Point3DData):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return False

    def __add__(self, other):
        """Add two points piecewise."""
        if isinstance(other, Point3DData):
            return Point3DData(self.x + other.x, self.y + other.y, self.z + other.z)
        return NotImplemented

    def __sub__(self, other):
        """Subtract a point piecewise."""
        if isinstance(other, Point3DData):
            return Point3DData(self.x - other.x, self.y - other.y, self.z - other.z)
        return NotImplemented

    def __mul__(self, other):
        """Compute a cross product if `Point3DData` is provided. otherwise scalar multiplication."""
        if isinstance(other, Point3DData):
            x = self.y * other.z - self.z * other.y
            y = self.z * other.x - self.x * other.y
            z = self.x * other.y - self.y * other.x
            return Point3DData(x, y, z)
        if isinstance(other, (int, float)):
            return Point3DData(self.x * other, self.y * other, self.z * other)
        return NotImplemented

    def __rmul__(self, other):
        """Compute a scalar multiplication."""
        return self.__mul__(other)

    def __div__(self, other):
        """Compute a scalar division."""
        if isinstance(other, (int, float)):
            return Point3DData(self.x / other, self.y / other, self.z / other)
        return NotImplemented

    def __neg__(self):
        """Negate the signs on point coordinates."""
        return Point3DData(0, 0, 0) - self

    @property
    def x(self):
        """:class:`Value<ansys.edb.core.utility.Value>`: x coordinate."""
        return self._x

    @x.setter
    def x(self, x):
        self._x = to_value(x)

    @property
    def y(self):
        """:class:`Value<ansys.edb.core.utility.Value>`: y coordinate."""
        return self._y

    @y.setter
    def y(self, y):
        self._y = to_value(y)

    @property
    def z(self):
        """:class:`Value<ansys.edb.core.utility.Value>`: z coordinate."""
        return self._z

    @z.setter
    def z(self, z):
        self._z = to_value(z)

    @property
    def magnitude(self):
        """:obj:`float`: The magnitude or a length of a point."""
        return self.magnitude_sqr.sqrt.double

    @property
    def magnitude_sqr(self):
        """:obj:`float`: The magnitude-square of a point."""
        return self.x * self.x + self.y * self.y + self.z * self.z

    def equals(self, other, tolerance=1e-9):
        """
        Compare equality of two points within tolerance.

        Parameters
        ----------
        other : Point3DData
        tolerance : float, optional

        Returns
        -------
        bool
        """
        if isinstance(other, Point3DData):
            return (
                self.x.equals(other.x, tolerance)
                and self.y.equals(other.y, tolerance)
                and self.z.equals(other.z, tolerance)
            )
        return False

    def distance(self, other):
        """
        Compute the distance to another point.

        Parameters
        ----------
        other : Point3DData

        Returns
        -------
        float
        """
        if isinstance(other, Point3DData):
            return (self - other).magnitude

    def midpoint(self, other):
        """
        Compute the midpoint of two points.

        Parameters
        ----------
        other : Point3DData

        Returns
        -------
        Point3DData
        """
        if isinstance(other, Point3DData):
            return 0.5 * (self + other)
