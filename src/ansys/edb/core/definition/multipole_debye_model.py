"""Dielectric material definition."""
from __future__ import annotations

from typing import List, Tuple

from ansys.api.edb.v1 import multipole_debye_model_pb2_grpc
import ansys.api.edb.v1.multipole_debye_model_pb2 as pb
from google.protobuf import empty_pb2

from ansys.edb.core import session
from ansys.edb.core.definition.dielectric_material_model import DielectricMaterialModel
from ansys.edb.core.inner import messages


class MultipoleDebyeModel(DielectricMaterialModel):
    """Represents a multipole Debye dielectric material model."""

    __stub: multipole_debye_model_pb2_grpc.MultipoleDebyeModelServiceStub = session.StubAccessor(
        session.StubType.multipole_debye_model
    )

    @classmethod
    def create(cls) -> MultipoleDebyeModel:
        """Create a multipole Debye dielectric material model.

        Returns
        -------
        .MultipoleDebyeModel
        """
        return MultipoleDebyeModel(cls.__stub.Create(empty_pb2.Empty()))

    @property
    def parameters(self) -> Tuple[List[float], List[float], List[float]]:
        """:obj:`tuple` of (:obj:`list` of :obj:`float`, :obj:`list` of :obj:`float`, :obj:`list` of :obj:`float`): \
        Get parameters used to define the model.

        The tuple is of the form ``(frequencies, relative_permittivities, dielectric_loss_tangents)`` \
        where each relative permittivity and dielectric loss tangent value map to the frequency at the \
        same index as itself.
        """
        parameters_msg = self.__stub.GetParameters(messages.edb_obj_message(self))
        return (
            [i.value for i in parameters_msg.frequencies],
            [i.value for i in parameters_msg.relative_permitivities],
            [i.value for i in parameters_msg.loss_tangents],
        )

    @parameters.setter
    def parameters(self, params: Tuple[List[float], List[float], List[float]]):
        frequencies_msg = [messages.double_message(i) for i in params[0]]
        permitivities_msg = [messages.double_message(i) for i in params[1]]
        loss_tangents_msg = [messages.double_message(i) for i in params[2]]
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
