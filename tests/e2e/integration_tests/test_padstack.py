from ansys.edb.definition import PadGeometryType, PadstackDef
from ansys.edb.layout import Cell


def test_get_hole_parameters(cell_with_padstack_def: Cell):
    padstack_def = PadstackDef.find_by_name(cell_with_padstack_def.database, "VIA050070100")
    assert not padstack_def.is_null
    padstack_def_data = padstack_def.data
    assert not padstack_def_data.is_null
    hole_parameters = padstack_def_data.get_hole_parameters()
    assert hole_parameters[0] == PadGeometryType.PADGEOMTYPE_CIRCLE
    assert len(hole_parameters[1]) == 1
    assert round(hole_parameters[1][0].double - 50e-6, 9) == 0.0
