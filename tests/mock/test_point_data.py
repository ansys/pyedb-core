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

import ansys.api.edb.v1.edb_messages_pb2 as edb_messages_pb2
from utils.fixtures import *  # noqa

import ansys.edb.core.geometry.point_data as point_data
import ansys.edb.core.utility.value as value


@pytest.mark.parametrize(
    "p2, expected",
    [
        [(1, 2), (2, 3)],
        [[1, 2], (2, 3)],
        [point_data.PointData((1, 2)), (2, 3)],
        [(1 + 2j, 3), (2 + 2j, 4)],
    ],
)
def test_addition(p2, expected):
    p1 = point_data.PointData((1, 1))
    p3 = p1 + p2
    assert p3.x.complex == expected[0]
    assert p3.y.complex == expected[1]


@pytest.mark.parametrize(
    "p2, expected",
    [
        [(1, 2), (4, 3)],
        [[1, 2], (4, 3)],
        [point_data.PointData((1, 2)), (4, 3)],
        [(1 + 2j, 3), (4 - 2j, 2)],
    ],
)
def test_subtraction(p2, expected):
    p1 = point_data.PointData((5, 5))
    p3 = p1 - p2
    assert p3.x.complex == expected[0]
    assert p3.y.complex == expected[1]


@pytest.mark.parametrize(
    "coord, expected",
    [
        [1, False],
        [(1, 2), False],
        [value.Value(1), False],
        [(value.Value(1), value.Value(2)), False],
        ["h", True],
        [("x", 2), True],
        [(1, "y"), True],
    ],
)
def test_is_parametric(mocked_stub, coord, expected):
    mock = mocked_stub(value, value.Value)
    mock.CreateValue.side_effect = lambda payload: edb_messages_pb2.ValueMessage(text=payload.text)
    p = point_data.PointData(coord)
    assert p.is_parametric == expected


@pytest.mark.parametrize("coord, magnitude", [[(3, 4), 5], [1, 0]])
def test_magnitude(coord, magnitude):
    p = point_data.PointData(coord)
    assert p.magnitude() == magnitude


@pytest.mark.parametrize("coord, normalized_coord", [[(3, 4), (3 / 5, 4 / 5)], [1, 0]])
def test_normalized(coord, normalized_coord):
    p = point_data.PointData(coord)
    assert p.normalized() == point_data.PointData(normalized_coord)


@pytest.mark.parametrize("coord1, coord2, dist", [[(1, 2), (4, 6), 5], [1, (1, 1), 0]])
def test_distance(coord1, coord2, dist):
    p1, p2 = point_data.PointData(coord1), point_data.PointData(coord2)
    assert p1.distance(p2) == dist
