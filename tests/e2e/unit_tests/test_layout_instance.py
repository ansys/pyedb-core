from ansys.edb.core.layout.cell import Cell


def test_layout_instance_smoke(circuit_cell_with_edge_terminals: Cell):
    layout = circuit_cell_with_edge_terminals.layout
    assert layout is not None
    objs = layout.layout_instance.query_layout_obj_instances(["L1"])
    assert len(objs) == 3
