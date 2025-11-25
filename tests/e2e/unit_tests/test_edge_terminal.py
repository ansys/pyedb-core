from ansys.edb.core.geometry.polygon_data import PolygonData
from ansys.edb.core.layout.cell import Cell
from ansys.edb.core.net.net import Net
from ansys.edb.core.primitive.path import Path as Line
from ansys.edb.core.primitive.path import PathCornerType, PathEndCapType
from ansys.edb.core.primitive.primitive import PrimitiveType
from ansys.edb.core.terminal.edge_terminal import EdgeTerminal, PrimitiveEdge
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
