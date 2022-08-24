"""Material Definition."""

from enum import Enum

import ansys.api.edb.v1.material_def_pb2 as pb

from ansys.edb.core import ObjBase, messages
from ansys.edb.session import MaterialDefServiceStub, StubAccessor, StubType
from ansys.edb.utility import Value


class DielectricMaterialModel(ObjBase):
    """Class representing a dielectric material model."""


class ThermalModifier(ObjBase):
    """Class representing a thermal modifier model."""


class MaterialProperty(Enum):
    """Enum representing property types."""

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
            msg_params["component"]: messages.edb_internal_id_message(component)
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
            msg_params["component"]: messages.edb_internal_id_message(component)
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
    def material_def_set_property_message(material_def, material_property_id, thermal_modifier):
        return pb.SetMaterialDefPropertyMessage(
            materialDef=messages.edb_obj_message(material_def),
            propertyId=material_property_id.value,
            thermal_modifier=messages.edb_obj_message(thermal_modifier),
        )

    @staticmethod
    def material_def_get_anisotropic_property_message(
        material_def, material_property_id, component
    ):
        return pb.MaterialDefPropertyComponentMessage(
            materialDef=messages.edb_obj_message(material_def),
            propertyId=material_property_id.value,
            component=component,
        )

    @staticmethod
    def material_def_set_anisotropic_property_message(
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
        """Create a material definition.

        Parameters
        ----------
        database : Database
        name : str

        Returns
        -------
        MaterialDef
        """
        return MaterialDef(cls.__stub.Create(_QueryBuilder.create(database, name, **kwargs)))

    @classmethod
    def find_by_name(cls, database, name):
        """Find a material definition by Name.

        Parameters
        ----------
        database : Database
        name : str

        Returns
        -------
        MaterialDef
        """
        return MaterialDef(cls.__stub.FindByName(messages.edb_obj_name_message(database, name)))

    def delete(self):
        """Delete a material definition."""
        self.__stub.Delete(messages.edb_obj_message(self))

    def set_property(self, material_property, value, component=-1, col=-1, row=-1):
        """Set a property value of a material.

        Parameters
        ----------
        material_property : MaterialProperty
        value : float
        component : int, optional
        row : int, optional
        col : int, optional
        """
        self.__stub.SetProperty(
            _QueryBuilder.set_property(self, material_property, value, component, col, row)
        )

    def get_property(self, material_property, component=None, row=None, col=None):
        """Set a property value of a material.

        Parameters
        ----------
        material_property : MaterialProperty
        component : int, optional
        row : int, optional
        col : int, optional

        Returns
        -------
        Value
        """
        return Value(
            self.__stub.GetProperty(
                _QueryBuilder.get_property(self, material_property, component, col, row)
            )
        )

    def get_all_properties(self):
        """Set a property value of a material.

        Returns
        -------
        List[Value]
        """
        msg = self.__stub.GetAllProperties(messages.edb_obj_message(self))
        return [MaterialProperty(i) for i in msg.properties]

    def remove_property(self, material_property):
        """Remove a property value of a material def.

        Parameters
        ----------
        material_property : MaterialProperty
        row : int, optional
        col : int, optional
        """
        self.__stub.RemoveProperty(
            _QueryBuilder.get_property(
                messages.edb_obj_message(self), material_property, None, None, None
            )
        )

    @property
    def name(self):
        """Remove a property value of a material def.

        Returns
        ----------
        name : str
        """
        return self.__stub.GetName(messages.edb_obj_message(self))

    @property
    def dielectric_material_model(self):
        """Remove a property value of a material def.

        Returns
        ----------
        DielectricMaterialModel
        """
        return DielectricMaterialModel(
            self.__stub.GetDielectricMaterialModel(messages.edb_obj_message(self))
        )

    @property
    @dielectric_material_model.setter
    def dielectric_material_model(self, dielectric):
        """Remove a property value of a material def.

        Parameters
        ----------
        dielectric : DielectricMaterialModel
        """
        self.__stub.SetDielectricMaterialModel(messages.pointer_property_message(self, dielectric))

    def get_dimensions(self, material_property_id):
        """Remove a property value of a material def.

        Parameters
        ----------
        material_property_id : MaterialProperty

        Returns
        ----------
        Tuple[Int, Int]
        """
        msg = self.__stub.GetDimensions(
            _QueryBuilder.material_def_get_property_message(self, material_property_id)
        )
        return [msg.tensor.col, msg.tensor.row]

    def get_thermal_modifier(self, material_property_id):
        """Remove a property value of a material def.

        Parameters
        ----------
        material_property_id : MaterialProperty

        Returns
        ----------
        DielectricMaterialModel
        """
        return ThermalModifier(
            self.__stub.GetThermalModifier(
                _QueryBuilder.material_def_get_property_message(self, material_property_id)
            )
        )

    def set_thermal_modifier(self, material_property_id, thermal_modifier):
        """Remove a property value of a material def.

        Parameters
        ----------
        material_property_id : MaterialProperty
        thermal_modifier : ThermalModifier
        """
        self.__stub.SetThermalModifier(
            _QueryBuilder.material_def_set_property_message(
                self, material_property_id, thermal_modifier
            )
        )

    def get_anisotropic_thermal_modifier(self, material_property_id, component):
        """Get anisotropic thermal modifier of a material def.

        Parameters
        ----------
        material_property_id : MaterialProperty
        component: int

        Returns
        ----------
        ThermalModifier
        """
        return ThermalModifier(
            self.__stub.GetAnisotropicThermalModifier(
                _QueryBuilder.material_def_get_anisotropic_property_message(
                    self, material_property_id, component
                )
            )
        )

    def set_anisotropic_thermal_modifier(self, material_property_id, component, thermal_modifier):
        """Set anisotropic thermal modifier of a material def.

        Parameters
        ----------
        material_property_id : MaterialProperty
        component: int
        thermal_modifier : ThermalModifier
        """
        self.__stub.SetAnisotropicThermalModifier(
            _QueryBuilder.material_def_set_anisotropic_property_message(
                self, material_property_id, component, thermal_modifier
            )
        )
