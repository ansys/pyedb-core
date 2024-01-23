"""Dielectric material definition."""
from enum import Enum

from ansys.api.edb.v1 import dielectric_material_model_pb2_grpc

from ansys.edb.core import session
from ansys.edb.core.inner import ObjBase


class DielectricMaterialModelType(Enum):
    """Provides an eum representing dielectric material model types."""

    DEBYE = 0
    MULTIPOLE_DEBYE = 1
    DJORDJECVIC_SARKAR = 2


class DielectricMaterialModel(ObjBase):
    """Represents a dielectric material model."""

    __stub: dielectric_material_model_pb2_grpc.DielectricMaterialModelServiceStub = (
        session.StubAccessor(session.StubType.dielectric_material_model)
    )

    @property
    def type(self):
        """:class:`DielectricMaterialModelType`: Type of the dielectric material model."""
        return DielectricMaterialModelType(self.__stub.GetType(self.msg).value)
