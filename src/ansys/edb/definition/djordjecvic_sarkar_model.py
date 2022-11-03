"""Dielectric Material Definition."""

from ansys.api.edb.v1 import djordjecvic_sarkar_model_pb2_grpc

from ansys.edb import session
from ansys.edb.core import messages
from ansys.edb.definition.dielectric_material_model import DielectricMaterialModel
from ansys.edb.utility import Value


class DjordjecvicSarkarModel(DielectricMaterialModel):
    """Class representing a Djordjecvic-Sarkar dielectric material model object."""

    __stub: djordjecvic_sarkar_model_pb2_grpc.DjordjecvicSarkarModelServiceStub = (
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
