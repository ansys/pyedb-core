import math

from ansys.api.edb.v1 import edb_messages_pb2, point_data_pb2
from google.protobuf import wrappers_pb2
import pytest
from utils.fixtures import *  # noqa

from ansys.edb.core import geometry, utility

@pytest.mark.parametrize(
    "args, kwargs, expect_call",
    [
        [[(1, 1), (2, 2)], {}, False],
        [[(1, 1), (2, 2)], {"height": 3}, False],
        [[(1, 1), (2, 2)], {"radius": 3, "direction": "cw", "is_big": False}, True],
        [[(1, 1), (2, 2)], {"center": (2, 1), "direction": "cw"}, True],
        [[(1, 1), (2, 2)], {"thru": (1.5, 1.5)}, True],
        [[(1, 1), (2, 2)], {}, False],
    ],
)
def test_height(mocked_stub, args, kwargs, expect_call):
    mock = mocked_stub(geometry.arc_data, geometry.arc_data.ArcData).GetHeight
    mock.return_value = wrappers_pb2.FloatValue(value=2)
    _ = geometry.ArcData(*args, **kwargs).height

    if expect_call:
        mock.assert_called_once()
    else:
        mock.assert_not_called()


test_arcs = [
    geometry.ArcData((1, 1), (2, 2)),
    geometry.ArcData((1, 1), (1 - 1e-10, 1 + 1e-10)),
    geometry.ArcData((1, 1), (1, 1), height=1e9),
    geometry.ArcData((1, 1), (1 - 1e-8, 1 + 1e-8)),
]


@pytest.mark.parametrize(
    "arc, tol, is_segment", zip(test_arcs, [0, 1e-9, 1e-9, 1e-9], [True, True, False, True])
)
def test_is_segment(arc, tol, is_segment):
    assert arc.is_segment(tol) == is_segment


@pytest.mark.parametrize(
    "arc, tol, is_point", zip(test_arcs, [0, 1e-9, 1e-9, 1e-9], [False, True, False, False])
)
def test_is_point(arc, tol, is_point):
    assert arc.is_point(tol) == is_point


def test_center(mocked_stub):
    mock = mocked_stub(geometry, geometry.ArcData).GetCenter
    mock.return_value = point_data_pb2.PointMessage(
        x=edb_messages_pb2.ValueMessage(constant=edb_messages_pb2.ComplexMessage(real=2)),
        y=edb_messages_pb2.ValueMessage(constant=edb_messages_pb2.ComplexMessage(real=2)),
    )
    arc = geometry.ArcData((2, 0), (0, 2), height=2.0)
    center = arc.center
    mock.assert_called_once()
    assert center.x == 2
    assert center.y == 2


def test_bbox(mocked_stub):
    mock = mocked_stub(geometry, geometry.ArcData)
    mock.GetBoundingBox.return_value = point_data_pb2.BoxMessage(
        lower_left=point_data_pb2.PointMessage(
            x=edb_messages_pb2.ValueMessage(constant=edb_messages_pb2.ComplexMessage(real=0)),
            y=edb_messages_pb2.ValueMessage(constant=edb_messages_pb2.ComplexMessage(real=0)),
        ),
        upper_right=point_data_pb2.PointMessage(
            x=edb_messages_pb2.ValueMessage(constant=edb_messages_pb2.ComplexMessage(real=3)),
            y=edb_messages_pb2.ValueMessage(constant=edb_messages_pb2.ComplexMessage(real=4)),
        ),
    )
    arc = geometry.ArcData((0, 0), (3, 4))
    bbox = arc.bbox
    assert len(bbox) == 4
    assert bbox.points == geometry.PolygonData(lower_left=(0, 0), upper_right=(3, 4)).points


@pytest.mark.parametrize(
    "height, is_big", [[0, False], [2.4, False], [2.6, True], [-2.4, False], [-2.6, True]]
)
def test_is_big(height, is_big):
    arc = geometry.ArcData(start=(0, 0), end=(3, 4), height=height)
    assert utility.Value(arc.start.distance(arc.end)).equals(5, 1e-6)
    assert arc.is_big() == is_big


@pytest.mark.parametrize(
    "expect_call, height, arc, length",
    [
        [False, 0, geometry.ArcData(start=(0, 0), end=(3, 4), height=0), 5],
        [
            True,
            1,
            geometry.ArcData(start=(0, 0), end=(3, 4), radius=1, direction="cw", is_big=False),
            math.acos(1) / 4,
        ],
    ],
)
def test_length(mocked_stub, expect_call, height, arc, length):
    mock = mocked_stub(geometry, geometry.ArcData)
    mock.GetHeight.return_value = wrappers_pb2.FloatValue(value=1)
    mock.GetRadius.return_value = wrappers_pb2.FloatValue(value=2)
    mock.GetAngle.return_value = wrappers_pb2.FloatValue(value=math.acos(1) / 8)

    assert utility.Value(arc.length).equals(length, 1e-6)
    if expect_call:
        mock.GetRadius.assert_called_once()
        mock.GetAngle.assert_called_once()
    else:
        mock.GetRadius.assert_not_called()
        mock.GetAngle.assert_not_called()


def test_angle(mocked_stub):
    mock = mocked_stub(geometry, geometry.ArcData)
    mock.GetAngle.return_value = wrappers_pb2.FloatValue(value=0.5)
    arc = geometry.ArcData(start=(0, 0), end=(3, 4))

    assert arc.angle() == 0.5
    mock.GetAngle.assert_called_once()

    arc1 = geometry.ArcData(start=(0, 0), end=(3, 4))
    arc2 = geometry.ArcData(start=(0, 0), end=(-3, -4))
    arc1.angle(arc2)


@pytest.mark.parametrize(
    "arc, tangent",
    [
        [geometry.ArcData(start=(0, 0), end=(3, 4)), (3, 4)],
        [geometry.ArcData(start=(0, 0), end=(3, 4), height=-0.1), (-4, 3)],
        [geometry.ArcData(start=(0, 0), end=(3, 4), height=+0.1), (4, -3)],
    ],
)
def test_tangent_at(mocked_stub, arc, tangent):
    mock = mocked_stub(geometry, geometry.ArcData)
    mock.GetCenter.return_value = point_data_pb2.PointMessage(
        x=edb_messages_pb2.ValueMessage(constant=edb_messages_pb2.ComplexMessage(real=0)),
        y=edb_messages_pb2.ValueMessage(constant=edb_messages_pb2.ComplexMessage(real=0)),
    )
    point = (3, 4)
    assert arc.tangent_at(point) == tangent
