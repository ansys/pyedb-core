"""Session manager for gRPC."""

from contextlib import contextmanager
from enum import Enum
from os import path
from struct import pack, unpack
import subprocess
from sys import modules
from typing import Union

from ansys.api.edb.v1.adaptive_settings_pb2_grpc import AdaptiveSettingsServiceStub
from ansys.api.edb.v1.arc_data_pb2_grpc import ArcDataServiceStub
from ansys.api.edb.v1.bondwire_def_pb2_grpc import (
    ApdBondwireDefServiceStub,
    BondwireDefServiceStub,
    Jedec4BondwireDefServiceStub,
    Jedec5BondwireDefServiceStub,
)
from ansys.api.edb.v1.bondwire_pb2_grpc import BondwireServiceStub
from ansys.api.edb.v1.bundle_term_pb2_grpc import BundleTerminalServiceStub
from ansys.api.edb.v1.cell_instance_pb2_grpc import CellInstanceServiceStub
from ansys.api.edb.v1.cell_pb2_grpc import CellServiceStub
from ansys.api.edb.v1.circle_pb2_grpc import CircleServiceStub
from ansys.api.edb.v1.component_def_pb2_grpc import ComponentDefServiceStub
from ansys.api.edb.v1.component_group_pb2_grpc import ComponentGroupServiceStub
from ansys.api.edb.v1.component_model_pb2_grpc import (
    ComponentModelServiceStub,
    DynamicLinkComponentModelServiceStub,
    NPortComponentModelServiceStub,
)
from ansys.api.edb.v1.component_pin_pb2_grpc import ComponentPinServiceStub
from ansys.api.edb.v1.component_property_pb2_grpc import ComponentPropertyServiceStub
from ansys.api.edb.v1.connectable_pb2_grpc import ConnectableServiceStub
from ansys.api.edb.v1.database_pb2_grpc import DatabaseServiceStub
from ansys.api.edb.v1.dataset_def_pb2_grpc import DatasetDefServiceStub
from ansys.api.edb.v1.debye_model_pb2_grpc import DebyeModelServiceStub
from ansys.api.edb.v1.die_property_pb2_grpc import DiePropertyServiceStub
from ansys.api.edb.v1.dielectric_material_model_pb2_grpc import DielectricMaterialModelServiceStub
from ansys.api.edb.v1.differential_pair_pb2_grpc import DifferentialPairServiceStub
from ansys.api.edb.v1.djordjecvic_sarkar_model_pb2_grpc import DjordjecvicSarkarModelServiceStub
from ansys.api.edb.v1.edge_term_pb2_grpc import EdgeServiceStub, EdgeTerminalServiceStub
from ansys.api.edb.v1.extended_net_pb2_grpc import ExtendedNetServiceStub
from ansys.api.edb.v1.group_pb2_grpc import GroupServiceStub
from ansys.api.edb.v1.hierarchy_obj_pb2_grpc import HierarchyObjectServiceStub
from ansys.api.edb.v1.ic_component_property_pb2_grpc import ICComponentPropertyServiceStub
from ansys.api.edb.v1.layer_collection_pb2_grpc import LayerCollectionServiceStub
from ansys.api.edb.v1.layer_map_pb2_grpc import LayerMapServiceStub
from ansys.api.edb.v1.layer_pb2_grpc import LayerServiceStub
from ansys.api.edb.v1.layout_instance_context_pb2_grpc import LayoutInstanceContextServiceStub
from ansys.api.edb.v1.layout_instance_pb2_grpc import LayoutInstanceServiceStub
from ansys.api.edb.v1.layout_obj_instance_2d_geometry_pb2_grpc import (
    LayoutObjInstance2DGeometryServiceStub,
)
from ansys.api.edb.v1.layout_obj_instance_3d_geometry_pb2_grpc import (
    LayoutObjInstance3DGeometryServiceStub,
)
from ansys.api.edb.v1.layout_obj_instance_geometry_pb2_grpc import (
    LayoutObjInstanceGeometryServiceStub,
)
from ansys.api.edb.v1.layout_obj_instance_pb2_grpc import LayoutObjInstanceServiceStub
from ansys.api.edb.v1.layout_obj_pb2_grpc import LayoutObjServiceStub
from ansys.api.edb.v1.layout_pb2_grpc import LayoutServiceStub
from ansys.api.edb.v1.material_def_pb2_grpc import MaterialDefServiceStub
from ansys.api.edb.v1.multipole_debye_model_pb2_grpc import MultipoleDebyeModelServiceStub
from ansys.api.edb.v1.mcad_model_pb2_grpc import McadModelServiceStub
from ansys.api.edb.v1.net_pb2_grpc import NetServiceStub
from ansys.api.edb.v1.netclass_pb2_grpc import NetClassServiceStub
from ansys.api.edb.v1.package_def_pb2_grpc import PackageDefServiceStub
from ansys.api.edb.v1.padstack_def_data_pb2_grpc import PadstackDefDataServiceStub
from ansys.api.edb.v1.padstack_def_pb2_grpc import PadstackDefServiceStub
from ansys.api.edb.v1.padstack_inst_term_pb2_grpc import PadstackInstanceTerminalServiceStub
from ansys.api.edb.v1.padstack_instance_pb2_grpc import PadstackInstanceServiceStub
from ansys.api.edb.v1.path_pb2_grpc import PathServiceStub
from ansys.api.edb.v1.pin_group_pb2_grpc import PinGroupServiceStub
from ansys.api.edb.v1.pin_group_term_pb2_grpc import PinGroupTerminalServiceStub
from ansys.api.edb.v1.point_data_pb2_grpc import PointDataServiceStub
from ansys.api.edb.v1.point_term_pb2_grpc import PointTerminalServiceStub
from ansys.api.edb.v1.polygon_data_pb2_grpc import PolygonDataServiceStub
from ansys.api.edb.v1.polygon_pb2_grpc import PolygonServiceStub
from ansys.api.edb.v1.port_property_pb2_grpc import PortPropertyServiceStub
from ansys.api.edb.v1.primitive_pb2_grpc import PrimitiveServiceStub
from ansys.api.edb.v1.rectangle_pb2_grpc import RectangleServiceStub
from ansys.api.edb.v1.simulation_settings_pb2_grpc import HFSSSimulatonSettingsServiceStub
from ansys.api.edb.v1.simulation_setup_info_pb2_grpc import SimulationSetupInfoServiceStub
from ansys.api.edb.v1.simulation_setup_pb2_grpc import SimulationSetupServiceStub
from ansys.api.edb.v1.solder_ball_property_pb2_grpc import SolderBallPropertyServiceStub
from ansys.api.edb.v1.stackup_layer_pb2_grpc import StackupLayerServiceStub
from ansys.api.edb.v1.structure3d_pb2_grpc import Structure3DServiceStub
from ansys.api.edb.v1.term_inst_pb2_grpc import TerminalInstanceServiceStub
from ansys.api.edb.v1.term_inst_term_pb2_grpc import TerminalInstanceTerminalServiceStub
from ansys.api.edb.v1.term_pb2_grpc import TerminalServiceStub
from ansys.api.edb.v1.text_pb2_grpc import TextServiceStub
from ansys.api.edb.v1.value_pb2_grpc import ValueServiceStub
from ansys.api.edb.v1.variable_server_pb2_grpc import VariableServerServiceStub
from ansys.api.edb.v1.via_group_pb2_grpc import ViaGroupServiceStub
from ansys.api.edb.v1.via_layer_pb2_grpc import ViaLayerServiceStub
from ansys.api.edb.v1.voltage_regulator_pb2_grpc import VoltageRegulatorServiceStub
import grpc

from ansys.edb.core import edb_errors

# The session module singleton
MOD = modules[__name__]
MOD.current_session = None


class StubAccessor(object):
    """A descriptor to assign specific stub to a model."""

    def __init__(self, stub_type):
        """Initialize a descriptor stub with name and stub service.

        Parameters
        ----------
        stub_type : StubType
        """
        self.__stub_name = stub_type.name

    def __get__(self, instance=None, owner=None):
        """Return the corresponding stub service if a session is active."""
        if MOD.current_session is not None:
            return MOD.current_session.stub(self.__stub_name)
        raise EDBSessionException("No active session detected")


class _Stub:
    def __init__(self, s):
        self._stub = s

    def __getattr__(self, item):
        if hasattr(self._stub, item):
            return edb_errors.handle_grpc_exception(getattr(self._stub, item))


# Helper class for storing data used by the session
class _Session:
    def __init__(self, ip_address, port_num, ansys_em_root):
        if MOD.current_session is None:
            MOD.current_session = self
        else:
            raise EDBSessionStartupException("There can be only one session active at a time")

        self.ip_address = ip_address or "localhost"
        self.port_num = port_num
        self.ansys_em_root = ansys_em_root
        self.channel = None
        self.local_server_proc = None
        self.stubs = None
        self.session = None

    def __enter__(self):
        if MOD.current_session == self:
            self.connect()
            return self
        else:
            raise EDBSessionStartupException("There can be only one session active at a time")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def _initialize_stub(self, stub):
        return _Stub(stub(self.channel))

    def _initialize_stubs(self):
        self.stubs = {stub.name: self._initialize_stub(stub.value) for stub in StubType}

    @property
    def server_url(self):
        if self.is_local():
            return "localhost:{}".format(self.port_num)
        else:
            return "{}:{}".format(self.ip_address, self.port_num)

    @property
    def server_executable(self):
        if self.is_local():
            return path.join(self.ansys_em_root, "EDB_RPC_Server")
        else:
            return ""

    def stub(self, name):
        if self.is_active():
            return self.stubs.get(name)

    def is_active(self):
        return self.channel is not None and self.stubs is not None

    def is_local(self):
        return self.ansys_em_root is not None

    def connect(self):
        if self.is_active():
            return

        if self.is_local():
            self.start_server()

        print("connecting...")
        self.channel = grpc.insecure_channel(self.server_url)

        self._initialize_stubs()
        print("successfully connected.")

    def disconnect(self):
        print("disconnecting...")
        if self.stubs is not None:
            self.stubs = None

        if self.channel is not None:
            self.channel.close()
            self.channel = None

        print("successfully disconnected.")
        if MOD.current_session == self:
            MOD.current_session = None

        if self.is_local():
            self.stop_server()

    def start_server(self):
        try:
            print(f"starting a server from {self.server_executable}...")
            self.local_server_proc = subprocess.Popen(
                self.server_executable, stdout=subprocess.PIPE
            )
        except OSError as os_err:
            raise EDBSessionStartupException(
                'The OS error "{}" occurred when starting the local server. '
                "Was the correct Ansys EM root directory specified?".format(os_err)
            )
        except Exception as err:
            self.disconnect()
            raise _raise_unknown_startup_exception(err)

        self.wait_server_ready()
        print("successfully started a server.")

    def wait_server_ready(self):
        """Wait for the server to say it successfully started up."""
        local_server_proc_output = self.local_server_proc.stdout.readline()
        stdout = local_server_proc_output.decode().rstrip()
        expected_output = "Server listening on 127.0.0.1:{}".format(self.port_num)

        if stdout != expected_output:
            try:
                print("local server failed to start properly. trying to gracefully shutdown...")
                if self.local_server_proc.wait(10):
                    self._on_server_startup_error()
            except subprocess.TimeoutExpired:
                # If the server has not stopped, it will be manually terminated
                # when _disconnect is called in _launch_session.
                # Throw an exception with what info we have.
                raise _raise_unknown_startup_exception(stdout)
            finally:
                self.disconnect()

    def _on_server_startup_error(self):
        # Check if the server process has exited
        if not self.local_server_proc.poll():
            return

        # Get the return code in a usable format
        ret_code = self.local_server_proc.returncode
        ret_code = ret_code if ret_code < 0 else unpack("i", pack("I", ret_code))[0]

        # Handle the return code
        raise EDBSessionStartupException(
            _local_server_error_code_exception_msg_map.get(
                ret_code, "Local server exited with error code {}".format(ret_code)
            )
        )

    def stop_server(self):
        if self.local_server_proc and not self.local_server_proc.poll():
            print("stopping server...")
            self.local_server_proc.terminate()
            self.local_server_proc.wait()
            print("successfully stopped server.")
        self.local_server_proc = None


class StubType(Enum):
    """Enum representing available service stubs."""

    cell = CellServiceStub
    database = DatabaseServiceStub
    layer_collection = LayerCollectionServiceStub
    layer = LayerServiceStub
    stackup_layer = StackupLayerServiceStub
    via_layer = ViaLayerServiceStub
    layout = LayoutServiceStub
    material = MaterialDefServiceStub
    net = NetServiceStub
    primitive = PrimitiveServiceStub
    polygon = PolygonServiceStub
    polygon_data = PolygonDataServiceStub
    path = PathServiceStub
    rectangle = RectangleServiceStub
    adaptive_settings = AdaptiveSettingsServiceStub
    simulation_setup = SimulationSetupServiceStub
    hfss_simulation_settings = HFSSSimulatonSettingsServiceStub
    simulation_setup_info = SimulationSetupInfoServiceStub
    via_group = ViaGroupServiceStub
    circle = CircleServiceStub
    text = TextServiceStub
    terminal = TerminalServiceStub
    terminal_instance = TerminalInstanceServiceStub
    terminal_instance_terminal = TerminalInstanceTerminalServiceStub
    bundle_terminal = BundleTerminalServiceStub
    edge = EdgeServiceStub
    edge_terminal = EdgeTerminalServiceStub
    point_terminal = PointTerminalServiceStub
    padstack_instance_terminal = PadstackInstanceTerminalServiceStub
    pin_group = PinGroupServiceStub
    pin_group_terminal = PinGroupTerminalServiceStub
    bondwire = BondwireServiceStub
    bondwire_def = BondwireDefServiceStub
    apd_bondwire_def = ApdBondwireDefServiceStub
    jedec4_bondwire_def = Jedec4BondwireDefServiceStub
    jedec5_bondwire_def = Jedec5BondwireDefServiceStub
    padstack_def = PadstackDefServiceStub
    value = ValueServiceStub
    variable_server = VariableServerServiceStub
    cell_instance = CellInstanceServiceStub
    hierarchy_obj = HierarchyObjectServiceStub
    group = GroupServiceStub
    netclass = NetClassServiceStub
    layer_map = LayerMapServiceStub
    point_data = PointDataServiceStub
    arc_data = ArcDataServiceStub
    padstack_instance = PadstackInstanceServiceStub
    voltage_regulator = VoltageRegulatorServiceStub
    connectable = ConnectableServiceStub
    component_group = ComponentGroupServiceStub
    layout_obj = LayoutObjServiceStub
    structure3d = Structure3DServiceStub
    layout_instance = LayoutInstanceServiceStub
    layout_instance_context = LayoutInstanceContextServiceStub
    layout_obj_instance = LayoutObjInstanceServiceStub
    layout_obj_instance_geometry = LayoutObjInstanceGeometryServiceStub
    layout_obj_instance_2d_geometry = LayoutObjInstance2DGeometryServiceStub
    layout_obj_instance_3d_geometry = LayoutObjInstance3DGeometryServiceStub
    component_def = ComponentDefServiceStub
    component_pin = ComponentPinServiceStub
    component_model = ComponentModelServiceStub
    nport_component_model = NPortComponentModelServiceStub
    dyn_link_component_model = DynamicLinkComponentModelServiceStub
    extended_net = ExtendedNetServiceStub
    padstack_def_data = PadstackDefDataServiceStub
    differential_pair = DifferentialPairServiceStub
    solder_ball_property = SolderBallPropertyServiceStub
    component_property = ComponentPropertyServiceStub
    ic_component_property = ICComponentPropertyServiceStub
    die_property = DiePropertyServiceStub
    port_property = PortPropertyServiceStub
    dataset_def = DatasetDefServiceStub
    package_def = PackageDefServiceStub
    dielectric_material_model = DielectricMaterialModelServiceStub
    debye_model = DebyeModelServiceStub
    multipole_debye_model = MultipoleDebyeModelServiceStub
    djordecvic_sarkar_model = DjordjecvicSarkarModelServiceStub
    mcad_model = McadModelServiceStub


# Dictionary for storing local server error code exception messages
_local_server_error_code_exception_msg_map = {
    -1: "Failed to initialize EDB",
    -2: "No valid license detected",
}


def launch_session(ansys_em_root, port_num, ip_address=None):
    r"""Launch a local session to an EDB API server.

    The session must be manually disconnected after use by calling session.disconnect()

    Parameters
    ----------
    ansys_em_root : str
        The installation directory of EDB_RPC_Server.exe
    port_num : int
        The port number to listen on
    ip_address : str, optional
        Currently not supported. Default value means local_host. It specifies the IP address of the machine where \
        the server executable is running. Future releases will support remotely running the API on another machine.

    Examples
    --------
    Creates a session and disconnects it

    >>> session = launch_session("C:\\Program Files\\AnsysEM\\v231\\Win64", 50051)
    >>> # program goes here
    >>> session.disconnect()
    """
    MOD.current_session = _Session(ip_address, port_num, ansys_em_root)
    MOD.current_session.connect()
    return MOD.current_session


@contextmanager
def session(ansys_em_root, port_num, ip_address=None):
    r"""Launch a local session to an EDB API server in a context manager.

    Parameters
    ----------
    ansys_em_root : str
        The installation directory of EDB_RPC_Server.exe
    port_num : int
        The port number to listen on
    ip_address : str, optional
        Currently not supported. Default value means local_host. It specifies the IP address of the machine where \
        the server executable is running. Future releases will support remotely running the API on another machine.

    Examples
    --------
    Creates a session that will automatically disconnect when it goes out of scope.

    >>> with session("C:\\Program Files\\AnsysEM\\v231\\Win64", 50051):
    >>>    # program goes here
    """
    try:
        MOD.current_session = _Session(ip_address, port_num, ansys_em_root)
        MOD.current_session.connect()
        yield
    except Exception as e:  # noqa
        print("EDB session ran into unhandled error.")
        print(e)
        raise
    finally:
        MOD.current_session.disconnect()


def _raise_unknown_startup_exception(error_msg: Union[str, Exception]) -> None:
    raise EDBSessionStartupException(
        "An unexpected error occurred when starting the local server: {}".format(error_msg)
    )


def get_database_stub():
    """Get Database stub.

    Returns
    -------
    DatabaseServiceStub
    """
    return StubAccessor(StubType.database).__get__()


def get_layer_collection_stub():
    """Get Layer collection stub.

    Returns
    -------
    LayerCollectionServiceStub
    """
    return StubAccessor(StubType.layer_collection).__get__()


def get_stackup_layer_stub():
    """Get Stackup layer stub.

    Returns
    -------
    StackupLayerServiceStub
    """
    return StubAccessor(StubType.stackup_layer).__get__()


def get_via_layer_stub():
    """Get Via layer stub.

    Returns
    -------
    ViaLayerServiceStub
    """
    return StubAccessor(StubType.via_layer).__get__()


def get_adaptive_settings_stub():
    """Get Adaptive settings stub.

    Returns
    -------
    AdaptiveSettingsServiceStub
    """
    return StubAccessor(StubType.adaptive_settings).__get__()


def get_simulation_setup_stub():
    """Get Simulation setup stub.

    Returns
    -------
    SimulationSetupServiceStub
    """
    return StubAccessor(StubType.simulation_setup).__get__()


def get_hfss_simulation_settings_stub():
    """Get HFSS simulation settings stub.

    Returns
    -------
    HFSSSimulatonSettingsServiceStub
    """
    return StubAccessor(StubType.hfss_simulation_settings).__get__()


def get_simulation_setup_info_stub():
    """Get Simulation setup info stub.

    Returns
    -------
    SimulationSetupInfoServiceStub
    """
    return StubAccessor(StubType.simulation_setup_info).__get__()


def get_via_group_stub():
    """Get Via group stub.

    Returns
    -------
    ViaGroupServiceStub
    """
    return StubAccessor(StubType.via_group).__get__()


def get_variable_server_stub():
    """Get VariableServer stub.

    Returns
    -------
    VariableServerServiceStub
    """
    return StubAccessor(StubType.variable_server).__get__()


def get_cell_instance_stub():
    """Get CellInstance stub.

    Returns
    -------
    CellInstanceServiceStub
    """
    return StubAccessor(StubType.cell_instance).__get__()


def get_extended_net_stub():
    """Get ExtendedNet stub.

    Returns
    -------
    ExtendedNetServiceStub
    """
    return StubAccessor(StubType.extended_net).__get__()


class EDBSessionException(Exception):
    """Base class for exceptions related to EDB sessions."""

    pass


class EDBSessionStartupException(EDBSessionException):
    """Exception managing startup process of EDB sessions."""

    pass
