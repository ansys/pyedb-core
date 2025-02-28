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
from ansys.api.edb.v1 import multipole_debye_model_pb2_grpc
import ansys.api.edb.v1.multipole_debye_model_pb2 as pb
from google.protobuf import empty_pb2

from ansys.edb.core import session
from ansys.edb.core.definition.dielectric_material_model import DielectricMaterialModel
from ansys.edb.core.inner import messages


class MultipoleDebyeModel(DielectricMaterialModel):
    """Represents a dielectric material model."""

    __stub: multipole_debye_model_pb2_grpc.MultipoleDebyeModelServiceStub = session.StubAccessor(
        session.StubType.multipole_debye_model
    )

    @classmethod
    def create(cls):
        """Create a multipole Debye dielectric material model.

        Returns
        -------
        MultipoleDebyeModel
        """
        return MultipoleDebyeModel(cls.__stub.Create(empty_pb2.Empty()))

    def get_parameters(self):
        """Get parameters used to define the model.

        Returns
        -------
        frequencies : list[float]
            List of frequencies.
        permitivities : list[float]
            List of relative permitivites at each frequency.
        loss_tangents : list[float]
            List of loss tangents at each frequency.
        """
        parameters_msg = self.__stub.GetParameters(messages.edb_obj_message(self))
        return (
            [i.value for i in parameters_msg.frequencies],
            [i.value for i in parameters_msg.relative_permitivities],
            [i.value for i in parameters_msg.loss_tangents],
        )

    def set_parameters(self, frequencies, permitivities, loss_tangents):
        """Set parameters used to define the model.

        Parameters
        ----------
        frequencies : list[float]
            List of frequencies.
        permitivities : list[float]
            List of relative permitivites at each frequency.
        loss_tangents : list[float]
            List of loss tangents at each frequency.
        """
        frequencies_msg = [messages.double_message(i) for i in frequencies]
        permitivities_msg = [messages.double_message(i) for i in permitivities]
        loss_tangents_msg = [messages.double_message(i) for i in loss_tangents]
        self.__stub.SetParameters(
            pb.MultipoleDebyeModelSetParams(
                target=self.msg,
                vectors=pb.MultipoleDebyeModelGetParams(
                    frequencies=frequencies_msg,
                    relative_permitivities=permitivities_msg,
                    loss_tangents=loss_tangents_msg,
                ),
            )
        )
