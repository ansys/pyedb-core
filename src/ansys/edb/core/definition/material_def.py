"""Material definition."""

from enum import Enum

import ansys.api.edb.v1.material_def_pb2 as pb

from ansys.edb.core.definition.dielectric_material_model import DielectricMaterialModel
from ansys.edb.core.edb_defs import DefinitionObjType
from ansys.edb.core.inner import ObjBase, messages
from ansys.edb.core.session import MaterialDefServiceStub, StubAccessor, StubType
from ansys.edb.core.utility.value import Value


class MaterialProperty(Enum):
    """Provides an enum representing material property types."""

    PERMITTIVITY = pb.PERMITTIVITY
    PERMEABILITY = pb.PERMEABILITY
    CONDUCTIVITY = pb.CONDUCTIVITY
    DIELECTRIC_LOSS_TANGENT = pb.DIELECTRIC_LOSS_TANGENT
    MAGNETIC_LOSS_TANGENT = pb.MAGNETIC_LOSS_TANGENT
    THERMAL_CONDUCTIVITY = pb.THERMAL_CONDUCTIVITY
    MASS_DENSITY = pb.MASS_DENSITY
    SPECIFIC_HEAT = pb.SPECIFIC_HEAT
    YOUNGS_MODULUS = pb.YOUNGS_MODULUS
    POISSONS_RATIO = pb.POISSONS_RATIO
    THERMAL_EXPANSION_COEFFICIENT = pb.THERMAL_EXPANSION_COEFFICIENT
    INVALID_PROPERTY = pb.INVALID_PROPERTY


class ThermalModifier(ObjBase):
    """Represents a thermal modifier model."""


class MaterialDef(ObjBase):
    """Represents a material definition."""

    __stub: MaterialDefServiceStub = StubAccessor(StubType.material)

    @classmethod
    def create(cls, database, name, **kwargs):
        """Create a material definition in a given database.

        Parameters
        ----------
        database : :class:`.Database`
            Database to create the material definition in.
        name : str
            Name of the material definition.
        kwargs : dict{ str : :class:`.Value` }
            Dictionary to convert to a ``MaterialDefPropertiesMessage`` object.
            The dictionary key is the material property name. The dictionary value is the
            material property value. The expected keys for the kwargs are:

            - ``permittivity``
            - ``permeability``
            - ``conductivity``
            - ``dielectric_loss_tangent``
            - ``magnetic_loss_tangent``
            - ``thermal_conductivity``
            - ``mass_density``
            - ``specific_heat``
            - ``youngs_modulus``
            - ``poissons_ratio``
            - ``thermal_expansion_coefficient``

        Returns
        -------
        MaterialDef
            Material definition object created.
        """
        return MaterialDef(
            cls.__stub.Create(
                pb.MaterialDefCreationMessage(
                    database=messages.edb_obj_message(database),
                    name=name,
                    properties=messages.material_properties_message(**kwargs),
                )
            )
        )

    @classmethod
    def find_by_name(cls, database, name):
        """Find a material definition by name in a given database.

        Parameters
        ----------
        database : :class:`.Database`
            Database to search for the material definition.
        name : str
            Name of the material definition.

        Returns
        -------
        MaterialDef
            Naterial definition found.
        """
        return MaterialDef(cls.__stub.FindByName(messages.edb_obj_name_message(database, name)))

    @property
    def definition_type(self):
        """:class:`.DefinitionObjType`: Type of the material definition."""
        return DefinitionObjType.MATERIAL_DEF

    @property
    def name(self):
        """:obj:`str`: Name of the material definition.

        This property is read-only.
        """
        return self.__stub.GetName(messages.edb_obj_message(self)).value

    @property
    def dielectric_material_model(self):
        """:class:`.DielectricMaterialModel`: \
        Dielectric material model of the material definition."""
        return DielectricMaterialModel(
            self.__stub.GetDielectricMaterialModel(messages.edb_obj_message(self))
        )

    @dielectric_material_model.setter
    def dielectric_material_model(self, dielectric):
        self.__stub.SetDielectricMaterialModel(messages.pointer_property_message(self, dielectric))

    def delete(self):
        """Delete the material definition."""
        self.__stub.Delete(messages.edb_obj_message(self))

    def set_property(self, material_property, value, component_id=None, col=None, row=None):
        """Set a material property for a given component.

        Parameters
        ----------
        material_property : :class:`MaterialProperty`
            ID of the material property.
        value : :class:`.Value`
            New value.
        component_id : int, default: None
            ID of the component.
        row : int, default: None
            Tensor row.
        col : int, default: None
            Tensor column.
        """
        msg_params = {
            "materialDef": messages.edb_obj_message(self),
            "propertyId": material_property.value,
            "value": messages.value_message(value),
        }
        if component_id is not None:
            msg_params["component"] = messages.edb_internal_id_message(component_id)
        elif row is not None and col is not None:
            msg_params["tensor"] = MaterialDef._tensor_pos_message(col, row)
        self.__stub.SetProperty(pb.MaterialDefSetPropertyMessage(**msg_params))

    def get_property(self, material_property, component_id=None, row=None, col=None):
        """Set a property value of the material.

        Parameters
        ----------
        material_property : :class:`MaterialProperty`, default: None
            Material property ID.
        component_id : int, default: None
            Component ID.
        row : int, default: None
            Tensor row.
        col : int, default: None
            Tensor column.

        Returns
        -------
        :class:`.Value`
            Value of the material property.
        """
        return Value(
            self.__stub.GetProperty(
                MaterialDef._get_property_message(self, material_property, component_id, col, row)
            )
        )

    def get_all_properties(self):
        """Get all properties of the material.

        Returns
        -------
        `list` of :class:`MaterialProperty`
            All properties for the material definition.
        """
        msg = self.__stub.GetAllProperties(messages.edb_obj_message(self))
        return [MaterialProperty(i) for i in msg.properties]

    def remove_property(self, material_property):
        """Remove the value from a material property.

        Parameters
        ----------
        material_property : :class:`MaterialProperty`
            Property ID.
        """
        self.__stub.RemoveProperty(
            MaterialDef._get_property_message(
                messages.edb_obj_message(self), material_property, None, None, None
            )
        )

    def get_dimensions(self, material_property_id):
        """Get dimensions of a given material definition.

        Types are Simple 1x1, Anisotropic 3x1, and Tensor 3x3.

        Parameters
        ----------
        material_property_id : \
        :class:`MaterialProperty`
            Property ID.

        Returns
        -------
        tuple[int, int]
            The tuple is in a ``(col, row)`` format:

            - ``col``: Number of rows of the material property.
            - ``row``: Number of columns of the material property.
        """
        msg = self.__stub.GetDimensions(MaterialDef._property_message(self, material_property_id))
        return [msg.tensor.col, msg.tensor.row]

    def get_thermal_modifier(self, material_property_id):
        """Get the thermal modifier of a given material definition.

        Parameters
        ----------
        material_property_id : \
        :class:`MaterialProperty`
            Property ID.

        Returns
        -------
        ThermalModifier
            Thermal modifier of the material definition.
        """
        return ThermalModifier(
            self.__stub.GetThermalModifier(
                MaterialDef._property_message(self, material_property_id)
            )
        )

    def set_thermal_modifier(self, material_property_id, thermal_modifier):
        """Set the thermal modifier of the material definition.

        Parameters
        ----------
        material_property_id : \
        :class:`MaterialProperty`
            Property ID.
        thermal_modifier : ThermalModifier
            Thermal modifier to set to the material definition.
        """
        self.__stub.SetThermalModifier(
            pb.SetMaterialDefPropertyMessage(
                materialDef=messages.edb_obj_message(self),
                propertyId=material_property_id.value,
                thermal_modifier=messages.edb_obj_message(thermal_modifier),
            )
        )

    def get_anisotropic_thermal_modifier(self, material_property_id, component_id):
        """Get the anisotropic thermal modifier of a given material definition.

        Parameters
        ----------
        material_property_id : \
        :class:`MaterialProperty`
            Property ID.
        component_id : int
            Component ID.

        Returns
        -------
        :class:`.ThermalModifier`
            Anisotropic thermal modifier of the material definition.
        """
        return ThermalModifier(
            self.__stub.GetAnisotropicThermalModifier(
                pb.MaterialDefPropertyComponentMessage(
                    materialDef=messages.edb_obj_message(self),
                    propertyId=material_property_id.value,
                    component=component_id,
                )
            )
        )

    def set_anisotropic_thermal_modifier(
        self, material_property_id, component_id, thermal_modifier
    ):
        """Set the anisotropic thermal modifier of a given material definition.

        Parameters
        ----------
        material_property_id : \
        :class:`MaterialProperty`
            Property ID.
        component_id : int
            Component ID.
        thermal_modifier : :class:`.ThermalModifier`
            Anisotropic thermal modifier to set to the material definition.
        """
        self.__stub.SetAnisotropicThermalModifier(
            pb.SetMaterialDefPropertyComponentMessage(
                materialDef=messages.edb_obj_message(self),
                propertyId=material_property_id.value,
                component=component_id,
                thermal_modifier=messages.edb_obj_message(thermal_modifier),
            )
        )

    @staticmethod
    def _tensor_pos_message(col, row):
        return pb.TensorPositionMessage(
            col=col,
            row=row,
        )

    @staticmethod
    def _get_property_message(material_def, material_property, component, col, row):
        msg_params = {
            "materialDef": messages.edb_obj_message(material_def),
            "propertyId": material_property.value,
        }
        if component is not None:
            msg_params["component"] = messages.edb_internal_id_message(component)
        elif row is not None and col is not None:
            msg_params["tensor"] = MaterialDef._tensor_pos_message(col, row)
        return pb.MaterialDefGetPropertyMessage(**msg_params)

    @staticmethod
    def _property_message(material_def, material_property_id):
        return pb.MaterialDefPropertyMessage(
            materialDef=messages.edb_obj_message(material_def),
            propertyId=material_property_id.value,
        )
