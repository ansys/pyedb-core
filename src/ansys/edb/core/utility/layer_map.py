"""Layer Map."""

from enum import Enum

from ansys.api.edb.v1 import layer_map_pb2 as pb

from ..interfaces.grpc import messages
from ..models.base import ObjBase
from ..session import get_layer_map_stub
from .edb_errors import handle_grpc_exception


class _QueryBuilder:
    @staticmethod
    def layer_map_unique_direction_message(direction):
        """Create a LayerMapUniqueDirection Message.

        Parameters
        ----------
        direction: LayerMapUniqueDirection
        """
        return pb.LayerMapUniqueDirectionMessage(
            direction=direction.value,
        )

    @staticmethod
    def layer_map_two_int_properties_message(target, from_id, to_id):
        """Create a LayerMapTwoIntProperties Message.

        Parameters
        ----------
        target: LayerMapUniqueDirection
        from_id: int
        to_id: int
        """
        return pb.LayerMapTwoIntPropertiesMessage(
            target=target,
            from_id=from_id,
            to_id=to_id,
        )


class LayerMap(ObjBase):
    """Class representing a Layer Map two way map where key and val is layer id."""

    class LayerMapUniqueDirection(Enum):
        """Enum representing unique direction."""

        FORWARD_UNIQUE = pb.FORWARD_UNIQUE
        BACKWARD_UNIQUE = pb.BACKWARD_UNIQUE
        TWOWAY_UNIQUE = pb.TWOWAY_UNIQUE
        ILLEGAL_UNIQUE_DIRECTION = pb.ILLEGAL_UNIQUE_DIRECTION

    @staticmethod
    @handle_grpc_exception
    def create(direction):
        """Create a LayerMap object.

        Parameters
        ----------
        direction: LayerMapUniqueDirection
                Variable representing map's direction

        Returns
        -------
        LayerMap
            The LayerMap Object that was created.
        """
        return LayerMap(
            get_layer_map_stub().Create(_QueryBuilder.layer_map_unique_direction_message(direction))
        )

    @handle_grpc_exception
    def clear(self):
        """Clear a LayerMap's entries."""
        get_layer_map_stub().Clear(
            self.msg,
        )

    @handle_grpc_exception
    def set_mapping(self, from_id, to_id):
        """Create an entry to the LayerMap object.

        Parameters
        ----------
        from_id: int
            Layer Id (key) "from" which to map with the "to_id"
        to_id: int
            Layer Id (value) "to" which to map with the "from_id"
        """
        get_layer_map_stub().SetMapping(
            _QueryBuilder.layer_map_two_int_properties_message(
                target=self.msg,
                from_id=from_id,
                to_id=to_id,
            )
        )

    @handle_grpc_exception
    def get_mapping_forward(self, layer_id):
        """Get list of ids mapped forward with the given id (key)."""
        msg = get_layer_map_stub().GetMappingForward(
            messages.int_property_message(
                target=self,
                value=layer_id,
            )
        )
        return [int(to_id) for to_id in msg.ids]

    @handle_grpc_exception
    def get_mapping_backward(self, layer_id):
        """Get list of ids mapped backward with the given id (value)."""
        msg = get_layer_map_stub().GetMappingBackward(
            messages.int_property_message(
                target=self,
                value=layer_id,
            )
        )
        return [int(from_id) for from_id in msg.ids]
