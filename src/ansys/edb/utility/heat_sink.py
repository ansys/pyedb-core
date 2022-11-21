"""HeatSink."""

from ansys.edb.definition.package_def import HeatSinkFinOrientation
from ansys.edb.utility import Value, conversions


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
        value_handle = lambda v: v if type(v) is Value else conversions.to_value(v)
        self.fin_thickness = value_handle(fin_thickness)
        self.fin_spacing = value_handle(fin_spacing)
        self.fin_base_height = value_handle(fin_base_height)
        self.fin_height = value_handle(fin_height)
        self.fin_orientation = fin_orientation
