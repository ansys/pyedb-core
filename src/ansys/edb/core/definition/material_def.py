"""Material definition."""
from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Tuple

if TYPE_CHECKING:
    from ansys.edb.core.typing import ValueLike
    from ansys.edb.core.database import Database

from enum import Enum

import ansys.api.edb.v1.material_def_pb2 as pb

from ansys.edb.core.definition.dielectric_material_model import DielectricMaterialModel
from ansys.edb.core.definition.material_property_thermal_modifier import (
    MaterialPropertyThermalModifier,
)
from ansys.edb.core.edb_defs import DefinitionObjType
from ansys.edb.core.inner import ObjBase, messages
from ansys.edb.core.session import MaterialDefServiceStub, StubAccessor, StubType
from ansys.edb.core.utility.value import Value


class MaterialProperty(Enum):
    """Enum representing material property types."""

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


class MaterialDef(ObjBase):
    """Represents a material and all its properties."""

    __stub: MaterialDefServiceStub = StubAccessor(StubType.material)

    @classmethod
    def create(cls, database: Database, name: str, **kwargs: Dict[str, ValueLike]) -> MaterialDef:
        """Create a material definition in a given database.

        Parameters
        ----------
        database : .Database
            Database to create the material definition in.
        name : str
            Name of the material definition.
        kwargs : dict of { str : :term:`ValueLike` }
            Dictionary of material property values.
            The dictionary key is the material property name. The dictionary value is the \
            material property value. The expected keys for the kwargs are:

            - ``"permittivity"``
            - ``"permeability"``
            - ``"conductivity"``
            - ``"dielectric_loss_tangent"``
            - ``"magnetic_loss_tangent"``
            - ``"thermal_conductivity"``
            - ``"mass_density"``
            - ``"specific_heat"``
            - ``"youngs_modulus"``
            - ``"poissons_ratio"``
            - ``"thermal_expansion_coefficient"``

        Returns
        -------
        .MaterialDef
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
    def find_by_name(cls, database: Database, name: str) -> MaterialDef:
        """Find a material definition by name in a given database.

        Parameters
        ----------
        database : .Database
            Database to search for the material definition.
        name : str
            Name of the material definition.

        Returns
        -------
        .MaterialDef
            Material definition object found.
            If a material definition isn't found, the returned material definition is :meth:`null <.is_null>`.
        """
        return MaterialDef(cls.__stub.FindByName(messages.edb_obj_name_message(database, name)))

    @property
    def definition_type(self) -> DefinitionObjType:
        """:class:`.DefinitionObjType`: Definition object type.

        This property is read-only.
        """
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

    def set_property(
        self,
        material_property: MaterialProperty,
        value: ValueLike,
        component_id: int = None,
        col: int = None,
        row: int = None,
    ):
        """Set a material property value.

            Material properties can be defined in 3 ways:
                1. Simple: A constant value.
                    - To define a simple material property, the ``material_property`` \
                    and ``value`` parameters should be provided.
                2. Anisotropic: A 3x3 tensor consisting of only diagonal entries.
                    - To define a component of an anisotropic material property, the ``material_property``, \
                    ``value``, and ``component_id`` parameters should be provided.
                    - ``component_id`` specifies the \
                    :term:`anisotropic component ID <Anisotropic Material Property Component IDs>` \
                    of the component to set the value of.
                3. Tensor: A 3x3 tensor consisting of diagonal and off-diagonal entries.
                    - To define an entry in a tensor material property, the ``material_property``, \
                    ``value``, ``col`` and ``row`` parameters should be provided. The entry at ``T[row,col]`` \
                    will be set to the provided ``value``.

        Parameters
        ----------
        material_property : .MaterialProperty
            ID of the material property.
        value : :term:`ValueLike`
            New value.
        component_id : int, default: None
            ID of the anisotropic component (only used for anisotropic material properties).
        row : int, default: None
            Tensor row (only used for tensor material properties).
        col : int, default: None
            Tensor column (only used for tensor material properties).
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
        """Get a material property value.

            Material properties can be defined in 3 ways:
                1. Simple: A constant value.
                    - To retrieve a simple material property, the ``material_property`` \
                    parameter should be provided.
                2. Anisotropic: A 3x3 tensor consisting of only diagonal entries.
                    - To retrieve a component of an anisotropic material property, the ``material_property`` \
                    and ``component_id`` parameters should be provided.
                    - ``component_id`` specifies the \
                    :term:`anisotropic component ID <Anisotropic Material Property Component IDs>` \
                    of the component to get the value of.
                3. Tensor: A 3x3 tensor consisting of diagonal and off-diagonal entries.
                    - To retrieve an entry in a tensor material property, the ``material_property``, \
                    ``col`` and ``row`` parameters should be provided. The entry at ``T[row,col]`` \
                    will be returned.

        Parameters
        ----------
        material_property : .MaterialProperty
            ID of the material property.
        component_id : int, default: None
            ID of the anisotropic component (only used for anisotropic material properties).
        row : int, default: None
            Tensor row (only used for tensor material properties).
        col : int, default: None
            Tensor column (only used for tensor material properties).

        Returns
        -------
        .Value
        """
        return Value(
            self.__stub.GetProperty(
                MaterialDef._get_property_message(self, material_property, component_id, col, row)
            )
        )

    @property
    def all_properties(self) -> List[MaterialProperty]:
        """:obj:`list` of :class:`.MaterialProperty`: All properties defined in the material definition.

        This property is read-only.
        """
        msg = self.__stub.GetAllProperties(messages.edb_obj_message(self))
        return [MaterialProperty(i) for i in msg.properties]

    def remove_property(self, material_property: MaterialProperty):
        """Remove a property from the material definition.

        Parameters
        ----------
        material_property : .MaterialProperty
            Material property to be removed.
        """
        self.__stub.RemoveProperty(
            MaterialDef._get_property_message(
                messages.edb_obj_message(self), material_property, None, None, None
            )
        )

    def get_dimensions(self, material_property_id: MaterialProperty) -> Tuple[int, int]:
        """Get the dimensions of the tensor of a material property.

            The mappings between the types of material properties and dimensions are as follows:
                - ``Simple`` -> ``1x1``
                - ``Anisotropic`` -> ``3x1``
                - ``Tensor`` -> ``3x3``.

        Parameters
        ----------
        material_property_id : .MaterialProperty
            Material property to get the dimensions of.

        Returns
        -------
        tuple of (int, int)
            The tuple is of the format ``(col, row)``:

            - ``col``: Number of rows of the material property.
            - ``row``: Number of columns of the material property.
        """
        msg = self.__stub.GetDimensions(MaterialDef._property_message(self, material_property_id))
        return msg.tensor.col, msg.tensor.row

    def get_thermal_modifier(
        self, material_property_id: MaterialProperty
    ) -> MaterialPropertyThermalModifier:
        """Get the thermal modifier of a material property.

        Parameters
        ----------
        material_property_id : .MaterialProperty
            Material property to get the thermal modifier of.

        Returns
        -------
        .MaterialPropertyThermalModifier
        """
        return MaterialPropertyThermalModifier(
            self.__stub.GetThermalModifier(
                MaterialDef._property_message(self, material_property_id)
            )
        )

    def set_thermal_modifier(
        self,
        material_property_id: MaterialProperty,
        thermal_modifier: MaterialPropertyThermalModifier,
    ):
        """Set the thermal modifier of the material property.

        Parameters
        ----------
        material_property_id : .MaterialProperty
            Material property to set the thermal modifier on.
        thermal_modifier : .MaterialPropertyThermalModifier
            Thermal modifier to assign to the material property.
        """
        self.__stub.SetThermalModifier(
            pb.SetMaterialDefPropertyMessage(
                materialDef=messages.edb_obj_message(self),
                propertyId=material_property_id.value,
                thermal_modifier=messages.edb_obj_message(thermal_modifier),
            )
        )

    def get_anisotropic_thermal_modifier(self, material_property_id, component_id):
        """Get the thermal modifier of an anisotropic material property.

        Parameters
        ----------
        material_property_id : .MaterialProperty
            Material property to get the thermal modifier of.
        component_id : int
            :term:`Anisotropic component ID <Anisotropic Material Property Component IDs>` of the \
            material property to get the thermal modifier of.

        Returns
        -------
        .MaterialPropertyThermalModifier
        """
        return MaterialPropertyThermalModifier(
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
        """Set the thermal modifier of an anisotropic material property.

        Parameters
        ----------
        material_property_id : .MaterialProperty
            Type of material property to set the thermal modifier on.
        component_id : int
            :term:`Anisotropic component ID <Anisotropic Material Property Component IDs>` of the \
            material property to set the thermal modifier on.
        thermal_modifier : .MaterialPropertyThermalModifier
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
