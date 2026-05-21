import pytest

from ansys.edb.core.geometry.point_data import PointData
from ansys.edb.core.geometry.polygon_data import PolygonData
from ansys.edb.core.layout.cell import Cell


def test_query_layout_obj_instances(circuit_cell_with_edge_terminals: Cell):
    loi_list = circuit_cell_with_edge_terminals.layout.layout_instance.query_layout_obj_instances()
    assert len(loi_list) == 4


@pytest.mark.parametrize(
    ["spatial_filter", "expected_lengths"],
    [
        (PointData([0.0, 0.0]), 2),
        ([PointData([-0.1e-3, 0.0]), PointData([0.1e-3, 0.0])], [2, 2]),
    ],
)
def test_query_layout_obj_instances_spatial_filter(
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
    else:
        assert len(loi_list) == len(expected_lengths)
        for loi, expected_length in zip(loi_list, expected_lengths):
            assert len(loi) == expected_length
