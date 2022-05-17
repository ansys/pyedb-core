"""Layer Collection."""

from enum import Enum

import ansys.api.edb.v1.layer_collection_pb2 as layer_collection_pb2

from ...session import get_layer_collection_stub
from ...utility.edb_errors import handle_grpc_exception
from ..base import ObjBase
from .layer import Layer


class LayerCollectionMode(Enum):
    """Enum representing possible modes of layer collection."""

    LAMINATE = layer_collection_pb2.LAMINATE
    OVERLAPPING = layer_collection_pb2.OVERLAPPING
    MULTIZONE = layer_collection_pb2.MULTIZONE


class LayerCollection(ObjBase):
    """Layer Collection."""

    def __init__(self, is_owner, msg):
        """Initialize a layer collection."""
        super().__init__(msg)
        self._is_owner = is_owner

    def __del__(self):
        """Clean up a layer collection."""
        if self._is_owner:
            get_layer_collection_stub().Cleanup(self.msg)

    @staticmethod
    def create(mode=LayerCollectionMode.LAMINATE):
        """Create a layer collection.

        Parameters
        ----------
        mode : LayerCollectionMode, optional

        Returns
        -------
        LayerCollection
        """
        return LayerCollection(
            True,
            get_layer_collection_stub().Create(
                layer_collection_pb2.LayerCollectionCreateMessage(mode=mode.value)
            ),
        )

    @handle_grpc_exception
    def add_layers(self, layers):
        """Add layers to a layer collection.

        Parameters
        ----------
        layers : list of Layer

        Returns
        -------
        bool
        """
        layer_msgs = [lyr.msg for lyr in layers]
        return (
            get_layer_collection_stub()
            .AddLayers(
                layer_collection_pb2.AddLayersMessage(layer_collection=self.msg, layers=layer_msgs)
            )
            .value
        )

    @handle_grpc_exception
    def find_by_name(self, layer_name):
        """Find a layer in the layer collection.

        Parameters
        ----------
        layer_name : str

        Returns
        -------
        Layer
        """
        return Layer._create(
            get_layer_collection_stub().FindByName(
                layer_collection_pb2.FindLayerByNameMessage(
                    layer_collection=self.msg, name=layer_name
                )
            )
        )
