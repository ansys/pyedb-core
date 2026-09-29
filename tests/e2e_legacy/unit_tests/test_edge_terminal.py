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

from ansys.edb.core.geometry.polygon_data import PolygonData
from ansys.edb.core.layout.cell import Cell
from ansys.edb.core.net.net import Net
from ansys.edb.core.primitive.path import Path as Line
from ansys.edb.core.primitive.path import PathCornerType
from ansys.edb.core.primitive.path import PathEndCapType
from ansys.edb.core.primitive.primitive import PrimitiveType
from ansys.edb.core.terminal.edge_terminal import EdgeTerminal
from ansys.edb.core.terminal.edge_terminal import PrimitiveEdge
from ansys.edb.core.terminal.terminal import Terminal


def test_primitive_edge_primitive(circuit_cell_with_edge_terminals: Cell):
    layout = circuit_cell_with_edge_terminals.layout
    terminal: EdgeTerminal = Terminal.find(layout, "P1")
    assert len(terminal.edges) == 1
    assert terminal.edges[0].primitive.primitive_type == PrimitiveType.PATH


def test_set_edges(circuit_cell_with_edge_terminals: Cell):
    layout = circuit_cell_with_edge_terminals.layout

    line = Line.create(
        circuit_cell_with_edge_terminals.layout,
        "L1",
        Net.create(circuit_cell_with_edge_terminals.layout, "NET2"),
        0.2e-3,
        PathEndCapType.FLAT,
        PathEndCapType.FLAT,
        PathCornerType.ROUND,
        PolygonData([[-0.9e-3, -0.4e-3], [0.9e-3, -0.4e-3]]),
    )

    terminal: EdgeTerminal = Terminal.find(layout, "P1")
    assert len(terminal.edges) == 1

    edge1 = PrimitiveEdge.create(line, [-0.9e-3, -0.4e-3])
    assert terminal.edges[0].id != edge1.id
    terminal.edges = [edge1]
    assert terminal.edges[0].id == edge1.id
