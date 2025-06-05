"""Dielectric material definition."""
from __future__ import annotations

from ansys.api.edb.v1 import djordjecvic_sarkar_model_pb2_grpc
from google.protobuf import empty_pb2

from ansys.edb.core import session
from ansys.edb.core.definition.dielectric_material_model import DielectricMaterialModel
from ansys.edb.core.inner import messages


class DjordjecvicSarkarModel(DielectricMaterialModel):
    """Represents a Djordjecvic-Sarkar dielectric material model."""

    __stub: djordjecvic_sarkar_model_pb2_grpc.DjordjecvicSarkarModelServiceStub = (
        session.StubAccessor(session.StubType.djordecvic_sarkar_model)
    )

    @classmethod
    def create(cls) -> DjordjecvicSarkarModel:
        """Create a Djordjecvic Sarkar dielectric material model.

        Returns
        -------
        .DjordjecvicSarkarModel
        """
        return DjordjecvicSarkarModel(cls.__stub.Create(empty_pb2.Empty()))

    @property
    def use_dc_relative_conductivity(self) -> bool:
        """:obj:`bool`: Flag indicating whether the DC relative permittivity nominal value is used."""
        return self.__stub.UseDCRelativePermitivity(self.msg).value

    @use_dc_relative_conductivity.setter
    def use_dc_relative_conductivity(self, enabled: bool):
        self.__stub.SetUseDCRelativePermitivity(messages.bool_property_message(self, enabled))

    @property
    def frequency(self) -> float:
        """:obj:`float`: Frequency value."""
        return self.__stub.GetFrequency(self.msg).value

    @frequency.setter
    def frequency(self, frequency: float):
        self.__stub.SetFrequency(messages.double_property_message(self, frequency))

    @property
    def relative_permittivity_at_frequency(self) -> float:
        """:obj:`float`: Relative permittivity value at the specified :meth:`frequency <.frequency>`."""
        return self.__stub.GetRelativePermitivityAtFrequency(self.msg).value

    @relative_permittivity_at_frequency.setter
    def relative_permittivity_at_frequency(self, frequency: float):
        self.__stub.SetRelativePermitivityAtFrequency(
            messages.double_property_message(self, frequency)
        )

    @property
    def loss_tangent_at_frequency(self) -> float:
        """:obj:`float`: Loss tangent value at the specified :meth:`frequency <.frequency>`."""
        return self.__stub.GetLossTangentAtFrequency(self.msg).value

    @loss_tangent_at_frequency.setter
    def loss_tangent_at_frequency(self, frequency: float):
        self.__stub.SetLossTangentAtFrequency(messages.double_property_message(self, frequency))

    @property
    def dc_relative_permittivity(self) -> float:
        """:obj:`float`: DC relative permittivity value."""
        return self.__stub.GetDCRelativePermitivity(self.msg).value

    @dc_relative_permittivity.setter
    def dc_relative_permittivity(self, permittivity: float):
        self.__stub.SetDCRelativePermitivity(messages.double_property_message(self, permittivity))

    @property
    def dc_conductivity(self) -> float:
        """:obj:`float`: DC conductivity value."""
        return self.__stub.GetDCConductivity(self.msg).value

    @dc_conductivity.setter
    def dc_conductivity(self, conductivity: float):
        self.__stub.SetDCConductivity(messages.double_property_message(self, conductivity))
