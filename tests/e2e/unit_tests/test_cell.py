def test_get_database(circuit_cell, new_database):
    cell_db = circuit_cell.database
    assert not cell_db.is_null
    assert cell_db.id == new_database.id


def test_get_layout(circuit_cell):
    cell_lyt = circuit_cell.layout
    assert not cell_lyt.is_null
    assert circuit_cell.id == cell_lyt.cell.id
