"""Layout object instance 3D geometry."""

from ansys.edb.core.geometry.triangle3d_data import Triangle3DData
from ansys.edb.core.inner import utils
from ansys.edb.core.inner.parser import to_point3d_data
from ansys.edb.core.layout_instance.layout_obj_instance_geometry import LayoutObjInstanceGeometry
from ansys.edb.core.session import LayoutObjInstance3DGeometryServiceStub, StubAccessor, StubType


class LayoutObjInstance3DGeometry(LayoutObjInstanceGeometry):
    """Represents a layout object instance 3D geometry."""

    __stub: LayoutObjInstance3DGeometryServiceStub = StubAccessor(
        StubType.layout_obj_instance_3d_geometry
    )

    @property
    def tesselation_data(self):
        """:obj:`list` of :class:`.Triangle3DData`: All triangle 3D data instances.

        This list contains triangle 3D data instances that correspond to the
        underlying tessellation data of the geometry.
        """
        tesselation_data = self.__stub.GetTesselationData(self.msg)

        def to_3d_triangle(triangle_msg):
            return Triangle3DData(
                to_point3d_data(triangle_msg.point_1),
                to_point3d_data(triangle_msg.point_2),
                to_point3d_data(triangle_msg.point_3),
            )

        return utils.map_list(tesselation_data.tesselation_data, to_3d_triangle)
