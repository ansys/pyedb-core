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

"""PadstackInstance Terminal."""

from ansys.edb.core.inner import TypeField
from ansys.edb.core.inner import messages
from ansys.edb.core.layer.layer import Layer
from ansys.edb.core.session import StubAccessor
from ansys.edb.core.session import StubType
from ansys.edb.core.terminal.terminal import Terminal
from ansys.edb.core.terminal.terminal import TerminalType


class PadstackInstanceTerminal(Terminal):
    """Represents a padstack instance terminal."""

    __stub = StubAccessor(StubType.padstack_instance_terminal)
    type = TypeField(TerminalType.PADSTACK_INST)

    @classmethod
    def create(cls, layout, name, padstack_instance, layer, net, is_ref=False):
        """Create a padstack instance terminal.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the padstack instance terminal in.
        name : :obj:`str`
            Name of the padstack instance terminal.
        padstack_instance : :class:`.PadstackInstance`
            Padstack instance.
        layer : :class:`.Layer` or :obj:`str`
            Layer to place the padstack instance terminal on.
        net : :class:`.Net` or :obj:`str` or None
            Net.
        is_ref : :obj:`bool`, default: False
            Whether the padstack instance terminal is a reference terminal.

        Returns
        -------
        PadstackInstanceTerminal
        """
        return PadstackInstanceTerminal(
            cls.__stub.Create(
                messages.padstack_inst_term_creation_message(layout, name, padstack_instance, layer, net, is_ref)
            )
        )

    @property
    def params(self):
        """:obj:`list` of :class:`.PadstackInstance` and :class:`.Layer`: Padstack instance and layer."""
        from ansys.edb.core.primitive import padstack_instance

        res = self.__stub.GetParameters(self.msg)
        padstack_instance = padstack_instance.PadstackInstance(res.padstack_instance)
        layer = Layer(res.layer.id).cast()
        return padstack_instance, layer

    @params.setter
    def params(self, params):
        (padstack_instance, layer) = params
        self.__stub.SetParameters(messages.padstack_inst_term_set_params_message(self, padstack_instance, layer))

    @property
    def padstack_instance(self):
        """:class:`.PadstackInstance`: Padstack instance of the terminal."""
        return self.params[0]

    @property
    def layer(self):
        """:class:`.Layer`: Layer the terminal is placed on."""
        return self.params[1]
