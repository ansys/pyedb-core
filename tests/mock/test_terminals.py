import ansys.api.edb.v1.layer_pb2 as layer_pb2
import ansys.api.edb.v1.term_pb2 as term_pb2
from utils.fixtures import *  # noqa
from utils.test_utils import create_edb_obj_collection_msg, equals

from ansys.edb.core.geometry.point_data import PointData
from ansys.edb.core.inner import messages
from ansys.edb.core.layer import layer as layer_api
import ansys.edb.core.terminal.bundle_terminal as bundle_terminal_mod
import ansys.edb.core.terminal.point_terminal as point_terminal_mod
import ansys.edb.core.terminal.terminal as terminal_mod
from ansys.edb.core.utility.port_post_processing_prop import PortPostProcessingProp
from ansys.edb.core.utility.rlc import Rlc


@pytest.fixture
def patch(mocker):
    def _patch(cls):
        mock = mocker.Mock()
        path = f"ansys.edb.core.terminal.terminals.{cls.__name__}._{cls.__name__}__stub"
        mocker.patch(path, mock)
        return mock

    return _patch


@pytest.fixture
def bundle_terminal(edb_obj_msg):
    return bundle_terminal_mod.BundleTerminal(edb_obj_msg)


@pytest.fixture
def point_terminal(edb_obj_msg):
    return point_terminal_mod.PointTerminal(edb_obj_msg)


@pytest.fixture
def lyr_type_mock(mocked_stub):
    lyr_mock = mocked_stub(layer_api, layer_api.Layer)
    lyr_mock.GetLayerType.return_value = layer_pb2.LayerTypeMessage(
        type=layer_api.LayerType.USER_LAYER.value
    )
    return lyr_mock


def test_bundle_terminal_create(mocked_stub, point_terminal, bundle_terminal, edb_obj_msg):
    mock = mocked_stub(bundle_terminal_mod, bundle_terminal_mod.BundleTerminal).Create
    mock.return_value = edb_obj_msg

    bt = bundle_terminal_mod.BundleTerminal.create([point_terminal, bundle_terminal])

    mock.assert_called_once_with(
        messages.edb_obj_collection_message([point_terminal, bundle_terminal])
    )
    assert isinstance(bt, bundle_terminal_mod.BundleTerminal)
    assert not bt.is_null
    assert bt.id == edb_obj_msg.id


@pytest.mark.parametrize(
    "term_type, term_cls",
    [
        (term_pb2.TerminalType.POINT_TERM, point_terminal_mod.PointTerminal),
        (term_pb2.TerminalType.BUNDLE_TERM, bundle_terminal_mod.BundleTerminal),
    ],
)
def test_bundle_terminal_get_terminals(mocked_stub, bundle_terminal, term_type, term_cls):
    get_terminals = mocked_stub(
        bundle_terminal_mod, bundle_terminal_mod.BundleTerminal
    ).GetTerminals
    get_terminals.return_value = expected = create_edb_obj_collection_msg(2)
    get_params = mocked_stub(terminal_mod, terminal_mod.Terminal).GetParams
    get_params.return_value = term_pb2.TermParamsMessage(term_type=term_type)

    terms = bundle_terminal.terminals
    get_terminals.assert_called_once_with(bundle_terminal.msg)
    get_params.assert_called()

    assert len(terms) == 2
    for t in terms:
        assert isinstance(t, term_cls)
    assert sorted([t.id for t in terms]) == sorted([msg.id for msg in expected.items])


def test_bundle_terminal_ungroup(mocked_stub, bundle_terminal):
    expected = bundle_terminal.msg
    mock = mocked_stub(bundle_terminal_mod, bundle_terminal_mod.BundleTerminal).Ungroup
    mock.return_value = None

    bundle_terminal.ungroup()
    mock.assert_called_once_with(expected)
    assert bundle_terminal.is_null


def test_point_terminal_create(mocked_stub, layout, net, layer, edb_obj_msg):
    mock = mocked_stub(point_terminal_mod, point_terminal_mod.PointTerminal).Create
    mock.return_value = edb_obj_msg

    pt = point_terminal_mod.PointTerminal.create(layout, net, layer, "test-point-term", (1, 2))

    mock.assert_called_once_with(
        messages.point_term_creation_message(layout, net, layer, "test-point-term", (1, 2))
    )
    assert isinstance(pt, point_terminal_mod.PointTerminal)
    assert not pt.is_null
    assert pt.id == edb_obj_msg.id


def test_point_terminal_get_params(mocked_stub, point_terminal, layer, lyr_type_mock):
    point = (1e-9, 2e-9)
    mock = mocked_stub(point_terminal_mod, point_terminal_mod.PointTerminal).GetParameters
    mock.return_value = messages.point_term_params_message(layer, point)

    res = point_terminal.params

    mock.assert_called_once_with(point_terminal.msg)
    assert isinstance(res, tuple)
    assert len(res) == 2
    assert isinstance(res[0], Layer)
    assert isinstance(res[1], PointData)
    assert res[0].id == layer.id
    assert res[1].x == point[0]
    assert res[1].y == point[1]


@pytest.mark.parametrize(
    "layer_ref, point, success",
    [
        ("layer", (1e-9, 2e-9), True),  # Layer instance fixture & float & success
        ("random_str", (5, 6), False),  # Layer str name fixture & int   & fail
    ],
    indirect=["layer_ref"],
)
def test_point_terminal_set_params(mocked_stub, point_terminal, layer_ref, point, success):
    mock = mocked_stub(point_terminal_mod, point_terminal_mod.PointTerminal).SetParameters
    mock.return_value = messages.bool_message(success)

    point_terminal.params = (layer_ref, point)

    mock.assert_called_once_with(
        messages.point_term_set_params_message(point_terminal, layer_ref, point)
    )


def test_terminal_get_params(mocked_stub, point_terminal, bundle_terminal, layer, lyr_type_mock):
    mock = mocked_stub(terminal_mod, terminal_mod.Terminal)
    mock.GetParams.return_value = term_pb2.TermParamsMessage(
        term_type=term_pb2.TerminalType.POINT_TERM,
        boundary_type=terminal_mod.BoundaryType.RLC.value,
        term_to_ground=terminal_mod.SourceTermToGroundType.POSITIVE.value,
        hfss_pi_type=terminal_mod.HfssPIType.COAXIAL_SHORTENED.value,
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

    assert point_terminal.boundary_type == terminal_mod.BoundaryType.RLC
    assert point_terminal.term_to_ground == terminal_mod.SourceTermToGroundType.POSITIVE
    assert point_terminal.hfss_pi_type == terminal_mod.HfssPIType.COAXIAL_SHORTENED
    assert point_terminal.reference_terminal is None
    assert equals(point_terminal.reference_layer, layer)
    assert equals(point_terminal.bundle_terminal, bundle_terminal)
    assert point_terminal.is_interface_terminal
    assert not point_terminal.is_reference_terminal
    assert not point_terminal.is_auto_port
    assert not point_terminal.is_circuit_port
    assert point_terminal.use_reference_from_hierarchy
    assert point_terminal.name == "name"
    assert point_terminal.impedance.double == 50.0
    assert point_terminal.source_amplitude.double == 10.0
    assert point_terminal.source_phase.double == 5.0
    assert point_terminal.model == "model"
    rlc = point_terminal.rlc_boundary_parameters
    assert rlc is not None
    assert rlc.r.double == 10.0
    assert rlc.r_enabled and rlc.is_parallel
    assert not rlc.l_enabled and not rlc.c_enabled
    prop = point_terminal.port_post_processing_prop
    assert prop is not None
    assert prop.renormalization_impedance.double == 50.0
    assert prop.do_renormalize
    assert not prop.do_deembed and not prop.do_deembed_gap_l

    assert mock.GetParams.call_count == 18


def test_terminal_set_params(mocked_stub, point_terminal, bundle_terminal, layer):
    mock = mocked_stub(terminal_mod, terminal_mod.Terminal).SetParams
    mock.return_value = None

    point_terminal.boundary_type = terminal_mod.BoundaryType.RLC
    point_terminal.term_to_ground = terminal_mod.SourceTermToGroundType.NO_GROUND
    point_terminal.hfss_pi_type = terminal_mod.HfssPIType.COAXIAL_OPEN
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
