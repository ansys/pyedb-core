from enum import Enum
from typing import Union

import ansys.api.edb.v1.layer_pb2 as layer_pb2

from ...interfaces.grpc import messages
from ...session import get_layer_stub, get_stackup_layer_stub, get_via_layer_stub
from ...utility.edb_errors import handle_grpc_exception
from ..base import ObjBase


class LayerType(Enum):
    SIGNAL_LAYER = layer_pb2.SIGNAL_LAYER
    DIELECTRIC_LAYER = layer_pb2.DIELECTRIC_LAYER
    CONDUCTING_LAYER = layer_pb2.CONDUCTING_LAYER
    AIRLINES_LAYER = layer_pb2.AIRLINES_LAYER
    ERRORS_LAYER = layer_pb2.ERRORS_LAYER
    SYMBOL_LAYER = layer_pb2.SYMBOL_LAYER
    MEASURE_LAYER = layer_pb2.MEASURE_LAYER
    ASSEMBLY_LAYER = layer_pb2.ASSEMBLY_LAYER
    SILKSCREEN_LAYER = layer_pb2.SILKSCREEN_LAYER
    SOLDER_MASK_LAYER = layer_pb2.SOLDER_MASK_LAYER
    SOLDER_PASTE_LAYER = layer_pb2.SOLDER_PASTE_LAYER
    GLUE_LAYER = layer_pb2.GLUE_LAYER
    WIREBOND_LAYER = layer_pb2.WIREBOND_LAYER
    USER_LAYER = layer_pb2.USER_LAYER
    SIWAVE_HFSS_SOLVER_REGIONS = layer_pb2.SIWAVE_HFSS_SOLVER_REGIONS
    POST_PROCESSING_LAYER = layer_pb2.POST_PROCESSING_LAYER
    OUTLINE_LAYER = layer_pb2.OUTLINE_LAYER
    LAYER_TYPES_COUNT = layer_pb2.LAYER_TYPES_COUNT
    UNDEFINED_LAYER_TYPE = layer_pb2.UNDEFINED_LAYER_TYPE


class Layer(ObjBase):
    def __init__(self, msg):
        super().__init__(msg)
        self._is_owner = False

    def __del__(self):
        if self._is_owner:
            get_layer_stub().Cleanup(self._msg)

    @staticmethod
    @handle_grpc_exception
    def _create(msg) -> Union["Layer", "StackupLayer", "ViaLayer"]:
        lyr = Layer(msg)
        if lyr.is_stackup_layer():
            if lyr.is_via_layer():
                return ViaLayer(msg)
            else:
                return StackupLayer(msg)
        else:
            return lyr

    @handle_grpc_exception
    def get_layer_type(self) -> LayerType:
        return LayerType(get_layer_stub().GetLayerType(self._msg).type)

    @handle_grpc_exception
    def is_stackup_layer(self) -> bool:
        layer_type = self.get_layer_type()
        return (
            layer_type == LayerType.DIELECTRIC_LAYER
            or layer_type == LayerType.CONDUCTING_LAYER
            or layer_type == LayerType.SIGNAL_LAYER
        )

    @handle_grpc_exception
    def is_via_layer(self) -> bool:
        return get_layer_stub().IsViaLayer(self._msg).value

    @handle_grpc_exception
    def get_name(self) -> str:
        return get_layer_stub().GetName(self._msg).value


class StackupLayer(Layer):
    @staticmethod
    @handle_grpc_exception
    def create(name, layer_type, thickness, elevation, material, layout=None, negative=None):
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
            get_stackup_layer_stub().Create(layer_pb2.StackupLayerCreationMessage(**params))
        )
        stackup_layer._is_owner = True
        return stackup_layer

    @handle_grpc_exception
    def set_negative(self, is_negative: bool) -> None:
        return get_stackup_layer_stub().SetNegative(
            layer_pb2.SetNegativeMessage(layer=self._msg, is_negative=is_negative)
        )


class ViaLayer(StackupLayer):
    @staticmethod
    @handle_grpc_exception
    def create(
        name, lower_ref_layer_name, upper_ref_layer_name, material_name, layout=None
    ) -> "ViaLayer":
        params = {
            "via_layer_name": name,
            "lower_ref_layer_name": lower_ref_layer_name,
            "upper_ref_layer_name": upper_ref_layer_name,
            "material_name": material_name,
        }
        messages.optional(params, "layout", layout, messages.edb_obj_message)
        via_layer = ViaLayer(
            get_via_layer_stub().Create(layer_pb2.ViaLayerCreationMessage(**params))
        )
        via_layer._is_owner = True
        return via_layer
