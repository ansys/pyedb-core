# Copyright (C) 2022 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

"""This module performs conversions from arbitrary user input to explicit types."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.typing import Point3DLike
    from ansys.edb.core.typing import PointLike
    from ansys.edb.core.typing import ValueLike

from ansys.api.edb.v1.edb_messages_pb2 import ValueMessage

from ansys.edb.core.geometry import point3d_data
from ansys.edb.core.geometry import point_data
from ansys.edb.core.utility import value


def to_value(val: ValueLike) -> value.Value:
    """Take a value implicitly convertible to a :class:`.Value` type and return as a :class:`.Value` type.

    Parameters
    ----------
    val : :term:`ValueLike`

    Returns
    -------
    .Value
    """
    if isinstance(val, value.Value):
        return val
    elif type(val) in [int, float, complex, str, ValueMessage]:
        return value.Value(val)
    else:
        raise TypeError(f"Value-like objects must be either of type Value or int/float/complex/str. - Received '{val}'")


def to_point(val: PointLike) -> point_data.PointData:
    """Take a value implicitly convertible to a :class:`.PointData` type and return as a :class:`.PointData` type.

    Parameters
    ----------
    val : :term:`Point2DLike`

    Returns
    -------
    .PointData
    """
    if isinstance(val, point_data.PointData):
        return val
    try:
        if len(val) == 2:
            return point_data.PointData(val)
    except TypeError:
        return point_data.PointData(val)

    raise TypeError(
        "Point-like objects must be either of type PointData or a list/tuple containing (start, end) or (arc_height)."
    )


def to_point3d(val: Point3DLike) -> point3d_data.Point3DData:
    """Take a value implicitly convertible to a :class:`.Point3DData` type and return as a :class:`.Point3DData` type.

    Parameters
    ----------
    val : :term:`Point3DLike`

    Returns
    -------
    .Point3DData
    """
    if isinstance(val, point3d_data.Point3DData):
        return val
    if len(val) == 3:
        return point3d_data.Point3DData(val[0], val[1], val[2])
