"""HeatSink."""

from ansys.edb.definition.package_def import HeatSinkOrientation
from ansys.edb.utility.value import Value


class HeatSink:
    """Class representing HeatSink.

    Attributes
    ----------
        fin_thickness : str, int, float, complex, Value, optional
            HeatSink's thickness.
        fin_spacing : str, int, float, complex, Value, optional
            HeatSink's spacing.
        fin_base_height : str, int, float, complex, Value, optional
            Base elevation of the HeatSink
        fin_height : str, int, float, complex, Value, optional
            HeatSink's height.
        fin_orientation : str, int, float, complex, Value, optional
            HeatSink's orientation.
    """

    def __init__(
        self,
        fin_thickness=Value(0),
        fin_spacing=Value(0),
        fin_base_height=Value(0),
        fin_height=Value(0),
        fin_orientation=HeatSinkOrientation.X_ORIENTED,
    ):
        """Construct a HeatSink object using given values.

        Parameters
        ----------
        fin_thickness : str, int, float, complex, Value, optional
            HeatSink's thickness.
        fin_spacing : str, int, float, complex, Value, optional
            HeatSink's spacing.
        fin_base_height : str, int, float, complex, Value, optional
            Base elevation of the HeatSink
        fin_height : str, int, float, complex, Value, optional
            HeatSink's height.
        fin_orientation : str, int, float, complex, Value, optional
            HeatSink's orientation if not set is set to X axis orientation.
        """
        self.fin_thickness = fin_thickness
        self.fin_spacing = fin_spacing
        self.fin_base_height = fin_base_height
        self.fin_height = fin_height
        self.fin_orientation = fin_orientation
