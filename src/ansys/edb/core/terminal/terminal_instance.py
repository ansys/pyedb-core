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

"""Terminal Instance."""

from ansys.edb.core.edb_defs import LayoutObjType
from ansys.edb.core.inner import conn_obj
from ansys.edb.core.inner import messages
from ansys.edb.core.session import StubAccessor
from ansys.edb.core.session import StubType
from ansys.edb.core.terminal.terminal import Terminal


class TerminalInstance(conn_obj.ConnObj):
    """Represents a terminal instance."""

    __stub = StubAccessor(StubType.terminal_instance)
    layout_obj_type = LayoutObjType.TERMINAL_INSTANCE

    @classmethod
    def create(cls, layout, cell_instance, name, net_ref):
        """Create a terminal instance.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the terminal instance in.
        cell_instance : :class:`.CellInstance`
            Name of the cell instance to create the terminal instance on.
        name : :obj:`str`
            Name of the terminal instance.
        net_ref : :class:`.Net` or :obj:`str` or None
            Net reference.

        Returns
        -------
        TerminalInstance
        """
        return TerminalInstance(
            cls.__stub.Create(messages.term_inst_creation_message(layout, net_ref, cell_instance, name))
        )

    @property
    def owning_cell_instance(self):
        """:class:`.CellInstance`: Cell instance that owns the terminal."""
        from ansys.edb.core.hierarchy import cell_instance

        return cell_instance.CellInstance(self.__stub.GetOwningCellInstance(self.msg))

    @property
    def definition_terminal(self):
        """:class:`Terminal`: Definition terminal, if any."""
        return Terminal(self.__stub.GetDefinitionTerminal(self.msg)).cast()

    @property
    def definition_terminal_name(self):
        """:obj:`str`: Name of the definition terminal."""
        return self.__stub.GetDefinitionTerminalName(self.msg).value
