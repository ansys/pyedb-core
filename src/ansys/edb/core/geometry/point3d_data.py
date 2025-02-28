# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Point3D data."""
from ansys.edb.core.utility import conversions


class Point3DData:
    """Represents a point on a 3D coordinate system."""

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
        """Compute a cross product if ``Point3DData`` is provided. Otherwise, perform scalar multiplication."""
        if isinstance(other, Point3DData):
            x = self.y * other.z - self.z * other.y
            y = self.z * other.x - self.x * other.y
            z = self.x * other.y - self.y * other.x
            return Point3DData(x, y, z)
        if isinstance(other, (int, float)):
            return Point3DData(self.x * other, self.y * other, self.z * other)
        return NotImplemented

    def __rmul__(self, other):
        """Perform scalar multiplication."""
        return self.__mul__(other)

    def __div__(self, other):
        """Perform scalar division."""
        if isinstance(other, (int, float)):
            return Point3DData(self.x / other, self.y / other, self.z / other)
        return NotImplemented

    def __neg__(self):
        """Negate the signs on the point coordinates."""
        return Point3DData(0, 0, 0) - self

    @property
    def x(self):
        """:class:`.Value`: X coordinate."""
        return self._x

    @x.setter
    def x(self, x):
        self._x = conversions.to_value(x)

    @property
    def y(self):
        """:class:`.Value`: Y coordinate."""
        return self._y

    @y.setter
    def y(self, y):
        self._y = conversions.to_value(y)

    @property
    def z(self):
        """:class:`.Value`: Z coordinate."""
        return self._z

    @z.setter
    def z(self, z):
        self._z = conversions.to_value(z)

    @property
    def magnitude(self):
        """:obj:`float`: Magnitude or length of the point."""
        return self.magnitude_sqr.sqrt.double

    @property
    def magnitude_sqr(self):
        """:obj:`float`: Magnitude-square of the point."""
        return self.x * self.x + self.y * self.y + self.z * self.z

    def equals(self, other, tolerance=1e-9):
        """
        Compare the equality of two 3D points within a given tolerance.

        Parameters
        ----------
        other : Point3DData
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

    def distance(self, other):
        """
        Compute the distance from this point to another point.

        Parameters
        ----------
        other : Point3DData
            Other point

        Returns
        -------
        float
           Distance to the other point.
        """
        if isinstance(other, Point3DData):
            return (self - other).magnitude

    def midpoint(self, other):
        """
        Compute the midpoint of this point and another point.

        Parameters
        ----------
        other : Point3DData
            Other point

        Returns
        -------
        Point3DData
            Midpoint of the two points.
        """
        if isinstance(other, Point3DData):
            return 0.5 * (self + other)
