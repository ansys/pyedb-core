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

"""Netlist model."""
from ansys.edb.core.hierarchy.model import Model
from ansys.edb.core.inner import messages
from ansys.edb.core.session import NetlistModelServiceStub, StubAccessor, StubType


class NetlistModel(Model):
    """Represents a netlist model object."""

    __stub: NetlistModelServiceStub = StubAccessor(StubType.netlist_model)

    @classmethod
    def create(cls, name):
        """Create a netlist model.

        Parameters
        ----------
        name : str
            Name of the netlist model.

        Returns
        -------
        NetlistModel
            Netlist model created.
        """
        return cls(cls.__stub.Create(messages.str_message(name)))

    @property
    def netlist(self):
        """:obj:`str`: Netlist name."""
        return self.__stub.GetNetlist(messages.edb_obj_message(self)).value

    @netlist.setter
    def netlist(self, name):
        self.__stub.SetNetlist(messages.string_property_message(self, name))
