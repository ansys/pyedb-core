from ansys.edb.core.layout.cell import Cell
from ansys.edb.core.primitive.primitive import PrimitiveType
from ansys.edb.core.terminal.edge_terminal import EdgeTerminal
from ansys.edb.core.terminal.terminal import Terminal


def test_primitive_edge_primitive(circuit_cell_with_edge_terminals: Cell):
    layout = circuit_cell_with_edge_terminals.layout
    terminal: EdgeTerminal = Terminal.find(layout, "P1")
    assert len(terminal.edges) == 1
    assert terminal.edges[0].primitive.primitive_type == PrimitiveType.PATH
