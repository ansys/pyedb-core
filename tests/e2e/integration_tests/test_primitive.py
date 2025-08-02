import pytest

from ansys.edb.core.layout.cell import Cell
from ansys.edb.core.primitive.circle import Circle

# from ansys.edb.core.primitive.primitive import Primitive


def test_primitive_find_by_id(circuit_cell_with_stackup: Cell):
    circle = Circle.create(
        circuit_cell_with_stackup.layout, "L1", None, center_x=0.0, center_y=0.0, radius=5.0e-3
    )
    assert not circle.is_null
    assert circle.id
    found_primitive = Circle.find_by_id(circuit_cell_with_stackup.layout, circle.id)
    assert not found_primitive.is_null
    assert isinstance(found_primitive, Circle)
    assert found_primitive.polygon_data.area() == pytest.approx(
        7.8539816339744830961566084581988e-5
    )

    # below fails as edb_uid is always 0, even if circuit_cell_with_stackup.database.save() is called
    # # circuit_cell_with_stackup.database.save()
    # assert circle.edb_uid
    # found_primitive = Circle.find_by_id(circuit_cell_with_stackup.layout, circle.edb_uid)
    # assert not found_primitive.is_null
    # assert isinstance(found_primitive, Circle)
    # assert found_primitive.polygon_data.area() == pytest.approx(7.8539816339744830961566084581988e-5)

    # what I think ultimately should work, with maybe a call to cast to the concrete type
    # found_primitive = Primitive.find_by_id(circuit_cell_with_stackup.layout, circle.edb_uid)
    # assert not found_primitive.is_null
    # assert isinstance(found_primitive, Circle)
    # assert found_primitive.polygon_data.area() == pytest.approx(7.8539816339744830961566084581988e-5)
