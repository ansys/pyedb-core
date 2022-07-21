"""Transform 3D Class."""

from ..utility.value import Value


class Transform3D:
    """Class representing a 3d transformation."""

    def __init__(self, anchor, rot_axis_from, rot_axis_to, rot_angle, offset):
        """Initialize a transform 3d object.

        Parameters
        ----------
        anchor : triple of Values
        rot_axis_from : triple of Values
        rot_axis_to : triple of Values
        rot_angle : Value
        offset : triple of Values
        """
        self.anchor = [Value(val) for val in anchor]
        self.rot_axis_from = [Value(val) for val in rot_axis_from]
        self.rot_axis_to = [Value(val) for val in rot_axis_to]
        self.rot_angle = Value(rot_angle)
        self.offset = [Value(val) for val in offset]
