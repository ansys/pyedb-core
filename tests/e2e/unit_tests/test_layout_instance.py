import pytest

from ansys.edb.core.geometry.point_data import PointData
from ansys.edb.core.geometry.polygon_data import PolygonData
from ansys.edb.core.layout.cell import Cell
from ansys.edb.core.layout_instance.layout_obj_instance import LayoutObjInstance


@pytest.mark.parametrize(
    ["spatial_filter", "expected_lengths"],
    [
        (None, 4),
        (PointData([0.0, 0.0]), 2),
        ([PointData([0.0, 0.0])], [2]),
        ([PointData([-0.1e-3, 0.0]), PointData([0.1e-3, 0.0])], [2, 2]),
    ],
)
def test_query_layout_obj_instances(
    circuit_cell_with_edge_terminals: Cell,
    expected_lengths: int | list[int],
    spatial_filter: PolygonData | PointData | None | list[PolygonData | PointData],
):
    layout = circuit_cell_with_edge_terminals.layout
    loi_list = layout.layout_instance.query_layout_obj_instances(
        spatial_filter=spatial_filter,
    )
    if isinstance(expected_lengths, int):
        assert len(loi_list) == expected_lengths
        assert all(isinstance(loi, LayoutObjInstance) for loi in loi_list)
    else:
        assert len(loi_list) == len(expected_lengths)
        for loi_result, expected_length in zip(loi_list, expected_lengths):
            assert isinstance(loi_result, list)
            assert len(loi_result) == expected_length
            assert all(isinstance(loi, LayoutObjInstance) for loi in loi_result)
