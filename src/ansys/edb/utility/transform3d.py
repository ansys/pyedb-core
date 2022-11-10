"""Transform 3D Class."""

from ansys.edb.utility import conversions
from ansys.edb.utility.value import Value


class Transform3D:
    """Represents a 3d transformation.

    Parameters
    ----------
    anchor : :class:`Point3DData <ansys.edb.geometry.Point3DData>`
    rot_axis_from : :class:`Point3DData <ansys.edb.geometry.Point3DData>`
    rot_axis_to : :class:`Point3DData <ansys.edb.geometry.Point3DData>`
    rot_angle : str, int, float, complex, Value
        Rotation angle, specified CCW in radians, from rot_axis_from towards rot_axis_to
    offset : :class:`Point3DData <ansys.edb.geometry.Point3DData>`
    """

    def __init__(self, anchor, rot_axis_from, rot_axis_to, rot_angle, offset):
        """Construct a Transform3D."""
        self.anchor = conversions.to_point3d(anchor)
        self.rot_axis_from = conversions.to_point3d(rot_axis_from)
        self.rot_axis_to = conversions.to_point3d(rot_axis_to)
        self.rot_angle = Value(rot_angle)
        self.offset = conversions.to_point3d(offset)
