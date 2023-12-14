"""Net class."""

import ansys.api.edb.v1.netclass_pb2 as nc_pb2

from ansys.edb.core.edb_defs import LayoutObjType
from ansys.edb.core.inner.layout_obj import LayoutObj
from ansys.edb.core.inner.messages import (
    edb_obj_message,
    edb_obj_name_message,
    string_property_message,
)
from ansys.edb.core.session import StubAccessor, StubType


class _QueryBuilder:
    @staticmethod
    def create(layout, name):
        return nc_pb2.NetClassCreationMessage(layout=layout.msg, name=name)


class NetClass(LayoutObj):
    """Net class."""

    __stub = StubAccessor(StubType.netclass)
    layout_obj_type = LayoutObjType.NET_CLASS

    @classmethod
    def create(cls, layout, name):
        """
        Create net class.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.core.layout.Layout>`
            Layout containing new net class.
        name : str
            Name of the new net class.

        Returns
        -------
        NetClass
            Newly created net class.
        """
        return NetClass(cls.__stub.Create(_QueryBuilder.create(layout, name)))

    @classmethod
    def find_by_name(cls, layout, name):
        """
        Find net class by name.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.core.layout.Layout>`
            Layout being searched for net class.
        name : str
            Name of net class being searched for.

        Returns
        -------
        NetClass
            Net class matching the requested name. Check the returned net class's \
            :obj:`is_null <ansys.edb.core.net.NetClass.is_null>` property to see if it exists.
        """
        return NetClass(cls.__stub.FindByName(edb_obj_name_message(layout, name)))

    @property
    def name(self):
        """:obj:`str`: Name of this object."""
        return self.__stub.GetName(self.msg).value

    @name.setter
    def name(self, newname):
        self.__stub.SetName(edb_obj_name_message(self.msg, newname))

    @property
    def description(self):
        """:obj:`str` : Description of this object."""
        return self.__stub.GetDescription(self.msg).value

    @description.setter
    def description(self, newdesc):
        self.__stub.SetDescription(string_property_message(self, newdesc))

    @property
    def is_power_ground(self):
        """:class:`bool`: True if object belongs to Power/Ground :class:`NetClass`.

        Read-Only.
        """
        return self.__stub.IsPowerGround(edb_obj_message(self.msg)).value

    @property
    def nets(self):
        """:obj:`list` of :class:`Net <ansys.edb.core.net.Net>`: List of nets in this object.

        Read-Only.
        """
        from ansys.edb.core.net.net import Net

        nets = self.__stub.GetNets(self.msg).items
        return [Net(n) for n in nets]

    def add_net(self, net):
        """
        Add net to this this object.

        Parameters
        ----------
        net : Net
            Net to add
        """
        return self.__stub.AddNet(nc_pb2.NetClassEditMessage(netclass=self.msg, net=net.msg))

    def remove_net(self, net):
        """
        Remove net from this object.

        Parameters
        ----------
        net : Net
            Net to remove
        """
        self.__stub.RemoveNet(nc_pb2.NetClassEditMessage(netclass=self.msg, net=net.msg))

    def contains_net(self, net):
        """
        Check if net exists in this object.

        Parameters
        ----------
        net : Net
            Net to check for.

        Returns
        -------
        bool
            True if net is in this object
        """
        return self.__stub.ContainsNet(
            nc_pb2.NetClassEditMessage(netclass=self.msg, net=net.msg)
        ).value
