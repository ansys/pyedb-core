"""ConnObj."""
from ansys.api.edb.v1 import connectable_pb2

from ansys.edb.core.layout_obj import LayoutObj, LayoutObjType
import ansys.edb.core.messages as messages
from ansys.edb.session import ConnectableServiceStub, StubAccessor, StubType


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

    __stub: ConnectableServiceStub = StubAccessor(StubType.connectable)

    @classmethod
    def _validate_edb_obj_type(cls, edb_obj_msg):
        """Verify that the object type received from the server matches the object type requested by the client."""
        client_obj = cls(edb_obj_msg)
        if cls.layout_obj_type == LayoutObjType.PRIMITIVE:
            import ansys.edb.primitive as primitive

            def get_client_prim_type_from_class():
                if cls == primitive.Circle:
                    return primitive.PrimitiveType.CIRCLE
                if cls == primitive.Rectangle:
                    return primitive.PrimitiveType.RECTANGLE
                if cls == primitive.Polygon:
                    return primitive.PrimitiveType.POLYGON
                if cls == primitive.Path:
                    return primitive.PrimitiveType.PATH
                if cls == primitive.Bondwire:
                    return primitive.PrimitiveType.BONDWIRE
                if cls == primitive.BoardBendDef:
                    return primitive.PrimitiveType.BOARD_BEND
                if cls == primitive.Text:
                    return primitive.PrimitiveType.TEXT

            if (
                get_client_prim_type_from_class()
                == primitive.Primitive(edb_obj_msg).get_primitive_type()
            ):
                return client_obj
        elif cls.layout_obj_type == LayoutObjType.TERMINAL:
            import ansys.edb.terminal as terminal

            server_term_type = terminal.Terminal(edb_obj_msg).type
            if client_obj.type == server_term_type:
                return client_obj
        else:
            return client_obj
        return cls(None)

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
        found_edb_obj_msg = cls.__stub.FindByIdAndType(
            _QueryBuilder.find_id_layout_obj_message(
                layout=layout, type=cls.layout_obj_type, id=uid
            )
        )
        return cls._validate_edb_obj_type(found_edb_obj_msg)

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
