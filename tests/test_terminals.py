import pytest

import ansys.edb.core.interfaces.grpc.messages as messages
from ansys.edb.core.models.cell.layer import Layer
from ansys.edb.core.models.cell.terminals import BundleTerminal, PointTerminal, Terminal
from utils.fixtures import *  # noqa
from utils.test_utils import create_edb_obj_msgs, patch_stub


@pytest.fixture
def patch(mocker):
    def _patch(terminal_type, method_name, expected_response):
        return patch_stub(
            f"ansys.edb.core.models.cell.terminals.get_{terminal_type}_stub",
            mocker,
            method_name,
            expected_response,
        )

    return _patch


@pytest.fixture
def bundle_terminal(edb_obj_msg):
    return BundleTerminal(edb_obj_msg)


@pytest.fixture
def point_terminal(edb_obj_msg):
    return PointTerminal(edb_obj_msg)


def test_bundle_terminal_create(patch, point_terminal, bundle_terminal, edb_obj_msg):
    mock = patch("bundle_terminal", "Create", edb_obj_msg)

    bt = BundleTerminal.create([point_terminal, bundle_terminal])

    mock.assert_called_once_with(
        messages.bundle_term_terminals_message([point_terminal, bundle_terminal])
    )
    assert isinstance(bt, BundleTerminal)
    assert not bt.is_null()
    assert bt.id == edb_obj_msg.id


def test_bundle_terminal_get_terminals(patch, bundle_terminal):
    expected = create_edb_obj_msgs(2)
    mock = patch("bundle_terminal", "GetTerminals", expected)

    terminals = bundle_terminal.terminals
    mock.assert_called_once_with(bundle_terminal.msg)
    assert len(terminals) == 2
    for t in terminals:
        assert isinstance(t, Terminal)
    assert sorted([t.id for t in terminals]) == sorted([msg.id for msg in expected])


def test_bundle_terminal_ungroup(patch, bundle_terminal):
    expected = bundle_terminal.msg
    mock = patch("bundle_terminal", "Ungroup", None)

    bundle_terminal.ungroup()
    mock.assert_called_once_with(expected)
    assert bundle_terminal.is_null()


def test_point_terminal_create(patch, layout, net, layer, edb_obj_msg):
    mock = patch("point_terminal", "Create", edb_obj_msg)

    pt = PointTerminal.create(layout, net, layer, "test-point-term", 1, 2)

    mock.assert_called_once_with(
        messages.point_term_creation_message(layout, net, layer, "test-point-term", 1, 2)
    )
    assert isinstance(pt, PointTerminal)
    assert not pt.is_null()
    assert pt.id == edb_obj_msg.id


def test_point_terminal_get_params(patch, point_terminal, layer):
    point = (1e-9, 2e-9)
    mock = patch(
        "point_terminal", "GetParameters", messages.point_term_params_message(layer, point)
    )

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
def test_point_terminal_set_params(patch, point_terminal, layer_ref, point, success):
    mock = patch("point_terminal", "SetParameters", messages.bool_message(success))

    point_terminal.set_params(layer_ref, point)

    mock.assert_called_once_with(
        messages.point_term_set_params_message(point_terminal, layer_ref, point)
    )
