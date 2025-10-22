import pytest
import settings

from ansys.edb.core.database import Database
from ansys.edb.core.definition.padstack_def import PadstackDef
from ansys.edb.core.definition.padstack_def_data import PadGeometryType, PadstackDefData, PadType
from ansys.edb.core.geometry.polygon_data import PolygonData
from ansys.edb.core.layer.layer import LayerType
from ansys.edb.core.layer.stackup_layer import StackupLayer
from ansys.edb.core.layout.cell import Cell, CellType
from ansys.edb.core.net.net import Net
from ansys.edb.core.primitive.path import Path as Line
from ansys.edb.core.primitive.path import PathCornerType, PathEndCapType
from ansys.edb.core.primitive.rectangle import Rectangle, RectangleRepresentationType
from ansys.edb.core.session import session
from ansys.edb.core.terminal.edge_terminal import EdgeTerminal, PrimitiveEdge


@pytest.fixture
def test_session():
    with session(settings.server_exe_dir(), 50051):
        yield


@pytest.fixture
def new_database_path(tmp_path):
    return str(tmp_path / "test.aedb")


@pytest.fixture
def new_database(test_session, new_database_path):
    db = Database.create(new_database_path)
    yield db
    db.close()


@pytest.fixture
def circuit_cell(new_database):
    return Cell.create(new_database, CellType.CIRCUIT_CELL, "circuit_cell")


@pytest.fixture()
def circuit_cell_with_stackup(circuit_cell: Cell):
    layers = [
        StackupLayer.create("L1", LayerType.CONDUCTING_LAYER, 25e-6, 0.0, "copper"),
        StackupLayer.create("D1", LayerType.DIELECTRIC_LAYER, 100e-6, 0.0, "FR4_epoxy"),
        StackupLayer.create("L2", LayerType.CONDUCTING_LAYER, 25e-6, 0.0, "copper"),
    ]
    for layer in layers:
        circuit_cell.layout.layer_collection.add_layer_bottom(layer)
    yield circuit_cell


@pytest.fixture()
def circuit_cell_with_padstack_def(circuit_cell_with_stackup: Cell):
    db = circuit_cell_with_stackup.database
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
    yield circuit_cell_with_stackup


@pytest.fixture
def circuit_cell_with_edge_terminals(circuit_cell_with_padstack_def: Cell) -> Cell:
    _ = Rectangle.create(
        circuit_cell_with_padstack_def.layout,
        "L2",
        Net.create(circuit_cell_with_padstack_def.layout, "GND"),
        RectangleRepresentationType.CENTER_WIDTH_HEIGHT,
        0.0,
        0.0,
        2e-3,
        1e-3,
        0.0,
        0.0,
    )

    line = Line.create(
        circuit_cell_with_padstack_def.layout,
        "L1",
        Net.create(circuit_cell_with_padstack_def.layout, "NET1"),
        0.2e-3,
        PathEndCapType.FLAT,
        PathEndCapType.FLAT,
        PathCornerType.ROUND,
        PolygonData([[-0.9e-3, 0.0], [0.9e-3, 0.0]]),
    )

    edge1 = PrimitiveEdge.create(line, [-0.9e-3, 0.0])
    edge_terminal1 = EdgeTerminal.create(
        circuit_cell_with_padstack_def.layout,
        "P1",
        [edge1],
        Net.find_by_name(circuit_cell_with_padstack_def.layout, "NET1"),
    )
    edge_terminal1.reference_layer = "L2"

    edge2 = PrimitiveEdge.create(line, [0.9e-3, 0.0])
    edge_terminal2 = EdgeTerminal.create(
        circuit_cell_with_padstack_def.layout,
        "P2",
        [edge2],
        Net.find_by_name(circuit_cell_with_padstack_def.layout, "NET1"),
    )
    edge_terminal2.reference_layer = "L2"

    return circuit_cell_with_padstack_def
