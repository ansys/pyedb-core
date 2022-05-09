"""Terminals."""

import ansys.api.edb.v1.point_term_pb2 as pt
import ansys.api.edb.v1.term_pb2 as t

from ...interfaces.grpc import messages
from ...session import get_point_terminal_stub, get_terminal_stub
from ...utility.edb_errors import handle_grpc_exception
from ..base import ObjBase


class _TerminalQueryBuilder:
    @staticmethod
    def set_reference(source, ref):
        return t.TermSetRefMessage(source_term=source.msg, ref_term=ref.msg)


class Terminal(ObjBase):
    """Class representing a terminal object."""

    @handle_grpc_exception
    def set_reference(self, ref):
        """
        Set the reference of a terminal.

        Parameters
        ----------
        ref : Terminal

        Returns
        -------
        bool
        """
        return (
            get_terminal_stub().SetReference(_TerminalQueryBuilder.set_reference(self, ref)).value
        )


class _PointTerminalQueryBuilder:
    @staticmethod
    def create(layout, net, layer: str, name: str, x: float, y: float):
        return pt.PointTermCreationMessage(
            layout=layout.id,
            net=messages.net_ref_message(net),
            layer=messages.layer_ref_message(layer),
            name=name,
            point=messages.point_message((x, y)),
        )


class PointTerminal(Terminal):
    """Class representing a point terminal object."""

    @staticmethod
    @handle_grpc_exception
    def create(layout, net, layer, name, x, y):
        """
        Create a point terminal.

        Parameters
        ----------
        layout : Layout
        net : str
        layer : str
        name : str
        x : float
        y : float

        Returns
        -------
        PointTerminal
        """
        return PointTerminal(
            get_point_terminal_stub().Create(
                _PointTerminalQueryBuilder.create(layout, net, layer, name, x, y)
            )
        )
