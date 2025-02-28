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
from ansys.edb.core.inner.conn_obj import ConnObj

_type_creator_params_dict = None


class _CreatorParams:
    def __init__(self, obj_type, do_cast=False):
        self.obj_type = obj_type
        self.do_cast = do_cast


def _initialize_type_creator_params_dict():
    global _type_creator_params_dict

    from ansys.edb.core.hierarchy.cell_instance import CellInstance
    from ansys.edb.core.hierarchy.group import Group
    from ansys.edb.core.hierarchy.pin_group import PinGroup
    from ansys.edb.core.layout.voltage_regulator import VoltageRegulator
    from ansys.edb.core.net.differential_pair import DifferentialPair
    from ansys.edb.core.net.extended_net import ExtendedNet
    from ansys.edb.core.net.net import Net
    from ansys.edb.core.net.net_class import NetClass
    from ansys.edb.core.primitive.primitive import PadstackInstance, Primitive
    from ansys.edb.core.terminal.terminals import Terminal, TerminalInstance

    _type_creator_params_dict = {
        LayoutObjType.PRIMITIVE: _CreatorParams(Primitive, True),
        LayoutObjType.PADSTACK_INSTANCE: _CreatorParams(PadstackInstance),
        LayoutObjType.TERMINAL: _CreatorParams(Terminal, True),
        LayoutObjType.TERMINAL_INSTANCE: _CreatorParams(TerminalInstance),
        LayoutObjType.CELL_INSTANCE: _CreatorParams(CellInstance),
        LayoutObjType.GROUP: _CreatorParams(Group, True),
        LayoutObjType.PIN_GROUP: _CreatorParams(PinGroup),
        LayoutObjType.VOLTAGE_REGULATOR: _CreatorParams(VoltageRegulator),
        LayoutObjType.NET_CLASS: _CreatorParams(NetClass),
        LayoutObjType.EXTENDED_NET: _CreatorParams(ExtendedNet),
        LayoutObjType.DIFFERENTIAL_PAIR: _CreatorParams(DifferentialPair),
        LayoutObjType.NET: _CreatorParams(Net),
    }


def _get_type_creator_dict():
    if _type_creator_params_dict is None:
        _initialize_type_creator_params_dict()
    return _type_creator_params_dict


def create_obj(msg, obj_type, do_cast):
    """Create an object from the provided message of the provided type."""
    obj = obj_type(msg)
    if do_cast:
        obj = obj.cast()
    return obj


def create_lyt_obj(msg, lyt_obj_type):
    """Create a layout object from the provided message of the type corresponding to the provided layout object type."""
    params = _get_type_creator_dict()[lyt_obj_type]
    return create_obj(msg, params.obj_type, params.do_cast)


def create_conn_obj(msg):
    """Create a connection object of its derived type based on its layout object type.

    Parameters
    ----------
    msg : ansys.api.edb.v1.edb_messages_pb2.EDBObjMessage

    Returns
    -------
    ansys.edb.core.inner.ConnObj
    """
    return create_lyt_obj(msg, ConnObj(msg).obj_type)
