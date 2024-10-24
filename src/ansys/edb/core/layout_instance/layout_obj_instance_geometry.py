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
