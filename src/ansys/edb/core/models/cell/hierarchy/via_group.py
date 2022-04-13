import ansys.api.edb.v1.via_group_pb2 as via_group_pb2
from ansys.edb.cell.hierarchy.group import Group
from ansys.edb.cell.layout import Layout
from ansys.edb.cell.net import Net
from ansys.edb.session import get_via_group_stub
from ansys.edb.utility.edb_errors import handle_grpc_exception

import ansys.edb.core.communications.grpc.messages as messages
from ansys.edb.core.models.base import Points2D


class _QueryBuilder:
    @staticmethod
    def create(
        layout: Layout, outline: Points2D, conductivity_ratio: float, layer: str, net: Net
    ) -> via_group_pb2.ViaGroupCreationMessage:

        return via_group_pb2.ViaGroupCreationMessage(
            layout=layout.id,
            points=messages.points_message(outline),
            layer=messages.layer_ref_message(layer),
            net=messages.net_ref_message(net),
            conductivity_ratio=conductivity_ratio,
        )


class ViaGroup(Group):
    @staticmethod
    @handle_grpc_exception
    def create(
        layout: Layout, outline: Points2D, conductivity_ratio: float, layer: str, net: Net = None
    ) -> "ViaGroup":
        return ViaGroup(
            get_via_group_stub().Create(
                _QueryBuilder.create(layout, outline, conductivity_ratio, layer, net)
            )
        )
