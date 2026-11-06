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

"""Bundle Terminal."""

from ansys.edb.core.inner import TypeField
from ansys.edb.core.inner import messages
from ansys.edb.core.session import StubAccessor
from ansys.edb.core.session import StubType
from ansys.edb.core.terminal.terminal import Terminal
from ansys.edb.core.terminal.terminal import TerminalType


class BundleTerminal(Terminal):
    """Represents a bundle terminal object."""

    __stub = StubAccessor(StubType.bundle_terminal)
    type = TypeField(TerminalType.BUNDLE)

    @classmethod
    def create(cls, terminals):
        """Create a bundle terminal.

        Parameters
        ----------
        terminals : list of Terminal

        Returns
        -------
        BundleTerminal
        """
        return BundleTerminal(cls.__stub.Create(messages.edb_obj_collection_message(terminals)))

    @property
    def terminals(self):
        """:obj:`list` of Terminal: All terminals grouped in the terminal."""
        return [Terminal(msg).cast() for msg in self.__stub.GetTerminals(self.msg).items]

    def ungroup(self):
        """Delete the grouping."""
        self.__stub.Ungroup(self.msg)
        self.msg = None
