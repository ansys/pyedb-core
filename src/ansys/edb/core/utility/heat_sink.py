"""Heat sink."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.typing import ValueLike

from enum import Enum

import ansys.api.edb.v1.package_def_pb2 as pb

from ansys.edb.core.utility import conversions


class HeatSinkFinOrientation(Enum):
    """Provides an enum representing bondwire types."""

    X_ORIENTED = pb.X_ORIENTED
    Y_ORIENTED = pb.Y_ORIENTED
    OTHER_ORIENTED = pb.OTHER_ORIENTED


class HeatSink:
    """Represents a heat sink, a three-dimensional modeling component \
    that can exchange radiation with other objects in the model.

    Attributes
    ----------
        fin_thickness : :term:`ValueLike`
            Fin thickness of the heat sink.
        fin_spacing : :term:`ValueLike`
            Fin spacing of the heat sink.
        fin_base_height : :term:`ValueLike`
            Base elevation of the the heat sink.
        fin_height : :term:`ValueLike`
            Fin height of the heat sink.
        fin_orientation : .HeatSinkFinOrientation
            Fin orientation of the heat sink if it is not set to the X axis.
    """

    def __init__(
        self,
        fin_thickness: ValueLike = 0,
        fin_spacing: ValueLike = 0,
        fin_base_height: ValueLike = 0,
        fin_height: ValueLike = 0,
        fin_orientation: HeatSinkFinOrientation = HeatSinkFinOrientation.X_ORIENTED,
    ):
        """Initialize a heat sink object using given values.

        Parameters
        ----------
        fin_thickness : :term:`ValueLike`
            Fin thickness of the heat sink.
        fin_spacing : :term:`ValueLike`
            Fin spacing of the heat sink.
        fin_base_height : :term:`ValueLike`
            Base elevation of the the heat sink.
        fin_height : :term:`ValueLike`
            Fin height of the heat sink.
        fin_orientation : .HeatSinkFinOrientation
            Fin orientation of the heat sink if it is not set to the X axis.
        """
        self.fin_thickness = conversions.to_value(fin_thickness)
        self.fin_spacing = conversions.to_value(fin_spacing)
        self.fin_base_height = conversions.to_value(fin_base_height)
        self.fin_height = conversions.to_value(fin_height)
        self.fin_orientation = fin_orientation
