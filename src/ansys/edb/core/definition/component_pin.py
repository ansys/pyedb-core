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

"""Component pin Definition."""
from ansys.api.edb.v1.component_pin_pb2_grpc import ComponentPinServiceStub

from ansys.edb.core.definition import component_def
from ansys.edb.core.inner import ObjBase, messages
from ansys.edb.core.session import StubAccessor, StubType


class ComponentPin(ObjBase):
    """Represents a component pin."""

    __stub: ComponentPinServiceStub = StubAccessor(StubType.component_pin)

    @classmethod
    def create(cls, comp_def, name):
        """Create a component pin in a given component definition.

        Parameters
        ----------
        comp_def : :class:`.ComponentDef`
            Component definition to create the component pin in.
        name : str
            Name of the component pin.

        Returns
        -------
        ComponentPin
            Component pin created.
        """
        return ComponentPin(cls.__stub.Create(messages.edb_obj_name_message(comp_def, name)))

    @classmethod
    def find(cls, comp_def, name):
        """Find a component pin in a given component definition.

        Parameters
        ----------
        comp_def : :class:`.ComponentDef`
            Component definition to search for the component pin.
        name : str
            Name of the component pin.

        Returns
        -------
        ComponentPin
            Component pin found, ``None`` otherwise.
        """
        return ComponentPin(cls.__stub.FindByName(messages.edb_obj_name_message(comp_def, name)))

    @property
    def name(self):
        """:obj:`str`: Name of the component pin."""
        return self.__stub.GetName(self.msg).value

    @name.setter
    def name(self, value):
        self.__stub.SetName(messages.string_property_message(self, value))

    @property
    def number(self):
        """:obj:`int`: Serial number of the component pin inside its component definition.

        This property is read-only.
        """
        return self.__stub.GetNumber(self.msg).value

    @property
    def component_def(self):
        """:class:`.ComponentDef`: Component definition that the component pin belongs to.

        This property is read-only.
        """
        return component_def.ComponentDef(self.__stub.GetComponentDef(self.msg))
