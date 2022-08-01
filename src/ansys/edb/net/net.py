"""Net."""

import ansys.api.edb.v1.net_pb2 as net_pb2

from ansys.edb.core import LayoutObj, LayoutObjType
from ansys.edb.session import get_net_stub


class _QueryBuilder:
    @staticmethod
    def create(layout, name):
        return net_pb2.NetCreationMessage(layout=layout.msg, name=name)

    @staticmethod
    def find_by_name(layout, name):
        return net_pb2.NetLookupMessage(layout=layout.msg, name=name)


class Net(LayoutObj):
    """Class representing net."""

    layout_obj_type = LayoutObjType.NET_CLASS

    @staticmethod
    def create(layout, name):
        """Create a net.

        Parameters
        ----------
        layout : Layout
        name : str

        Returns
        -------
        Net
        """
        return Net(get_net_stub().Create(_QueryBuilder.create(layout, name)))

    @staticmethod
    def find_by_name(layout, name):
        """Find a net in a layout by name.

        Parameters
        ----------
        layout : Layout
        name : str

        Returns
        -------
        Net
        """
        return Net(get_net_stub().FindByName(_QueryBuilder.find_by_name(layout, name)))
