from enum import Enum
from typing import Tuple, Union

import ansys.api.edb.v1.cell_pb2 as cell_pb2
from ansys.api.edb.v1.edb_messages_pb2 import ValueMessage
from google.protobuf.wrappers_pb2 import BoolValue

from ...session import get_cell_stub
from ..base import ObjBase
from .layout import Layout


class CellType(Enum):
    CIRCUIT_CELL = cell_pb2.CIRCUIT_CELL
    FOOTPRINT_CELL = cell_pb2.FOOTPRINT_CELL


def to_extent_message(val: Union[float, Tuple[float, bool]]):
    if type(val) == float:
        value = val
        absolute = False
    else:
        value, absolute = val

    return cell_pb2.ExtentMessage(value=ValueMessage(value=value), absolute=absolute)


def to_bool_message(val: bool):
    return BoolValue(value=val)


# dit representing options of HFSS Extents available via API.
HFSS_EXTENT_ARGS = {
    "dielectric": to_extent_message,
    "airbox_horizontal": to_extent_message,
    "airbox_vertical": to_extent_message,
    "airbox_vertical_positive": to_extent_message,
    "airbox_vertical_negative": to_extent_message,
    "airbox_truncate_at_ground": to_bool_message,
}


# takes user-provided arbitrary args and a list of allowed keywords
# return a copy including only the valid args
def sanitize_args(args):
    return {
        k: HFSS_EXTENT_ARGS[k](args[k])
        for k in filter(lambda k: k in args, HFSS_EXTENT_ARGS.keys())
    }


class _QueryBuilder:
    @staticmethod
    def create(db: "Database", cell_type: CellType, name: str):
        return cell_pb2.CellCreationMessage(database=db._msg, type=cell_type.value, name=name)

    @staticmethod
    def get_layout(cell):
        return cell._msg

    @staticmethod
    def set_hfss_extents(cell, **extents):
        extents = sanitize_args(extents)
        return cell_pb2.CellHfssExtentsMessage(cell=cell._msg, **extents)


class Cell(ObjBase):
    @staticmethod
    def create(db: "Database", cell_type: CellType, cell_name: str):
        return Cell(get_cell_stub().Create(_QueryBuilder.create(db, cell_type, cell_name)))

    def get_layout(self) -> Layout:
        return Layout(get_cell_stub().GetLayout(_QueryBuilder.get_layout(self)))

    def set_hfss_extents(self, **extents) -> bool:
        return get_cell_stub().SetHfssExtents(_QueryBuilder.set_hfss_extents(self, **extents)).value
