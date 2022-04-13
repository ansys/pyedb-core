from typing import List, Tuple

from ansys.api.edb.v1.simulation_settings_pb2 import (
    MeshOperationMessage,
    MeshOperationsMessage,
    MeshOpNetLayerInfoMessage,
    SetMeshOperationsMessage,
    SkinDepthMeshOperationMessage,
)

from ....session import get_hfss_simulation_settings_stub
from ....utility.edb_errors import handle_grpc_exception
from .adaptive.hfss_adaptive_settings import HFSSAdaptiveSettings
from .mesh_operation.mesh_operation import MeshOperation
from .mesh_operation.skin_depth_mesh_operation import SkinDepthMeshOperation
from .simulation_settings import SimulationSettings


class _QueryBuilder:
    @staticmethod
    def get_adaptive_settings(hfss_sim_settings: "HFSSSimulationSettings"):
        return hfss_sim_settings._msg

    @staticmethod
    def set_mesh_operations(
        hfss_sim_settings: "HFSSSimulationSettings", new_mesh_ops: List[MeshOperation]
    ):
        new_mesh_op_msgs = []
        for mesh_op in new_mesh_ops:
            mesh_op_msg = _QueryBuilder.mesh_op_message(mesh_op)

            if isinstance(mesh_op, SkinDepthMeshOperation):
                mesh_op_msg.skin_depth_mesh_op.CopyFrom(
                    _QueryBuilder.skin_depth_op_message(mesh_op)
                )

            new_mesh_op_msgs.append(mesh_op_msg)
        new_mesh_op_msg = MeshOperationsMessage(mesh_operations=new_mesh_op_msgs)
        return SetMeshOperationsMessage(
            hfss_simulation_settings=hfss_sim_settings._msg, mesh_operations=new_mesh_op_msg
        )

    @staticmethod
    def mesh_op_message(op: MeshOperation):
        return MeshOperationMessage(
            name=op.name,
            enabled=op.enabled,
            refine_inside=op.refine_inside,
            mesh_region=op.mesh_region,
            net_layer_info=_QueryBuilder.mesh_op_net_layer_message(op.net_layer_info),
        )

    @staticmethod
    def mesh_op_net_layer_message(nls: List[Tuple[str, str, bool]]):
        return [MeshOpNetLayerInfoMessage(net=nl[0], layer=nl[1], is_sheet=nl[2]) for nl in nls]

    @staticmethod
    def skin_depth_op_message(op: SkinDepthMeshOperation):
        return SkinDepthMeshOperationMessage(
            skin_depth=op.skin_depth,
            max_surface_triangle_length=op.surf_tri_length,
            num_layers=op.num_layers,
            max_elements=op.max_elems,
            restrict_max_elements=op.restrict_max_elem,
        )


class HFSSSimulationSettings(SimulationSettings):
    @property
    @handle_grpc_exception
    def adaptive_settings(self) -> HFSSAdaptiveSettings:
        return HFSSAdaptiveSettings(
            get_hfss_simulation_settings_stub().GetAdaptiveSettings(
                _QueryBuilder.get_adaptive_settings(self)
            )
        )

    @property
    def mesh_operations(self):
        pass

    @mesh_operations.setter
    def mesh_operations(self, new_mesh_ops: List[MeshOperation]) -> None:
        query = _QueryBuilder.set_mesh_operations(self, new_mesh_ops)
        get_hfss_simulation_settings_stub().SetMeshOperations(query)
