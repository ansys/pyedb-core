"""Dielectric material definition."""
from __future__ import annotations

from typing import Tuple

from ansys.api.edb.v1 import debye_model_pb2_grpc
import ansys.api.edb.v1.debye_model_pb2 as pb
from google.protobuf import empty_pb2

from ansys.edb.core import session
from ansys.edb.core.definition.dielectric_material_model import DielectricMaterialModel
from ansys.edb.core.inner import messages


class DebyeModel(DielectricMaterialModel):
    """Represents a Debye dielectric material model."""

    __stub: debye_model_pb2_grpc.DebyeModelServiceStub = session.StubAccessor(
        session.StubType.debye_model
    )

    @classmethod
    def create(cls) -> DebyeModel:
        """Create a Debye dielectric material model.

        Returns
        -------
        .DebyeModel
        """
        return DebyeModel(cls.__stub.Create(empty_pb2.Empty()))

    @property
    def frequency_range(self) -> Tuple[float, float]:
        """:obj:`tuple` of (:obj:`float`, :obj:`float`): Frequency range (low, high)."""
        range_msg = self.__stub.GetFrequencyRange(messages.edb_obj_message(self))
        return range_msg.low.value, range_msg.high.value

    @frequency_range.setter
    def frequency_range(self, freq: Tuple[float, float]):
        low = freq[0]
        high = freq[1]
        self.__stub.SetFrequencyRange(DebyeModel._set_frequency_range_message(self, low, high))

    @property
    def relative_permittivity_at_high_low_frequency(self) -> Tuple[float, float]:
        """:obj:`tuple` of (:obj:`float`, :obj:`float`): \
        Relative permittivity value at the frequency range minimum and maximum.

        Tuple is of the form ``(rel_perm_at_min_freq, rel_perm_at_max_freq)``.
        """
        range_msg = self.__stub.GetRelativePermitivityAtHighLowFrequency(
            messages.edb_obj_message(self)
        )
        return range_msg.low.value, range_msg.high.value

    @relative_permittivity_at_high_low_frequency.setter
    def relative_permittivity_at_high_low_frequency(self, freq: Tuple[float, float]):
        low = freq[0]
        high = freq[1]
        self.__stub.SetRelativePermitivityAtHighLowFrequency(
            DebyeModel._set_frequency_range_message(self, low, high)
        )

    @property
    def loss_tangent_at_high_low_frequency(self) -> Tuple[float, float]:
        """:obj:`tuple` of (:obj:`float`, :obj:`float`): \
        Dielectric loss tangent value at the frequency range minimum and maximum.

        Tuple is of the form ``(diel_loss_tan_at_min_freq, diel_loss_tan_at_max_freq)``.
        """
        range_msg = self.__stub.GetLossTangentAtHighLowFrequency(messages.edb_obj_message(self))
        return range_msg.low.value, range_msg.high.value

    @loss_tangent_at_high_low_frequency.setter
    def loss_tangent_at_high_low_frequency(self, freq: Tuple[float, float]):
        low = freq[0]
        high = freq[1]
        self.__stub.SetLossTangentAtHighLowFrequency(
            DebyeModel._set_frequency_range_message(self, low, high)
        )

    @property
    def is_relative_permitivity_enabled_at_optical_frequency(self) -> bool:
        """:obj:`bool`: Flag indicating if the relative permittivity at optical frequency is enabled."""
        return self.__stub.IsRelativePermitivityEnabledAtOpticalFrequency(self.msg).value

    @is_relative_permitivity_enabled_at_optical_frequency.setter
    def is_relative_permitivity_enabled_at_optical_frequency(self, enabled: bool):
        self.__stub.SetRelativePermitivityEnabledAtOpticalFrequency(
            messages.bool_property_message(self, enabled)
        )

    @property
    def use_dc_conductivity(self) -> bool:
        """:obj:`bool`: Flag indicating if the DC conductivity nominal value is used."""
        return self.__stub.UseDCConductivity(self.msg).value

    @use_dc_conductivity.setter
    def use_dc_conductivity(self, enabled: bool):
        self.__stub.SetUseDCConductivity(messages.bool_property_message(self, enabled))

    @property
    def relative_permittivity_at_optical_frequency(self) -> float:
        """:obj:`float`: Relative permittivity value at the optical frequency."""
        return self.__stub.GetRelativePermitivityAtOpticalFrequency(self.msg).value

    @relative_permittivity_at_optical_frequency.setter
    def relative_permittivity_at_optical_frequency(self, frequency: float):
        self.__stub.SetRelativePermitivityAtOpticalFrequency(
            messages.double_property_message(self, frequency)
        )

    @property
    def dc_conductivity(self) -> float:
        """:obj:`float`: DC conductivity nominal value."""
        return self.__stub.GetDCConductivity(self.msg).value

    @dc_conductivity.setter
    def dc_conductivity(self, conductivity: float):
        self.__stub.SetDCConductivity(messages.double_property_message(self, conductivity))

    @staticmethod
    def _frequency_range_message(low, high):
        return pb.FrequencyRangeMessage(
            low=messages.double_message(low), high=messages.double_message(high)
        )

    @staticmethod
    def _set_frequency_range_message(target, low, high):
        return pb.SetFrequencyRangeMessage(
            target=target.msg,
            range=DebyeModel._frequency_range_message(low, high),
        )
