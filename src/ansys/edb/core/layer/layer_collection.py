"""Layer collection."""

from enum import Enum

import ansys.api.edb.v1.layer_collection_pb2 as layer_collection_pb2

from ansys.edb.core.inner import ObjBase
from ansys.edb.core.inner.messages import (
    get_product_property_ids_message,
    get_product_property_message,
    set_product_property_message,
)
from ansys.edb.core.layer.layer import Layer, LayerType
from ansys.edb.core.layer.stackup_layer import StackupLayer
from ansys.edb.core.session import get_layer_collection_stub


class LayerCollectionMode(Enum):
    """Provides an enum representing possible modes of the layer collection."""

    LAMINATE = layer_collection_pb2.LAMINATE
    OVERLAPPING = layer_collection_pb2.OVERLAPPING
    MULTIZONE = layer_collection_pb2.MULTIZONE


class LayerTypeSet(Enum):
    """Provides an enum representing layer type sets used for filtering layers."""

    STACKUP_LAYER_SET = 0
    SIGNAL_LAYER_SET = 1
    DIELECTRIC_LAYER_SET = 2
    NON_STACKUP_LAYER_SET = 3
    ALL_LAYER_SET = 4


class DielectricMergingMethod(Enum):
    """Provides an enum representing dielectric merging method options."""

    WEIGHTED_AVERAGE = layer_collection_pb2.WEIGHTED_AVERAGE
    KRASZEWSKI = layer_collection_pb2.KRASZEWSKI
    WEIGHTED_CAPACITANCE = layer_collection_pb2.WEIGHTED_CAPACITANCE


def _layer_collection_zone_message(layer_collection, zone):
    """Convert to a ``LayerCollectionZoneMessage`` object."""
    return layer_collection_pb2.LayerCollectionZoneMessage(
        layer_collection=layer_collection.msg, zone=zone
    )


class LayerCollection(ObjBase):
    """Represents a layer collection."""

    @staticmethod
    def create(mode=LayerCollectionMode.LAMINATE):
        """Create a layer collection.

        Parameters
        ----------
        mode : LayerCollectionMode, default: LAMINATE
            Mode of the layer collection.

        Returns
        -------
        LayerCollection
            Layer collection created.
        """
        return LayerCollection(
            get_layer_collection_stub().Create(
                layer_collection_pb2.LayerCollectionModeMessage(mode=mode.value)
            )
        )

    def clone(self):
        """Create a clone of the layer collection.

        Returns
        -------
        LayerCollection
           Layer collection cloned.
        """
        return LayerCollection(get_layer_collection_stub().Clone(self.msg))

    @property
    def mode(self):
        """:class:`LayerCollectionMode`: Mode of the layer collection."""
        return LayerCollectionMode(get_layer_collection_stub().GetMode(self.msg).mode)

    @mode.setter
    def mode(self, mode):
        get_layer_collection_stub().SetMode(
            layer_collection_pb2.SetLayerCollectionModeMessage(
                layer_collection=self.msg, mode=mode.value
            )
        )

    def add_layers(self, layers):
        """Add a list of layers to the layer collection.

        Parameters
        ----------
        layers : list[Layer]
           List of layers.
        """
        layer_msgs = [lyr.msg for lyr in layers]
        get_layer_collection_stub().AddLayers(
            layer_collection_pb2.AddLayersMessage(layer_collection=self.msg, layers=layer_msgs)
        )

    def import_from_control_file(self, control_file_path, schema_file_path=None):
        """Import layers from a control file and optional XML schema file.

        Parameters
        ----------
        control_file_path : str
            Full path to the control file.
        schema_file_path : str, default: None
            Full path to the XML schema file.
        """
        import_msg = layer_collection_pb2.ImportFromControlFileMessage(
            layer_collection=self.msg, control_file_path=control_file_path
        )
        if schema_file_path is not None:
            import_msg.schema_path = schema_file_path
        get_layer_collection_stub().ImportFromControlFile(import_msg)

    def _add_layer(self, layer, above_below=None, add_top=None):
        """Pack layer addition arguments into the ``AddLayersMessage`` object and send to the server."""
        add_layer_msg = layer_collection_pb2.AddLayerMessage(
            layer_collection=self.msg, layer=layer.msg
        )
        if above_below is not None:
            above_below_msg = layer_collection_pb2.AddLayerAboveBelowMessage(
                above_below_layer_name=above_below[0], add_above=above_below[1]
            )
            add_layer_msg.above_below_msg.CopyFrom(above_below_msg)
        elif add_top is not None:
            add_layer_msg.add_top = add_top
        return Layer(get_layer_collection_stub().AddLayer(add_layer_msg)).cast()

    def _add_layer_relative(self, layer, relative_layer_name, add_above):
        """Add a layer above or below another layer."""
        return self._add_layer(layer, (relative_layer_name, add_above))

    def add_layer_above(self, layer_to_add, layer_to_add_above_name):
        """Add a new layer above the specified layer.

        This method adjusts existing layers as needed to maintain stackup consistency.

        Parameters
        ----------
        layer_to_add : Layer
            Name of the layer to add.
        layer_to_add_above_name : str
            Name of the layer above which to add the new layer.

        Returns
        -------
        Layer
        """
        return self._add_layer_relative(layer_to_add, layer_to_add_above_name, True)

    def add_layer_below(self, layer_to_add, layer_to_add_below_name):
        """Add a new layer below the specified layer.

        This method adjusts existing layers as needed to maintain stackup consistency.

        Parameters
        ----------
        layer_to_add : Layer
            Name of the layer to add.
        layer_to_add_below_name : str
            Name of the layer below which to add the new layer.

        Returns
        -------
        Layer
        """
        return self._add_layer_relative(layer_to_add, layer_to_add_below_name, False)

    def add_layer_top(self, layer_to_add):
        """Add a new layer to the top of the layer collection.

        This method adjusts existing layers as needed to maintain stackup consistency.

        Parameters
        ----------
        layer_to_add : Layer
            Name of the layer to add.

        Returns
        -------
        Layer
        """
        return self._add_layer(layer_to_add, add_top=True)

    def add_layer_bottom(self, layer_to_add):
        """Add a new layer to the bottom of the layer collection.

        This method adjusts existing layers as needed to maintain stackup consistency.

        Parameters
        ----------
        layer_to_add : Layer
            Name of the layer to add.

        Returns
        -------
        Layer
        """
        return self._add_layer(layer_to_add, add_top=False)

    def add_stackup_layer_at_elevation(self, stackup_layer_to_add):
        """Add a stackup layer at a user-specified elevation.

        This method doe not change the elevenation of other stackup layers.

        Parameters
        ----------
        stackup_layer_to_add : StackupLayer

        Returns
        -------
        StackupLayer
        """
        return self._add_layer(stackup_layer_to_add)

    def add_via_layer(self, via_layer_to_add):
        """Add a via layer to the layer collection.

        Parameters
        ----------
        via_layer_to_add : ViaLayer

        Returns
        -------
        ViaLayer
        """
        return self._add_layer(via_layer_to_add)

    def is_valid(self):
        """Determine if the layer collection is in a valid state.

        For a laminate stackup, this method checks whether there is layer overlapping or a gap.
        For an overlapping stackup, this method checks whether there is a dielectric layer
        overlapping or a gap.

        Returns
        -------
        bool
            ``True`` if the layer collection is in a valid state, ``False`` otherwise.
        """
        return get_layer_collection_stub().IsValid(self.msg).value

    def find_by_name(self, layer_name):
        """Find a layer in the layer collection.

        Parameters
        ----------
        layer_name : str
           Layer name.

        Returns
        -------
        Layer
        """
        return Layer(
            get_layer_collection_stub().FindByName(
                layer_collection_pb2.FindLayerByNameMessage(
                    layer_collection=self.msg, name=layer_name
                )
            )
        ).cast()

    @staticmethod
    def _get_layer_filter(layer_types):
        """Convert a list of layer types to an integer representation of a layer filter."""
        if not isinstance(layer_types, list):
            layer_types = [layer_types]
        layer_filter = 0
        for layer_type in layer_types:
            layer_type_value = layer_type.value
            if layer_type_value >= 0:
                layer_filter = layer_filter | (1 << layer_type_value)
        return layer_filter

    @staticmethod
    def _get_layer_filter_from_layer_type_set(layer_type_set):
        def _get_layer_type_list():
            if layer_type_set == LayerTypeSet.STACKUP_LAYER_SET:
                return [
                    LayerType.DIELECTRIC_LAYER,
                    LayerType.CONDUCTING_LAYER,
                    LayerType.SIGNAL_LAYER,
                ]
            elif layer_type_set == LayerTypeSet.SIGNAL_LAYER_SET:
                return [LayerType.CONDUCTING_LAYER, LayerType.SIGNAL_LAYER]
            elif layer_type_set == LayerTypeSet.DIELECTRIC_LAYER_SET:
                return [LayerType.DIELECTRIC_LAYER]
            elif layer_type_set == LayerTypeSet.NON_STACKUP_LAYER_SET:
                return list(LayerType)[LayerType.AIRLINES_LAYER.value : -2]
            else:
                return []

        return LayerCollection._get_layer_filter(_get_layer_type_list())

    def get_top_bottom_stackup_layers(self, layer_type_set):
        """Get the top and bottom stackup layers of a specific type and their elevations.

        Parameters
        ----------
        layer_type_set : LayerTypeSet
            Layer type set indicating the layer types to retrieve.

        Returns
        -------
        tuple[Layer, float, Layer, float]
            Returns a tuple in this format:
            (upper_layer, upper_layer_top_elevation, lower_layer, lower_layer_lower_elevation)
        """
        request = layer_collection_pb2.GetTopBottomStackupLayersMessage(
            layer_collection=self.msg,
            layer_type_set=LayerCollection._get_layer_filter_from_layer_type_set(layer_type_set),
        )
        response = get_layer_collection_stub().GetTopBottomStackupLayers(request)
        return (
            Layer(response.top_layer).cast(),
            response.top_layer_elevation,
            Layer(response.bottom_layer).cast(),
            response.bottom_layer_elevation,
        )

    def get_layers(self, layer_filter=LayerTypeSet.ALL_LAYER_SET):
        """Get a list of layers in the layer collection using a layer filter.

        Parameters
        ----------
        layer_filter : LayerTypeSet or LayerType or list[LayerType], default: ALL_LAYER_SET
            Layer filter.

        Returns
        -------
        list[Layer]
            List of layers based on the filter used.
        """
        layer_filter_int = (
            LayerCollection._get_layer_filter_from_layer_type_set(layer_filter)
            if isinstance(layer_filter, LayerTypeSet)
            else LayerCollection._get_layer_filter(layer_filter)
        )

        response = get_layer_collection_stub().GetLayers(
            layer_collection_pb2.GetLayersMessage(
                layer_collection=self.msg, layer_filter=layer_filter_int
            )
        )

        return [Layer(msg).cast() for msg in response.items]

    def get_product_property(self, prod_id, attr_it):
        """Get the product property of the layer collection for a given product ID and attribute ID.

        Parameters
        ----------
        prod_id : :class:`.ProductIdType`
            Product ID.
        attr_it : int
            Attribute ID.

        Returns
        -------
        str
            Product property.
        """
        return (
            get_layer_collection_stub()
            .GetProductProperty(get_product_property_message(self, prod_id, attr_it))
            .value
        )

    def set_product_property(self, prod_id, attr_it, prop_value):
        """Set the product property of the layer collection for a given product ID and attribute ID.

        Parameters
        ----------
        prod_id : :class:`.ProductIdType`
            Product ID.
        attr_it : int
            Attribute ID.
        prop_value : str
            New property value.
        """
        get_layer_collection_stub().SetProductProperty(
            set_product_property_message(self, prod_id, attr_it, prop_value)
        )

    def get_product_property_ids(self, prod_id):
        """Get a list of attribute IDs for a given product ID for the layer collection.

        Parameters
        ----------
        prod_id : :class:`.ProductIdType`
            Product ID.

        Returns
        -------
        list[int]
            List of attribute IDs for the given product ID.
        """
        attr_ids = (
            get_layer_collection_stub()
            .GetProductPropertyIds(get_product_property_ids_message(self, prod_id))
            .ids
        )
        return [attr_id for attr_id in attr_ids]

    def merge_dielectrics(
        self,
        layout,
        start_layer_name,
        end_layer_name,
        merging_method,
        merged_layer_name,
        merged_mat_name,
    ):
        """Merge the dielectric layers in a range of layers into one large dielectric layer.

        Parameters
        ----------
        layout : :class:`.Layout`
        start_layer_name : str
        end_layer_name : str
        merging_method : DielectricMergingMethod
        merged_layer_name : str
        merged_mat_name : str

        Returns
        -------
        StackupLayer
        """
        return StackupLayer(
            get_layer_collection_stub().MergeDielectrics(
                layer_collection_pb2.MergeDielectricsMessage(
                    layer_collection=self.msg,
                    layout=layout.msg,
                    start_layer_name=start_layer_name,
                    end_layer_name=end_layer_name,
                    merging_method=merging_method.value,
                    merged_layer_name=merged_layer_name,
                    merged_mat_name=merged_mat_name,
                )
            )
        )

    @property
    def zone_ids(self):
        r""":obj:`list`\[:obj:`int`\]: List of all zones in the layer collection."""
        zones = get_layer_collection_stub().GetZoneIds(self.msg).zones
        return [zone for zone in zones]

    def get_zone_name(self, zone):
        """Get the name for a given zone.

        Parameters
        ----------
        zone : int
           Zone ID.

        Returns
        -------
        str
            Name of the zone.
        """
        return (
            get_layer_collection_stub()
            .GetZoneName(_layer_collection_zone_message(self, zone))
            .value
        )

    def set_zone_name(self, zone, name):
        """Set the name for a given zone.

        Parameters
        ----------
        zone : int
            Zone ID.
        name : str
            New name to give the zone.
        """
        request = layer_collection_pb2.SetZoneNameMessage(
            layer_collection=self.msg, zone=zone, zone_name=name
        )
        get_layer_collection_stub().SetZoneName(request)

    def insert_zone(self, copy_zone=-1):
        """Insert a zone.

        Parameters
        ----------
        copy_zone : int, default: -1
            Zone to copy from when inserting a new zone.
            If valid, the new zone is inserted as a copy of the given zone.
            Otherwise, the new zone is empty.

        Returns
        -------
        int
            ID of the zone inserted if successful.
        """
        request = layer_collection_pb2.InsertZoneMessage(
            layer_collection=self.msg, copy_zone=copy_zone
        )
        return get_layer_collection_stub().InsertZone(request).value

    def remove_zone(self, zone):
        """Remove a zone.

        Parameters
        ----------
        zone : int
           ID of the zone.
        """
        get_layer_collection_stub().RemoveZone(_layer_collection_zone_message(self, zone))

    def simplify_dielectrics_for_phi(
        self,
        database,
        layer_thickness_thresh=-1,
        merging_method=DielectricMergingMethod.WEIGHTED_CAPACITANCE,
    ):
        """Split dielectric layers at the boundaries of signal layers and merge them.

        Parameters
        ----------
        database : :class:`.Database`
        layer_thickness_thresh : float, default: -1
           Thickness threshold for the layer.
        merging_method : DielectricMergingMethod, default: WEIGHTED_CAPACITANCE
           Method for merging.

        Returns
        -------
        list[StackupLayer]
            List of dielectric layers created during the dielectric simplification process.
        """
        simplified_lyrs = (
            get_layer_collection_stub()
            .SimplifyDielectricsForPhi(
                layer_collection_pb2.SimplifyDielectricsForPhiMessage(
                    layer_collection=self.msg,
                    database=database.msg,
                    layer_thickness_thresh=layer_thickness_thresh,
                    merging_method=merging_method.value,
                )
            )
            .items
        )
        return [StackupLayer(simplified_lyr) for simplified_lyr in simplified_lyrs]

    def add_zone_to_layer(self, layer, zone, in_zone):
        """Set the zone to the layer and update the layer in the collection.

        Parameters
        ----------
        layer : Layer
        zone : int
        in_zone : bool
        """
        request = layer_collection_pb2.AddZoneToLayerMessage(
            layer_collection=self.msg, layer=layer.msg, zone=zone, in_zone=in_zone
        )
        get_layer_collection_stub().AddZoneToLayer(request)
