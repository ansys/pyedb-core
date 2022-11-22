"""ConnObj."""
from ansys.api.edb.v1 import connectable_pb2

from ansys.edb.core import layout_obj, messages
from ansys.edb.edb_defs import LayoutObjType
from ansys.edb.layout import mcad_model as mm
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


class ConnObj(layout_obj.LayoutObj):
    """Base class representing ConnObj."""

    __stub: ConnectableServiceStub = StubAccessor(StubType.connectable)
    layout_obj_type = LayoutObjType.INVALID_LAYOUT_OBJ

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

            if get_client_prim_type_from_class() == primitive.Primitive(edb_obj_msg).primitive_type:
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
        """Find a :term:`Connectable` object by Database ID.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.layout.Layout>`
            The owning Layout.
        uid : int
             Database ID

        Returns
        -------
        :term:`Connectable`
            Connectable of the given uid.
        """
        found_edb_obj_msg = cls.__stub.FindByIdAndType(
            _QueryBuilder.find_id_layout_obj_message(
                layout=layout, type=cls.layout_obj_type, id=uid
            )
        )
        return cls._validate_edb_obj_type(found_edb_obj_msg)

    @property
    def edb_uid(self):
        """:obj:`int`: The unique, persistent ID for the :term:`Connectable` object.

        This id is unique across the all :term:`Connectable` objects in the cell and persistent across closing and \
        reopening the database.

        Read-Only.
        """
        return self.__stub.GetId(self.msg).id

    @property
    def component(self):
        """:class:`ComponentGroup <ansys.edb.hierarchy.ComponentGroup>`: Component of the :term:`Connectable` object."""
        from ansys.edb.hierarchy import ComponentGroup

        return ComponentGroup(self.__stub.GetComponent(self.msg))

    @property
    def group(self):
        """:class:`Group <ansys.edb.hierarchy.Group>`: Group of the :term:`Connectable` object."""
        from ansys.edb.hierarchy import Group

        return Group(self.__stub.GetGroup(self.msg)).cast()

    @group.setter
    def group(self, group):
        """Set the group of the connectable object."""
        self.__stub.SetGroup(messages.pointer_property_message(target=self, value=group))

    @property
    def net(self):
        """:class:`Net <ansys.edb.net.Net>`: Net of the :term:`Connectable` object.

        This property can be set with :class:`Net <ansys.edb.net.Net>`, str, None.
        """
        from ansys.edb.net import Net

        return Net(self.__stub.GetNet(self.msg))

    @net.setter
    def net(self, net):
        """Set the net of the connectable object."""
        self.__stub.SetNet(_QueryBuilder.set_net_message(self, net))

    def create_stride(self):
        """Create a stride model.

        Returns
        -------
        :class:`McadModel <ansys.edb.layout.McadModel>`
        """
        return mm.McadModel.create_stride(connectable=self)

    def create_hfss(self):
        """Create a HFSS model.

        Returns
        -------
        :class:`McadModel <ansys.edb.layout.McadModel>`
        """
        return mm.McadModel.create_hfss(connectable=self)

    def create_3d_comp(self):
        """Create a 3dComp model.

        Returns
        -------
        :class:`McadModel <ansys.edb.layout.McadModel>`
        """
        return mm.McadModel.create_3d_comp(connectable=self)

    @property
    def is_mcad(self):
        """:obj:`bool`: True if this is a Mcad Model.

        Read-Only.
        """
        return mm.McadModel.is_mcad(self)

    @property
    def is_mcad_stride(self):
        """:obj:`bool`: True if this is a Stride Mcad Model.

        Read-Only.
        """
        return mm.McadModel.is_mcad_stride(self)

    @property
    def is_mcad_hfss(self):
        """:obj:`bool`: True if this is a HFSS Mcad Model.

        Read-Only.
        """
        return mm.McadModel.is_mcad_hfss(self)

    @property
    def is_mcad_3d_comp(self):
        """:obj:`bool`: True if this is a 3D Comp Mcad Model.

        Read-Only.
        """
        return mm.McadModel.is_mcad_3d_comp(self)
