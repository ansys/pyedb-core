"""Layer map."""

from enum import Enum

from ansys.api.edb.v1 import layer_map_pb2 as pb

from ansys.edb.core.inner import ObjBase, messages
from ansys.edb.core.session import StubAccessor, StubType


class _QueryBuilder:
    @staticmethod
    def layer_map_unique_direction_message(direction):
        """Create a ``LayerMapUniqueDirection`` message.

        Parameters
        ----------
        direction: LayerMapUniqueDirection
        """
        return pb.LayerMapUniqueDirectionMessage(
            direction=direction.value,
        )

    @staticmethod
    def layer_map_two_int_properties_message(target, from_id, to_id):
        """Create a ``LayerMapTwoIntProperties`` message.

        Parameters
        ----------
        target: LayerMapUniqueDirection
        from_id: int
        to_id: int
        """
        return pb.LayerMapTwoIntPropertiesMessage(
            target=target,
            from_id=messages.edb_internal_id_message(from_id),
            to_id=messages.edb_internal_id_message(to_id),
        )


class LayerMap(ObjBase):
    """Represents a two-way layer map where the key and value is the layer ID."""

    __stub = StubAccessor(StubType.layer_map)

    class LayerMapUniqueDirection(Enum):
        """Provides an enum representing a unique direction."""

        FORWARD_UNIQUE = pb.FORWARD_UNIQUE
        """FORWARD_UNIQUE Mapping many to one (1,1), (2,1), (3,1)"""
        BACKWARD_UNIQUE = pb.BACKWARD_UNIQUE
        """BACKWARD_UNIQUE Mapping one to many (1,1), (1,2), (1,3)"""
        TWOWAY_UNIQUE = pb.TWOWAY_UNIQUE
        """TWOWAY_UNIQUE Mapping one to one (1,1), (2,3), (3,2)"""

    @staticmethod
    def create(direction):
        """Create a layer map object.

        Parameters
        ----------
        direction: LayerMapUniqueDirection
                Variable representing the map's direction.

        Returns
        -------
        LayerMap
            LayerMap object created.
        """
        return LayerMap(
            StubAccessor(StubType.layer_map)
            .__get__()
            .Create(_QueryBuilder.layer_map_unique_direction_message(direction))
        )

    def clear(self):
        """Clear the entrties of the layer map."""
        self.__stub.Clear(
            self.msg,
        )

    def set_mapping(self, from_id, to_id):
        """Create an entry in the layer map object.

        Parameters
        ----------
        from_id: int
            Layer ID (key) "from" which to map with the ``to_id`` parameter.
        to_id: int
            Layer ID (value) "to" which to map with the ``from_id`` parameter.
        """
        self.__stub.SetMapping(
            _QueryBuilder.layer_map_two_int_properties_message(
                target=self.msg,
                from_id=from_id,
                to_id=to_id,
            )
        )

    def get_mapping_forward(self, layer_id):
        """Get the list of IDs mapped forward with the given ID (key)."""
        msg = self.__stub.GetMappingForward(
            messages.int_property_message(
                target=self,
                value=layer_id,
            )
        )
        return [int(to_id) for to_id in msg.ids]

    def get_mapping_backward(self, layer_id):
        """Get a list of IDs mapped backward with the given ID (value)."""
        msg = self.__stub.GetMappingBackward(
            messages.int_property_message(
                target=self,
                value=layer_id,
            )
        )
        return [int(from_id) for from_id in msg.ids]
