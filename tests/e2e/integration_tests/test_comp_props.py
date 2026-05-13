import os
from pathlib import Path

import pytest

from ansys.edb.core.database import Database
from ansys.edb.core.definition.component_def import ComponentDef
from ansys.edb.core.definition.component_pin import ComponentPin
from ansys.edb.core.definition.die_property import DieOrientation, DieType
from ansys.edb.core.definition.ic_component_property import ICComponentProperty
from ansys.edb.core.definition.padstack_def import PadstackDef
from ansys.edb.core.definition.padstack_def_data import PadGeometryType, PadstackDefData, PadType
from ansys.edb.core.definition.solder_ball_property import SolderballShape
from ansys.edb.core.hierarchy.component_group import ComponentGroup, ComponentType
from ansys.edb.core.layer.layer import LayerType
from ansys.edb.core.layer.layer_collection import LayerCollectionMode
from ansys.edb.core.layer.stackup_layer import StackupLayer
from ansys.edb.core.layer.via_layer import ViaLayer
from ansys.edb.core.layout.cell import Cell, CellType
from ansys.edb.core.net.net import Net
from ansys.edb.core.primitive.padstack_instance import PadstackInstance
from ansys.edb.core.session import session


@pytest.mark.parametrize("_n", range(1000))
def test_comp_props(_n: int, tmp_path: Path):
    worker_name = os.environ.get("PYTEST_XDIST_WORKER", None)
    port_num = None
    if worker_name is not None:
        # use a per-worker port to avoid conflicts when running tests in parallel with pytest-xdist
        port_num = int(worker_name.strip("gw")) + 30051 + 1970
    with session(os.environ["ANSYSEM_EDB_EXE_DIR"], port_num):
        db_path = (tmp_path / "output.aedb").as_posix()
        db = Database.create(db_path)
        try:
            cell = Cell.create(db, CellType.CIRCUIT_CELL, "output")

            layers = [
                StackupLayer.create("D1", LayerType.DIELECTRIC_LAYER, 150e-6, 0.0, "FR4_epoxy"),
                StackupLayer.create("L1", LayerType.CONDUCTING_LAYER, 25e-6, 125e-6, "copper"),
                StackupLayer.create("L2", LayerType.CONDUCTING_LAYER, 25e-6, 0.0, "copper"),
                ViaLayer.create("V1", "L2", "L1", "copper"),
            ]
            layout = cell.layout
            layout.layer_collection.mode = LayerCollectionMode.OVERLAPPING
            for layer in layers:
                layout.layer_collection.add_stackup_layer_at_elevation(layer)

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
                    PadGeometryType.PADGEOMTYPE_SQUARE,
                    [70e-6],
                )
                padstack_def_data.set_pad_parameters(
                    name,
                    PadType.ANTI_PAD,
                    0.0,
                    0.0,
                    0.0,
                    PadGeometryType.PADGEOMTYPE_SQUARE,
                    [100e-6],
                )
            padstack_def = PadstackDef.create(db, "PAD070")
            padstack_def.data = padstack_def_data
            comp_def = ComponentDef.create(cell.database, "IC_PART", None)
            for i in range(4):
                pin_def = ComponentPin.create(comp_def, f"{i+1}")
                assert not pin_def.is_null

            locations = [
                [0.0, 0.0],
                [150e-6, 0.0],
                [0.0, 150e-6],
                [150e-6, 150e-6],
            ]
            ref_des = "U1"
            create_component(cell, layout, padstack_def, comp_def, locations, ref_des)
            create_component(
                cell,
                layout,
                padstack_def,
                comp_def,
                [[200e-6, 0.0], [350e-6, 0.0], [200e-6, 150e-6], [350e-6, 150e-6]],
                "U2",
            )
            group = ComponentGroup.find(layout, ref_des)
            group.component_type = ComponentType.IC
            component_property = ICComponentProperty(group.component_property.clone().msg)
            # component_property = group.component_property
            die_property = component_property.die_property
            die_property.die_type = DieType.FLIPCHIP
            die_property.die_orientation = DieOrientation.CHIP_DOWN
            component_property.die_property = die_property
            group.component_property = component_property
            component_property = ICComponentProperty(group.component_property.clone().msg)
            solder_ball_property = component_property.solder_ball_property
            solder_ball_property.shape = SolderballShape.SOLDERBALL_CYLINDER
            solder_ball_property.set_diameter(250e-6, 0.0)
            solder_ball_property.height = 150e-6
            solder_ball_property.material_name = "solder"
            component_property.solder_ball_property = solder_ball_property
            group.component_property = component_property

            group = ComponentGroup.find(layout, "U2")
            group.component_type = ComponentType.IC
            component_property = ICComponentProperty(group.component_property.clone().msg)
            # component_property = group.component_property
            die_property = component_property.die_property
            die_property.die_type = DieType.FLIPCHIP
            die_property.die_orientation = DieOrientation.CHIP_UP
            component_property.die_property = die_property
            group.component_property = component_property
            component_property = ICComponentProperty(group.component_property.clone().msg)
            solder_ball_property = component_property.solder_ball_property
            solder_ball_property.shape = SolderballShape.SOLDERBALL_CYLINDER
            solder_ball_property.set_diameter(300e-6, 0.0)
            solder_ball_property.height = 150e-6
            solder_ball_property.material_name = "copper"
            component_property.solder_ball_property = solder_ball_property
            group.component_property = component_property

            db.save()

            _assert_comp_props(ref_des, db)
        finally:
            db.close()

        # new_db = Database.open(db_path, True)
        # try:
        #     _assert_comp_props(ref_des, new_db)
        # finally:
        #     new_db.close()


def _assert_comp_props(ref_des, new_db):
    new_layout = new_db.top_circuit_cells[0].layout
    new_component = ComponentGroup.find(new_layout, ref_des)
    assert not new_component.is_null
    assert new_component.component_type == ComponentType.IC
    assert new_component.component_property.die_property.die_type == DieType.FLIPCHIP
    assert new_component.component_property.die_property.die_orientation == DieOrientation.CHIP_DOWN
    assert (
        new_component.component_property.solder_ball_property.shape
        == SolderballShape.SOLDERBALL_CYLINDER
    )
    assert new_component.component_property.solder_ball_property.get_diameter()[0].double == 250e-6
    assert new_component.component_property.solder_ball_property.height == 150e-6
    assert new_component.component_property.solder_ball_property.material_name == "solder"


def create_component(cell, layout, padstack_def, comp_def, locations, ref_des):
    layer1 = layout.layer_collection.find_by_name("L1")
    assert not layer1.is_null
    instances = [
        PadstackInstance.create(
            layout,
            Net.find_by_name(layout, Net.no_net_name),
            f"{i+1}",
            padstack_def,
            *locations[i],
            0.0,
            top_layer=layer1,
            bottom_layer=layer1,
        )
        for i in range(len(locations))
    ]
    group = ComponentGroup.create(layout, ref_des, "IC_PART")
    for instance in instances:
        assert not instance.is_null
        instance.is_layout_pin = True
        group.add_member(instance)
