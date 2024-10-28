# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Dielectric material definition."""
from ansys.api.edb.v1 import djordjecvic_sarkar_model_pb2_grpc
from google.protobuf import empty_pb2

from ansys.edb.core import session
from ansys.edb.core.definition.dielectric_material_model import DielectricMaterialModel
from ansys.edb.core.inner import messages


class DjordjecvicSarkarModel(DielectricMaterialModel):
    """Represents a Djordjecvic-Sarkar dielectric material model object."""

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
        return DjordjecvicSarkarModel(cls.__stub.Create(empty_pb2.Empty()))

    @property
    def use_dc_relative_conductivity(self):
        """:obj:`bool`: Flag indicating whether the DC relative permitivity nominal value is used."""
        return self.__stub.UseDCRelativePermitivity(self.msg).value

    @use_dc_relative_conductivity.setter
    def use_dc_relative_conductivity(self, enabled):
        self.__stub.SetUseDCRelativePermitivity(messages.bool_property_message(self, enabled))

    @property
    def frequency(self):
        """:obj:`float`: Frequency."""
        return self.__stub.GetFrequency(self.msg).value

    @frequency.setter
    def frequency(self, frequency):
        self.__stub.SetFrequency(messages.double_property_message(self, frequency))

    @property
    def relative_permitivity_at_frequency(self):
        """:obj:`float`: Relative permitivity frequency."""
        return self.__stub.GetRelativePermitivityAtFrequency(self.msg).value

    @relative_permitivity_at_frequency.setter
    def relative_permitivity_at_frequency(self, frequency):
        self.__stub.SetRelativePermitivityAtFrequency(
            messages.double_property_message(self, frequency)
        )

    @property
    def loss_tangent_at_frequency(self):
        """:obj:`float`: Loss tangent at frequency."""
        return self.__stub.GetLossTangentAtFrequency(self.msg).value

    @loss_tangent_at_frequency.setter
    def loss_tangent_at_frequency(self, frequency):
        self.__stub.SetLossTangentAtFrequency(messages.double_property_message(self, frequency))

    @property
    def dc_relative_permitivity(self):
        """:obj:`float`: DC relative permitivity."""
        return self.__stub.GetDCRelativePermitivity(self.msg).value

    @dc_relative_permitivity.setter
    def dc_relative_permitivity(self, permitivity):
        self.__stub.SetDCRelativePermitivity(messages.double_property_message(self, permitivity))

    @property
    def dc_conductivity(self):
        """:obj:`float`: DC conductivity."""
        return self.__stub.GetDCConductivity(self.msg).value

    @dc_conductivity.setter
    def dc_conductivity(self, conductivity):
        self.__stub.SetDCConductivity(messages.double_property_message(self, conductivity))
