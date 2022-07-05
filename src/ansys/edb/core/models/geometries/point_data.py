"""Point Data."""
import math
from typing import Iterable, Union

import numpy as np

from ...utility.value import ValueLikeT, value_like


def point_like(val):
    """Take a value implicitly convertible to PointData and return as PointData.

    Parameters
    ----------
    val : ansys.edb.core.models.geometries.PointLikeT

    Returns
    -------
    PointData
    """
    if isinstance(val, PointData):
        return val
    try:
        if len(val) in [1, 2]:
            return PointData(val)
    except TypeError:
        pass

    raise TypeError(
        "point-like objects must be either of type PointData or a list/tuple containing (start, end) or (arc_height)."
    )


class PointData(object):
    """represents arbitrary (x, y) coordinates that exist on 2D space."""

    def __init__(self, data):
        """Initialize a point data from list of coordinates.

        Parameters
        ----------
        data : Iterable[ansys.edb.core.utility.value.ValueLikeT]
        """
        if len(data) == 2:
            self._x, self._y = [value_like(val) for val in data]
            self._arc_h = None
        else:
            self._x = self._y = None
            self._arc_h, *_ = [value_like(val) for val in data]

    def __eq__(self, other):
        """Compare if two objects represent the same coordinates.

        Parameters
        ----------
        other : PointData

        Returns
        -------
        bool
        """
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __len__(self):
        """Return the number of coordinates present.

        Returns
        -------
        int
        """
        return 1 if self.is_arc else 2

    def __add__(self, other):
        """Perform matrix addition of two points.

        Parameters
        ----------
        other : ansys.edb.core.models.geometries.PointLikeT

        Returns
        -------
        PointData
        """
        _other = point_like(other)
        return self.__class__(self.matrix + _other.matrix)

    def __sub__(self, other):
        """Perform matrix subtraction of two points.

        Parameters
        ----------
        other : ansys.edb.core.models.geometries.PointLikeT

        Returns
        -------
        PointData
        """
        _other = point_like(other)
        return self.__class__(self.matrix - _other.matrix)

    def __str__(self):
        """Generate unique name for point object.

        Returns
        -------
        str
        """
        coord = ",".join(self._matrix_values)
        return f"<{coord}>" if self.is_arc else f"({coord})"

    @property
    def _matrix_values(self):
        """Return coordinates of this point as a list of Value.

        Returns
        -------
        list of ansys.edb.core.utility.Value
        """
        return [self._arc_h] if self.is_arc else [self._x, self._y]

    @property
    def matrix(self):
        """Evaluate any parametric values and return as numpy array.

        Returns
        -------
        np.ndarray
        """
        return np.array([v.double for v in self._matrix_values])

    @property
    def is_arc(self):
        """Return if the point represents an arc.

        Returns
        -------
        bool
        """
        return self._arc_h is not None

    @property
    def arc_height(self):
        """Return the height of arc.

        Returns
        -------
        ansys.edb.core.utility.Value
        """
        return self._arc_h

    @property
    def is_parametric(self):
        """Return if this point contains parametric values (variable expressions).

        Returns
        -------
        bool
        """
        return any(val.is_parametric for val in self._matrix_values)

    @property
    def magnitude(self):
        """Return the magnitude of point vector.

        Returns
        -------
        float
        """
        if self.is_arc:
            return 0
        return np.linalg.norm(self.matrix)

    def normalize(self):
        """Normalize the point vector.

        Returns
        -------
        PointData
        """
        vec = self.matrix
        return self.__class__(vec / np.linalg.norm(vec))

    def closest(self, start, end):
        """Return the closest point on the line segment [start, end] from the point.

        Parameters
        ----------
        start : ansys.edb.core.models.geometries.PointLikeT
        end : ansys.edb.core.models.geometries.PointLikeT

        Returns
        -------
        PointData
        """
        point = self.matrix
        start = point_like(start).matrix
        end = point_like(end).matrix

        line_vec = end - start
        line_len2 = np.dot(line_vec, line_vec)

        t = max(0, min(1, np.dot(point - start, line_vec) / line_len2))
        return self.__class__(start + t * line_vec)

    def distance(self, start, end=None):
        """Compute the shortest distance from the point to the line segment [start, end] when end point is given, \
        otherwise the distance between the point and another.

        Parameters
        ----------
        start : ansys.edb.core.models.geometries.PointLikeT
        end : ansys.edb.core.models.geometries.PointLikeT, optional

        Returns
        -------
        float
        """
        to = point_like(start) if end is None else self.closest(start, end)
        return np.linalg.norm(self.matrix - to.matrix)

    def cross(self, other):
        """Compute the cross product of the point vector with another.

        Parameters
        ----------
        other : ansys.edb.core.models.geometries.PointLikeT

        Returns
        -------
        np.ndarray
        """
        _other = point_like(other)

        if not self.is_arc and not _other.is_arc:
            return np.cross(self.matrix, _other.matrix)

    def move(self, vector):
        """Move the point by a vector.

        Parameters
        ----------
        vector : ansys.edb.core.models.geometries.PointLikeT

        Returns
        -------
        PointData
        """
        _vector = point_like(vector)
        if not self.is_arc and not _vector.is_arc:
            return self + _vector

    def rotate(self, angle, center):
        """Rotate a point at the specified center by the specified angle.

        Parameters
        ----------
        angle : float
            in radians.
        center : ansys.edb.core.models.geometries.PointLikeT

        Returns
        -------
        PointData
        """
        if not self.is_arc:
            center = point_like(center).matrix
            dist = center - self.matrix
            cos, sin = math.cos(angle), math.sin(angle)
            rotation = np.array([[cos, -sin], [sin, cos]])

            return self.__class__(center + rotation * dist)


PointLikeT = Union[PointData, Iterable[ValueLikeT]]
