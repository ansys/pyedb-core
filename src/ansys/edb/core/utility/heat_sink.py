# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Heat sink."""

from enum import Enum

import ansys.api.edb.v1.package_def_pb2 as pb

from ansys.edb.core.utility import conversions


class HeatSinkFinOrientation(Enum):
    """Provides an enum representing bondwire types."""

    X_ORIENTED = pb.X_ORIENTED
    Y_ORIENTED = pb.Y_ORIENTED
    OTHER_ORIENTED = pb.OTHER_ORIENTED


class HeatSink:
    """Represents a heat sink.

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
        fin_orientation : HeatSinkFinOrientation
            Fin orientation of the heat sink if it is not set to the X axis.

    """

    def __init__(
        self,
        fin_thickness=0,
        fin_spacing=0,
        fin_base_height=0,
        fin_height=0,
        fin_orientation=HeatSinkFinOrientation.X_ORIENTED,
    ):
        """Initialize a heat sink object using given values."""
        self.fin_thickness = conversions.to_value(fin_thickness)
        self.fin_spacing = conversions.to_value(fin_spacing)
        self.fin_base_height = conversions.to_value(fin_base_height)
        self.fin_height = conversions.to_value(fin_height)
        self.fin_orientation = fin_orientation
