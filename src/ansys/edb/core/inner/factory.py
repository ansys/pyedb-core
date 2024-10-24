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

"""This module allows for the creating of objects while avoid circular imports."""

from ansys.edb.core.edb_defs import LayoutObjType
from ansys.edb.core.hierarchy import cell_instance
from ansys.edb.core.hierarchy.group import Group
from ansys.edb.core.hierarchy.pin_group import PinGroup
from ansys.edb.core.layout import voltage_regulator
from ansys.edb.core.primitive.primitive import PadstackInstance, Primitive
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.terminal.terminals import Terminal, TerminalInstance


def create_conn_obj(msg):
    """Create a connection object of its derived type based on its layout object type.

    Parameters
    ----------
    msg : ansys.api.edb.v1.edb_messages_pb2.EDBObjMessage

    Returns
    -------
    ansys.edb.core.inner.ConnObj
    """
    type = LayoutObjType(StubAccessor(StubType.connectable).__get__().GetObjType(msg).type)
    if type == LayoutObjType.PRIMITIVE:
        return Primitive(msg).cast()
    elif type == LayoutObjType.PADSTACK_INSTANCE:
        return PadstackInstance(msg)
    elif type == LayoutObjType.TERMINAL:
        return Terminal(msg).cast()
    elif type == LayoutObjType.TERMINAL_INSTANCE:
        return TerminalInstance(msg)
    elif type == LayoutObjType.CELL_INSTANCE:
        return cell_instance.CellInstance(msg)
    elif type == LayoutObjType.GROUP:
        return Group(msg).cast()
    elif type == LayoutObjType.PIN_GROUP:
        return PinGroup(msg)
    elif type == LayoutObjType.VOLTAGE_REGULATOR:
        return voltage_regulator.VoltageRegulator(msg)
    raise TypeError("Encountered an unknown layout object type.")
