"""Transform 3D Class."""

from ansys.edb.utility.value import Value


class Transform3D:
    """Represents a 3d transformation.

    Parameters
    ----------
    anchor : list[str, int, float, complex, Value]
        Triple of Values for x, y, z
    rot_axis_from : list[str, int, float, complex, Value]
        Triple of Values for x, y, z
    rot_axis_to : list[str, int, float, complex, Value]
        Triple of Values for x, y, z
    rot_angle : str, int, float, complex, Value
        Rotation angle, specified CCW in radians, from rot_axis_from towards rot_axis_to
    offset : list[str, int, float, complex, Value]
        Triple of Values for x, y, z
    """

    def __init__(self, anchor, rot_axis_from, rot_axis_to, rot_angle, offset):
        """Construct a Transform3D."""
        self.anchor = [Value(val) for val in anchor]
        self.rot_axis_from = [Value(val) for val in rot_axis_from]
        self.rot_axis_to = [Value(val) for val in rot_axis_to]
        self.rot_angle = Value(rot_angle)
        self.offset = [Value(val) for val in offset]
