"""Via layer."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.typing import ValueLike

import ansys.api.edb.v1.via_layer_pb2 as via_layer_pb2

from ansys.edb.core.inner.messages import bool_property_message, int_property_message, value_message
from ansys.edb.core.layer.stackup_layer import StackupLayer
from ansys.edb.core.session import get_via_layer_stub
from ansys.edb.core.utility.value import Value


def _via_lyr_ref_lyr_id_msg(lyr, is_upper_ref):
    """Convert to a ``ViaLayerRefLayerIdMessage`` object."""
    return via_layer_pb2.ViaLayerRefLayerIdMessage(via_layer=lyr.msg, is_upper_ref=is_upper_ref)


class ViaLayer(StackupLayer):
    """Represents a via layer."""

    @staticmethod
    def create(name, lr_layer, ur_layer, material):
        """Create a via layer.

        Parameters
        ----------
        name : str
            Name of the via layer.
        lr_layer : str
        ur_layer : str
        material : str

        Returns
        -------
        ViaLayer
            Via layer created.
        """
        params = {
            "via_layer_name": name,
            "lower_ref_layer_name": lr_layer,
            "upper_ref_layer_name": ur_layer,
            "material_name": material,
        }
        via_layer = ViaLayer(
            get_via_layer_stub().Create(via_layer_pb2.ViaLayerCreationMessage(**params))
        )
        return via_layer

    def get_ref_layer_name(self, upper_ref):
        """Get the name of the reference layer of the via layer.

        Parameters
        ----------
        upper_ref : bool
            Whether to get the name of the upper or lower reference layer.

        Returns
        -------
        str
            Name of the reference layer.
        """
        return get_via_layer_stub().GetRefLayerName(_via_lyr_ref_lyr_id_msg(self, upper_ref)).value

    def set_ref_layer(self, ref_layer, upper_ref):
        """Set the reference layer of the via layer.

        Parameters
        ----------
        ref_layer : StackupLayer
            Layer to set as the new reference layer of the via layer.
        upper_ref : bool
            Whether to set the new reference layer as the
            upper or lower reference layer.
        """
        get_via_layer_stub().SetRefLayer(
            via_layer_pb2.SetViaLayerRefLayerMessage(
                via_layer_ref_layer_id=_via_lyr_ref_lyr_id_msg(self, upper_ref),
                new_ref_layer=ref_layer.msg,
            )
        )

    @property
    def is_tsv(self) -> bool:
        """:obj:`bool`: Flag indicating if this via layer is a TSV layer."""
        return get_via_layer_stub().GetIsTSV(self.msg).value

    @is_tsv.setter
    def is_tsv(self, is_tsv: bool):
        get_via_layer_stub().SetIsTSV(bool_property_message(self, is_tsv))

    def add_oxide_layers(self, oxide_layers: tuple[ValueLike, str] | list[tuple[ValueLike, str]]):
        """Add oxide layers to the via layer.

        Parameters
        ----------
        oxide_layers: tuple of (:term:`ValueLike`, str) or list of tuple of (:term:`ValueLike`, str)
            Tuples representing the oxide layer data. The data in the tuple is of the format \
            (``thickness``, ``material``). If a single tuple is provided, one oxide layer will \
            be provided. If a list of tuples is provided, one oxide layer will be created per tuple.
        """
        _oxide_layers = [oxide_layers] if not isinstance(oxide_layers, list) else oxide_layers
        oxide_layer_msgs = []
        for oxide_layer in _oxide_layers:
            oxide_layer_msgs.append(
                via_layer_pb2.OxideLayerMessage(
                    thickness=value_message(oxide_layer[0]), material=oxide_layer[1]
                )
            )
        get_via_layer_stub().AddOxideLayers(
            via_layer_pb2.OxideLayersPropertyMessage(target=self.msg, oxide_layers=oxide_layer_msgs)
        )

    def remove_oxide_layer(self, oxide_lyr_idx: int):
        """Remove the oxide layer at the specified index.

        Parameters
        ----------
        oxide_lyr_idx: int
            Index of the oxide layer to remove.
        """
        get_via_layer_stub().RemoveOxideLayers(int_property_message(self, oxide_lyr_idx))

    def clear_oxide_layers(self):
        """Remove all oxide layers from the via layer."""
        self.remove_oxide_layer(-1)

    @property
    def num_oxide_layers(self):
        """:obj:`int`: Number of oxide layers in the via layer.

        This property is read-only.
        """
        return get_via_layer_stub().GetNumOxideLayers(self.msg).value

    @staticmethod
    def _msg_to_oxide_layer(msg: via_layer_pb2.OxideLayerMessage) -> tuple[Value, str]:
        return Value(msg.thickness), msg.material

    @property
    def oxide_layers(self):
        """:obj:`list` of :obj:`tuple` of (:term:`ValueLike`, Obj:`str`): List of oxide layers placed on the via layer.

        This property is read-only.
        """
        response = get_via_layer_stub().GetOxideLayers(int_property_message(self, -1))
        return [
            self._msg_to_oxide_layer(oxide_layer_msg) for oxide_layer_msg in response.oxide_layers
        ]

    def get_oxide_layer(self, oxide_lyr_idx: int):
        """Get the oxide layer at the specified index.

        Parameters
        ----------
        oxide_lyr_idx: int
            Index of the oxide layer to be retrieved

        Returns
        -------
        tuple of (:term:`ValueLike`, str)
        """
        return self._msg_to_oxide_layer(
            get_via_layer_stub()
            .GetOxideLayers(int_property_message(self, oxide_lyr_idx))
            .oxide_layers[0]
        )

    def set_oxide_layer_data(
        self, oxide_lyr_idx: int, thickness: ValueLike | None = None, material: str | None = None
    ):
        """Set the thickness or material of the oxide layer at the specified index.

        Parameters
        ---------
        oxide_lyr_idx: int
            Index of the oxide layer to be retrieved
        thickness: :term:`ValueLike`, default: None
            Thickness of the oxide layer. If :obj:`None`, the thickness will not be set.
        material: str, default: None
            Material of the oxide layer.  If :obj:`None`, the material will not be set.
        """
        get_via_layer_stub().SetOxideLayerData(
            via_layer_pb2.SetOxideDataLayerMessage(
                target=int_property_message(self, oxide_lyr_idx),
                oxide_layer_data=via_layer_pb2.OxideLayerMessage(
                    thickness=None if thickness is None else value_message(thickness),
                    material=material,
                ),
            )
        )
