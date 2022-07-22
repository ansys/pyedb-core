"""Layout Object."""
import enum

import ansys.api.edb.v1.layout_obj_pb2 as layout_obj_pb2

from ansys.edb.core import ObjBase


class LayoutObjType(enum.Enum):
    """Layout Object type."""

    INVALID_LAYOUT_OBJ = layout_obj_pb2.INVALID_LAYOUT_OBJ
    PRIMITIVE = layout_obj_pb2.PRIMITIVE
    PADSTACK_INSTANCE = layout_obj_pb2.PADSTACK_INST
    TERMINAL = layout_obj_pb2.TERM
    TERMINAL_INSTANCE = layout_obj_pb2.TERM_INST
    CELL_INSTANCE = layout_obj_pb2.CELL_INST
    LAYER = layout_obj_pb2.LAYER
    NET = layout_obj_pb2.NET
    PADSTACK = layout_obj_pb2.PADSTACK
    GROUP = layout_obj_pb2.GROUP
    NET_CLASS = layout_obj_pb2.NET_CLASS
    CELL = layout_obj_pb2.CELL
    DIFFERENTIAL_PAIR = layout_obj_pb2.DIFFERENTIAL_PAIR
    PIN_GROUP = layout_obj_pb2.PIN_GROUP
    VOLTAGE_REGULATOR = layout_obj_pb2.VOLTAGE_REGULATOR
    EXTENDED_NET = layout_obj_pb2.EXTENDED_NET


class LayoutObj(ObjBase):
    """Layout Object class."""

    pass
