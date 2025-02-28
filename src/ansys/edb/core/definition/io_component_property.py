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

"""IO component property."""

from ansys.api.edb.v1.io_component_property_pb2_grpc import IOComponentPropertyServiceStub
import google.protobuf.empty_pb2 as empty_pb2

from ansys.edb.core.definition import component_property, port_property, solder_ball_property
from ansys.edb.core.inner import messages
from ansys.edb.core.session import StubAccessor, StubType


class IOComponentProperty(component_property.ComponentProperty):
    """Represents an I0 component property."""

    __stub: IOComponentPropertyServiceStub = StubAccessor(StubType.io_component_property)

    @classmethod
    def create(cls):
        """
        Create an IO component property.

        Returns
        -------
        IOComponentProperty
            IO component property created.
        """
        return IOComponentProperty(cls.__stub.Create(empty_pb2.Empty()))

    @property
    def solder_ball_property(self):
        """:obj:`SolderBallProperty`: Solder ball property.

        A copy is returned. Use the setter for any modifications to be reflected.
        """
        return solder_ball_property.SolderBallProperty(
            self.__stub.GetSolderBallProperty(messages.edb_obj_message(self))
        )

    @solder_ball_property.setter
    def solder_ball_property(self, value):
        self.__stub.SetSolderBallProperty(
            messages.pointer_property_message(target=self, value=value)
        )

    @property
    def port_property(self):
        """:obj:`PortProperty`: Port property.

        A copy is returned. Use the setter for any modifications to be reflected.
        """
        return port_property.PortProperty(
            self.__stub.GetPortProperty(messages.edb_obj_message(self))
        )

    @port_property.setter
    def port_property(self, value):
        self.__stub.SetPortProperty(messages.pointer_property_message(target=self, value=value))
