"""Stackup Layer."""

from enum import Enum

import ansys.api.edb.v1.stackup_layer_pb2 as stackup_layer_pb2

from ...interfaces.grpc import messages
from ...session import get_stackup_layer_stub
from ...utility.edb_errors import handle_grpc_exception
from .layer import Layer


class DCThicknessType(Enum):
    """Enum representing DC thickness types of StackupLayers."""

    EFFECTIVE = stackup_layer_pb2.HFSSSolverPropertiesMessage.EFFECTIVE
    LAYER = stackup_layer_pb2.HFSSSolverPropertiesMessage.LAYER
    MANUAL = stackup_layer_pb2.HFSSSolverPropertiesMessage.MANUAL


class StackupLayer(Layer):
    """Stackup layer."""

    @staticmethod
    @handle_grpc_exception
    def create(name, layer_type, thickness, elevation, material):
        """Create a stackup layer.

        Parameters
        name : str
        layer_type : LayerType
        thickness : float
        thickness : float
        material : str
        layout : Layout, optional
        negative : bool, optional

        Returns
        -------
        StackupLayer
        """
        params = {
            "name": name,
            "type": layer_type.value,
            "thickness": messages.value_message(thickness),
            "elevation": messages.value_message(elevation),
            "material": material,
        }

        stackup_layer = StackupLayer(
            get_stackup_layer_stub().Create(stackup_layer_pb2.StackupLayerCreationMessage(**params))
        )
        return stackup_layer

    @property
    @handle_grpc_exception
    def negative(self):
        """Get the negative property of the layer.

        Returns
        -------
        bool
        """
        return get_stackup_layer_stub().GetNegative(self.msg).value

    @negative.setter
    @handle_grpc_exception
    def negative(self, is_negative):
        """Set the negative property of the layer.

        Parameters
        ----------
        is_negative : bool
        """
        get_stackup_layer_stub().SetNegative(
            stackup_layer_pb2.SetNegativeMessage(layer=self.msg, is_negative=is_negative)
        )

    @property
    @handle_grpc_exception
    def thickness(self):
        """Get the thickness value of the layer.

        Returns
        -------
        Value
        """
        # TODO once Brad's changes are merged
        pass

    @thickness.setter
    @handle_grpc_exception
    def thickness(self, thickness):
        """Set the thickness value of the layer.

        Parameters
        ----------
        thickness : Value
        """
        # TODO once Brad's changes are merged
        pass

    @property
    @handle_grpc_exception
    def lower_elevation(self):
        """Get the lower elevation value of the layer.

        Returns
        -------
        Value
        """
        # TODO once Brad's changes are merged
        pass

    @lower_elevation.setter
    @handle_grpc_exception
    def lower_elevation(self, lower_elevation):
        """Set the lower elevation value of the layer.

        Parameters
        ----------
        lower_elevation : Value
        """
        # TODO once Brad's changes are merged
        pass

    @property
    @handle_grpc_exception
    def upper_elevation(self):
        """Get the upper elevation value of the layer.

        Returns
        -------
        Value
        """
        # TODO once Brad's changes are merged
        pass

    @property
    @handle_grpc_exception
    def material(self):
        """Get the name of the material of the layer.

        Returns
        -------
        str
        """
        return get_stackup_layer_stub().GetMaterial(self.msg)

    @material.setter
    @handle_grpc_exception
    def material(self, material_name):
        """Set the name of the material of the layer.

        Parameters
        ----------
        material_name : str
        """
        get_stackup_layer_stub().SetMaterial(
            stackup_layer_pb2.SetMaterialMessage(layer=self.msg, value=material_name)
        )

    @property
    @handle_grpc_exception
    def fill_material(self):
        """Get the name of the material of the layer.

        Returns
        -------
        str
        """
        return get_stackup_layer_stub().GetMaterial(self.msg)

    @fill_material.setter
    @handle_grpc_exception
    def fill_material(self, fill_material_name):
        """Set the name of the fill material of the layer.

        Parameters
        ----------
        fill_material_name : str
        """
        get_stackup_layer_stub().SetFillMaterial(
            stackup_layer_pb2.SetMaterialMessage(layer=self.msg, value=fill_material_name)
        )

    @property
    @handle_grpc_exception
    def roughness_enabled(self):
        """Check if roughness models are used by the layer.

        Returns
        -------
        bool
        """
        return get_stackup_layer_stub().IsRoughnessEnabled(self.msg).value

    @roughness_enabled.setter
    @handle_grpc_exception
    def roughness_enabled(self, enable_roughness):
        """Set if roughness models are used by the layer.

        Parameters
        ----------
        enable_roughness : bool
        """
        get_stackup_layer_stub().SetRoughnessEnabled(
            stackup_layer_pb2.SetLayerPropEnabledMessage(layer=self.msg, enabled=enable_roughness)
        )

    @property
    @handle_grpc_exception
    def roughness_model(self):
        """Get the roughness model used by the layer.

        Returns
        -------
        Value or tuple[Value, Value]
            If a Groisse roughness model is being used by the layer, a single Value
            object is returned representing the roughness value. If a Huray roughness
            model us being used,the returned value is a tuple of the form
            [nodule_radius_value, surface_ratio_value]
        """
        # TODO once Brad's changes are merged
        pass

    @roughness_model.setter
    @handle_grpc_exception
    def roughness_model(self, roughness_model):
        """Set the roughness model used by the layer.

        Parameters
        ----------
        roughness_model : Value or tuple[Value, Value]
            If roughness_model is a single Value object, a Groisse roughness model
            with a roughness value equal to the provided value will be assigned to
            the layer. If roughness_model is a tuple of two Value objects, a Huray
            roughness model will be assigned to the layer with a nodule radius value
            equal to roughness_model[0] and a surface ratio value equal to roughness_model[1]
        """
        # TODO once Brad's changes are merged
        pass

    @property
    @handle_grpc_exception
    def etch_factor_enabled(self):
        """Check if etch factor is used by the layer.

        Returns
        -------
        bool
        """
        return get_stackup_layer_stub().IsEtchFactorEnabled(self.msg).value

    @etch_factor_enabled.setter
    @handle_grpc_exception
    def etch_factor_enabled(self, enable_etch_factor):
        """Set if etch factor is used by the layer.

        Parameters
        ----------
        enable_etch_factor : bool
        """
        get_stackup_layer_stub().SetEtchFactorEnabled(
            stackup_layer_pb2.SetLayerPropEnabledMessage(layer=self.msg, enabled=enable_etch_factor)
        )

    @property
    @handle_grpc_exception
    def etch_factor(self):
        """Get the etch factor of the layer.

        Returns
        -------
        Value
        """
        # TODO once Brad's changes are merged
        pass

    @etch_factor.setter
    @handle_grpc_exception
    def etch_factor(self, etch_factor):
        """Set the etch factor of the layer.

        Parameters
        ----------
        etch_factor : Value
        """
        # TODO once Brad's changes are merged
        pass

    @property
    @handle_grpc_exception
    def use_solver_properties(self):
        """Check if solver properties are used by the layer.

        Returns
        -------
        bool
        """
        return get_stackup_layer_stub().IsEtchFactorEnabled(self.msg).value

    @use_solver_properties.setter
    @handle_grpc_exception
    def use_solver_properties(self, use_solver_properties):
        """Set if solver properties are used by the layer.

        Parameters
        ----------
        use_solver_properties : bool
        """
        get_stackup_layer_stub().SetUseSolverProperties(
            stackup_layer_pb2.SetLayerPropEnabledMessage(
                layer=self.msg, enabled=use_solver_properties
            )
        )

    @property
    @handle_grpc_exception
    def hfss_solver_properties(self):
        """Get the solver properties of the layer.

        Returns
        -------
        tuple[DCThicknessType, Value, bool]
            Tuple is of the form [dc_thickness_type, dc_thickness_value, solve_inside_enabled]
        """
        # TODO once Brad's changes are merged
        pass

    @hfss_solver_properties.setter
    @handle_grpc_exception
    def hfss_solver_properties(self, hfss_solver_props):
        """Set the solver properties of the layer.

        Parameters
        ----------
        tuple[DCThicknessType, Value, bool]
            Tuple is of the form [dc_thickness_type, dc_thickness_value, solve_inside_enabled]
        """
        # TODO once Brad's changes are merged
        pass

    @property
    @handle_grpc_exception
    def referencing_via_layer_ids(self):
        """Retrieve the layer ids of all via layers referencing the layer.

        Returns
        -------
        list[int]
        """
        return [
            via_lyr_id
            for via_lyr_id in get_stackup_layer_stub()
            .GetReferencingViaLayerIds(self.msg)
            .ref_layer_ids
        ]
