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

    def __init__(self, msg):
        """Initialize a layer collection."""
        super().__init__(msg)

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
            get_layer_collection_stub().Create(
                layer_collection_pb2.LayerCollectionModeMessage(mode=mode.value)
            )
        )

    @staticmethod
    @handle_grpc_exception
    def clone(self):
        """Create a clone of the layer collection.

        Returns
        -------
        LayerCollection
        """
        return LayerCollection(get_layer_collection_stub().Clone(self.msg))

    @property
    @handle_grpc_exception
    def mode(self):
        """Get the mode the layer collection.

        Returns
        -------
        LayerCollectionMode
        """
        return LayerCollectionMode(get_layer_collection_stub().Clone(self.msg).mode)

    @mode.setter
    @handle_grpc_exception
    def mode(self, mode):
        """Set the mode the layer collection.

        Parameters
        ----------
        mode : LayerCollectionMode
        """
        get_layer_collection_stub().SetMode(
            layer_collection_pb2.SetLayerCollectionModeMessage(
                layer_collection=self.msg, mode=mode.value
            )
        )

    @handle_grpc_exception
    def add_layers(self, layers):
        """Add layers to a layer collection.

        Parameters
        ----------
        layers : list of Layer
        """
        layer_msgs = [lyr.msg for lyr in layers]
        get_layer_collection_stub().AddLayers(
            layer_collection_pb2.AddLayersMessage(layer_collection=self.msg, layers=layer_msgs)
        )

    @handle_grpc_exception
    def import_from_control_file(self, control_file_path, schema_file_path=None):
        """Import layers from the provided control file and optional XML schema.

        Parameters
        ----------
        control_file_path : str
        schema_file_path : str
        """
        import_msg = layer_collection_pb2.ImportFromControlFileMessage(
            layer_collection=self.msg, control_file_path=control_file_path
        )
        if schema_file_path:
            import_msg.schema_path = schema_file_path
        get_layer_collection_stub().ImportFromControlFile(import_msg)

    def _add_layer(self, layer, above_below=None, add_top=None):
        """Pack layer addition arguments into AddLayersMessage and send to server."""
        add_layer_msg = layer_collection_pb2.AddLayersMessage(
            layer_collection=self.msg, layer=layer.msg
        )
        if above_below:
            above_below_msg = layer_collection_pb2.AddLayerAboveBelowMessage(
                above_below_layer_name=above_below[0], add_above=above_below[1]
            )
            add_layer_msg.above_below_msg.CopyFrom(above_below_msg)
        elif add_top:
            add_layer_msg.add_top = add_top
        return Layer._create(get_layer_collection_stub().AddLayer(add_layer_msg))

    def _add_layer_relative(self, layer, relative_layer_name, add_above):
        """Add a layer above or below another layer."""
        return self._add_layer(layer, (relative_layer_name, add_above))

    @handle_grpc_exception
    def add_layer_above(self, layer_to_add, layer_to_add_above_name):
        """Add a new layer above the specified layer.

         Adjusts existing layers as needed to maintain stackup consistency.

        Parameters
        ----------
        layer_to_add : Layer
        layer_to_add_above_name : str

        Returns
        -------
        Layer
        """
        return self._add_layer_relative(layer_to_add, layer_to_add_above_name, True)

    @handle_grpc_exception
    def add_layer_below(self, layer_to_add, layer_to_add_below_name):
        """Add a new layer below the specified layer.

         Adjusts existing layers as needed to maintain stackup consistency.

        Parameters
        ----------
        layer_to_add : Layer
        layer_to_add_below_name : str

        Returns
        -------
        Layer
        """
        return self._add_layer_relative(layer_to_add, layer_to_add_below_name, False)

    @handle_grpc_exception
    def add_layer_top(self, layer_to_add):
        """Add a new layer to the top of the LayerCollection.

         Adjusts existing layers as needed to maintain stackup consistency.

        Parameters
        ----------
        layer_to_add : Layer

        Returns
        -------
        Layer
        """
        return self._add_layer(layer_to_add, add_top=True)

    @handle_grpc_exception
    def add_layer_top(self, layer_to_add):
        """Add a new layer to the bottom of the LayerCollection.

         Adjusts existing layers as needed to maintain stackup consistency.

        Parameters
        ----------
        layer_to_add : Layer

        Returns
        -------
        Layer
        """
        return self._add_layer(layer_to_add, add_top=False)

    @handle_grpc_exception
    def add_stackup_layer_at_elevation(self, stackup_layer_to_add):
        """Add a stackup layer at user specified elevation.

         Doesn't change other stackup layer's elevation.

        Parameters
        ----------
        stackup_layer_to_add : StackupLayer

        Returns
        -------
        StackupLayer
        """
        return self._add_layer(stackup_layer_to_add)

    @handle_grpc_exception
    def add_via_layer_at_elevation(self, via_layer_to_add):
        """Add a via layer to the layer collection.

        Parameters
        ----------
        via_layer_to_add : ViaLayer

        Returns
        -------
        ViaLayer
        """
        return self._add_layer(via_layer_to_add)

    @handle_grpc_exception
    def is_valid(self):
        """Check if the layer collection is  in a valid state.

        Check whether there is layer overlapping or gap for laminate stackup.
        Check whether there is dielectric layer overlapping or gap for overlapping stackup.

        Returns
        -------
        bool
        """
        return get_layer_collection_stub().IsValid().value

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
