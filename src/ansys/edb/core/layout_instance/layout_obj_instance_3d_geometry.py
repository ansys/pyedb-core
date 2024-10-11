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
