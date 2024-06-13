"""Net class."""

import ansys.api.edb.v1.netclass_pb2 as nc_pb2

from ansys.edb.core.edb_defs import LayoutObjType
from ansys.edb.core.inner import layout_obj, messages
from ansys.edb.core.session import StubAccessor, StubType


class NetClass(layout_obj.LayoutObj):
    """Represents a net class."""

    __stub = StubAccessor(StubType.netclass)
    layout_obj_type = LayoutObjType.NET_CLASS

    @classmethod
    def create(cls, layout, name):
        """
        Create a net.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the net class in.
        name : str
            Name of the net.

        Returns
        -------
        NetClass
            Net class created.
        """
        return NetClass(
            cls.__stub.Create(nc_pb2.NetClassCreationMessage(layout=layout.msg, name=name))
        )

    @classmethod
    def find_by_name(cls, layout, name):
        """
        Find a net class by name in a given layout.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to search for the net class.
        name : str
            Name of the net class.

        Returns
        -------
        NetClass
            Net class found. Check the :obj:`is_null <s.NetClass.is_null>` property
            of the returned net class to see if it exists.
        """
        return NetClass(cls.__stub.FindByName(messages.edb_obj_name_message(layout, name)))

    @property
    def name(self):
        """:obj:`str`: Name of the net class."""
        return self.__stub.GetName(self.msg).value

    @name.setter
    def name(self, newname):
        self.__stub.SetName(messages.edb_obj_name_message(self.msg, newname))

    @property
    def description(self):
        """:obj:`str` : Description of the net class."""
        return self.__stub.GetDescription(self.msg).value

    @description.setter
    def description(self, newdesc):
        self.__stub.SetDescription(messages.string_property_message(self, newdesc))

    @property
    def is_power_ground(self):
        """:class:`bool`: Flag indicating in the net class belongs to the power/ground \
            :class:`NetClass` class.

        This property is read-only.
        """
        return self.__stub.IsPowerGround(messages.edb_obj_message(self.msg)).value

    @property
    def nets(self):
        """:obj:`list` of :class:`.Net`: List of nets in the net class.

        This property is read-only.
        """
        from ansys.edb.core.net.net import Net

        nets = self.__stub.GetNets(self.msg).items
        return [Net(n) for n in nets]

    def add_net(self, net):
        """
        Add a net to the net class.

        Parameters
        ----------
        net : Net
            Net to add.
        """
        return self.__stub.AddNet(nc_pb2.NetClassEditMessage(netclass=self.msg, net=net.msg))

    def remove_net(self, net):
        """
        Remove a net from the net class.

        Parameters
        ----------
        net : Net
            Net to remove.
        """
        self.__stub.RemoveNet(nc_pb2.NetClassEditMessage(netclass=self.msg, net=net.msg))

    def contains_net(self, net):
        """
        Determine if a net exists in the net class.

        Parameters
        ----------
        net : Net
            Net to search for.

        Returns
        -------
        bool
            ``True`` if the net is in the net class, ``False`` otherwise.
        """
        return self.__stub.ContainsNet(
            nc_pb2.NetClassEditMessage(netclass=self.msg, net=net.msg)
        ).value
