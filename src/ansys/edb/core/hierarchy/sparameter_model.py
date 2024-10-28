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

"""S-parameter model."""
from ansys.edb.core.hierarchy.model import Model
from ansys.edb.core.inner import messages
from ansys.edb.core.session import SParameterModelServiceStub, StubAccessor, StubType


class SParameterModel(Model):
    """Represents an S-parameter model object."""

    __stub: SParameterModelServiceStub = StubAccessor(StubType.sparameter_model)

    @classmethod
    def create(cls, name, ref_net):
        """Create an S-parameter model.

        Parameters
        ----------
        name : str
            Name of the S-parameter model.
        ref_net : str
            Name of the reference net.
        """
        return cls(cls.__stub.Create(messages.sparameter_model_message(name, ref_net)))

    @property
    def _properties(self):
        return self.__stub.GetProperties(messages.edb_obj_message(self))

    @property
    def component_model(self):
        """:obj:`str`: Name of the component model."""
        return self._properties.name

    @component_model.setter
    def component_model(self, name):
        self.__stub.SetComponentModelName(messages.string_property_message(self, name))

    @property
    def reference_net(self):
        """:obj:`str`: Name of the reference net."""
        return self._properties.ref_net

    @reference_net.setter
    def reference_net(self, name):
        self.__stub.SetReferenceNet(messages.string_property_message(self, name))
