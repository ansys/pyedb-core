from ansys.edb.hierarchy.component_group import ComponentGroup
from ansys.edb.layout.cell import Cell


def test_create_component_group(circuit_cell_with_two_pin_component: Cell):
    component = ComponentGroup.find(circuit_cell_with_two_pin_component.layout, "C1")
    assert not component.is_null
    assert component.component_def.name == "PAD01005"
    assert len(component.members) == 2
