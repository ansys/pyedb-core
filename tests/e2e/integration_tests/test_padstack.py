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

from ansys.edb.core.definition.padstack_def import PadstackDef
from ansys.edb.core.definition.padstack_def_data import PadGeometryType
from ansys.edb.core.layout.cell import Cell


def test_get_hole_parameters(circuit_cell_with_padstack_def: Cell):
    padstack_def = PadstackDef.find_by_name(circuit_cell_with_padstack_def.database, "VIA050070100")
    assert not padstack_def.is_null
    padstack_def_data = padstack_def.data
    assert not padstack_def_data.is_null
    hole_parameters = padstack_def_data.get_hole_parameters()
    assert hole_parameters[0] == PadGeometryType.PADGEOMTYPE_CIRCLE
    assert len(hole_parameters[1]) == 1
    assert round(hole_parameters[1][0].double - 50e-6, 9) == 0.0
