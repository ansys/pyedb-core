"""Layout Obj Instance 2D Geometry."""

from ansys.api.edb.v1.layout_obj_instance_2d_geometry_pb2 import GetPolygonDataMessage

from ansys.edb.geometry import PolygonData
from ansys.edb.layout_instance.layout_obj_instance_geometry import LayoutObjInstanceGeometry
from ansys.edb.session import LayoutObjInstance2DGeometryServiceStub, StubAccessor, StubType


class LayoutObjInstance2DGeometry(LayoutObjInstanceGeometry):
    """Class representing layout obj instance 2D geometry."""

    __stub: LayoutObjInstance2DGeometryServiceStub = StubAccessor(
        StubType.layout_obj_instance_2d_geometry
    )

    @property
    def is_negative(self):
        """Get flag indicating if the layout obj instance geometry is negative.

        Returns
        -------
        bool
        """
        return self.__stub.IsNegative(self.msg).value

    @property
    def polygon_data(self, apply_negatives=False):
        """Get the underlying polygon data of the layout obj instance geometry.

        Returns
        -------
        PolygonData
        """
        return PolygonData(
            msg=self.__stub.GetPolygonData(
                GetPolygonDataMessage(layout_obj_inst_geom=self.msg, apply_neg=apply_negatives)
            )
        )
