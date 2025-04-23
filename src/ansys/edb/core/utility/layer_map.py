"""Layer map."""
from __future__ import annotations

from enum import Enum
from typing import List

from ansys.api.edb.v1 import layer_map_pb2 as pb

from ansys.edb.core.inner import ObjBase, messages
from ansys.edb.core.session import StubAccessor, StubType


class LayerMapUniqueDirection(Enum):
    """Provides an enum representing a unique direction."""

    FORWARD_UNIQUE = pb.FORWARD_UNIQUE
    """FORWARD_UNIQUE Mapping many to one (1,1), (2,1), (3,1)"""
    BACKWARD_UNIQUE = pb.BACKWARD_UNIQUE
    """BACKWARD_UNIQUE Mapping one to many (1,1), (1,2), (1,3)"""
    TWOWAY_UNIQUE = pb.TWOWAY_UNIQUE
    """TWOWAY_UNIQUE Mapping one to one (1,1), (2,3), (3,2)"""


class LayerMap(ObjBase):
    """Represents a two-way layer map where the key and value is the layer ID."""

    __stub = StubAccessor(StubType.layer_map)

    @staticmethod
    def create(direction: LayerMapUniqueDirection) -> LayerMap:
        """Create a layer map object.

        Parameters
        ----------
        direction : .LayerMapUniqueDirection
                Variable representing the map's direction.

        Returns
        -------
        .LayerMap
            LayerMap object created.
        """
        return LayerMap(
            StubAccessor(StubType.layer_map)
            .__get__()
            .Create(pb.LayerMapUniqueDirectionMessage(direction=direction.value))
        )

    def clear(self):
        """Clear the entrties of the layer map."""
        self.__stub.Clear(
            self.msg,
        )

    def set_mapping(self, from_id: int, to_id: int):
        """Create an entry in the layer map object.

        Parameters
        ----------
        from_id : int
            Layer ID (key) "from" which to map with the ``to_id`` parameter.
        to_id : int
            Layer ID (value) "to" which to map with the ``from_id`` parameter.
        """
        self.__stub.SetMapping(
            pb.LayerMapTwoIntPropertiesMessage(
                target=self.msg,
                from_id=messages.edb_internal_id_message(from_id),
                to_id=messages.edb_internal_id_message(to_id),
            )
        )

    def get_mapping_forward(self, layer_id: int) -> List[int]:
        """Get the list of IDs mapped forward with the given ID (key).

        Parameters
        ----------
        layer_id : int

        Returns
        -------
        list of int
        """
        msg = self.__stub.GetMappingForward(
            messages.int_property_message(
                target=self,
                value=layer_id,
            )
        )
        return [int(to_id) for to_id in msg.ids]

    def get_mapping_backward(self, layer_id: int) -> List[int]:
        """Get a list of IDs mapped backward with the given ID (value).

        Parameters
        ----------
        layer_id : int

        Returns
        -------
        list of int
        """
        msg = self.__stub.GetMappingBackward(
            messages.int_property_message(
                target=self,
                value=layer_id,
            )
        )
        return [int(from_id) for from_id in msg.ids]
