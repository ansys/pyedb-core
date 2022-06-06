"""Cell Instance."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ansys.api.edb.v1.cell_inst_pb2 as pb

from ....session import get_cell_inst_stub
from ....utility.edb_errors import handle_grpc_exception
from ...cell.hierarchy.hierarchy_obj import HierarchyObj

if TYPE_CHECKING:
    from ..layout import Layout


class _CellInstQueryBuilder:
    """Class for creating cell instance messages."""

    @staticmethod
    def create(layout: Layout, name: str, ref_layout: Layout):
        """Create cell instance create message."""
        return pb.CellInstCreationMessage(layout=layout.msg, name=name, ref_layout=ref_layout.msg)


class CellInst(HierarchyObj):
    """Class for representing cell instance hierarchy object."""

    def __init__(self, msg):
        """Initialize a cell instance."""
        super().__init__(msg)
        self = False

    @staticmethod
    @handle_grpc_exception
    def create(layout, name, ref_layout):
        """Create a cell instance object.

        Parameters
        ----------
        layout: Layout
        name: str
        ref_layout: Reference Layout

        Returns
        -------
        CellInst
            Cell instance created.
        """
        return CellInst(
            get_cell_inst_stub().Create(_CellInstQueryBuilder.create(layout, name, ref_layout))
        )
