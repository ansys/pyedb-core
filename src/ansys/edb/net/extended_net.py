"""Extended Net."""

import ansys.api.edb.v1.extended_net_pb2 as enet_pb2

from ansys.edb.edb_defs import LayoutObjType
from ansys.edb.net import net_class
from ansys.edb.session import StubAccessor, StubType, get_extended_net_stub


class ExtendedNet(net_class.NetClass):
    """ExtendedNet class."""

    __stub = StubAccessor(StubType.extended_net)
    layout_obj_type = LayoutObjType.EXTENDED_NET

    @staticmethod
    def create(layout, name):
        """Create an extendednet.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.layout.Layout>`
            The layout object
        name : str
            Name of the extendednet to create

        Returns
        -------
        ExtendedNet
            Newly created extended netobject
        """
        return ExtendedNet(
            get_extended_net_stub().Create(
                enet_pb2.ExtendedNetCreationMessage(layout=layout.msg, name=name)
            )
        )

    @staticmethod
    def find_by_name(layout, name):
        """Find an extendednet in a layout by name.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.layout.Layout>`
            The layout object
        name : str
            Name of the extendednet to find

        Returns
        -------
        ExtendedNet
            The extended net that was found. Null object is returned if it is not found.
        """
        return ExtendedNet(
            get_extended_net_stub().FindByName(
                enet_pb2.ExtendedNetLookupMessage(layout=layout.msg, name=name)
            )
        )

    def add_net(self, net):
        """Add net to an extendednet.

        Parameters
        ----------
        net : :class:`Net <ansys.edb.layout.Net>`
            The net object to be added

        """
        self.__stub.AddNet(enet_pb2.ExtendedNetModifyMessage(ext_net=self.msg, net=net.msg))

    def remove_net(self, net):
        """Remove net from extendednet.

        Parameters
        ----------
        net : :class:`Net <ansys.edb.layout.Net>`
            The net object to be removed

        """
        self.__stub.RemoveNet(enet_pb2.ExtendedNetModifyMessage(ext_net=self.msg, net=net.msg))

    def remove_all_nets(self):
        """Remove all nets from extendednet."""
        self.__stub.RemoveAllNets(self.msg)
