"""Via Layer."""

import ansys.api.edb.v1.via_layer_pb2 as via_layer_pb2

from ...interfaces.grpc import messages
from ...session import get_via_layer_stub
from ...utility.edb_errors import handle_grpc_exception
from .stackup_layer import StackupLayer


class ViaLayer(StackupLayer):
    """Via layer."""

    @staticmethod
    @handle_grpc_exception
    def create(name, lr_layer, ur_layer, material, layout=None):
        """Create a via layer.

        Parameters
        ----------
        name : str
        lr_layer : str
        ur_layer : str
        material : str
        layout : Layout, optional

        Returns
        -------
        ViaLayer
        """
        params = {
            "via_layer_name": name,
            "lower_ref_layer_name": lr_layer,
            "upper_ref_layer_name": ur_layer,
            "material_name": material,
        }
        messages.optional(params, "layout", layout, messages.edb_obj_message)
        via_layer = ViaLayer(
            get_via_layer_stub().Create(via_layer_pb2.ViaLayerCreationMessage(**params))
        )
        via_layer._is_owner = True
        return via_layer
