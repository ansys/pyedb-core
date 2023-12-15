"""Extended net."""

import ansys.api.edb.v1.extended_net_pb2 as enet_pb2

from ansys.edb.core.edb_defs import LayoutObjType
from ansys.edb.core.net import net_class
from ansys.edb.core.session import StubAccessor, StubType


class _ExtendedNetQueryBuilder:
    @staticmethod
    def extnet_create_msg(layout, name):
        return enet_pb2.ExtendedNetCreationMessage(layout=layout.msg, name=name)

    @staticmethod
    def extenet_find_by_name_msg(layout, name):
        return enet_pb2.ExtendedNetLookupMessage(layout=layout.msg, name=name)

    @staticmethod
    def extnet_modify_net_msg(ext_net, net):
        return enet_pb2.ExtendedNetModifyMessage(ext_net=ext_net.msg, net=net.msg)


class ExtendedNet(net_class.NetClass):
    """Represents an extended net."""

    __stub = StubAccessor(StubType.extended_net)
    layout_obj_type = LayoutObjType.EXTENDED_NET

    @classmethod
    def create(cls, layout, name):
        """Create an extended net.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.core.layout.Layout>`
            Layout to create the extended net in.
        name : str
            Name of the extended net.

        Returns
        -------
        ExtendedNet
            Extended net created.
        """
        return ExtendedNet(
            cls.__stub.Create(_ExtendedNetQueryBuilder.extnet_create_msg(layout, name))
        )

    @classmethod
    def find_by_name(cls, layout, name):
        """Find an extended net by name in a given layout.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.core.layout.Layout>`
            Layout to search for the extended net.
        name : str
            Name of the extended net.

        Returns
        -------
        ExtendedNet
            Extended net that was found. Check the :obj:`is_null <ansys.edb.core.net.ExtendedNet.is_null>`
            property of the extended net to see if it exists.
        """
        return ExtendedNet(
            cls.__stub.FindByName(_ExtendedNetQueryBuilder.extenet_find_by_name_msg(layout, name))
        )

    def add_net(self, net):
        """Add a net to the extended net.

        Parameters
        ----------
        net : Net
            Net to add.
        """
        self.__stub.AddNet(_ExtendedNetQueryBuilder.extnet_modify_net_msg(self, net))

    def remove_net(self, net):
        """Remove a net from the extended net.

        Parameters
        ----------
        net : Net
            Net to remove.
        """
        self.__stub.RemoveNet(_ExtendedNetQueryBuilder.extnet_modify_net_msg(self, net))

    def remove_all_nets(self):
        """Remove all nets from the extended net."""
        self.__stub.RemoveAllNets(self.msg)
