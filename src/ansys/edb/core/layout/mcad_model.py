"""Mcad Model."""

from ansys.edb.core.hierarchy.cell_instance import CellInstance
from ansys.edb.core.inner.base import ObjBase
from ansys.edb.core.inner.messages import (
    double_property_message,
    edb_obj_message,
    int_property_message,
    mcad_model_bool_message,
    mcad_model_creation_message,
    mcad_model_hfss_creation_message,
    mcad_model_set_rotation_message,
    mcad_model_string_message,
    point_3d_property_message,
    string_property_message,
)
from ansys.edb.core.inner.parser import to_point3d_data
from ansys.edb.core.session import McadModelServiceStub, StubAccessor, StubType


class McadModel(ObjBase):
    """Class representing a Mcad Model."""

    __stub: McadModelServiceStub = StubAccessor(StubType.mcad_model)

    @classmethod
    def create_stride(cls, connectable=None, layout=None, filename=None):
        """Create a Stride model.

        call directly on :term:`Connectable` or :func:`Layout<ansys.edb.core.layout.Layout.create_stride>`.
        """
        return cls(
            cls.__stub.CreateStride(mcad_model_creation_message(connectable, layout, filename))
        )

    @classmethod
    def create_hfss(cls, connectable=None, layout=None, filename=None, design=None):
        """Create a HFSS model.

        call directly on :term:`Connectable` or :func:`Layout<ansys.edb.core.layout.Layout.create_hfss>`.
        """
        return cls(
            cls.__stub.CreateHfss(
                mcad_model_hfss_creation_message(connectable, layout, filename, design)
            )
        )

    @classmethod
    def create_3d_comp(cls, connectable=None, layout=None, filename=None):
        """Create a 3D Component model.

        call directly on :term:`Connectable` or :func:`Layout<ansys.edb.core.layout.Layout.create_3d_comp>`.
        """
        return cls(
            cls.__stub.Create3dComp(mcad_model_creation_message(connectable, layout, filename))
        )

    @classmethod
    def is_mcad(cls, connectable):
        """Get if a connectable object is Mcad model.

        call directly on :term:`Connectable`.
        """
        return cls.__stub.IsMcad(edb_obj_message(connectable))

    @classmethod
    def is_mcad_stride(cls, connectable):
        """Get if a connectable object is Stride model.

        call directly on :term:`Connectable`.
        """
        return cls.__stub.IsMcadStride(edb_obj_message(connectable))

    @classmethod
    def is_mcad_hfss(cls, connectable):
        """Get if a connectable object is HFSS model.

        call directly on :term:`Connectable`.
        """
        return cls.__stub.IsMcadHfss(edb_obj_message(connectable))

    @classmethod
    def is_mcad_3d_comp(cls, connectable):
        """Get if a connectable object is 3D Component model.

        call directly on :term:`Connectable`.
        """
        return cls.__stub.IsMcad3dComp(edb_obj_message(connectable))

    @property
    def cell_instance(self):
        """:class:`CellInstance <ansys.edb.core.hierarchy.CellInstance>` Cell instance of a Mcad model.

        Read-Only.
        """
        return CellInstance(self.__stub.GetCellInst(edb_obj_message(self)))

    @property
    def model_name(self):
        """:obj:`str` Model name of a Mcad model.

        Read-Only.
        """
        return self.__stub.GetModelName(edb_obj_message(self)).value

    @property
    def design_name(self):
        """:obj:`str` Design name of a Mcad model.

        Read-Only.
        """
        return self.__stub.GetDesignName(edb_obj_message(self)).value

    @property
    def origin(self):
        """:class:`Point3DData <ansys.edb.core.geometry.Point3DData>` Origin 3D point of a Mcad model."""
        return self.__stub.GetOrigin(edb_obj_message(self))

    @origin.setter
    def origin(self, pnt):
        self.__stub.SetOrigin(point_3d_property_message(self, pnt))

    @property
    def rotation(self):
        r""":obj:`tuple`\[:class:`Point3DData <ansys.edb.core.geometry.Point3DData>`, :class:`Point3DData <ansys.edb.core.geometry.Point3DData>`, :obj:`float`\] Rotation from/to axis and angle."""  # noqa
        msg = self.__stub.GetRotation(edb_obj_message(self))
        return (
            to_point3d_data(msg.axis_from),
            to_point3d_data(msg.axis_to),
            msg.angle.value,
        )

    @rotation.setter
    def rotation(self, value):
        self.set_rotation(*value)

    def set_rotation(self, axis_from, axis_to, angle):
        """Set rotation from/to axis and angle in radians.

        Parameters
        ----------
        axis_from : :class:`Point3DData <ansys.edb.core.geometry.Point3DData>`
        axis_to : :class:`Point3DData <ansys.edb.core.geometry.Point3DData>`
        angle : float
        """
        self.__stub.SetRotation(mcad_model_set_rotation_message(self, axis_from, axis_to, angle))

    @property
    def scale(self):
        """:obj:`float` The scale of a Mcad model."""
        return self.__stub.GetScale(edb_obj_message(self)).value

    @scale.setter
    def scale(self, scale):
        self.__stub.SetScale(double_property_message(self, scale))

    def material(self, index):
        """Get material name of a Mcad model part at index.

        Parameters
        ----------
        index : int

        Returns
        -------
        str
        """
        return self.__stub.GetMaterial(int_property_message(self, index)).value

    def set_material(self, index, material):
        """Set material name of a Mcad model part at index.

        Parameters
        ----------
        index : int
        material : str
        """
        self.__stub.SetMaterial(mcad_model_string_message(self, index, material))

    def visible(self, index):
        """Get visibility of a Mcad model part at index.

        Parameters
        ----------
        index : int

        Returns
        -------
        bool
        """
        return self.__stub.GetVisible(int_property_message(self, index)).value

    def set_visible(self, index, visible):
        """Set visibility of a Mcad model part at index.

        Parameters
        ----------
        index : int
        visible : bool
        """
        self.__stub.SetVisible(mcad_model_bool_message(self, index, visible))

    def modeled(self, index):
        """Get if a Mcad model part at index is included in analysis.

        Parameters
        ----------
        index : int

        Returns
        -------
        bool
        """
        return self.__stub.GetModeled(int_property_message(self, index)).value

    def set_modeled(self, index, modeled):
        """Set if a Mcad model part at index is modeled.

        Parameters
        ----------
        index : int
        modeled : bool
        """
        self.__stub.SetModeled(mcad_model_bool_message(self, index, modeled))

    def part_count(self):
        """Mcad model part count.

        Returns
        -------
        int
        """
        return self.__stub.GetPartCount(edb_obj_message(self)).value

    def part_index(self, name):
        """Index of a Mcad model part with the specified name.

        Parameters
        ----------
        name : str

        Returns
        -------
        int
        """
        return self.__stub.GetPartIndex(string_property_message(self, name)).value

    def part_name(self, index):
        """Name of a Mcad model part at the specified index.

        Parameters
        ----------
        index : int

        Returns
        -------
        str
        """
        return self.__stub.GetPartName(int_property_message(self, index)).value
