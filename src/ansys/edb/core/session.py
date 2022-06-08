"""Session manager for gRPC."""

from contextlib import contextmanager
from os import path
from struct import pack, unpack
import subprocess
from sys import modules
from typing import Union

from ansys.api.edb.v1.adaptive_settings_pb2_grpc import AdaptiveSettingsServiceStub
from ansys.api.edb.v1.bondwire_pb2_grpc import BondwireServiceStub
from ansys.api.edb.v1.bundle_term_pb2_grpc import BundleTerminalServiceStub
from ansys.api.edb.v1.cell_instance_pb2_grpc import CellInstanceServiceStub
from ansys.api.edb.v1.cell_pb2_grpc import CellServiceStub
from ansys.api.edb.v1.circle_pb2_grpc import CircleServiceStub
from ansys.api.edb.v1.database_pb2_grpc import DatabaseServiceStub
from ansys.api.edb.v1.edb_iterator_pb2_grpc import EDBIteratorServiceStub
from ansys.api.edb.v1.layer_collection_pb2_grpc import LayerCollectionServiceStub
from ansys.api.edb.v1.layer_pb2_grpc import LayerServiceStub
from ansys.api.edb.v1.layout_pb2_grpc import LayoutServiceStub
from ansys.api.edb.v1.material_def_pb2_grpc import MaterialDefServiceStub
from ansys.api.edb.v1.net_pb2_grpc import NetServiceStub
from ansys.api.edb.v1.path_pb2_grpc import PathServiceStub
from ansys.api.edb.v1.point_term_pb2_grpc import PointTerminalServiceStub
from ansys.api.edb.v1.polygon_data_pb2_grpc import PolygonDataServiceStub
from ansys.api.edb.v1.polygon_pb2_grpc import PolygonServiceStub
from ansys.api.edb.v1.primitive_pb2_grpc import PrimitiveServiceStub
from ansys.api.edb.v1.rectangle_pb2_grpc import RectangleServiceStub
from ansys.api.edb.v1.simulation_settings_pb2_grpc import HFSSSimulatonSettingsServiceStub
from ansys.api.edb.v1.simulation_setup_info_pb2_grpc import SimulationSetupInfoServiceStub
from ansys.api.edb.v1.simulation_setup_pb2_grpc import SimulationSetupServiceStub
from ansys.api.edb.v1.stackup_layer_pb2_grpc import StackupLayerServiceStub
from ansys.api.edb.v1.term_pb2_grpc import TerminalServiceStub
from ansys.api.edb.v1.text_pb2_grpc import TextServiceStub
from ansys.api.edb.v1.via_group_pb2_grpc import ViaGroupServiceStub
from ansys.api.edb.v1.via_layer_pb2_grpc import ViaLayerServiceStub
import grpc

# The session module singleton
MOD = modules[__name__]
MOD.current_session = None


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

    def _initialize_stubs(self):
        self.stubs = {key: stub(self.channel) for key, stub in _type_to_stub_ctor_map.items()}

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


# Keywords for accessing stubs
_cell_stub_keyword = "Cell"
_db_stub_keyword = "Database"
_edb_iter_stub_keyword = "EDBDIterator"
_lc_stub_keyword = "LayerCollection"
_lyr_stub_keyword = "Layer"
_stk_lyr_stub_keyword = "StackupLayer"
_via_lyr_stub_keyword = "ViaLayer"
_lyt_stub_keyword = "Layout"
_mat_def_stub_keyword = "MaterialDef"
_net_stub_keyword = "Net"
_prim_stub_keyword = "Primitive"
_poly_stub_keyword = "Polygon"
_poly_data_stub_keyword = "PolygonData"
_path_stub_keyword = "Path"
_rect_stub_keyword = "Rectangle"
_term_stub_keyword = "Terminal"
_bundle_term_keyword = "BundleTerminal"
_pt_term_keyword = "PointTerminal"
_adaptive_settings_stub_keyword = "AdaptiveSettings"
_sim_setup_stub_keyword = "SimulationSetup"
_hfss_sim_settings_stub_keyword = "HFSSSimulationSettings"
_sim_setup_info_stub_keyword = "SimulationSetupInfo"
_via_group_stub_keyword = "ViaGroup"
_circle_stub_keyword = "Circle"
_text_stub_keyword = "Text"
_bondwire_stub_keyword = "Bondwire"
_cell_instance_stub_keyword = "CellInstance"


# Map of stub keywords to stub ctors. Used for initializing stubs when connecting to the server.
_type_to_stub_ctor_map = {
    _cell_stub_keyword: CellServiceStub,
    _db_stub_keyword: DatabaseServiceStub,
    _edb_iter_stub_keyword: EDBIteratorServiceStub,
    _lc_stub_keyword: LayerCollectionServiceStub,
    _lyr_stub_keyword: LayerServiceStub,
    _stk_lyr_stub_keyword: StackupLayerServiceStub,
    _via_lyr_stub_keyword: ViaLayerServiceStub,
    _lyt_stub_keyword: LayoutServiceStub,
    _mat_def_stub_keyword: MaterialDefServiceStub,
    _net_stub_keyword: NetServiceStub,
    _prim_stub_keyword: PrimitiveServiceStub,
    _poly_stub_keyword: PolygonServiceStub,
    _poly_data_stub_keyword: PolygonDataServiceStub,
    _path_stub_keyword: PathServiceStub,
    _rect_stub_keyword: RectangleServiceStub,
    _term_stub_keyword: TerminalServiceStub,
    _bundle_term_keyword: BundleTerminalServiceStub,
    _pt_term_keyword: PointTerminalServiceStub,
    _adaptive_settings_stub_keyword: AdaptiveSettingsServiceStub,
    _sim_setup_stub_keyword: SimulationSetupServiceStub,
    _hfss_sim_settings_stub_keyword: HFSSSimulatonSettingsServiceStub,
    _sim_setup_info_stub_keyword: SimulationSetupInfoServiceStub,
    _via_group_stub_keyword: ViaGroupServiceStub,
    _circle_stub_keyword: CircleServiceStub,
    _text_stub_keyword: TextServiceStub,
    _bondwire_stub_keyword: BondwireServiceStub,
    _cell_instance_stub_keyword: CellInstanceServiceStub,
}

# Dictionary for storing local server error code exception messages
_local_server_error_code_exception_msg_map = {
    -1: "Failed to initialize EDB",
    -2: "No valid license detected",
}


def launch_session(ansys_em_root, port_num, ip_address=None):
    """Launch a local session to an EDB API server. must be manually disconnected after use.

    Parameters
    ----------
    ansys_em_root : str, optional
    port_num : int
    ip_address : str, optional
    Returns
    -------
    None
    """
    MOD.current_session = _Session(ip_address, port_num, ansys_em_root)
    MOD.current_session.connect()
    return MOD.current_session


@contextmanager
def session(ansys_em_root, port_num, ip_address=None):
    """Launch a local session to an EDB API server in a context manager.

    Parameters
    ----------
    ansys_em_root : atr, optional
    port_num : int
    ip_address : str, optional
    Returns
    -------
    None
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


def _get_stub(keyword: str):
    if MOD.current_session is not None:
        return MOD.current_session.stub(keyword)
    raise EDBSessionException("No active session detected")


def get_cell_stub():
    """Get Cell stub.

    Returns
    -------
    CellServiceStub
    """
    return _get_stub(_cell_stub_keyword)


def get_database_stub():
    """Get Database stub.

    Returns
    -------
    DatabaseServiceStub
    """
    return _get_stub(_db_stub_keyword)


def get_edb_iterator_stub():
    """Get Iterator stub.

    Returns
    -------
    EDBIteratorServiceStub
    """
    return _get_stub(_edb_iter_stub_keyword)


def get_layer_collection_stub():
    """Get Layer collection stub.

    Returns
    -------
    LayerCollectionServiceStub
    """
    return _get_stub(_lc_stub_keyword)


def get_layer_stub():
    """Get Layer stub.

    Returns
    -------
    LayerServiceStub
    """
    return _get_stub(_lyr_stub_keyword)


def get_stackup_layer_stub():
    """Get Stackup layer stub.

    Returns
    -------
    StackupLayerServiceStub
    """
    return _get_stub(_stk_lyr_stub_keyword)


def get_via_layer_stub():
    """Get Via layer stub.

    Returns
    -------
    ViaLayerServiceStub
    """
    return _get_stub(_via_lyr_stub_keyword)


def get_layout_stub():
    """Get Layout stub.

    Returns
    -------
    LayoutServiceStub
    """
    return _get_stub(_lyt_stub_keyword)


def get_material_def_stub():
    """Get Material definition stub.

    Returns
    -------
    MaterialDefServiceStub
    """
    return _get_stub(_mat_def_stub_keyword)


def get_net_stub():
    """Get Net stub.

    Returns
    -------
    NetServiceStub
    """
    return _get_stub(_net_stub_keyword)


def get_primitive_stub():
    """Get Primitive stub.

    Returns
    -------
    PrimitiveServiceStub
    """
    return _get_stub(_prim_stub_keyword)


def get_polygon_stub():
    """Get Polygon stub.

    Returns
    -------
    PolygonServiceStub
    """
    return _get_stub(_poly_stub_keyword)


def get_polygon_data_stub():
    """Get Polygon data stub.

    Returns
    -------
    PolygonDataServiceStub
    """
    return _get_stub(_poly_data_stub_keyword)


def get_path_stub():
    """Get Path stub.

    Returns
    -------
    PathServiceStub
    """
    return _get_stub(_path_stub_keyword)


def get_rectangle_stub():
    """Get Rectangle stub.

    Returns
    -------
    RectangleServiceStub
    """
    return _get_stub(_rect_stub_keyword)


def get_terminal_stub():
    """Get Terminal stub.

    Returns
    -------
    TerminalServiceStub
    """
    return _get_stub(_term_stub_keyword)


def get_bundle_terminal_stub():
    """Get Bundle terminal stub.

    Returns
    -------
    BundleTerminalServiceStub
    """
    return _get_stub(_bundle_term_keyword)


def get_point_terminal_stub():
    """Get Point terminal stub.

    Returns
    -------
    PointTerminalServiceStub
    """
    return _get_stub(_pt_term_keyword)


def get_adaptive_settings_stub():
    """Get Adaptive settings stub.

    Returns
    -------
    AdaptiveSettingsServiceStub
    """
    return _get_stub(_adaptive_settings_stub_keyword)


def get_simulation_setup_stub():
    """Get Simulation setup stub.

    Returns
    -------
    SimulationSetupServiceStub
    """
    return _get_stub(_sim_setup_stub_keyword)


def get_hfss_simulation_settings_stub():
    """Get HFSS simulation settings stub.

    Returns
    -------
    HFSSSimulatonSettingsServiceStub
    """
    return _get_stub(_hfss_sim_settings_stub_keyword)


def get_simulation_setup_info_stub():
    """Get Simulation setup info stub.

    Returns
    -------
    SimulationSetupInfoServiceStub
    """
    return _get_stub(_sim_setup_info_stub_keyword)


def get_via_group_stub():
    """Get Via group stub.

    Returns
    -------
    ViaGroupServiceStub
    """
    return _get_stub(_via_group_stub_keyword)


def get_circle_stub() -> CircleServiceStub:
    """Get Circle stub.

    Returns
    -------
    CircleServiceStub
    """
    return _get_stub(_circle_stub_keyword)


def get_text_stub():
    """Get Text stub.

    Returns
    -------
    TextServiceStub
    """
    return _get_stub(_text_stub_keyword)


def get_bondwire_stub():
    """Get Bondwire stub.

    Returns
    -------
    BondwireServiceStub
    """
    return _get_stub(_bondwire_stub_keyword)


def get_cell_instance_stub():
    """Get CellInstance stub.

    Returns
    -------
    CellInstanceServiceStub
    """
    return _get_stub(_cell_instance_stub_keyword)


class EDBSessionException(Exception):
    """Base class for exceptions related to EDB sessions."""

    pass


class EDBSessionStartupException(EDBSessionException):
    """Exception managing startup process of EDB sessions."""

    pass
