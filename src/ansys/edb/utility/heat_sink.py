"""HeatSink."""

from ansys.edb.definition.package_def import HeatSinkOrientation
from ansys.edb.typing import ValueLike
from ansys.edb.utility import conversions


class HeatSink:
    """Class representing HeatSink.

    Attributes
    ----------
        fin_thickness : ValueLike
            HeatSink's thickness.
        fin_spacing : ValueLike
            HeatSink's spacing.
        fin_base_height : ValueLike
            Base elevation of the HeatSink
        fin_height : ValueLike
            HeatSink's height.
        fin_orientation : ValueLike
            HeatSink's orientation.
    """

    def __init__(
        self,
        fin_thickness=0,
        fin_spacing=0,
        fin_base_height=0,
        fin_height=0,
        fin_orientation=HeatSinkOrientation.X_ORIENTED,
    ):
        """Construct a HeatSink object using given values.

        Parameters
        ----------
        fin_thickness : ValueLike
            HeatSink's thickness.
        fin_spacing : ValueLike
            HeatSink's spacing.
        fin_base_height : ValueLike
            Base elevation of the HeatSink
        fin_height : ValueLike
            HeatSink's height.
        fin_orientation : ValueLike
            HeatSink's orientation if not set is set to X axis orientation.
        """
        value_handle = lambda v: v if type(v) is ValueLike else conversions.to_value(v)
        self.fin_thickness = value_handle(fin_thickness)
        self.fin_spacing = value_handle(fin_spacing)
        self.fin_base_height = value_handle(fin_base_height)
        self.fin_height = value_handle(fin_height)
        self.fin_orientation = fin_orientation
