"""Layer Map."""

from enum import Enum

from ansys.api.edb.v1 import layer_map_pb2 as pb

from ansys.edb.core.core import messages
from ansys.edb.core.core.base import ObjBase
from ansys.edb.core.session import StubAccessor, StubType
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

    __stub = StubAccessor(StubType.layer_map)

    class LayerMapUniqueDirection(Enum):
        """Enum representing unique direction."""

        FORWARD_UNIQUE = pb.FORWARD_UNIQUE
        """FORWARD_UNIQUE Mapping many to one (1,1), (2,1), (3,1)"""
        BACKWARD_UNIQUE = pb.BACKWARD_UNIQUE
        """BACKWARD_UNIQUE Mapping one to many (1,1), (1,2), (1,3)"""
        TWOWAY_UNIQUE = pb.TWOWAY_UNIQUE
        """TWOWAY_UNIQUE Mapping one to one (1,1), (2,3), (3,2)"""

    @staticmethod
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
            StubAccessor(StubType.layer_map)
            .__get__()
            .Create(_QueryBuilder.layer_map_unique_direction_message(direction))
        )

    def clear(self):
        """Clear a LayerMap's entries."""
        self.__stub.Clear(
            self.msg,
        )

    def set_mapping(self, from_id, to_id):
        """Create an entry to the LayerMap object.

        Parameters
        ----------
        from_id: int
            Layer Id (key) "from" which to map with the "to_id"
        to_id: int
            Layer Id (value) "to" which to map with the "from_id"
        """
        self.__stub.SetMapping(
            _QueryBuilder.layer_map_two_int_properties_message(
                target=self.msg,
                from_id=from_id,
                to_id=to_id,
            )
        )

    def get_mapping_forward(self, layer_id):
        """Get list of ids mapped forward with the given id (key)."""
        msg = self.__stub.GetMappingForward(
            messages.int_property_message(
                target=self,
                value=layer_id,
            )
        )
        return [int(to_id) for to_id in msg.ids]

    def get_mapping_backward(self, layer_id):
        """Get list of ids mapped backward with the given id (value)."""
        msg = self.__stub.GetMappingBackward(
            messages.int_property_message(
                target=self,
                value=layer_id,
            )
        )
        return [int(from_id) for from_id in msg.ids]
