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

import pytest

from ansys.edb.core.geometry.point_data import PointData
from ansys.edb.core.geometry.polygon_data import PolygonData
from ansys.edb.core.layout.cell import Cell
from ansys.edb.core.layout_instance.layout_obj_instance import LayoutObjInstance


@pytest.mark.parametrize(
    ["spatial_filter", "expected_lengths"],
    [
        (None, 4),
        (PointData([0.0, 0.0]), 2),
        ([PointData([0.0, 0.0])], [2]),
        ([PointData([-0.1e-3, 0.0]), PointData([0.1e-3, 0.0])], [2, 2]),
    ],
)
def test_query_layout_obj_instances(
    circuit_cell_with_edge_terminals: Cell,
    expected_lengths: int | list[int],
    spatial_filter: PolygonData | PointData | None | list[PolygonData | PointData],
):
    layout = circuit_cell_with_edge_terminals.layout
    loi_list = layout.layout_instance.query_layout_obj_instances(
        spatial_filter=spatial_filter,
    )
    if isinstance(expected_lengths, int):
        assert len(loi_list) == expected_lengths
        assert all(isinstance(loi, LayoutObjInstance) for loi in loi_list)
    else:
        assert len(loi_list) == len(expected_lengths)
        for loi_result, expected_length in zip(loi_list, expected_lengths):
            assert isinstance(loi_result, list)
            assert len(loi_result) == expected_length
            assert all(isinstance(loi, LayoutObjInstance) for loi in loi_result)
