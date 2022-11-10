"""Point3D Data."""
from ansys.edb.utility import conversions


class Point3DData:
    """Class representing 3D point system."""

    def __init__(self, x, y, z):
        """Initialize a 3D point.

        Parameters
        ----------
        x : :term:`ValueLike`
        y : :term:`ValueLike`
        z : :term:`ValueLike`
        """
        self.x = conversions.to_value(x)
        self.y = conversions.to_value(y)
        self.z = conversions.to_value(z)
