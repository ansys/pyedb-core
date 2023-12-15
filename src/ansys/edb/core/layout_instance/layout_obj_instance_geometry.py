"""Layout object instance geometry."""

from ansys.api.edb.v1.layout_obj_instance_geometry_pb2 import LayoutObjInstanceGeometryMessage

from ansys.edb.core.inner import ObjBase
from ansys.edb.core.inner.messages import edb_obj_message
from ansys.edb.core.session import LayoutObjInstanceGeometryServiceStub, StubAccessor, StubType


class LayoutObjInstanceGeometry(ObjBase):
    """Represents layout object instance geometry."""

    __stub: LayoutObjInstanceGeometryServiceStub = StubAccessor(
        StubType.layout_obj_instance_geometry
    )

    def __init__(self, geometry, owning_drawing, placement_lyr):
        """Initialize the layout object instance geometry object.

        Parameters
        ----------
        geometry : EDBObjMessage
        owning_drawing : EDBObjMessage
        placement_lyr : EDBObjMessage
        """
        super().__init__(geometry)
        self._owning_drawing_id = owning_drawing.id
        self._placement_layer_id = placement_lyr.id

    @ObjBase.msg.getter
    def msg(self):
        """Protobuf message that represents this object's ID.

        Returns
        -------
        LayoutObjInstanceGeometryMessage
        """
        return LayoutObjInstanceGeometryMessage(
            geometry=super().msg,
            owning_drawing=edb_obj_message(self._owning_drawing_id),
            placement_layer=edb_obj_message(self._placement_layer_id),
        )

    @property
    def material(self):
        """:obj:`str`: Material of the geometry.

        This property is read-only.
        """
        return self.__stub.GetMaterial(self.msg).value

    @property
    def color(self):
        """:obj:`int`: Color of the geometry.

        This property is read-only.
        """
        return self.__stub.GetColor(self.msg).value
