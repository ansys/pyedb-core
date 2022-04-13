import ansys.api.edb.v1.layout_pb2 as layout_pb2

from ...session import get_layout_stub
from ...utility.edb_iterator import EDBIterator
from ..base import ObjBase
from .layer_collection import LayerCollection
from .primitive import Primitive


class Layout(ObjBase):
    def get_layer_collection(self):
        return LayerCollection(False, get_layout_stub().GetLayerCollection(self._msg))

    def set_layer_collection(self, layer_collection):
        return (
            get_layout_stub()
            .SetLayerCollection(
                layout_pb2.SetLayerCollectionMessage(
                    layout=self._msg, layer_collection=layer_collection._msg
                )
            )
            .value
        )

    @property
    def primitives(self):
        return EDBIterator(get_layout_stub().GetPrimitiveIter(self._msg), Primitive._create)
