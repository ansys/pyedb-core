from types import SimpleNamespace

from ansys.api.edb.v1.edb_messages_pb2 import EDBObjMessage
import pytest
from utils.fixtures import *  # noqa

from ansys.edb.core.geometry.point_data import PointData
from ansys.edb.core.geometry.polygon_data import PolygonData
import ansys.edb.core.layout_instance.layout_instance as layout_instance_mod
from ansys.edb.core.layout_instance.layout_obj_instance import LayoutObjInstance


@pytest.fixture
def layout_instance(edb_obj_msg):
    return layout_instance_mod.LayoutInstance(edb_obj_msg)


def _hit(edb_obj_id, is_group_end=False):
    return SimpleNamespace(
        edb_obj=EDBObjMessage(id=edb_obj_id),
        is_partial=False,
        is_end_of_query_results_group=is_group_end,
    )


def _group(start_id, count):
    hits = [_hit(start_id + i) for i in range(count)]
    hits.append(_hit(0, is_group_end=True))
    return hits


def _hits_for_spatial_filter(spatial_filter):
    if spatial_filter is None:
        return _group(1, 4)
    if isinstance(spatial_filter, PointData):
        return _group(101, 2)
    if isinstance(spatial_filter, list):
        all_hits = []
        start_id = 201
        for _ in spatial_filter:
            all_hits.extend(_group(start_id, 2))
            start_id += 10
        return all_hits
    raise ValueError("Unsupported spatial filter fixture value")


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
    mocker,
    mocked_stub,
    layout_instance,
    expected_lengths: int | list[int],
    spatial_filter: PolygonData | PointData | None | list[PolygonData | PointData],
):
    mocker.patch("ansys.edb.core.layout_instance.layout_instance.is_in_memory", return_value=True)
    stub = mocked_stub(layout_instance_mod, layout_instance_mod.LayoutInstance)
    stub.BatchQueryLayoutObjInstances.return_value = SimpleNamespace(
        query_results=_hits_for_spatial_filter(spatial_filter)
    )

    loi_list = layout_instance.query_layout_obj_instances(spatial_filter=spatial_filter)

    stub.BatchQueryLayoutObjInstances.assert_called_once()
    stub.StreamLayoutObjInstancesQuery.assert_not_called()

    assert_loi_list(loi_list, expected_lengths)


@pytest.mark.parametrize(
    ["spatial_filter", "expected_lengths"],
    [
        (None, 4),
        (PointData([0.0, 0.0]), 2),
        ([PointData([0.0, 0.0])], [2]),
        ([PointData([-0.1e-3, 0.0]), PointData([0.1e-3, 0.0])], [2, 2]),
    ],
)
def test_query_layout_obj_instances_stream_path(
    mocker,
    mocked_stub,
    layout_instance,
    expected_lengths: int | list[int],
    spatial_filter: PolygonData | PointData | None | list[PolygonData | PointData],
):
    mocker.patch("ansys.edb.core.layout_instance.layout_instance.is_in_memory", return_value=False)
    stub = mocked_stub(layout_instance_mod, layout_instance_mod.LayoutInstance)
    all_hits = _hits_for_spatial_filter(spatial_filter)
    stub.StreamLayoutObjInstancesQuery.return_value = [SimpleNamespace(query_results=all_hits)]

    loi_list = layout_instance.query_layout_obj_instances(spatial_filter=spatial_filter)

    stub.BatchQueryLayoutObjInstances.assert_not_called()
    stub.StreamLayoutObjInstancesQuery.assert_called_once()

    assert_loi_list(loi_list, expected_lengths)


def assert_loi_list(
    loi_list: list[LayoutObjInstance | list[LayoutObjInstance]], expected_lengths: int | list[int]
):
    """Assert that the given list of layout object instances matches the expected lengths and types.

    Parameters
    ----------
    loi_list : list[LayoutObjInstance | list[LayoutObjInstance]]
        List of layout object instances to check, as returned by :func:`LayoutInstance.query_layout_obj_instances()`.
        Can be a list of layout object instances or a list of lists of layout object instances, depending on whether the
        spatial filter provided to the query was a list.
    expected_lengths : int | list[int]
        The expected length(s) of the list(s) of layout object instances. Can be a single integer if the query was made
        with a non-list spatial filter, or a list of integers if the query was made with a list spatial filter.
    """
    if isinstance(expected_lengths, int):
        assert len(loi_list) == expected_lengths
        assert all(isinstance(loi, LayoutObjInstance) for loi in loi_list)
    else:
        assert len(loi_list) == len(expected_lengths)
        for loi_result, expected_length in zip(loi_list, expected_lengths):
            assert isinstance(loi_result, list)
            assert len(loi_result) == expected_length
            assert all(isinstance(loi, LayoutObjInstance) for loi in loi_result)
