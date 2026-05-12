from pathlib import Path
import shutil

import pytest

from ansys.edb.core.database import Database
from ansys.edb.core.definition.component_def import ComponentDef
from ansys.edb.core.definition.component_pin import ComponentPin
from ansys.edb.core.definition.die_property import DieOrientation, DieType
from ansys.edb.core.definition.ic_component_property import ICComponentProperty  # noqa: F401
from ansys.edb.core.definition.padstack_def import PadstackDef
from ansys.edb.core.hierarchy.component_group import ComponentGroup, ComponentType
from ansys.edb.core.layout.cell import Cell
from ansys.edb.core.net.net import Net
from ansys.edb.core.primitive.padstack_instance import PadstackInstance


@pytest.fixture
def circuit_cell_with_ic_component(circuit_cell_with_padstack_def: Cell):
    layout = circuit_cell_with_padstack_def.layout
    locations = [
        [0.0, 0.0],
        [150e-6, 0.0],
        [0.0, 150e-6],
        [150e-6, 150e-6],
    ]
    padstack_def = PadstackDef.find_by_name(circuit_cell_with_padstack_def.database, "VIA050070100")
    circuit_cell_with_padstack_def.database.save()
    layer1 = layout.layer_collection.find_by_name("L1")
    assert not layer1.is_null
    instances = [
        PadstackInstance.create(
            layout,
            Net.no_net_name,
            f"{i+1}",
            padstack_def,
            *locations[i],
            0.0,
            top_layer=layer1,
            bottom_layer=layer1,
        )
        for i in range(len(locations))
    ]
    comp_def = ComponentDef.create(circuit_cell_with_padstack_def.database, "IC_PART", None)
    for i in range(4):
        pin_def = ComponentPin.create(comp_def, f"{i+1}")
        assert not pin_def.is_null
    group = ComponentGroup.create(layout, "U1", "IC_PART")
    for instance in instances:
        assert not instance.is_null
        instance.is_layout_pin = True
        group.add_member(instance)
    group.component_type = ComponentType.IC
    # component_property = ICComponentProperty(group.component_property.clone().msg)
    component_property = group.component_property
    die_property = component_property.die_property
    die_property.die_type = DieType.FLIPCHIP
    die_property.die_orientation = DieOrientation.CHIP_DOWN
    component_property.die_property = die_property
    group.component_property = component_property
    yield circuit_cell_with_padstack_def


def test_ic_component(circuit_cell_with_ic_component: Cell, tmp_path: Path):
    """Test that finding a layer by name returns a correct layer object."""
    layout = circuit_cell_with_ic_component.layout
    component = ComponentGroup.find(layout, "U1")
    assert component.component_property.die_property.die_type == DieType.FLIPCHIP
    assert component.component_property.die_property.die_orientation == DieOrientation.CHIP_DOWN
    circuit_cell_with_ic_component.database.save()
    old_aedb_folder = tmp_path / "test.aedb"
    new_aedb_folder = tmp_path / "new.aedb"
    shutil.copytree(old_aedb_folder, new_aedb_folder)
    new_db = Database.open(new_aedb_folder.as_posix(), True)
    try:
        new_layout = new_db.top_circuit_cells[0].layout
        new_component = ComponentGroup.find(new_layout, "U1")
        assert not new_component.is_null
        assert new_component.component_type == ComponentType.IC
        assert new_component.component_property.die_property.die_type == DieType.FLIPCHIP
        assert (
            new_component.component_property.die_property.die_orientation
            == DieOrientation.CHIP_DOWN
        )
    finally:
        new_db.close()
