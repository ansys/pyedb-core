"""Material Definition."""

from enum import Enum

import ansys.api.edb.v1.material_def_pb2 as pb

from ...interfaces.grpc import messages
from ...session import get_material_def_stub
from ...utility.edb_errors import handle_grpc_exception
from ..base import ObjBase


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
            database=database, name=name, properties=messages.material_properties_message(**kwargs)
        )

    @staticmethod
    def set_property(material_def, material_property, value):
        return pb.MaterialDefSetPropertyMessage(
            materialDef=material_def,
            propertyId=material_property.value,
            value=messages.value_message(value),
        )


class MaterialDef(ObjBase):
    """Class representing a material definition."""

    @staticmethod
    @handle_grpc_exception
    def create(database, name, **kwargs):
        """Create a material definition.

        Parameters
        ----------
        database : Database
        name : str

        Returns
        -------
        MaterialDef
        """
        return MaterialDef(
            get_material_def_stub().Create(_QueryBuilder.create(database.msg, name, **kwargs))
        )

    @handle_grpc_exception
    def set_property(self, material_property, value):
        """Set a property value of a material.

        Parameters
        ----------
        material_property : MaterialProperty
        value : float

        Returns
        -------
        bool
        """
        return (
            get_material_def_stub()
            .SetProperty(_QueryBuilder.set_property(self.msg, material_property, value))
            .value
        )
