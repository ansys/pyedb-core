"""Net class."""

import ansys.api.edb.v1.netclass_pb2 as nc_pb2

from ansys.edb.core import layout_obj, messages
from ansys.edb.edb_defs import LayoutObjType
from ansys.edb.session import StubAccessor, StubType


class _QueryBuilder:
    @staticmethod
    def create(layout, name):
        return nc_pb2.NetClassCreationMessage(layout=layout.msg, name=name)


class NetClass(layout_obj.LayoutObj):
    """Net class."""

    __stub = StubAccessor(StubType.netclass)
    layout_obj_type = LayoutObjType.NET_CLASS

    @classmethod
    def create(cls, layout, name):
        """
        Create net class.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.layout.Layout>`
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
        layout : :class:`Layout <ansys.edb.layout.Layout>`
            Layout being searched for net class.
        name : str
            Name of net class being searched for.

        Returns
        -------
        NetClass
            Net class matching the requested name. Check the returned net class's \
            :obj:`is_null <ansys.edb.net.NetClass.is_null>` property to see if it exists.
        """
        return NetClass(cls.__stub.FindByName(messages.edb_obj_name_message(layout, name)))

    @property
    def name(self):
        """:obj:`str`: Name of this object."""
        return self.__stub.GetName(self.msg).value

    @name.setter
    def name(self, newname):
        self.__stub.SetName(messages.edb_obj_name_message(self.msg, newname))

    @property
    def description(self):
        """:obj:`str` : Description of this object."""
        return self.__stub.GetDescription(self.msg).value

    @description.setter
    def description(self, newdesc):
        self.__stub.SetDescription(messages.string_property_message(self, newdesc))

    @property
    def is_power_ground(self):
        """:class:`bool`: True if object belongs to Power/Ground :class:`NetClass`.

        Read-Only.
        """
        return self.__stub.IsPowerGround(messages.edb_obj_message(self.msg)).value

    @property
    def nets(self):
        """:obj:`list` of :class:`Net <ansys.edb.net.Net>`: List of nets in this object.

        Read-Only.
        """
        from ansys.edb.net.net import Net

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
