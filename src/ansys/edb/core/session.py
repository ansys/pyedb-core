"""Session manager for gRPC."""

from contextlib import contextmanager
from pathlib import Path as PathlibPath
from struct import pack, unpack
import subprocess
from sys import modules
from typing import Optional, Union

from ansys.api.edb.v1.adaptive_settings_pb2_grpc import AdaptiveSettingsServiceStub
from ansys.api.edb.v1.cell_pb2_grpc import CellServiceStub
from ansys.api.edb.v1.circle_pb2_grpc import CircleServiceStub
from ansys.api.edb.v1.database_pb2_grpc import DatabaseServiceStub
from ansys.api.edb.v1.edb_iterator_pb2_grpc import EDBIteratorServiceStub
from ansys.api.edb.v1.layer_collection_pb2_grpc import LayerCollectionServiceStub
from ansys.api.edb.v1.layer_pb2_grpc import (
    LayerServiceStub,
    StackupLayerServiceStub,
    ViaLayerServiceStub,
)
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
from ansys.api.edb.v1.term_pb2_grpc import TerminalServiceStub
from ansys.api.edb.v1.via_group_pb2_grpc import ViaGroupServiceStub
import grpc


# Helper class for storing data used by the session
class _EDBSessionData:
    def __init__(self):
        self.ip_address = ""
        self.port_num = ""
        self.ansys_em_root: Optional[PathlibPath] = None
        self.channel: Optional["grpc.Channel"] = None
        self.local_server_proc: Optional["subprocess.Popen"] = None
        self.stubs = {}

    def initialize(self, ip_address: str, port_num: str, ansys_em_root: PathlibPath = None):
        self.ip_address = ip_address
        self.port_num = port_num
        self.ansys_em_root = ansys_em_root

    def reset(self):
        self.ip_address = ""
        self.port_num = ""
        self.ansys_em_root = None
        self.channel = None
        self.local_server_proc = None
        self.stubs.clear()


# The session module singleton
session = modules[__name__]
session.data = _EDBSessionData()

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
_pt_term_keyword = "PointTerminal"
_adaptive_settings_stub_keyword = "AdaptiveSettings"
_sim_setup_stub_keyword = "SimulationSetup"
_hfss_sim_settings_stub_keyword = "HFSSSimulationSettings"
_sim_setup_info_stub_keyword = "SimulationSetupInfo"
_via_group_stub_keyword = "ViaGroup"
_circle_stub_keyword = "Circle"


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
    _pt_term_keyword: PointTerminalServiceStub,
    _adaptive_settings_stub_keyword: AdaptiveSettingsServiceStub,
    _sim_setup_stub_keyword: SimulationSetupServiceStub,
    _hfss_sim_settings_stub_keyword: HFSSSimulatonSettingsServiceStub,
    _sim_setup_info_stub_keyword: SimulationSetupInfoServiceStub,
    _via_group_stub_keyword: ViaGroupServiceStub,
    _circle_stub_keyword: CircleServiceStub,
}

# Dictionary for storing local server error code exception messages
_local_server_error_code_exception_msg_map = {
    -1: "Failed to initialize EDB",
    -2: "No valid license detected",
}


def launch_local_session(ansys_em_root, port_num):
    """Launch a local session of the EDB API.

    Parameters
    ----------
    ansys_em_root : pathlib.Path, optional
    port_num : str

    Returns
    -------
    None
    """
    return _launch_session("localhost", port_num, ansys_em_root)


@contextmanager
def _launch_session(ip_address: str, port_num: str, ansys_em_root: PathlibPath = None) -> None:

    session.data.initialize(ip_address, port_num, ansys_em_root)
    try:
        _connect()
        yield session
    finally:
        _disconnect()


def _raise_unknown_startup_exception(error_msg: Union[str, Exception]) -> None:
    raise EDBSessionStartupException(
        "An unexpected error occurred when starting the local server: {}".format(error_msg)
    )


def _handle_local_server_startup_exit_code() -> None:
    # Check if the server process has exited
    if not session.data.local_server_proc.poll():
        return

    # Get the return code in a usable format
    original_return_code = session.data.local_server_proc.returncode
    final_return_code = (
        original_return_code
        if original_return_code < 0
        else unpack("i", pack("I", original_return_code))[0]
    )

    # Handle the return code
    raise EDBSessionStartupException(
        _local_server_error_code_exception_msg_map.get(
            final_return_code, "Local server exited with error code {}".format(final_return_code)
        )
    )


def _start_local_server() -> None:
    # Start the server
    server_exe_path = str(PathlibPath.joinpath(session.data.ansys_em_root, "EDB_RPC_Server.exe"))
    try:
        session.data.local_server_proc = subprocess.Popen(server_exe_path, stdout=subprocess.PIPE)
    except OSError as os_err:
        raise EDBSessionStartupException(
            'The OS error "{}" occurred when starting the local server. '
            "Was the correct Ansys EM root directory specified?".format(os_err)
        )
    except Exception as err:
        raise _raise_unknown_startup_exception(err)

    # Wait for the server to say it successfully started up
    local_server_proc_output = session.data.local_server_proc.stdout.readline()
    expected_ip_address = (
        "127.0.0.1" if session.data.ip_address == "localhost" else session.data.ip_address
    )
    expected_address = "{}:{}".format(expected_ip_address, session.data.port_num)
    expected_output = "Server listening on {}".format(expected_address)
    clean_local_server_proc_output = local_server_proc_output.decode().rstrip()
    if clean_local_server_proc_output != expected_output:
        try:
            # If we received unexpected output
            # give the server time to exit since it most likely failed to start
            if session.data.local_server_proc.wait(10):
                # If the server exited, throw the corresponding exception
                _handle_local_server_startup_exit_code()
        except subprocess.TimeoutExpired:
            # If the server has not stopped, it will be manually terminated
            # when _disconnect is called in _launch_session.
            # Throw an exception with what info we have.
            raise _raise_unknown_startup_exception(clean_local_server_proc_output)


def _session_is_active() -> bool:
    return bool(session.data.channel) and bool(session.data.stubs)


def _is_local_session() -> bool:
    return bool(session.data.ansys_em_root)


def _get_stub(keyword: str):
    if _session_is_active():
        return session.data.stubs.get(keyword)
    raise EDBSessionException("No active session detected")


def _initialize_stubs() -> None:
    for key, stub in _type_to_stub_ctor_map.items():
        session.data.stubs.update({key: stub(session.data.channel)})


def _connect() -> None:
    # Make sure there isn't already an active session
    if _session_is_active():
        raise EDBSessionStartupException("There can be only one session active at a time")

    # Initialize the channel and stubs
    session.data.channel = grpc.insecure_channel(
        "{}:{}".format(session.data.ip_address, session.data.port_num)
    )
    _initialize_stubs()

    # If necessary, start the local server
    if _is_local_session():
        _start_local_server()


def _disconnect() -> None:
    # Cleanup the channel and stubs
    if session.data.channel:
        session.data.channel.close()

    # If necessary, shutdown the local server
    if session.data.local_server_proc and not session.data.local_server_proc.poll():
        session.data.local_server_proc.terminate()
        session.data.local_server_proc.wait()

    # Reset the data in the session data to its initial state
    session.data.reset()


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


class EDBSessionException(Exception):
    """Base class for exceptions related to EDB sessions."""

    pass


class EDBSessionStartupException(EDBSessionException):
    """Exception managing startup process of EDB sessions."""

    pass
