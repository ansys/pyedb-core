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

from ansys.edb.core.layout.cell import Cell


@pytest.mark.parametrize(("layer_name", "is_null"), (("L1", False), ("NonExistentLayer", True), ("l1", False)))
def test_find_by_name(circuit_cell_with_stackup: Cell, is_null: bool, layer_name: str):
    """Test that finding a layer by name returns a correct layer object."""
    layer = circuit_cell_with_stackup.layout.layer_collection.find_by_name(layer_name)
    assert layer is not None and layer.is_null == is_null


def test_tsv_properties(circuit_cell_with_overlapping_stackup: Cell):
    """Test that finding a layer by name returns a correct layer object."""
    layer = circuit_cell_with_overlapping_stackup.layout.layer_collection.find_by_name("V1")
    assert layer is not None and not layer.is_null
    assert not layer.is_tsv
    layer.is_tsv = True
    layer.add_oxide_layers([("0.1um", "silicon_dioxide"), ("25nm", "FR4_epoxy")])
    assert layer.is_tsv
    assert len(layer.oxide_layers) == 2
    assert layer.oxide_layers == [("0.1um", "silicon_dioxide"), ("25nm", "FR4_epoxy")]
