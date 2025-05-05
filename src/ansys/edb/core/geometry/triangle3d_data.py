"""Triangle 3D data."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.geometry.point3d_data import Point3DData


class Triangle3DData:
    """Represents a triangle defined by three 3D points."""

    def __init__(self, point_1: Point3DData, point_2: Point3DData, point_3: Point3DData):
        """Create a 3D triangle.

        Parameters
        ----------
        point_1 : .Point3DData
        point_2 : .Point3DData
        point_3 : .Point3DData
        """
        self._point_1 = point_1
        self._point_2 = point_2
        self._point_3 = point_3

    @property
    def point_1(self) -> Point3DData:
        """:class:`.Point3DData`: First 3D point."""
        return self._point_1

    @point_1.setter
    def point_1(self, point_1: Point3DData):
        self._point_1 = point_1

    @property
    def point_2(self) -> Point3DData:
        """:class:`.Point3DData`: Second 3D point."""
        return self._point_2

    @point_2.setter
    def point_2(self, point_2: Point3DData):
        self._point_2 = point_2

    @property
    def point_3(self) -> Point3DData:
        """:class:`.Point3DData`: Third 3D point."""
        return self._point_3

    @point_3.setter
    def point_3(self, point_3: Point3DData):
        self._point_3 = point_3
