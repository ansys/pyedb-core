"""Dielectric Material Definition."""
from enum import Enum

from ansys.api.edb.v1 import dielectric_material_model_pb2_grpc

from ansys.edb import session
from ansys.edb.core import ObjBase


class DielectricMaterialModelType(Enum):
    """Enum representing dielectric material model type.

    - DEBYE
    - MULTIPOLE_DEBYE
    - DJORDJECVIC_SARKAR
    """

    DEBYE = 0
    MULTIPOLE_DEBYE = 1
    DJORDJECVIC_SARKAR = 2


class DielectricMaterialModel(ObjBase):
    """Class representing a dielectric material model object."""

    __stub: dielectric_material_model_pb2_grpc.DielectricMaterialModelServiceStub = (
        session.StubAccessor(session.StubType.dielectric_material_model)
    )

    @property
    def type(self):
        """Type of dielectric material model.

        Returns
        -------
        DielectricMaterialModelType
        """
        return DielectricMaterialModelType(self.__stub.GetType(self.msg))
