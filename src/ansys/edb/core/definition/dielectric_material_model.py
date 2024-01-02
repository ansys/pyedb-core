"""Dielectric material definition."""
from enum import Enum

from ansys.api.edb.v1 import dielectric_material_model_pb2_grpc

from ansys.edb.core import session
from ansys.edb.core.inner.base import ObjBase


class DielectricMaterialModelType(Enum):
    """Provides an eum representing dielectric material model types.

    - DEBYE
    - MULTIPOLE_DEBYE
    - DJORDJECVIC_SARKAR
    """

    DEBYE = 0
    MULTIPOLE_DEBYE = 1
    DJORDJECVIC_SARKAR = 2


class DielectricMaterialModel(ObjBase):
    """Represents a dielectric material model object."""

    __stub: dielectric_material_model_pb2_grpc.DielectricMaterialModelServiceStub = (
        session.StubAccessor(session.StubType.dielectric_material_model)
    )

    @property
    def type(self):
        """DielectricMaterialModelType: Type of dielectric material model."""
        return DielectricMaterialModelType(self.__stub.GetType(self.msg).value)
