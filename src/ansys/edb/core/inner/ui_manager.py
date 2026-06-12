"""UI Manager."""

from ansys.api.edb.v1 import ui_manager_pb2_grpc
import google.protobuf.empty_pb2 as empty_pb2

from ansys.edb.core.session import StubAccessor, StubType


class UIManager:
    """Provides access to the UI Manager service."""

    __stub: ui_manager_pb2_grpc.UIManagerServiceStub = StubAccessor(StubType.ui_manager)

    @classmethod
    def sync_3d_layout_ui(cls):
        """Synchronize the 3D layout UI."""
        cls.__stub.Sync3DLayoutUI(empty_pb2.Empty())
