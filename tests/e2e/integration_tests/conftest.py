from pytest import fixture

from ansys.edb.definition import PadGeometryType, PadstackDef, PadstackDefData, PadType
from ansys.edb.layer import LayerType, StackupLayer
from ansys.edb.layout import Cell


@fixture()
def cell_with_stackup(circuit_cell: Cell):
    layers = [
        StackupLayer.create("L1", LayerType.CONDUCTING_LAYER, 25e-6, 0.0, "copper"),
        StackupLayer.create("D1", LayerType.DIELECTRIC_LAYER, 100e-6, 0.0, "FR4_epoxy"),
        StackupLayer.create("L2", LayerType.CONDUCTING_LAYER, 25e-6, 0.0, "copper"),
    ]
    for layer in layers:
        circuit_cell.layout.layer_collection.add_layer_bottom(layer)
    yield circuit_cell


@fixture()
def cell_with_padstack_def(cell_with_stackup: Cell):
    db = cell_with_stackup.database
    padstack_def_data = PadstackDefData.create()
    layer_names = ["Start", "Default", "Stop"]
    padstack_def_data.add_layers(layer_names)
    for name in layer_names:
        padstack_def_data.set_pad_parameters(
            name,
            PadType.REGULAR_PAD,
            0.0,
            0.0,
            0.0,
            PadGeometryType.PADGEOMTYPE_CIRCLE,
            [70e-6],
        )
        padstack_def_data.set_pad_parameters(
            name,
            PadType.ANTI_PAD,
            0.0,
            0.0,
            0.0,
            PadGeometryType.PADGEOMTYPE_CIRCLE,
            [100e-6],
        )
    padstack_def_data.set_hole_parameters(
        0.0, 0.0, 0.0, PadGeometryType.PADGEOMTYPE_CIRCLE, [50e-6]
    )
    padstack_def = PadstackDef.create(db, "VIA050070100")
    padstack_def.data = padstack_def_data
    yield cell_with_stackup
