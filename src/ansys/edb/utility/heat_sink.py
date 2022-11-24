"""HeatSink."""

from enum import Enum

import ansys.api.edb.v1.package_def_pb2 as pb


class HeatSinkFinOrientation(Enum):
    """Enum representing bondwire types.

    - X_ORIENTED
       X axis oriented.
    - Y_ORIENTED
       Y axis oriented.
    - OTHER_ORIENTED
       Other oriented.
    """

    X_ORIENTED = pb.X_ORIENTED
    Y_ORIENTED = pb.Y_ORIENTED
    OTHER_ORIENTED = pb.OTHER_ORIENTED


class HeatSink:
    """Class representing HeatSink.

    Attributes
    ----------
        fin_thickness : ValueLike
            HeatSink's fin thickness.
        fin_spacing : ValueLike
            HeatSink's fin spacing.
        fin_base_height : ValueLike
            Base elevation of the HeatSink
        fin_height : ValueLike
            HeatSink's fin height.
        fin_orientation : HeatSinkFinOrientation
            HeatSink's fin orientation if not set is set to X axis orientation.

    """

    def __init__(
        self,
        fin_thickness=0,
        fin_spacing=0,
        fin_base_height=0,
        fin_height=0,
        fin_orientation=HeatSinkFinOrientation.X_ORIENTED,
    ):
        """Construct a HeatSink object using given values."""
        self.fin_thickness = fin_thickness
        self.fin_spacing = fin_spacing
        self.fin_base_height = fin_base_height
        self.fin_height = fin_height
        self.fin_orientation = fin_orientation
