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
