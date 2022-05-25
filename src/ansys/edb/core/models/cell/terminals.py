"""Terminals."""

import ansys.api.edb.v1.term_pb2 as t

from ...interfaces.grpc import messages
from ...session import get_bundle_terminal_stub, get_point_terminal_stub, get_terminal_stub
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
        """
        get_terminal_stub().SetReference(_TerminalQueryBuilder.set_reference(self, ref))


class BundleTerminal(Terminal):
    """Class representing a bundle terminal object."""

    @staticmethod
    @handle_grpc_exception
    def create(terminals):
        """
        Create a bundle terminal.

        Parameters
        ----------
        terminals : list of Terminal

        Returns
        -------
        PointTerminal
        """
        return BundleTerminal(
            get_bundle_terminal_stub().Create(messages.bundle_term_terminals_message(terminals))
        )

    @property
    @handle_grpc_exception
    def terminals(self):
        """Get list of terminals grouped in this terminal.

        Returns
        -------
        list of Terminal
        """
        return [Terminal(msg) for msg in get_bundle_terminal_stub().GetTerminals(self.msg)]

    @handle_grpc_exception
    def ungroup(self):
        """Delete this grouping."""
        get_bundle_terminal_stub().Ungroup(self.msg)
        self.msg = None


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
        """
        get_point_terminal_stub().SetParameters(
            messages.point_term_set_params_message(self, layer, point)
        )
