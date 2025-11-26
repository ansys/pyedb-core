import pytest

from ansys.edb.core.layout.cell import Cell


@pytest.mark.parametrize(
    ("layer_name", "is_null"), (("L1", False), ("NonExistentLayer", True), ("l1", False))
)
def test_find_by_name(circuit_cell_with_stackup: Cell, is_null: bool, layer_name: str):
    """Test that finding a layer by name returns a correct layer object."""
    layer = circuit_cell_with_stackup.layout.layer_collection.find_by_name(layer_name)
    assert layer is not None and layer.is_null == is_null


def test_tsv_properties(circuit_cell_with_overlapping_stackup: Cell):
    """Test that finding a layer by name returns a correct layer object."""
    layer = circuit_cell_with_overlapping_stackup.layout.layer_collection.find_by_name("V1")
    assert layer is not None and not layer.is_null
    assert not layer.is_tsv
    layer.is_tsv = True
    layer.add_oxide_layers([("0.1um", "silicon_dioxide"), ("25nm", "FR4_epoxy")])
    assert layer.is_tsv
    assert len(layer.oxide_layers) == 2
    assert layer.oxide_layers == [("0.1um", "silicon_dioxide"), ("25nm", "FR4_epoxy")]
