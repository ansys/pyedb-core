# import pytest
# import settings

# from ansys.edb.database import Database
# from ansys.edb.definition import PadGeometryType, PadstackDef, PadstackDefData, PadType
# from ansys.edb.layer.layer import LayerType, StackupLayer
# from ansys.edb.layout import Cell, CellType
# from ansys.edb.session import session


# @pytest.fixture
# def test_session():
#     with session(settings.configs.get("RPC_SERVER_ROOT"), 50051):
#         yield


# @pytest.fixture
# def new_database_path(tmp_path):
#     return str(tmp_path / "test.aedb")


# @pytest.fixture
# def new_database(test_session, new_database_path):
#     db = Database.create(new_database_path)
#     yield db
#     db.close()


# @pytest.fixture
# def circuit_cell(new_database):
#     return Cell.create(new_database, CellType.CIRCUIT_CELL, "circuit_cell")


# @pytest.fixture()
# def circuit_cell_with_stackup(circuit_cell: Cell):
#     layers = [
#         StackupLayer.create("L1", LayerType.CONDUCTING_LAYER, 25e-6, 0.0, "copper"),
#         StackupLayer.create("D1", LayerType.DIELECTRIC_LAYER, 100e-6, 0.0, "FR4_epoxy"),
#         StackupLayer.create("L2", LayerType.CONDUCTING_LAYER, 25e-6, 0.0, "copper"),
#     ]
#     for layer in layers:
#         circuit_cell.layout.layer_collection.add_layer_bottom(layer)
#     yield circuit_cell


# @pytest.fixture()
# def circuit_cell_with_padstack_def(circuit_cell_with_stackup: Cell):
#     db = circuit_cell_with_stackup.database
#     padstack_def_data = PadstackDefData.create()
#     layer_names = ["Start", "Default", "Stop"]
#     padstack_def_data.add_layers(layer_names)
#     for name in layer_names:
#         padstack_def_data.set_pad_parameters(
#             name,
#             PadType.REGULAR_PAD,
#             0.0,
#             0.0,
#             0.0,
#             PadGeometryType.PADGEOMTYPE_CIRCLE,
#             [70e-6],
#         )
#         padstack_def_data.set_pad_parameters(
#             name,
#             PadType.ANTI_PAD,
#             0.0,
#             0.0,
#             0.0,
#             PadGeometryType.PADGEOMTYPE_CIRCLE,
#             [100e-6],
#         )
#     padstack_def_data.set_hole_parameters(
#         0.0, 0.0, 0.0, PadGeometryType.PADGEOMTYPE_CIRCLE, [50e-6]
#     )
#     padstack_def = PadstackDef.create(db, "VIA050070100")
#     padstack_def.data = padstack_def_data
#     yield circuit_cell_with_stackup
