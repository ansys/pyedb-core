"""Net class."""

import ansys.api.edb.v1.netclass_pb2 as nc_pb2

import ansys.edb.core.interface.grpc.messages as messages
from ansys.edb.core.layout.layout_obj import LayoutObj
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.edb_errors import handle_grpc_exception


class _QueryBuilder:
    @staticmethod
    def create(layout, name):
        return nc_pb2.NetClassCreationMessage(layout=layout.msg, name=name)


class NetClass(LayoutObj):
    """Net class."""

    __stub = StubAccessor(StubType.netclass)
    layout_type = layout_type = LayoutObjType.NET_CLASS

    @classmethod
    @handle_grpc_exception
    def create(cls, layout, name):
        """
        Create net class.

        Parameters
        ----------
        layout : Layout
        name : str

        Returns
        -------
        NetClass
        """
        return NetClass(cls.__stub.Create(_QueryBuilder.create(layout, name)))

    @classmethod
    @handle_grpc_exception
    def find(cls, layout, name):
        """
        Find net class by name.

        Parameters
        ----------
        layout : Layout
        name : str

        Returns
        -------
        NetClass
        """
        return NetClass(cls.__stub.FindByName(messages.edb_obj_name_message(layout, name)))

    @property
    def name(self):
        """
        Name of net class.

        Returns
        -------
        str
        """
        return self.__stub.GetName(self.msg).value

    @property
    def description(self):
        """
        Return description of net class.

        Returns
        -------
        str
        """
        return self.__stub.GetDescription(self.msg).value

    @name.setter
    @handle_grpc_exception
    def name(self, newname):
        """
        Set name of net class.

        Parameters
        ----------
        newname : str

        """
        return self.__stub.SetName(messages.edb_obj_name_message(self.msg, newname))

    @description.setter
    @handle_grpc_exception
    def description(self, newdesc):
        """
        Set description of net class.

        Parameters
        ----------
        newdesc : str

        """
        return self.__stub.SetDescription(messages.string_property_message(self, newdesc))

    @property
    def is_power_ground(self):
        """Return whether this netclass is power or ground.

        Returns
        -------
        bool
        """
        return self.__stub.IsPowerGround(messages.edb_obj_message(self.msg)).value

    @handle_grpc_exception
    def add_net(self, net):
        """
        Add net to netclass.

        Parameters
        ----------
        net : Net

        """
        return self.__stub.AddNet(nc_pb2.NetClassEditMessage(netclass=self.msg, net=net.msg))

    @handle_grpc_exception
    def remove_net(self, net):
        """
        Remove net from netclass.

        Parameters
        ----------
        net : Net

        """
        self.__stub.RemoveNet(nc_pb2.NetClassEditMessage(netclass=self.msg, net=net.msg))

    @handle_grpc_exception
    def contains_net(self, net):
        """
        Find if net exists in netclass.

        Parameters
        ----------
        net : Net

        Returns
        -------
        bool
        """
        return self.__stub.ContainsNet(
            nc_pb2.NetClassEditMessage(netclass=self.msg, net=net.msg)
        ).value
