"""Layout Obj Instance 3D Geometry."""

from ansys.edb.core import utils
from ansys.edb.layout_instance.layout_obj_instance_geometry import LayoutObjInstanceGeometry
from ansys.edb.session import LayoutObjInstance3DGeometryServiceStub, StubAccessor, StubType
from ansys.edb.utility import Value


class LayoutObjInstance3DGeometry(LayoutObjInstanceGeometry):
    """Class representing layout obj instance 3D geometry."""

    __stub: LayoutObjInstance3DGeometryServiceStub = StubAccessor(
        StubType.layout_obj_instance_3d_geometry
    )

    @property
    def tesselation_data(self):
        """Get the underlying tessellation data of the layout obj instance geometry.

        Returns
        -------
        list[ansys.edb.typing.Triangle3DLike]
        """
        tesselation_data = self.__stub.GetTesselationData(self.msg)

        def to_3d_triangle_like(triangle_msg):
            def to_3d_point_like(point_3d_msg):
                return (Value(point_3d_msg.x), Value(point_3d_msg.y), Value(point_3d_msg.z))

            return (
                to_3d_point_like(triangle_msg.point_1),
                to_3d_point_like(triangle_msg.point_2),
                to_3d_point_like(triangle_msg.point_3),
            )

        return utils.map_list(tesselation_data.tesselation_data, to_3d_triangle_like)
