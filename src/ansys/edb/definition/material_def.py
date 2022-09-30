"""Material Definition."""

from enum import Enum

import ansys.api.edb.v1.material_def_pb2 as pb

from ansys.edb.core import ObjBase, messages
from ansys.edb.session import MaterialDefServiceStub, StubAccessor, StubType
from ansys.edb.utility import Value


class MaterialProperty(Enum):
    """Enum representing property types.

    - PERMITTIVITY
       Permittivity property.
    - PERMEABILITY
       Permeability property.
    - CONDUCTIVITY
       Conductivity property.
    - DIELECTRIC_LOSS_TANGENT
       Dielectric loss tangent property.
    - MAGNETIC_LOSS_TANGENT
       Magnetic loss tangent property.
    - THERMAL_CONDUCTIVITY
       Thermal conductivity property.
    - MASS_DENSITY
       Mass density property.
    - SPECIFIC_HEAT
       Specific Heat property.
    - YOUNGS_MODULUS
       Youngs Modulus property.
    - POISSONS_RATIO
       Poissons Ratio property.
    - THERMAL_EXPANSION_COEFFICIENT
       Thermal expansion coefficient property.
    - INVALID_PROPERTY
       Invalid property.
    """

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


class DielectricMaterialModel(ObjBase):
    """Class representing a dielectric material model."""


class ThermalModifier(ObjBase):
    """Class representing a thermal modifier model."""


class _QueryBuilder:
    @staticmethod
    def create(database, name, **kwargs):
        return pb.MaterialDefCreationMessage(
            database=messages.edb_obj_message(database),
            name=name,
            properties=messages.material_properties_message(**kwargs),
        )

    @staticmethod
    def tensor_pos_message(col, row):
        return pb.TensorPositionMessage(
            col=col,
            row=row,
        )

    @staticmethod
    def set_property(material_def, material_property, value, component, col, row):
        msg_params = {
            "materialDef": messages.edb_obj_message(material_def),
            "propertyId": material_property.value,
            "value": messages.value_message(value),
        }
        if component is not None:
            msg_params["component"] = messages.edb_internal_id_message(component)
        elif row is not None and col is not None:
            msg_params["tensor"] = _QueryBuilder.tensor_pos_message(col, row)
        return pb.MaterialDefSetPropertyMessage(**msg_params)

    @staticmethod
    def get_property(material_def, material_property, component, col, row):
        msg_params = {
            "materialDef": messages.edb_obj_message(material_def),
            "propertyId": material_property.value,
        }
        if component is not None:
            msg_params["component"] = messages.edb_internal_id_message(component)
        elif row is not None and col is not None:
            msg_params["tensor"] = _QueryBuilder.tensor_pos_message(col, row)
        return pb.MaterialDefGetPropertyMessage(**msg_params)

    @staticmethod
    def material_def_get_property_message(material_def, material_property_id):
        return pb.MaterialDefPropertyMessage(
            materialDef=messages.edb_obj_message(material_def),
            propertyId=material_property_id.value,
        )

    @staticmethod
    def material_def_set_thermal_modifier_message(
        material_def, material_property_id, thermal_modifier
    ):
        return pb.SetMaterialDefPropertyMessage(
            materialDef=messages.edb_obj_message(material_def),
            propertyId=material_property_id.value,
            thermal_modifier=messages.edb_obj_message(thermal_modifier),
        )

    @staticmethod
    def material_def_get_anisotropic_thermal_modifier_message(
        material_def, material_property_id, component
    ):
        return pb.MaterialDefPropertyComponentMessage(
            materialDef=messages.edb_obj_message(material_def),
            propertyId=material_property_id.value,
            component=component,
        )

    @staticmethod
    def material_def_set_anisotropic_thermal_modifier_message(
        material_def, material_property_id, component, thermal_modifier
    ):
        return pb.SetMaterialDefPropertyComponentMessage(
            materialDef=messages.edb_obj_message(material_def),
            propertyId=material_property_id.value,
            component=component,
            thermal_modifier=messages.edb_obj_message(thermal_modifier),
        )


class MaterialDef(ObjBase):
    """Class representing a material definition."""

    __stub: MaterialDefServiceStub = StubAccessor(StubType.material)

    @classmethod
    def create(cls, database, name, **kwargs):
        """Create a material definition into the given database.

        Parameters
        ----------
        database : :class:`Database <ansys.edb.database.Database>`
            Database that will own the material definition.
        name : str
            Name of the material definition being created.
        kwargs : dict{ str : :class:`Value <ansys.edb.utility.Value>` }
            Dictionary to be converted to MaterialDefPropertiesMessage.\
            Dict key is the material property name.\
            Dict value is the material property value.\
            Expected keys for kwargs:
             - permittivity
             - permeability
             - conductivity
             - dielectric_loss_tangent
             - magnetic_loss_tangent
             - thermal_conductivity
             - mass_density
             - specific_heat
             - youngs_modulus
             - poissons_ratio
             - thermal_expansion_coefficient

        Returns
        -------
        MaterialDef
            The new material definition object.
        """
        return MaterialDef(cls.__stub.Create(_QueryBuilder.create(database, name, **kwargs)))

    @classmethod
    def find_by_name(cls, database, name):
        """Find a material definition in the database with given name.

        Parameters
        ----------
        database : :class:`Database <ansys.edb.database.Database>`
            Database that owns the material definition.
        name : str
            Name of the material definition.

        Returns
        -------
        MaterialDef
            The material definition object found.
        """
        return MaterialDef(cls.__stub.FindByName(messages.edb_obj_name_message(database, name)))

    def delete(self):
        """Delete a material definition."""
        self.__stub.Delete(messages.edb_obj_message(self))

    def set_property(self, material_property, value, component_id=None, col=None, row=None):
        """Set a property value of a material.

        Parameters
        ----------
        material_property : :class:`MaterialProperty`
            Property id.
        value : :class:`Value <ansys.edb.utility.Value>`
            Property value returned.
        component_id : int, optional
            Component id.
        row : int, optional
            Tensor row.
        col : int, optional
            Tensor column.
        """
        self.__stub.SetProperty(
            _QueryBuilder.set_property(self, material_property, value, component_id, col, row)
        )

    def get_property(self, material_property, component_id=None, row=None, col=None):
        """Set a property value of a material.

        Parameters
        ----------
        material_property : :class:`MaterialProperty`
            Property id.
        component_id : int, optional
            Component id.
        row : int, optional
            Tensor row.
        col : int, optional
            Tensor column.

        Returns
        -------
        :class:`Value <ansys.edb.utility.Value>`
            Value of the material property.
        """
        return Value(
            self.__stub.GetProperty(
                _QueryBuilder.get_property(self, material_property, component_id, col, row)
            )
        )

    def get_all_properties(self):
        """Set a property value of a material.

        Returns
        -------
        list [:class:`MaterialProperty`]
            List with Material Properties of the material definition.
        """
        msg = self.__stub.GetAllProperties(messages.edb_obj_message(self))
        return [MaterialProperty(i) for i in msg.properties]

    def remove_property(self, material_property):
        """Remove a property value of a material def.

        Parameters
        ----------
        material_property : :class:`MaterialProperty`
            Property id.
        """
        self.__stub.RemoveProperty(
            _QueryBuilder.get_property(
                messages.edb_obj_message(self), material_property, None, None, None
            )
        )

    @property
    def name(self):
        """:obj:`str`: Name of the material definition.

        Read-Only.
        """
        return self.__stub.GetName(messages.edb_obj_message(self)).value

    @property
    def dielectric_material_model(self):
        """:class:`DielectricMaterialModel <ansys.edb.definition.material_def.DielectricMaterialModel>`: \
        Dielectric material model of the material definition."""
        return DielectricMaterialModel(
            self.__stub.GetDielectricMaterialModel(messages.edb_obj_message(self))
        )

    @dielectric_material_model.setter
    def dielectric_material_model(self, dielectric):
        self.__stub.SetDielectricMaterialModel(messages.pointer_property_message(self, dielectric))

    def get_dimensions(self, material_property_id):
        """Get dimensions of a material definition Simple 1x1, Anisotropic 3x1, Tensor 3x3.

        Parameters
        ----------
        material_property_id : \
        :class:`MaterialProperty`
            Property id.

        Returns
        -------
        tuple[int, int]

            Returns a tuple of the following format:

            **(col, row)**

            **col** : Number of rows of the material property.

            **row** : Number of columns of the material property.
        """
        msg = self.__stub.GetDimensions(
            _QueryBuilder.material_def_get_property_message(self, material_property_id)
        )
        return [msg.tensor.col, msg.tensor.row]

    def get_thermal_modifier(self, material_property_id):
        """Get thermal modifier of the material definition.

        Parameters
        ----------
        material_property_id : \
        :class:`MaterialProperty`
            Property id.

        Returns
        -------
        ThermalModifier
            Thermal modifier of the material definition.
        """
        return ThermalModifier(
            self.__stub.GetThermalModifier(
                _QueryBuilder.material_def_get_property_message(self, material_property_id)
            )
        )

    def set_thermal_modifier(self, material_property_id, thermal_modifier):
        """Set thermal modifier of the material definition.

        Parameters
        ----------
        material_property_id : \
        :class:`MaterialProperty`
            Property id.
        thermal_modifier : ThermalModifier
            Thermal modifier to be set to the material definition.
        """
        self.__stub.SetThermalModifier(
            _QueryBuilder.material_def_set_thermal_modifier_message(
                self, material_property_id, thermal_modifier
            )
        )

    def get_anisotropic_thermal_modifier(self, material_property_id, component_id):
        """Get anisotropic thermal modifier of a material def.

        Parameters
        ----------
        material_property_id : \
        :class:`MaterialProperty`
            Property id.
        component_id : int
            Component id.

        Returns
        -------
        :class:`ThermalModifier <ansys.edb.definition.material_def.ThermalModifier>`
            Anisotropic thermal modifier of the material definition.
        """
        return ThermalModifier(
            self.__stub.GetAnisotropicThermalModifier(
                _QueryBuilder.material_def_get_anisotropic_thermal_modifier_message(
                    self, material_property_id, component_id
                )
            )
        )

    def set_anisotropic_thermal_modifier(
        self, material_property_id, component_id, thermal_modifier
    ):
        """Set anisotropic thermal modifier of a material def.

        Parameters
        ----------
        material_property_id : \
        :class:`MaterialProperty`
            Property id.
        component_id : int
            Component id
        thermal_modifier : :class:`ThermalModifier <ansys.edb.definition.material_def.ThermalModifier>`
            Anisotropic thermal modifier to be set to the material definition
        """
        self.__stub.SetAnisotropicThermalModifier(
            _QueryBuilder.material_def_set_anisotropic_thermal_modifier_message(
                self, material_property_id, component_id, thermal_modifier
            )
        )
