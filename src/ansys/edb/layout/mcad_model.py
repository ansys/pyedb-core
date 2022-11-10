"""Mcad Model."""

from ansys.edb.core import ObjBase, messages, parser
from ansys.edb.hierarchy import CellInstance
from ansys.edb.session import McadModelServiceStub, StubAccessor, StubType


class McadModel(ObjBase):
    """Class representing a Mcad Model."""

    __stub: McadModelServiceStub = StubAccessor(StubType.mcad_model)

    @classmethod
    def create_stride(cls, connectable=None, layout=None, filename=None):
        """Create a stride model.

        Parameters
        ----------
        connectable : :term:`Connectable`, optional
        layout : :class:`Layout <ansys.edb.layout.Layout>`, optional
        filename : str, optional

        Returns
        -------
        McadModel
        """
        return cls(
            cls.__stub.CreateStride(
                messages.mcad_model_creation_message(connectable, layout, filename)
            )
        )

    @classmethod
    def create_hfss(cls, connectable=None, layout=None, filename=None, design=None):
        """Create a HFSS model.

        Parameters
        ----------
        connectable : :term:`Connectable`, optional
        layout : :class:`Layout <ansys.edb.layout.Layout>`, optional
        filename : str, optional
        design : str, optional

        Returns
        -------
        McadModel
        """
        return cls(
            cls.__stub.CreateHfss(
                messages.mcad_model_hfss_creation_message(connectable, layout, filename, design)
            )
        )

    @classmethod
    def create_3d_comp(cls, connectable=None, layout=None, filename=None):
        """Create a 3dComp model.

        Parameters
        ----------
        connectable : :term:`Connectable`, optional
        layout : :class:`Layout <ansys.edb.layout.Layout>`, optional
        filename : str, optional

        Returns
        -------
        McadModel
        """
        return cls(
            cls.__stub.Create3dComp(
                messages.mcad_model_creation_message(connectable, layout, filename)
            )
        )

    @classmethod
    def is_mcad(cls, connectable):
        """Get if a connectable object is Mcad model.

        Parameters
        ----------
        connectable : :term:`Connectable`

        Returns
        -------
        bool
        """
        return cls.__stub.IsMcad(messages.edb_obj_message(connectable))

    @classmethod
    def is_mcad_stride(cls, connectable):
        """Get if a connectable object is Stride Mcad model.

        Parameters
        ----------
        connectable : :term:`Connectable`

        Returns
        -------
        bool
        """
        return cls.__stub.IsMcadStride(messages.edb_obj_message(connectable))

    @classmethod
    def is_mcad_hfss(cls, connectable):
        """Get if a connectable object is HFSS Mcad model.

        Parameters
        ----------
        connectable : :term:`Connectable`

        Returns
        -------
        bool
        """
        return cls.__stub.IsMcadHfss(messages.edb_obj_message(connectable))

    @classmethod
    def is_mcad_3d_comp(cls, connectable):
        """Get if a connectable object is 3dComp Mcad model.

        Parameters
        ----------
        connectable : :term:`Connectable`

        Returns
        -------
        bool
        """
        return cls.__stub.IsMcad3dComp(messages.edb_obj_message(connectable))

    @property
    def cell_instance(self):
        """:class:`CellInstance <ansys.edb.hierarchy.CellInstance>` Cell instance of a Mcad model."""
        return CellInstance(self.__stub.GetCellInst(messages.edb_obj_message(self)))

    @property
    def model_name(self):
        """:obj:`str` Model name of a Mcad model."""
        return self.__stub.GetModelName(messages.edb_obj_message(self)).value

    @property
    def design_name(self):
        """:obj:`str` Design name of a Mcad model."""
        return self.__stub.GetDesignName(messages.edb_obj_message(self)).value

    @property
    def origin(self):
        """:class:`Point3DData <ansys.edb.geometry.Point3DData>` Origin 3D point of a Mcad model."""
        return self.__stub.GetOrigin(messages.edb_obj_message(self))

    @origin.setter
    def origin(self, pnt):
        self.__stub.SetOrigin(messages.mcad_model_origin_message(self, pnt))

    @property
    def rotation(self):
        r""":obj:`tuple`\[:class:`Point3DData <ansys.edb.geometry.Point3DData>`, :class:`Point3DData <ansys.edb.geometry.Point3DData>`, :obj:`float`\] Rotation from/to axis and angle."""  # noqa
        msg = self.__stub.GetRotation(messages.edb_obj_message(self))
        return (
            parser.to_point3d_data(msg.axis_from),
            parser.to_point3d_data(msg.axis_to),
            msg.angle.value,
        )

    def set_rotation(self, axis_from, axis_to, angle):
        """Set rotation from/to axis and angle in radians.

        Parameters
        ----------
        axis_from : :class:`Point3DData <ansys.edb.geometry.Point3DData>`
        axis_to : :class:`Point3DData <ansys.edb.geometry.Point3DData>`
        angle : float
        """
        self.__stub.SetRotation(messages.mcad_model_set_rotation_message(axis_from, axis_to, angle))

    @property
    def scale(self):
        """:obj:`float` The scale of a Mcad model."""
        return self.__stub.GetScale(messages.edb_obj_message(self)).value

    @scale.setter
    def scale(self, scale):
        self.__stub.SetScale(messages.double_property_message(self, scale))

    def material(self, index):
        """Get material name of a Mcad model part at index.

        Parameters
        ----------
        index : int

        Returns
        -------
        str
        """
        return self.__stub.GetMaterial(messages.int_property_message(self, index)).value

    def set_material(self, index, material):
        """Set material name of a Mcad model part at index.

        Parameters
        ----------
        index : int
        material : str
        """
        self.__stub.SetMaterial(messages.mcad_model_string_message(self, index, material))

    def visible(self, index):
        """Get visibility of a Mcad model part at index.

        Parameters
        ----------
        index : int

        Returns
        -------
        bool
        """
        return self.__stub.GetVisible(messages.int_property_message(self, index)).value

    def set_visible(self, index, visible):
        """Set visibility of a Mcad model part at index.

        Parameters
        ----------
        index : int
        visible : bool
        """
        self.__stub.SetVisible(messages.mcad_model_bool_message(self, index, visible))

    def modeled(self, index):
        """Get if a Mcad model part at index is modeled.

        Parameters
        ----------
        index : int

        Returns
        -------
        bool
        """
        return self.__stub.GetModeled(messages.int_property_message(self, index)).value

    def set_modeled(self, index, modeled):
        """Set if a Mcad model part at index is modeled.

        Parameters
        ----------
        index : int
        modeled : bool
        """
        self.__stub.SetModeled(messages.mcad_model_bool_message(self, index, modeled))

    def part_count(self):
        """Mcad model part count.

        Returns
        -------
        int
        """
        return self.__stub.GetPartCount(messages.edb_obj_message(self)).value

    def part_index(self, name):
        """Index of a Mcad model part with the specified name.

        Parameters
        ----------
        name : str

        Returns
        -------
        int
        """
        return self.__stub.GetPartIndex(messages.string_property_message(self, name)).value

    def part_name(self, index):
        """Name of a Mcad model part at the specified index.

        Parameters
        ----------
        index : int

        Returns
        -------
        str
        """
        return self.__stub.GetPartName(messages.int_property_message(self, index)).value

    def apply_changes(self):
        """Apply changes to Mcad model."""
        self.__stub.ApplyChanges(messages.edb_obj_message(self))
