"""This module allows for the creating of objects while avoid circular imports."""

from ansys.edb.edb_defs import LayoutObjType
from ansys.edb.hierarchy.cell_instance import CellInstance
from ansys.edb.hierarchy.group import Group
from ansys.edb.hierarchy.pin_group import PinGroup
import ansys.edb.layout as layout
from ansys.edb.primitive.primitive import PadstackInstance, Primitive
from ansys.edb.session import StubAccessor, StubType
from ansys.edb.terminal.terminals import Terminal, TerminalInstance


def create_conn_obj(msg):
    """Create a ConnObj of its derived type based on its layout obj type.

    Parameters
    ----------
    msg : ansys.api.edb.v1.edb_messages_pb2.EDBObjMessage

    Returns
    -------
    ansys.edb.core.ConnObj
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
        return CellInstance(msg)
    elif type == LayoutObjType.GROUP:
        return Group(msg).cast()
    elif type == LayoutObjType.PIN_GROUP:
        return PinGroup(msg)
    elif type == LayoutObjType.VOLTAGE_REGULATOR:
        return layout.VoltageRegulator(msg)
    raise TypeError("Encountered an unknown layout obj type")
