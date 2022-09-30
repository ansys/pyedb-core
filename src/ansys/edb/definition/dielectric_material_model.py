"""Dielectric Material Definition."""
from enum import Enum

from ansys.api.edb.v1 import dielectric_material_model_pb2_grpc
import ansys.api.edb.v1.dielectric_material_model_pb2 as pb

from ansys.edb import session
from ansys.edb.core import ObjBase, messages
from ansys.edb.utility import Value


class _DielectricMaterialModelQueryBuilder:
    @staticmethod
    def frequency_range_message():
        return pb.FrequencyRangeMessage(
            low=messages.value_message(low), high=messages.value_message(high)
        )

    @staticmethod
    def set_frequency_range_message(target, low, high):
        return pb.SetFrequencyRangeMessage(
            target=target.msg,
            value=_DielectricMaterialModelQueryBuilder.frequency_range_message(low, high),
        )

    @staticmethod
    def multipole_debye_modelget_params(frequencies, permitivities, loss_tangents):
        frequencies_msg = [messages.value_message(i) for i in frequencies]
        permitivities_msg = [messages.value_message(i) for i in permitivities]
        loss_tangents_msg = [messages.value_message(i) for i in loss_tangents]
        return pb.MultipoleDebyeModelGetParams(
            frequencies=frequencies_msg,
            relative_permitivities=permitivities_msg,
            loss_tangents=loss_tangents_msg,
        )

    @staticmethod
    def set_multipole_debye_modelget_params(target, frequencies, permitivities, loss_tangents):
        return pb.MultipoleDebyeModelSetParams(
            target=target.msg,
            value=_DielectricMaterialModelQueryBuilder.multipole_debye_modelget_params(
                frequencies, permitivities, loss_tangents
            ),
        )


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


class DebyeModel(DielectricMaterialModel):
    """Class representing a debye dielectric material model object."""

    __stub: dielectric_material_model_pb2_grpc.DebyeModelServiceStub = session.StubAccessor(
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
            _DielectricMaterialModelQueryBuilder.frequency_range_message(self, low, high)
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
            _DielectricMaterialModelQueryBuilder.frequency_range_message(self, low, high)
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
            _DielectricMaterialModelQueryBuilder.frequency_range_message(self, low, high)
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


class MultipoleDebyeModel(DielectricMaterialModel):
    """Class representing a dielectric material model."""

    __stub: dielectric_material_model_pb2_grpc.MultipoleDebyeModelServiceStub = (
        session.StubAccessor(session.StubType.multipole_debye_model)
    )

    @classmethod
    def create(cls):
        """Create a Multipole Debye Dielectric Material Model.

        Returns
        -------
        MultipoleDebyeModel
        """
        return MultipoleDebyeModel(cls.__stub.Create())

    def get_parameters(self):
        """Get parameters used to define the model.

        Returns
        -------
        frequencies : :class:`Value <ansys.edb.utility.Value>`
            List of frequencies.
        permitivities : :class:`Value <ansys.edb.utility.Value>`
            List of relative permitivites at each frequency.
        loss_tangents : :class:`Value <ansys.edb.utility.Value>`
            List of loss tangents at each frequency.
        """
        parameters_msg = self.__stub.GetParameters(messages.edb_obj_message(self))
        return (
            [Value(i) for i in parameters_msg.frequencies],
            [Value(i) for i in parameters_msg.relative_permitivities],
            [Value(i) for i in parameters_msg.loss_tangents],
        )

    def set_parameters(self, frequencies, permitivities, loss_tangents):
        """Set parameters used to define the model.

        Parameters
        ----------
        frequencies : :class:`Value <ansys.edb.utility.Value>`
            List of frequencies.
        permitivities : :class:`Value <ansys.edb.utility.Value>`
            List of relative permitivites at each frequency.
        loss_tangents : :class:`Value <ansys.edb.utility.Value>`
            List of loss tangents at each frequency.
        """
        _DielectricMaterialModelQueryBuilder.set_multipole_debye_modelget_params(
            self, frequencies, permitivities, loss_tangents
        )


class DjordjecvicSarkarModel(DielectricMaterialModel):
    """Class representing a Djordjecvic-Sarkar dielectric material model object."""

    __stub: dielectric_material_model_pb2_grpc.DjordjecvicSarkarModelServiceStub = (
        session.StubAccessor(session.StubType.djordecvic_sarkar_model)
    )

    @classmethod
    def create(cls):
        """Create a Djordjecvic Sarkar dielectric material model.

        Returns
        -------
        DjordjecvicSarkarModel
        """
        return DjordjecvicSarkarModel(cls.__stub.Create())

    @property
    def use_dc_relative_conductivity(self):
        """Whether the DC relative permitivity nominal value is used.

        Returns
        -------
        bool
        """
        return self.__stub.UseDCRelativePermitivity(self.msg).value

    @use_dc_relative_conductivity.setter
    def use_dc_relative_conductivity(self, enabled):
        self.__stub.SetUseDCRelativePermitivity(messages.bool_property_message(self, enabled))

    @property
    def frequency(self):
        """Get the frequency.

        Returns
        -------
        :class:`Value <ansys.edb.utility.Value>`
        """
        return Value(self.__stub.GetFrequency(self.msg))

    @frequency.setter
    def frequency(self, frequency):
        self.__stub.SetFrequency(messages.value_message(frequency))

    @property
    def relative_permitivity_at_frequency(self):
        """Get the relative permitivity frequency.

        Returns
        -------
        :class:`Value <ansys.edb.utility.Value>`
        """
        return Value(self.__stub.GetRelativePermitivityAtFrequency(self.msg))

    @relative_permitivity_at_frequency.setter
    def relative_permitivity_at_frequency(self, frequency):
        self.__stub.SetRelativePermitivityAtFrequency(messages.value_message(frequency))

    @property
    def loss_tangent_at_frequency(self):
        """Get the loss tangent at frequency.

        Returns
        -------
        :class:`Value <ansys.edb.utility.Value>`
        """
        return Value(self.__stub.GetLossTangentAtFrequency(self.msg))

    @loss_tangent_at_frequency.setter
    def loss_tangent_at_frequency(self, frequency):
        self.__stub.SetLossTangentAtFrequency(messages.value_message(frequency))

    @property
    def dc_relative_permitivity(self):
        """Get the dc relative permitivity.

        Returns
        -------
        :class:`Value <ansys.edb.utility.Value>`
        """
        return Value(self.__stub.GetDCRelativePermitivity(self.msg))

    @dc_relative_permitivity.setter
    def dc_relative_permitivity(self, permitivity):
        self.__stub.SetDCRelativePermitivity(messages.value_message(permitivity))

    @property
    def dc_conductivity(self):
        """Get the dc conductivity.

        Returns
        -------
        :class:`Value <ansys.edb.utility.Value>`
        """
        return Value(self.__stub.GetDCConductivity(self.msg))

    @dc_conductivity.setter
    def dc_conductivity(self, conductivity):
        self.__stub.SetDCConductivity(messages.value_message(conductivity))
