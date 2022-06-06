import ansys.api.edb.v1.term_pb2 as term_pb2
import pytest

import ansys.edb.core.interfaces.grpc.messages as messages
from ansys.edb.core.models.cell.terminals import (
    BoundaryType,
    BundleTerminal,
    HfssPIType,
    PointTerminal,
    SourceTermToGroundType,
    Terminal,
)
from ansys.edb.core.models.port_post_processing_prop import PortPostProcessingProp
from ansys.edb.core.models.rlc import Rlc
from utils.fixtures import *  # noqa
from utils.test_utils import create_edb_obj_msgs, equals


@pytest.fixture
def patch(mocker):
    def _patch(cls):
        mock = mocker.Mock()
        path = f"ansys.edb.core.models.cell.terminals.{cls.__name__}._{cls.__name__}__stub"
        mocker.patch(path, mock)
        return mock

    return _patch


@pytest.fixture
def bundle_terminal(edb_obj_msg):
    return BundleTerminal(edb_obj_msg)


@pytest.fixture
def point_terminal(edb_obj_msg):
    return PointTerminal(edb_obj_msg)


def test_bundle_terminal_create(patch, point_terminal, bundle_terminal, edb_obj_msg):
    mock = patch(BundleTerminal).Create
    mock.return_value = edb_obj_msg

    bt = BundleTerminal.create([point_terminal, bundle_terminal])

    mock.assert_called_once_with(
        messages.bundle_term_terminals_message([point_terminal, bundle_terminal])
    )
    assert isinstance(bt, BundleTerminal)
    assert not bt.is_null()
    assert bt.id == edb_obj_msg.id


@pytest.mark.parametrize(
    "term_type, term_cls",
    [
        (term_pb2.TerminalType.POINT_TERM, PointTerminal),
        (term_pb2.TerminalType.BUNDLE_TERM, BundleTerminal),
    ],
)
def test_bundle_terminal_get_terminals(patch, bundle_terminal, term_type, term_cls):
    get_terminals = patch(BundleTerminal).GetTerminals
    get_terminals.return_value = expected = create_edb_obj_msgs(2)
    get_params = patch(Terminal).GetParams
    get_params.return_value = term_pb2.TermParamsMessage(term_type=term_type)

    terminals = bundle_terminal.terminals
    get_terminals.assert_called_once_with(bundle_terminal.msg)
    get_params.assert_called()

    assert len(terminals) == 2
    for t in terminals:
        assert isinstance(t, term_cls)
    assert sorted([t.id for t in terminals]) == sorted([msg.id for msg in expected])


def test_bundle_terminal_ungroup(patch, bundle_terminal):
    expected = bundle_terminal.msg
    mock = patch(BundleTerminal).Ungroup
    mock.return_value = None

    bundle_terminal.ungroup()
    mock.assert_called_once_with(expected)
    assert bundle_terminal.is_null()


def test_point_terminal_create(patch, layout, net, layer, edb_obj_msg):
    mock = patch(PointTerminal).Create
    mock.return_value = edb_obj_msg

    pt = PointTerminal.create(layout, net, layer, "test-point-term", 1, 2)

    mock.assert_called_once_with(
        messages.point_term_creation_message(layout, net, layer, "test-point-term", 1, 2)
    )
    assert isinstance(pt, PointTerminal)
    assert not pt.is_null()
    assert pt.id == edb_obj_msg.id


def test_point_terminal_get_params(patch, point_terminal, layer):
    point = (1e-9, 2e-9)
    mock = patch(PointTerminal).GetParameters
    mock.return_value = messages.point_term_params_message(layer, point)

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
    mock = patch(PointTerminal).SetParameters
    mock.return_value = messages.bool_message(success)

    point_terminal.set_params(layer_ref, point)

    mock.assert_called_once_with(
        messages.point_term_set_params_message(point_terminal, layer_ref, point)
    )


def test_terminal_get_params(patch, point_terminal, bundle_terminal, layer):
    mock = patch(Terminal)
    mock.GetParams.return_value = term_pb2.TermParamsMessage(
        term_type=term_pb2.TerminalType.POINT_TERM,
        boundary_type=BoundaryType.RLC.value,
        term_to_ground=SourceTermToGroundType.POSITIVE.value,
        hfss_pi_type=HfssPIType.COAXIAL_SHORTENED.value,
        ref_layer=layer.msg,
        bundle_term=bundle_terminal.msg,
        is_interface=True,
        is_reference=False,
        is_auto_port=False,
        is_circuit_port=False,
        use_ref_from_hierarchy=True,
        name="name",
        impedance=messages.value_message(50),
        source_amplitude=messages.value_message(10),
        source_phase=messages.value_message(5),
        s_param_model="model",
        rlc=messages.rlc_message(Rlc(r=10, r_enabled=True)),
        port_post_processing_prop=messages.port_post_processing_prop_message(
            PortPostProcessingProp(renormalization_impedance=50, do_renormalize=True)
        ),
    )

    assert point_terminal.boundary_type == BoundaryType.RLC
    assert point_terminal.term_to_ground == SourceTermToGroundType.POSITIVE
    assert point_terminal.hfss_pi_type == HfssPIType.COAXIAL_SHORTENED
    assert point_terminal.reference_terminal is None
    assert equals(point_terminal.reference_layer, layer)
    assert equals(point_terminal.bundle_terminal, bundle_terminal)
    assert point_terminal.is_interface_terminal
    assert not point_terminal.is_reference_terminal
    assert not point_terminal.is_auto_port
    assert not point_terminal.is_circuit_port
    assert point_terminal.use_reference_from_hierarchy
    assert point_terminal.name == "name"
    assert point_terminal.impedance == 50.0
    assert point_terminal.source_amplitude == 10.0
    assert point_terminal.source_phase == 5.0
    assert point_terminal.model == "model"
    rlc = point_terminal.rlc_boundary_parameters
    assert rlc is not None
    assert rlc.r == 10.0
    assert rlc.r_enabled and rlc.is_parallel
    assert not rlc.l_enabled and not rlc.c_enabled
    prop = point_terminal.port_post_processing_prop
    assert prop is not None
    assert prop.renormalization_impedance == 50.0
    assert prop.do_renormalize
    assert not prop.do_deembed and not prop.do_deembed_gap_l

    assert mock.GetParams.call_count == 18


def test_terminal_set_params(patch, point_terminal, bundle_terminal, layer):
    mock = patch(Terminal).SetParams
    mock.return_value = None

    point_terminal.boundary_type = BoundaryType.RLC
    point_terminal.term_to_ground = SourceTermToGroundType.NO_GROUND
    point_terminal.hfss_pi_type = HfssPIType.COAXIAL_OPEN
    point_terminal.is_circuit_port = True
    point_terminal.is_auto_port = False
    point_terminal.use_reference_from_hierarchy = True
    point_terminal.name = "new-name"
    point_terminal.reference_terminal = None
    point_terminal.reference_terminal = bundle_terminal
    point_terminal.reference_layer = None
    point_terminal.reference_layer = layer
    point_terminal.reference_layer = layer, "context1"
    point_terminal.impedance = 50
    point_terminal.source_amplitude = 10
    point_terminal.source_phase = 5
    point_terminal.model = "new-model"
    point_terminal.rlc_boundary_parameters = Rlc(r=5, l=10, c=15, r_enabled=True, c_enabled=True)
    point_terminal.port_post_processing_prop = PortPostProcessingProp(
        voltage_magnitude=10, renormalization_impedance=50, do_renormalize=True
    )
    assert mock.call_count == 18
