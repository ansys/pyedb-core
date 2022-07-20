"""Cell Instance."""

from __future__ import annotations

import ansys.api.edb.v1.cell_instance_pb2 as pb

from ansys.edb.core.core import handle_grpc_exception
from ansys.edb.core.hierarchy import HierarchyObj
from ansys.edb.core.session import get_cell_instance_stub


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
        ref_layout: Layout

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
