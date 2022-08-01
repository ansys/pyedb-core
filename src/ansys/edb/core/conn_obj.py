"""ConnObj."""
from ansys.api.edb.v1 import connectable_pb2

from ansys.edb.core.layout_obj import LayoutObj, LayoutObjType
import ansys.edb.core.messages as messages
from ansys.edb.session import StubAccessor, StubType


class _QueryBuilder:
    @staticmethod
    def find_id_layout_obj_message(layout, type, id):
        return connectable_pb2.FindByIdLayoutObjMessage(
            layout=layout.msg, type=type.value, id_msg=messages.edb_internal_id_message(id)
        )

    @staticmethod
    def set_net_message(target, net):
        return connectable_pb2.SetNetMessage(
            target=target.msg,
            net=messages.net_ref_message(net),
        )


class ConnObj(LayoutObj):
    """Base class representing ConnObj."""

    __stub = StubAccessor(StubType.connectable)
    layout_obj_type = LayoutObjType.INVALID_LAYOUT_OBJ

    @classmethod
    def find_by_id(cls, layout, uid):
        """Find a Connectable object by Database ID.

        Parameters
        ----------
        layout
             The owning Layout.
        uid
            Database ID
        Returns
        -------
            Connectable object (Net/Cell/Primitive/etc.) of given ID.
        """
        return cls(
            cls.__stub.FindByIdAndType(
                _QueryBuilder.find_id_layout_obj_message(
                    layout=layout, type=cls.layout_obj_type, id=uid
                )
            )
        )

    @property
    def edb_uid(self):
        """Get the unique, persistent ID for the Connectable object.

        Returns
        -------
            int
                This id is unique across the all Connectable objects in the cell
                and persistent across closing and reopening the database.
        """
        return self.__stub.GetId(self.msg).id

    @property
    def component(self):
        """Get the Component of the connectable object.

        Returns
        -------
            ansys.edb.hierarchy.ComponentGroup
                Component group of the connectable object.
        """
        from ansys.edb.hierarchy import ComponentGroup

        return ComponentGroup(self.__stub.GetComponent(self.msg))

    @property
    def group(self):
        """Get the group of the connectable object.

        Returns
        -------
        ansys.edb.hierarchy.Group
            Group of the connectable object.
        """
        from ansys.edb.hierarchy import Group

        return Group(self.__stub.GetGroup(self.msg))

    @group.setter
    def group(self, group):
        """Set the group of the connectable object.

        Parameters
        ----------
        group: ansys.edb.hierarchy.Group
            Group of the layout object.
        """
        self.__stub.SetGroup(messages.pointer_property_message(target=self, value=group))

    @property
    def net(self):
        """Get the net of the connectable object.

        Returns
        -------
        ansys.edb.net.Net
            Net of the connectable object.
        """
        from ansys.edb.net import Net

        return Net(self.__stub.GetNet(self.msg))

    @net.setter
    def net(self, net):
        """Set the net of the connectable object.

        Parameters
        ----------
        net: ansys.edb.net.Net or str
            A Net object(or Net name) to associate this connectable with.
        """
        self.__stub.SetNet(_QueryBuilder.set_net_message(self, net))
