"""Transform Class."""

from ansys.edb.utility.value import Value


class Transform:
    """Represents a transformation.

    Parameters
    ----------
    scale : str, int, float, complex, Value
        Scale parameter
    angle : str, int, float, complex, Value
        Rotation angle, specified CCW in radians.
    mirror : bool
        Mirror about Y-axis
    offset_x : str, int, float, complex, Value
        X offset
    offset_y : str, int, float, complex, Value
        Y offset
    """

    def __init__(self, scale, angle, mirror, offset_x, offset_y):
        """Construct a transform object."""
        self.scale = Value(scale)
        self.angle = Value(angle)
        self.mirror = mirror
        self.offset_x = Value(offset_x)
        self.offset_y = Value(offset_y)
