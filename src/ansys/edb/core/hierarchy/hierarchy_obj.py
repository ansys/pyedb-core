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

"""Hierarchy object."""

from ansys.edb.core.definition import component_def
from ansys.edb.core.inner import conn_obj, messages
from ansys.edb.core.layer.layer import Layer
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.transform import Transform
from ansys.edb.core.utility.value import Value


class HierarchyObj(conn_obj.ConnObj):
    """Provides the base class for an hierarchy object."""

    __stub = StubAccessor(StubType.hierarchy_obj)

    @property
    def transform(self):
        """:class:`.Transform`: \
        Transformation information of the hierarchy object."""
        transform_msg = self.__stub.GetTransform(self.msg)
        return Transform.create(
            transform_msg.scale,
            transform_msg.angle,
            transform_msg.mirror,
            transform_msg.offset_x,
            transform_msg.offset_y,
        )

    @transform.setter
    def transform(self, value):
        """Set transform."""
        self.__stub.SetTransform(messages.transform_property_message(self, value))

    @property
    def name(self):
        """:obj:`str`: Name of the hierarchy object."""
        return self.__stub.GetName(self.msg).value

    @name.setter
    def name(self, value):
        self.__stub.SetName(messages.edb_obj_name_message(self, value))

    @property
    def component_def(self):
        """:class:`.ComponentDef`: Component definition for the \
        hierarchy object if it exists, ``None`` otherwise.

        This property is read-only.
        """
        return component_def.ComponentDef(self.__stub.GetComponent(self.msg))

    @property
    def placement_layer(self):
        """:class:`.Layer`: Placement layer for the hierarchy object."""
        return Layer(self.__stub.GetPlacementLayer(self.msg)).cast()

    @placement_layer.setter
    def placement_layer(self, value):
        self.__stub.SetPlacementLayer(messages.pointer_property_message(self, value))

    @property
    def location(self):
        """:obj:`tuple` (:class:`.Value`, \
        :class:`.Value`): \
        Location [x, y] of the hierarchy object on the :obj:`placement_layer` object."""
        pnt_msg = self.__stub.GetLocation(self.msg)
        return [Value(pnt_msg.x), Value(pnt_msg.y)]

    @location.setter
    def location(self, value):
        self.__stub.SetLocation(messages.point_property_message(self, value))

    @property
    def solve_independent_preference(self):
        """:obj:`bool`: Flag indicating if the object is assigned to solve independent of its parent context.

        Returns
        -------
        bool
            ``True`` if the object is assigned to solve independently, ``False`` if the object is embedded.

        Notes
        -----
        For a :class:`.ComponentModel`
        instance, this flag indicates if the model is embedded with the field solver, when applicable.

        For a :class:`.CellInstance` instance,
        it indicates if the design's geometry is flattened/meshed with the parent, when applicable.
        """
        return self.__stub.GetSolveIndependentPreference(self.msg).value

    @solve_independent_preference.setter
    def solve_independent_preference(self, value):
        self.__stub.SetSolveIndependentPreference(messages.bool_property_message(self, value))
