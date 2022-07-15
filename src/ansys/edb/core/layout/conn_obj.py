"""ConnObj."""
from ansys.api.edb.v1 import connectable_pb2

import ansys.edb.core.hierarchy as hierarchy
from ansys.edb.core.interface.grpc import messages
from ansys.edb.core.layout.layout_obj import LayoutObj, LayoutObjType
from ansys.edb.core.net import Net
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.edb_errors import handle_grpc_exception


class _QueryBuilder:
    @staticmethod
    def find_id_layout_obj_message(layout, type, id):
        return connectable_pb2.FindByIdLayoutObjMessage(layout=layout.msg, type=type.value, id=id)

    @staticmethod
    def set_net_message(target, net):
        return connectable_pb2.FindByIdLayoutObjMessage(
            target=target.msg,
            net=messages.net_ref_message(net),
        )


class ConnObj(LayoutObj):
    """Base class representing ConnObj."""

    __stub = StubAccessor(StubType.connectable)

    @property
    @handle_grpc_exception
    def obj_type(self):
        """Get the layout object type.

        Returns
        -------
            LayoutObjType enum of the connectable.
        """
        return LayoutObjType(self.__stub.GetObjType(self.msg).type)

    @staticmethod
    @handle_grpc_exception
    def find_by_id(layout, uid):
        """Find a Connectable object by Database ID.

        Parameters
        ----------
        layout
             The owning Layout.
        uid
            Database ID
        Returns
        -------
            Connectable object of given ID.
        """
        return ConnObj(
            StubAccessor(StubType.connectable)
            .__get__()
            .FindById(messages.int_property_message(target=layout, value=uid))
            .msg
        )

    @staticmethod
    @handle_grpc_exception
    def find_by_id_and_type(layout, type, id):
        """Find a Connectable object by Database ID and type.

        Parameters
        ----------
        layout
            The owning Layout.
        type
            Cell type
        id
            Database ID

        Returns
        -------
            Connectable object of given ID.
        """
        return ConnObj(
            StubAccessor(StubType.connectable)
            .__get__()
            .FindByIdAndType(_QueryBuilder.find_id_layout_obj_message(layout, type, id))
            .msg
        )

    @property
    @handle_grpc_exception
    def edb_uid(self):
        """Get the unique, persistent ID for the Connectable object.

        Returns
        -------
            int
                This id is unique across the all Connectable objects in the cell
                and persistent across closing and reopening the database.
        """
        return self.__stub.GetId(self.msg)

    @property
    @handle_grpc_exception
    def component(self):
        """Get the Component of the connectable object.

        Returns
        -------
            ConnObj
                Component of the connectable object.
        """
        return ConnObj(self.__stub.GetComponent(self.msg))

    @property
    @handle_grpc_exception
    def group(self):
        """Get the group of the connectable object.

        Returns
        -------
        Group
            Group of the connectable object.
        """
        return hierarchy.Group(self.__stub.GetGroup(self.msg))

    @group.setter
    @handle_grpc_exception
    def group(self, group):
        """Set the group of the connectable object.

        Parameters
        ----------
        group: Group
            Group of the layout object.
        """
        self.__stub.SetGroup(messages.pointer_property_message(target=self, value=group))

    @property
    @handle_grpc_exception
    def net(self):
        """Get the net of the connectable object.

        Returns
        -------
        Net
            Net of the connectable object.
        """
        return Net(self.__stub.GetNet(self.msg))

    @net.setter
    @handle_grpc_exception
    def net(self, net):
        """Set the net of the connectable object.

        Parameters
        ----------
        net: Net
            A Net object to associate this connectable with.
        """
        self.__stub.SetNet(_QueryBuilder.set_net_message(self, net))
