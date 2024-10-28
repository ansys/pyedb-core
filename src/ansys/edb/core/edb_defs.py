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
