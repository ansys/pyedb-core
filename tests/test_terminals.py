import pytest

import ansys.edb.core.interfaces.grpc.messages as messages
from ansys.edb.core.models.cell.layer import Layer
from ansys.edb.core.models.cell.terminals import PointTerminal
from utils.fixtures import *  # noqa
from utils.test_utils import patch_stub


@pytest.fixture
def patch(mocker):
    def _patch(method_name, expected_response):
        return patch_stub(
            "ansys.edb.core.models.cell.terminals.get_point_terminal_stub",
            mocker,
            method_name,
            expected_response,
        )

    return _patch


@pytest.fixture
def point_terminal(edb_obj_msg):
    return PointTerminal(edb_obj_msg)


def test_create(patch, layout, net, layer, edb_obj_msg):
    mock = patch("Create", edb_obj_msg)

    pt = PointTerminal.create(layout, net, layer, "test-point-term", 1, 2)

    mock.assert_called_once_with(
        messages.point_term_creation_message(layout, net, layer, "test-point-term", 1, 2)
    )
    assert isinstance(pt, PointTerminal)
    assert not pt.is_null()
    assert pt.id == edb_obj_msg.id


def test_get_params(patch, point_terminal, layer):
    point = (1e-9, 2e-9)
    mock = patch("GetParameters", messages.point_term_params_message(layer, point))

    res = point_terminal.get_params()

    mock.assert_called_once_with(point_terminal.msg)
    assert isinstance(res, tuple)
    assert len(res) == 2
    assert isinstance(res[0], Layer)
    assert isinstance(res[1], tuple)
    assert res[0].id == layer.id
    assert res[1] == point


@pytest.mark.parametrize(
    "layer_ref, point, success",
    [
        ("layer", (1e-9, 2e-9), True),  # Layer instance fixture & float & success
        ("random_str", (5, 6), False),  # Layer str name fixture & int   & fail
    ],
    indirect=["layer_ref"],
)
def test_set_params(patch, point_terminal, layer_ref, point, success):
    mock = patch("SetParameters", messages.bool_message(success))

    res = point_terminal.set_params(layer_ref, point)

    mock.assert_called_once_with(
        messages.point_term_set_params_message(point_terminal, layer_ref, point)
    )
    assert res == success
