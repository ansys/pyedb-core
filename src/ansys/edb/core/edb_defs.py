"""Common definitions used in EDB."""

from enum import Enum

import ansys.api.edb.v1.definition_obj_pb2 as definition_obj_pb2
import ansys.api.edb.v1.layout_obj_pb2 as layout_obj_pb2


class LayoutObjType(Enum):
    """Provides an enum representing layout object types."""

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


class DefinitionObjType(Enum):
    """Provides an enum representing definition object types."""

    INVALID_DEFINITION_TYPE = definition_obj_pb2.INVALID_DEFINITION_TYPE
    PADSTACK_DEF = definition_obj_pb2.PADSTACK_DEF
    COMPONENT_DEF = definition_obj_pb2.COMPONENT_DEF
    BONDWIRE_DEF = definition_obj_pb2.BONDWIRE_DEF
    MATERIAL_DEF = definition_obj_pb2.MATERIAL_DEF
    DATASET_DEF = definition_obj_pb2.DATASET_DEF
    PACKAGE_DEF = definition_obj_pb2.PACKAGE_DEF
    DEFINITION_TYPE_COUNT = definition_obj_pb2.DEFINITION_TYPE_COUNT
