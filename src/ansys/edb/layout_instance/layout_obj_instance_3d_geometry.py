"""Layout Obj Instance 3D Geometry."""

from ansys.edb.core import utils
from ansys.edb.core.parser import to_point3d_data
from ansys.edb.geometry import Triangle3DData
from ansys.edb.layout_instance.layout_obj_instance_geometry import LayoutObjInstanceGeometry
from ansys.edb.session import LayoutObjInstance3DGeometryServiceStub, StubAccessor, StubType


class LayoutObjInstance3DGeometry(LayoutObjInstanceGeometry):
    """Class representing layout object instance 3D geometry."""

    __stub: LayoutObjInstance3DGeometryServiceStub = StubAccessor(
        StubType.layout_obj_instance_3d_geometry
    )

    @property
    def tesselation_data(self):
        r""":obj:`list`\[:class:`ansys.edb.geometry.Triangle3DData`\]: The underlying tessellation data of the geometry.

        Read-Only.
        """
        tesselation_data = self.__stub.GetTesselationData(self.msg)

        def to_3d_triangle(triangle_msg):
            return Triangle3DData(
                to_point3d_data(triangle_msg.point_1),
                to_point3d_data(triangle_msg.point_2),
                to_point3d_data(triangle_msg.point_3),
            )

        return utils.map_list(tesselation_data.tesselation_data, to_3d_triangle)
