# Copyright (C) 2022 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

"""Point Terminal."""

from ansys.edb.core.inner import TypeField
from ansys.edb.core.inner import messages
from ansys.edb.core.inner import parser
from ansys.edb.core.layer.layer import Layer
from ansys.edb.core.session import StubAccessor
from ansys.edb.core.session import StubType
from ansys.edb.core.terminal.terminal import Terminal
from ansys.edb.core.terminal.terminal import TerminalType


class PointTerminal(Terminal):
    """Represents a point terminal object."""

    __stub = StubAccessor(StubType.point_terminal)
    type = TypeField(TerminalType.POINT)

    @classmethod
    def create(cls, layout, net, layer, name, point):
        """Create a point terminal.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the point terminal in.
        net : :class:`.Net` or :obj:`str` or None
            Net.
        layer : :class:`.Layer` or :obj:`str`
            Layer to place the point terminal on.
        name : :obj:`str`
            Name of the point terminal.
        point : :term:`Point2DLike`
            Type of the point terminal.

        Returns
        -------
        PointTerminal
        """
        return PointTerminal(cls.__stub.Create(messages.point_term_creation_message(layout, net, layer, name, point)))

    @property
    def params(self):
        """:class:`.Layer`, :class:`.PointData`: Layer that the point terminal is placed on and \
        the (x, y) coordinates.
        """
        res = self.__stub.GetParameters(self.msg)
        point = parser.to_point_data(res.point)
        layer = Layer(res.layer.id).cast()
        return layer, point

    @params.setter
    def params(self, params):
        self.__stub.SetParameters(messages.point_term_set_params_message(self, *params))

    @property
    def layer(self):
        """:class:`.Layer`: Layer that the point terminal is placed on."""
        return self.params[0]

    @layer.setter
    def layer(self, value):
        self.params = (value, self.point)

    @property
    def point(self):
        """:class:`.PointData`: Coordinates (x, y) of the point terminal."""
        return self.params[1]

    @point.setter
    def point(self, value):
        self.params = (self.layer, value)
