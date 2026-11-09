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

"""Terminal Instance Terminal."""

from ansys.edb.core.inner import TypeField
from ansys.edb.core.inner import messages
from ansys.edb.core.session import StubAccessor
from ansys.edb.core.session import StubType
from ansys.edb.core.terminal.terminal import Terminal
from ansys.edb.core.terminal.terminal import TerminalType
from ansys.edb.core.terminal.terminal_instance import TerminalInstance


class TerminalInstanceTerminal(Terminal):
    """Represents a terminal instance terminal."""

    __stub = StubAccessor(StubType.terminal_instance_terminal)
    type = TypeField(TerminalType.TERM_INST)

    @classmethod
    def create(cls, layout, term_instance, name, net_ref, is_ref=False):
        """Create a terminal instance terminal.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the terminal instance terminal in.
        term_instance : TerminalInstance
            Terminal instance to create the terminal instance terminal on.
        name : :obj:`str`
            Name of the terminal instance terminal.
        net_ref : :class:`.Net` or :obj:`str` or None
            Net reference.
        is_ref : bool, default: False
            Whether the terminal instance terminal is a reference terminal.

        Returns
        -------
        TerminalInstanceTerminal
        """
        return TerminalInstanceTerminal(
            cls.__stub.Create(messages.term_inst_term_creation_message(layout, net_ref, name, term_instance, is_ref))
        )

    @property
    def terminal_instance(self):
        """:class:`TerminalInstance`: Terminal instance."""
        return TerminalInstance(self.__stub.GetTerminalInstance(self.msg))

    @terminal_instance.setter
    def terminal_instance(self, value):
        self.__stub.SetTerminalInstance(messages.term_inst_term_set_instance_message(self, value))
