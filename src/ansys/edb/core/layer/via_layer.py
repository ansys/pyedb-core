# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Via layer."""

import ansys.api.edb.v1.via_layer_pb2 as via_layer_pb2

from ansys.edb.core.layer.stackup_layer import StackupLayer
from ansys.edb.core.session import get_via_layer_stub


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
