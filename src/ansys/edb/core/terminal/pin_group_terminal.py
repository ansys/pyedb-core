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

"""Pin Group Terminal."""

from ansys.edb.core.inner import TypeField
from ansys.edb.core.inner import messages
from ansys.edb.core.layer.layer import Layer
from ansys.edb.core.session import StubAccessor
from ansys.edb.core.session import StubType
from ansys.edb.core.terminal.terminal import Terminal
from ansys.edb.core.terminal.terminal import TerminalType


class PinGroupTerminal(Terminal):
    """Represents a pin group terminal."""

    __stub = StubAccessor(StubType.pin_group_terminal)
    type = TypeField(TerminalType.PIN_GROUP)

    @classmethod
    def create(cls, layout, name, pin_group, net, is_ref=False):
        """Create a pin group terminal.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the pin group terminal in.
        net : :class:`.Net` or :obj:`str` or None
            Net reference.
        name : :obj:`str`
            Name of the pin group terminal.
        pin_group : :class:`.PinGroup`
            Pin group.
        is_ref : :obj:`bool`, default: False
            Whether the pin group terminal is a reference terminal.

        Returns
        -------
        PinGroupTerminal
        """
        return PinGroupTerminal(
            cls.__stub.Create(messages.pin_group_term_creation_message(layout, net, name, pin_group, is_ref))
        )

    @property
    def pin_group(self):
        """:class:`.PinGroup`: Pin group of the terminal."""
        from ansys.edb.core.hierarchy import pin_group

        return pin_group.PinGroup(self.__stub.GetPinGroup(self.msg))

    @pin_group.setter
    def pin_group(self, value):
        self.__stub.SetPinGroup(messages.pin_group_term_set_pin_group_message(self, value))

    @property
    def layer(self):
        """:class:`.Layer`: Layer."""
        return Layer(self.__stub.GetLayer(self.msg)).cast()

    @layer.setter
    def layer(self, value):
        self.__stub.SetLayer(messages.pin_group_term_set_layer_message(self, value))
