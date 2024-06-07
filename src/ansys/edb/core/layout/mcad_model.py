"""MCAD model."""

from ansys.edb.core.inner import ObjBase, messages, parser
from ansys.edb.core.session import McadModelServiceStub, StubAccessor, StubType


class McadModel(ObjBase):
    """Class representing an MCAD mdel."""

    __stub: McadModelServiceStub = StubAccessor(StubType.mcad_model)

    @classmethod
    def create_stride(cls, connectable=None, layout=None, filename=None):
        """Create a Stride model.

        This method makes a call directly on a :term:`Connectable` or
        :func:`Layout <ansys.edb.core.layout.layout.Layout.create_stride>`.
        """
        return cls(
            cls.__stub.CreateStride(
                messages.mcad_model_creation_message(connectable, layout, filename)
            )
        )

    @classmethod
    def create_hfss(cls, connectable=None, layout=None, filename=None, design=None):
        """Create an HFSS model.

        This method makes a call directly on a :term:`Connectable` or
        :func:`Layout <ansys.edb.core.layout.layout.Layout.create_hfss>`.
        """
        return cls(
            cls.__stub.CreateHfss(
                messages.mcad_model_hfss_creation_message(connectable, layout, filename, design)
            )
        )

    @classmethod
    def create_3d_comp(cls, connectable=None, layout=None, filename=None):
        """Create a 3D component model.

        This method makes a call directly on a :term:`Connectable` or
        :func:`Layout <ansys.edb.core.layout.Layout.create_3d_comp>`.
        """
        return cls(
            cls.__stub.Create3dComp(
                messages.mcad_model_creation_message(connectable, layout, filename)
            )
        )

    @classmethod
    def is_mcad(cls, connectable):
        """Determine if a connectable object is an MCAD model.

        This method makes a call directly on a :term:`Connectable`.
        """
        return cls.__stub.IsMcad(messages.edb_obj_message(connectable))

    @classmethod
    def is_mcad_stride(cls, connectable):
        """Determine if a connectable object is a Stride model.

        This method makes a call directly on a :term:`Connectable`.
        """
        return cls.__stub.IsMcadStride(messages.edb_obj_message(connectable))

    @classmethod
    def is_mcad_hfss(cls, connectable):
        """Determine if a connectable object is an HFSS model.

        This method makes a call directly on a :term:`Connectable`.
        """
        return cls.__stub.IsMcadHfss(messages.edb_obj_message(connectable))

    @classmethod
    def is_mcad_3d_comp(cls, connectable):
        """Determine if a connectable object is a 3D component model.

        This method makes a call directly on a :term:`Connectable`.
        """
        return cls.__stub.IsMcad3dComp(messages.edb_obj_message(connectable))

    @property
    def cell_instance(self):
        """:class:`.CellInstance`: Cell instance \
        of the MCAD model.

        This property is read-only.
        """
        from ansys.edb.core.hierarchy import cell_instance

        return cell_instance.CellInstance(self.__stub.GetCellInst(messages.edb_obj_message(self)))

    @property
    def model_name(self):
        """:obj:`str`: Name of the MCAD model.

        This property is read-only.
        """
        return self.__stub.GetModelName(messages.edb_obj_message(self)).value

    @property
    def design_name(self):
        """:obj:`str`: Design name of the MCAD model.

        This property is read-only.
        """
        return self.__stub.GetDesignName(messages.edb_obj_message(self)).value

    @property
    def origin(self):
        """:class:`.Point3DData`: \
        Origin 3D point of the MCAD model."""
        return self.__stub.GetOrigin(messages.edb_obj_message(self))

    @origin.setter
    def origin(self, pnt):
        self.__stub.SetOrigin(messages.point_3d_property_message(self, pnt))

    @property
    def rotation(self):
        r""":obj:`tuple`\[:class:`.Point3DData`, :class:`.Point3DData`, :obj:`float`\]: Rotation from/to the axis and the angle."""  # noqa
        msg = self.__stub.GetRotation(messages.edb_obj_message(self))
        return (
            parser.to_point3d_data(msg.axis_from),
            parser.to_point3d_data(msg.axis_to),
            msg.angle.value,
        )

    @rotation.setter
    def rotation(self, value):
        self.set_rotation(*value)

    def set_rotation(self, axis_from, axis_to, angle):
        """Set rotation from/to the axis and the angle in radians.

        Parameters
        ----------
        axis_from : :class:`.Point3DData`
        axis_to : :class:`.Point3DData`
        angle : float
            Angle in radians.
        """
        self.__stub.SetRotation(
            messages.mcad_model_set_rotation_message(self, axis_from, axis_to, angle)
        )

    @property
    def scale(self):
        """:obj:`float`: Scale of the MCAD model."""
        return self.__stub.GetScale(messages.edb_obj_message(self)).value

    @scale.setter
    def scale(self, scale):
        self.__stub.SetScale(messages.double_property_message(self, scale))

    def material(self, index):
        """Get the material name of the MCAD model part at a given index.

        Parameters
        ----------
        index : int
            Index of the MCAD model part.

        Returns
        -------
        str
            Material name.
        """
        return self.__stub.GetMaterial(messages.int_property_message(self, index)).value

    def set_material(self, index, material):
        """Set material name of a MCAD model part at a given index.

        Parameters
        ----------
        index : int
            Index of the MCAD model part.
        material : str
           New material name.
        """
        self.__stub.SetMaterial(messages.mcad_model_string_message(self, index, material))

    def visible(self, index):
        """Get visibility of a MCAD model part at a given index.

        Parameters
        ----------
        index : int
            Index of the MCAD model part.

        Returns
        -------
        bool
        """
        return self.__stub.GetVisible(messages.int_property_message(self, index)).value

    def set_visible(self, index, visible):
        """Set visibility of an MCAD model part at a given index.

        Parameters
        ----------
        index : int
            Index of the MCAD model part.
        visible : bool
        """
        self.__stub.SetVisible(messages.mcad_model_bool_message(self, index, visible))

    def modeled(self, index):
        """Determine if an MCAD model part at a given index is included in the analysis.

        Parameters
        ----------
        index : int
            Index of the MCAD model part.

        Returns
        -------
        bool
            ``True`` if the MCAD model part is included in the analysis, ``False`` otherwise.
        """
        return self.__stub.GetModeled(messages.int_property_message(self, index)).value

    def set_modeled(self, index, modeled):
        """Set if an MCAD model part at a given index is to be modeled.

        Parameters
        ----------
        index : int
            Index of the MCAD model part.
        modeled : bool
            Whether to model the MCAD model part.
        """
        self.__stub.SetModeled(messages.mcad_model_bool_message(self, index, modeled))

    def part_count(self):
        """Get the MCAD model part count.

        Returns
        -------
        int
            MCAD model part count.
        """
        return self.__stub.GetPartCount(messages.edb_obj_message(self)).value

    def part_index(self, name):
        """Get the index of an MCAD model part with a given name.

        Parameters
        ----------
        name : str
            Name of the MCAD model part.

        Returns
        -------
        int
           Index of the MCAD model part.
        """
        return self.__stub.GetPartIndex(messages.string_property_message(self, name)).value

    def part_name(self, index):
        """Get the name of an MCAD model part at a given index.

        Parameters
        ----------
        index : int
            Index of the MCAD model part.

        Returns
        -------
        str
           Name of the MCAD model part.
        """
        return self.__stub.GetPartName(messages.int_property_message(self, index)).value
