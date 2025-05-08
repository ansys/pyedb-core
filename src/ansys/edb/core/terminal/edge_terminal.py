"""Edge Terminal."""

from enum import Enum

import ansys.api.edb.v1.edge_term_pb2 as edge_term_pb2

from ansys.edb.core.geometry.arc_data import ArcData
from ansys.edb.core.inner import ObjBase, TypeField, messages, parser
from ansys.edb.core.layer.layer import Layer
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.terminal.terminal import Terminal, TerminalType


class EdgeType(Enum):
    """Provides an enum representing edge types."""

    PRIMITIVE = edge_term_pb2.PRIMITIVE_EDGE
    PADSTACK = edge_term_pb2.PAD_EDGE


class Edge(ObjBase):
    """Represents an edge."""

    __stub = StubAccessor(StubType.edge)
    type = TypeField(None)

    def cast(self):
        """Cast the base edge object to the correct subclass, if possible.

        Returns
        -------
        Edge
        """
        if self.is_null:
            return

        tp = self.type
        if tp == EdgeType.PRIMITIVE:
            return PrimitiveEdge(self.msg)
        if tp == EdgeType.PADSTACK:
            return PadEdge(self.msg)

    @classmethod
    def _create(cls, **params):
        return cls.__stub.Create(messages.edge_creation_message(cls.type.value, **params))

    @property
    def _type(self):
        return EdgeType(self.__stub.GetEdgeType(self.msg).t)

    @property
    def _params(self):
        res = self.__stub.GetParameters(self.msg)
        if self.type == EdgeType.PRIMITIVE:
            return res.primitive_params
        elif self.type == EdgeType.PADSTACK:
            return res.pad_params


class PadEdge(Edge):
    """Represents a padstack edge."""

    type = TypeField(EdgeType.PADSTACK)

    @classmethod
    def create(cls, padstack_instance, layer, arc):
        """Create a padstack edge.

        Parameters
        ----------
        padstack_instance : :class:`.PadstackInstance`
        layer : :class:`.Layer` or :obj:`str`
        arc : :class:`.ArcData`

        Returns
        -------
        PadEdge
        """
        return PadEdge(cls._create(padstack_instance=padstack_instance, layer=layer, arc=arc))

    @property
    def padstack_instance(self):
        """:class:`.PadstackInstance`: Padstack instance that the edge is on."""
        from ansys.edb.core.primitive.padstack_instance import PadstackInstance

        return PadstackInstance(self._params.padstack_instance)

    @property
    def layer(self):
        """:class:`.Layer`: Layer that the edge is on."""
        return Layer(self._params.layer.id).cast()

    @property
    def arc(self):
        """:class:`.ArcData`: Arc of the edge."""
        return ArcData(self._params.arc)


class PrimitiveEdge(Edge):
    """Represents a primitive edge."""

    type = TypeField(EdgeType.PRIMITIVE)

    @classmethod
    def create(cls, prim, point):
        """Create a primitive edge.

        Parameters
        ----------
        prim : :class:`.Primitive`
        point : :term:`Point2DLike`

        Returns
        -------
        PrimitiveEdge
        """
        return PrimitiveEdge(cls._create(primitive=prim, point=point))

    @property
    def primitive(self):
        """:class:`.Primitive`: Primitive of the terminal."""
        from ansys.edb.core.primitive import primitive

        return primitive.Primitive(self._params.primitive).cast()

    @property
    @parser.to_point_data
    def point(self):
        """:class:`.PointData`: Coordinates (x, y) of the terminal."""
        return self._params.point


class EdgeTerminal(Terminal):
    """Represents an edge terminal."""

    __stub = StubAccessor(StubType.edge_terminal)
    type = TypeField(TerminalType.EDGE)

    @classmethod
    def create(cls, layout, name, edges, net=None, is_ref=False):
        """Create an edge terminal.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the edge terminal in.
        name : :obj:`str`
            Name of the edge terminal.
        edges : list of Edge
        net : :class:`.Net` or :obj:`str` or None
            Net reference. The default is ``None``.
        is_ref : :obj:`bool`, default: False
            Whether the edge terminal is a reference terminal.

        Returns
        -------
        EdgeTerminal
        """
        return EdgeTerminal(
            cls.__stub.Create(messages.edge_term_creation_message(layout, net, name, edges, is_ref))
        )

    @property
    def edges(self):
        """:obj:`list` of :class:`.Edge`: All edges on the terminal."""
        return [Edge(msg).cast() for msg in self.__stub.GetEdges(self.msg).items]

    @edges.setter
    def edges(self, edges):
        self.__stub.GetEdges(messages.edge_term_set_edges_message(self, edges))
