"""Stackup Layer."""

import ansys.api.edb.v1.stackup_layer_pb2 as stackup_layer_pb2

from ...interfaces.grpc import messages
from ...session import get_stackup_layer_stub
from ...utility.edb_errors import handle_grpc_exception
from .layer import Layer


class StackupLayer(Layer):
    """Stackup layer."""

    @staticmethod
    @handle_grpc_exception
    def create(name, layer_type, thickness, elevation, material, layout=None, negative=None):
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
        messages.optional(params, "layout", layout, messages.edb_obj_message)
        messages.optional(params, "negative", negative, messages.bool_message)

        stackup_layer = StackupLayer(
            get_stackup_layer_stub().Create(stackup_layer_pb2.StackupLayerCreationMessage(**params))
        )
        stackup_layer._is_owner = True
        return stackup_layer

    @handle_grpc_exception
    def set_negative(self, is_negative):
        """Update negative.

        Parameters
        ----------
        is_negative : bool

        Returns
        -------
        bool
        """
        return get_stackup_layer_stub().SetNegative(
            stackup_layer_pb2.SetNegativeMessage(layer=self.msg, is_negative=is_negative)
        )
