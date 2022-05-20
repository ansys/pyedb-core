"""Via Group."""

import ansys.api.edb.v1.via_group_pb2 as via_group_pb2

from ....interfaces.grpc import messages
from ....session import get_via_group_stub
from ....utility.edb_errors import handle_grpc_exception
from .group import Group


class _QueryBuilder:
    @staticmethod
    def create(layout, outline, conductivity_ratio, layer, net):
        return via_group_pb2.ViaGroupCreationMessage(
            layout=layout.msg,
            points=messages.points_message(outline),
            layer=messages.layer_ref_message(layer),
            net=messages.net_ref_message(net),
            conductivity_ratio=conductivity_ratio,
        )


class ViaGroup(Group):
    """Class representing a via group."""

    @staticmethod
    @handle_grpc_exception
    def create(layout, outline, conductivity_ratio, layer, net=None):
        """Create a via group.

        Parameters
        ----------
        layout : Layout
        outline : list of Point2D
        conductivity_ratio : float
        layer : str or Layer
        net : str or Net, optional

        Returns
        -------
        ViaGroup
        """
        return ViaGroup(
            get_via_group_stub().Create(
                _QueryBuilder.create(layout, outline, conductivity_ratio, layer, net)
            )
        )
