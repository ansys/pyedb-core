import pytest

from ansys.edb.core.layout.cell import Cell


@pytest.mark.parametrize(("layer_name", "is_null"), (("L1", False), ("NonExistentLayer", True)))
def test_find_by_name(circuit_cell_with_stackup: Cell, is_null: bool, layer_name: str):
    """Test that finding a layer by name returns a correct layer object."""
    layer = circuit_cell_with_stackup.layout.layer_collection.find_by_name(layer_name)
    assert layer is not None and layer.is_null == is_null
