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

"""RLC component property."""

from ansys.api.edb.v1.rlc_component_property_pb2_grpc import RLCComponentPropertyServiceStub
import google.protobuf.empty_pb2 as empty_pb2

from ansys.edb.core.definition.component_property import ComponentProperty
from ansys.edb.core.inner import messages
from ansys.edb.core.session import StubAccessor, StubType


class RLCComponentProperty(ComponentProperty):
    """Represents an RLC component property."""

    __stub: RLCComponentPropertyServiceStub = StubAccessor(StubType.rlc_component_property)

    @classmethod
    def create(cls):
        """
        Create an RLC component property.

        Returns
        -------
        RLCComponentProperty
            RLC component property created.
        """
        return RLCComponentProperty(cls.__stub.Create(empty_pb2.Empty()))

    @property
    def enabled(self):
        """:obj:`bool`: Flag indicating if the RLC component property is enabled."""
        return self.__stub.GetEnabled(messages.edb_obj_message(self)).value

    @enabled.setter
    def enabled(self, value):
        self.__stub.SetEnabled(messages.bool_property_message(self, value))
