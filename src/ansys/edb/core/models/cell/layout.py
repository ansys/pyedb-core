"""Layout."""

import ansys.api.edb.v1.layout_pb2 as layout_pb2

from ...session import get_layout_stub
from ...utility.edb_iterator import EDBIterator
from ..base import ObjBase
from .layer_collection import LayerCollection
from .primitive import Primitive


class Layout(ObjBase):
    """Class representing layout object."""

    def get_layer_collection(self):
        """
        Get layer collection.

        Returns
        -------
        LayerCollection
        """
        return LayerCollection(False, get_layout_stub().GetLayerCollection(self.msg))

    def set_layer_collection(self, layer_collection):
        """
        Set layer collection.

        Parameters
        ----------
        layer_collection : LayerCollection
        """
        return (
            get_layout_stub()
            .SetLayerCollection(
                layout_pb2.SetLayerCollectionMessage(
                    layout=self.msg, layer_collection=layer_collection.msg
                )
            )
            .value
        )

    @property
    def primitives(self):
        """
        Get list of primitives.

        Returns
        -------
        EDBIterator
        """
        return EDBIterator(get_layout_stub().GetPrimitiveIter(self.msg), Primitive._create)
