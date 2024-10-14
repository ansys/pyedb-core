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

"""This module performs conversions from arbitrary user input to explicit types."""
from ansys.api.edb.v1.edb_messages_pb2 import ValueMessage

from ansys.edb.core.geometry import point3d_data, point_data
from ansys.edb.core.utility import value


def to_value(val):
    """Take a value implicitly convertible to a ``Value``type and return as a ``Value`` type.

    Parameters
    ----------
    val : ansys.edb.core.typing.ValueLike

    Returns
    -------
    :class:`.Value`
    """
    if isinstance(val, value.Value):
        return val
    elif type(val) in [int, float, complex, str, ValueMessage]:
        return value.Value(val)
    else:
        raise TypeError(
            f"Value-like objects must be either of type Value or int/float/complex/str. - Received '{val}'"
        )


def to_point(val):
    """Take a value implicitly convertible to a ``PointData`` type and return as a ``PointData`` type.

    Parameters
    ----------
    val : ansys.edb.core.typing.PointLike

    Returns
    -------
    :class:`.PointData`
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


def to_point3d(val):
    """Convert a value to a ``Point3DData`` object.

    Parameters
    ----------
    val : Point3DData, tuple[:term:`ValueLike`,:term:`ValueLike`,:term:`ValueLike`]
        Value to convert.

    Returns
    -------
    :class:`.Point3DData`
    """
    if isinstance(val, point3d_data.Point3DData):
        return val
    if len(val) == 3:
        return point3d_data.Point3DData(val[0], val[1], val[2])
