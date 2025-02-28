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

"""Component model definition."""
from ansys.api.edb.v1.component_model_pb2_grpc import (
    ComponentModelServiceStub,
    DynamicLinkComponentModelServiceStub,
    NPortComponentModelServiceStub,
)
import google.protobuf.wrappers_pb2 as proto_wrappers

from ansys.edb.core.inner import ObjBase, messages
from ansys.edb.core.session import StubAccessor, StubType


class ComponentModel(ObjBase):
    """Represents a component model."""

    __stub: ComponentModelServiceStub = StubAccessor(StubType.component_model)

    @property
    def reference_file(self):
        """:obj:`str`: Name of the reference file associated with the component model."""
        return self.__stub.GetReferenceFile(self.msg).value

    @reference_file.setter
    def reference_file(self, value):
        self.__stub.SetReferenceFile(messages.string_property_message(self, value))

    @classmethod
    def find_by_name(cls, comp_def, value):
        """Find a component model by name in a given component def.

        Parameters
        ----------
        comp_def : :class:`ComponentDef <ansys.edb.core.definition.ComponentDef>`
            Component def to search for the component model.
        value : str
            Name of the component model.

        Returns
        -------
        ComponentModel
            Component model that is found, ``None`` otherwise.
        """
        return ComponentModel(
            cls.__stub.FindByName(messages.string_property_message(comp_def, value))
        )

    @classmethod
    def find_by_id(cls, comp_def, value):
        """Find a component model by ID in a given component def.

        Parameters
        ----------
        comp_def : :class:`ComponentDef <ansys.edb.core.definition.ComponentDef>`
            Component def to search for the component model.
        value : int
            ID of the component model.

        Returns
        -------
        ComponentModel
            Component model that is found, ``None`` otherwise.
        """
        return ComponentModel(cls.__stub.FindById(messages.int_proprty_message(comp_def, value)))


class NPortComponentModel(ComponentModel):
    """Represents an NPort component model."""

    __stub: NPortComponentModelServiceStub = StubAccessor(StubType.nport_component_model)

    @classmethod
    def create(cls, name):
        """Create an NPort component model.

        Parameters
        ----------
        name : str
            Name of the NPport component model.

        Returns
        -------
        NPortComponentModel
            NPort component model created.

        Notes
        -----
        The component model does not belong to a specific database until it is added to a
        :class:`.ComponentDef` instance.
        """
        return NPortComponentModel(cls.__stub.Create(proto_wrappers.StringValue(value=name)))


class DynamicLinkComponentModel(ComponentModel):
    """Represents a dynamic link component model."""

    __stub: DynamicLinkComponentModelServiceStub = StubAccessor(StubType.dyn_link_component_model)

    @classmethod
    def create(cls, name):
        """Create a dynamic link component model.

        Parameters
        ----------
        name : str
            Name of the dynamic link component model.

        Returns
        -------
        DynamicLinkComponentModel
            Dynamic link component model created.

        Notes
        -----
        The component model does not belong to a specific database until it is added to a
        :class:`.ComponentDef` class.
        """
        return DynamicLinkComponentModel(cls.__stub.Create(proto_wrappers.StringValue(value=name)))

    @property
    def design_name(self):
        """:obj:`str`: Name of the design associated with the dynamic link component model."""
        return self.__stub.GetDesignName(self.msg).value

    @design_name.setter
    def design_name(self, value):
        self.__stub.SetDesignName(messages.string_property_message(self, value))
