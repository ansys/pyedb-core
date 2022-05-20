"""Terminals."""

import ansys.api.edb.v1.term_pb2 as t

from ...interfaces.grpc import messages
from ...session import get_point_terminal_stub, get_terminal_stub
from ...utility.edb_errors import handle_grpc_exception
from ..base import ObjBase
from .layer import Layer


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
        net : str or Net
        layer : str or Layer
        name : str
        x : Value
        y : Value

        Returns
        -------
        PointTerminal
        """
        return PointTerminal(
            get_point_terminal_stub().Create(
                messages.point_term_creation_message(layout, net, layer, name, x, y)
            )
        )

    @handle_grpc_exception
    def get_params(self):
        """Get x, y coordinates and the layer this point terminal is placed on.

        Returns
        -------
        (Layer, (Value, Value))
        """
        res = get_point_terminal_stub().GetParameters(self.msg)
        point = (res.point.x.value, res.point.y.value)
        layer = Layer(res.layer.id)
        return layer, point

    @handle_grpc_exception
    def set_params(self, layer, point):
        """Set x, y coordinates and the layer this point terminal is placed on.

        Parameters
        ----------
        layer : str or Layer
        point : PointData

        Returns
        -------
        bool
        """
        return (
            get_point_terminal_stub()
            .SetParameters(messages.point_term_set_params_message(self, layer, point))
            .value
        )
