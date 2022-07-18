"""Transform 3D Class."""

from ..utility.edb_errors import handle_grpc_exception
from ..utility.value import Value


class Transform3D:
    """Class representing a 3d transformation."""

    @handle_grpc_exception
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
        self.anchor = [Value(x) for x in anchor]
        self.rot_axis_from = [Value(x) for x in rot_axis_from]
        self.rot_axis_to = [Value(x) for x in rot_axis_to]
        self.rot_angle = Value(rot_angle)
        self.offset = [Value(x) for x in offset]
