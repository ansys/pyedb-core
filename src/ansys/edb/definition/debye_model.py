"""Dielectric Material Definition."""

from ansys.api.edb.v1 import debye_model_pb2_grpc
import ansys.api.edb.v1.debye_model_pb2 as pb

from ansys.edb import session
from ansys.edb.core import messages
from ansys.edb.definition.dielectric_material_model import DielectricMaterialModel
from ansys.edb.utility import Value


class _DebyeModelQueryBuilder:
    @staticmethod
    def frequency_range_message(low, high):
        return pb.FrequencyRangeMessage(
            low=messages.value_message(low), high=messages.value_message(high)
        )

    @staticmethod
    def set_frequency_range_message(target, low, high):
        return pb.SetFrequencyRangeMessage(
            target=target.msg,
            value=_DebyeModelQueryBuilder.frequency_range_message(low, high),
        )


class DebyeModel(DielectricMaterialModel):
    """Class representing a debye dielectric material model object."""

    __stub: debye_model_pb2_grpc.DebyeModelServiceStub = session.StubAccessor(
        session.StubType.debye_model
    )

    @classmethod
    def create(cls):
        """Create a Debye Dielectric Material Model.

        Returns
        -------
        DebyeModelService
        """
        return DebyeModel(cls.__stub.Create())

    @property
    def frequency_range(self):
        """Frequency range of the debye model.

        Returns
        -------
        low : :class:`Value <ansys.edb.utility.Value>`
            Lower bound of the frequency.
        high : :class:`Value <ansys.edb.utility.Value>`
            Higher bound of the frequency.
        """
        range_msg = self.__stub.IsRelativePermitivityEnabledAtOpticalFrequency(
            messages.edb_obj_message(self)
        )
        return range_msg.low, range_msg.high

    @frequency_range.setter
    def frequency_range(self, low, high):
        self.__stub.IsRelativePermitivityEnabledAtOpticalFrequency(
            _DebyeModelQueryBuilder.frequency_range_message(self, low, high)
        )

    @property
    def relative_permitivity_at_high_low_frequency(self):
        """Get the relative permitivity at low/high frequency.

        Returns
        -------
        low : :class:`Value <ansys.edb.utility.Value>`
            Relative permitivity at the low frequency.
        high : :class:`Value <ansys.edb.utility.Value>`
            Relative permitivity at the high frequency.
        """
        range_msg = self.__stub.GetRelativePermitivityAtHighLowFrequency(
            messages.edb_obj_message(self)
        )
        return range_msg.low, range_msg.high

    @relative_permitivity_at_high_low_frequency.setter
    def relative_permitivity_at_high_low_frequency(self, low, high):
        self.__stub.SetRelativePermitivityAtHighLowFrequency(
            _DebyeModelQueryBuilder.frequency_range_message(self, low, high)
        )

    @property
    def loss_tangent_at_high_low_frequency(self):
        """Get the relative permitivity at low/high frequency.

        Returns
        -------
        low : :class:`Value <ansys.edb.utility.Value>`
            Loss tangent at the low frequency.
        high : :class:`Value <ansys.edb.utility.Value>`
            Loss tangent at the high frequency.
        """
        range_msg = self.__stub.GetLossTangentAtHighLowFrequency(messages.edb_obj_message(self))
        return range_msg.low, range_msg.high

    @loss_tangent_at_high_low_frequency.setter
    def loss_tangent_at_high_low_frequency(self, low, high):
        self.__stub.SetLossTangentAtHighLowFrequency(
            _DebyeModelQueryBuilder.frequency_range_message(self, low, high)
        )

    @property
    def is_relative_permitivity_enabled_at_optical_frequency(self):
        """Whether the relative permitivity at optical frequency is enabled.

        Returns
        -------
        bool
        """
        return self.__stub.IsRelativePermitivityEnabledAtOpticalFrequency(self.msg).value

    @is_relative_permitivity_enabled_at_optical_frequency.setter
    def is_relative_permitivity_enabled_at_optical_frequency(self, enabled):
        self.__stub.IsRelativePermitivityEnabledAtOpticalFrequency(
            messages.bool_property_message(self, enabled)
        )

    @property
    def use_dc_conductivity(self):
        """Whether DC conductivity nominal value is used.

        Returns
        -------
        bool
        """
        return self.__stub.UseDCConductivity(self.msg).value

    @use_dc_conductivity.setter
    def use_dc_conductivity(self, enabled):
        self.__stub.SetUseDCConductivity(messages.bool_property_message(self, enabled))

    @property
    def relative_permitivity_at_optical_frequency(self):
        """Get the relative permitivity at optical frequency.

        Returns
        -------
        :class:`Value <ansys.edb.utility.Value>`
        """
        return Value(self.__stub.GetRelativePermitivityAtOpticalFrequency(self.msg))

    @relative_permitivity_at_optical_frequency.setter
    def relative_permitivity_at_optical_frequency(self, frequency):
        self.__stub.SetRelativePermitivityAtOpticalFrequency(messages.value_message(frequency))

    @property
    def dc_conductivity(self):
        """Get the DC conductivity nominal value.

        Returns
        -------
        :class:`Value <ansys.edb.utility.Value>`
        """
        return Value(self.__stub.GetDCConductivity(self.msg))

    @dc_conductivity.setter
    def dc_conductivity(self, conductivity):
        self.__stub.SetDCConductivity(messages.value_message(conductivity))
