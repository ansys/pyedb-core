"""Triangle3DData Class."""


class Triangle3DData:
    """Triangle defined by three 3D points."""

    def __init__(self, point_1, point_2, point_3):
        """Create a 3D triangle.

        Parameters
        ----------
        point_1: :class:`Point3DData`
        point_2: :class:`Point3DData`
        point_3: :class:`Point3DData`
        """
        self._point_1 = point_1
        self._point_2 = point_2
        self._point_3 = point_3

    @property
    def point_1(self):
        """:class:`Point3DData`: First point."""
        return self._point_1

    @point_1.setter
    def point_1(self, point_1):
        self._point_1 = point_1

    @property
    def point_2(self):
        """:class:`Point3DData`: Second point."""
        return self._point_2

    @point_2.setter
    def point_2(self, point_2):
        self._point_2 = point_2

    @property
    def point_3(self):
        """:class:`Point3DData`: Third point."""
        return self._point_3

    @point_3.setter
    def point_3(self, point_3):
        self._point_3 = point_3
