"""Cell Instance."""

from __future__ import annotations

import ansys.api.edb.v1.cell_instance_pb2 as pb

from ....session import get_cell_instance_stub
from ....utility.edb_errors import handle_grpc_exception
from ...cell.hierarchy.hierarchy_obj import HierarchyObj


class _CellInstanceQueryBuilder:
    """Class for creating cell instance messages."""

    @staticmethod
    def create(layout, name, ref_layout):
        """
        Create cell instance create message.

        Parameters
        ----------
        layout : Terminal
        name : str
        ref_layout : Layout
        """
        return pb.CellInstanceCreationMessage(
            layout=layout.msg, name=name, ref_layout=ref_layout.msg
        )


class CellInstance(HierarchyObj):
    """Class for representing cell instance hierarchy object."""

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
        CellInstance
            Cell instance created.
        """
        return CellInstance(
            get_cell_instance_stub().Create(
                _CellInstanceQueryBuilder.create(layout, name, ref_layout)
            )
        )
