"""Layout."""

import ansys.api.edb.v1.layout_pb2 as layout_pb2

from ...session import get_layout_stub
from ...utility.edb_iterator import EDBIterator
from ...utility.variable_server import _VariableServer
from ..base import ObjBase
from .layer_collection import LayerCollection
from .primitive import Primitive


class Layout(ObjBase, _VariableServer):
    """Class representing layout object."""

    def __init__(self, msg):
        """Initialize a new layout.

        Parameters
        ----------
        msg : EDBObjMessage
        """
        ObjBase.__init__(self, msg)
        _VariableServer.__init__(self, msg)

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
