"""Connection object."""
from ansys.api.edb.v1 import connectable_pb2

from ansys.edb.core.edb_defs import LayoutObjType
from ansys.edb.core.inner import layout_obj, messages
from ansys.edb.core.layout import mcad_model as mm
from ansys.edb.core.session import ConnectableServiceStub, StubAccessor, StubType


class ConnObj(layout_obj.LayoutObj):
    """Provides the base class representing the connection object."""

    __stub: ConnectableServiceStub = StubAccessor(StubType.connectable)
    layout_obj_type = LayoutObjType.INVALID_LAYOUT_OBJ

    @classmethod
    def _validate_edb_obj_type(cls, edb_obj_msg):
        """Verify that the object type received from the server matches the object type requested by the client."""
        client_obj = cls(edb_obj_msg)
        if cls.layout_obj_type == LayoutObjType.PRIMITIVE:
            import ansys.edb.core.primitive.primitive as primitive

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
            from ansys.edb.core.terminal import terminals

            server_term_type = terminals.Terminal(edb_obj_msg).type
            if client_obj.type == server_term_type:
                return client_obj
        else:
            return client_obj
        return cls(None)

    @classmethod
    def find_by_id(cls, layout, uid):
        """Find a :term:`Connectable` object by database ID in a given layout.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to search for the :term:`Connectable` object.
        uid : int
            Database ID.

        Returns
        -------
        :term:`Connectable`
            Connectable object with the given database ID.
        """
        found_edb_obj_msg = cls.__stub.FindByIdAndType(
            connectable_pb2.FindByIdLayoutObjMessage(
                layout=layout.msg,
                type=cls.layout_obj_type.value,
                id_msg=messages.edb_internal_id_message(uid),
            )
        )
        return cls._validate_edb_obj_type(found_edb_obj_msg)

    @property
    def edb_uid(self):
        """:obj:`int`: Unique, persistent ID for the :term:`Connectable` object.

        This ID is unique across all :term:`Connectable` objects in the cell and persistent across closing and \
        reopening the database.

        This property is read-only.
        """
        return self.__stub.GetId(self.msg).id

    @property
    def component(self):
        """:class:`.ComponentGroup`: \
        Component of the :term:`Connectable` object."""
        from ansys.edb.core.hierarchy.component_group import ComponentGroup

        return ComponentGroup(self.__stub.GetComponent(self.msg))

    @property
    def group(self):
        """:class:`.Group` object."""
        from ansys.edb.core.hierarchy.group import Group

        return Group(self.__stub.GetGroup(self.msg)).cast()

    @group.setter
    def group(self, group):
        self.__stub.SetGroup(messages.pointer_property_message(target=self, value=group))

    @property
    def net(self):
        """:class:`.Net`: Net of the :term:`Connectable` object.

        This property can be set with a :class:`.Net` instance, a string, or ``None``.
        """
        from ansys.edb.core.net.net import Net

        return Net(self.__stub.GetNet(self.msg))

    @net.setter
    def net(self, net):
        self.__stub.SetNet(
            connectable_pb2.SetNetMessage(
                target=self.msg,
                net=messages.net_ref_message(net),
            )
        )

    def create_stride(self):
        """Create a Stride model from an MCAD file.

        Returns
        -------
        :class:`.McadModel`
            Stride model created.
        """
        return mm.McadModel.create_stride(connectable=self)

    def create_hfss(self):
        """Create an HFSS model from an MCAD file.

        Returns
        -------
        :class:`.McadModel`
            HFSS model created.
        """
        return mm.McadModel.create_hfss(connectable=self)

    def create_3d_comp(self):
        """Create a 3D composite model from an MCAD file.

        Returns
        -------
        :class:`.McadModel`
            3D composite model created.
        """
        return mm.McadModel.create_3d_comp(connectable=self)

    @property
    def is_mcad(self):
        """:obj:`bool`: Flag indicating if this is an MCAD model.

        This property is read-only.
        """
        return mm.McadModel.is_mcad(self)

    @property
    def is_mcad_stride(self):
        """:obj:`bool`: Flag indicating if this is a Stride MCAD model.

        This property is read-only.
        """
        return mm.McadModel.is_mcad_stride(self)

    @property
    def is_mcad_hfss(self):
        """:obj:`bool`: Flag indicating if this is an HFSS MCAD model.

        This property is read-only.
        """
        return mm.McadModel.is_mcad_hfss(self)

    @property
    def is_mcad_3d_comp(self):
        """:obj:`bool`: Flag indicating if this is a 3D composite MCAD model.

        This property is read-only.
        """
        return mm.McadModel.is_mcad_3d_comp(self)
