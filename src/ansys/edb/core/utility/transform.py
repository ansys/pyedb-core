"""Transform Class."""

from ..utility.edb_errors import handle_grpc_exception
from ..utility.value import Value


class Transform:
    """Class representing a transformation."""

    @handle_grpc_exception
    def __init__(self, scale, angle, mirror, offset_x, offset_y):
        """Initialize transform object.

        Parameters
        ----------
        scale - scale parameter
        angle - rotation angle, specified CCW in radians.
        mirror - mirror about Y-axis
        offset_x - X offset
        offset_y - Y offset
        """
        self.scale = Value(scale)
        self.angle = Value(angle)
        self.mirror = mirror
        self.offset_x = Value(offset_x)
        self.offset_y = Value(offset_y)
