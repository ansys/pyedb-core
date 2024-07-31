"""Layout object instance 2D geometry."""

from ansys.api.edb.v1.layout_obj_instance_2d_geometry_pb2 import GetPolygonDataMessage

from ansys.edb.core.inner.parser import to_polygon_data
from ansys.edb.core.layout_instance.layout_obj_instance_geometry import LayoutObjInstanceGeometry
from ansys.edb.core.session import LayoutObjInstance2DGeometryServiceStub, StubAccessor, StubType


class LayoutObjInstance2DGeometry(LayoutObjInstanceGeometry):
    """Represents a layout object instance 2D geometry."""

    __stub: LayoutObjInstance2DGeometryServiceStub = StubAccessor(
        StubType.layout_obj_instance_2d_geometry
    )

    @property
    def is_negative(self):
        """:obj:`bool`: Flag indicating if the geometry is negative.

        This property is read-only.
        """
        return self.__stub.IsNegative(self.msg).value

    @to_polygon_data
    def get_polygon_data(self, apply_negatives=False):
        """Get the underlying polygon data of the geometry.

        Returns
        -------
        :class:`.PolygonData`
        """
        return self.__stub.GetPolygonData(
            GetPolygonDataMessage(layout_obj_inst_geom=self.msg, apply_neg=apply_negatives)
        )
