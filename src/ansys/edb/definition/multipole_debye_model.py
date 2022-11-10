"""Dielectric Material Definition."""

from ansys.api.edb.v1 import multipole_debye_model_pb2_grpc
import ansys.api.edb.v1.multipole_debye_model_pb2 as pb

from ansys.edb import session
from ansys.edb.core import messages
from ansys.edb.definition.dielectric_material_model import DielectricMaterialModel


class _MultipoleDebyeModelQueryBuilder:
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
            value=_MultipoleDebyeModelQueryBuilder.multipole_debye_modelget_params(
                frequencies, permitivities, loss_tangents
            ),
        )


class MultipoleDebyeModel(DielectricMaterialModel):
    """Class representing a dielectric material model."""

    __stub: multipole_debye_model_pb2_grpc.MultipoleDebyeModelServiceStub = session.StubAccessor(
        session.StubType.multipole_debye_model
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
        frequencies : list[float]
            List of frequencies.
        permitivities : list[float]
            List of relative permitivites at each frequency.
        loss_tangents : list[float]
            List of loss tangents at each frequency.
        """
        parameters_msg = self.__stub.GetParameters(messages.edb_obj_message(self))
        return (
            [float(i) for i in parameters_msg.frequencies],
            [float(i) for i in parameters_msg.relative_permitivities],
            [float(i) for i in parameters_msg.loss_tangents],
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
        _MultipoleDebyeModelQueryBuilder.set_multipole_debye_modelget_params(
            self, frequencies, permitivities, loss_tangents
        )
