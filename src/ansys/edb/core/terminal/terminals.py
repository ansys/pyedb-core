"""Terminals."""

from enum import Enum

import ansys.api.edb.v1.edge_term_pb2 as edge_term_pb2
import ansys.api.edb.v1.term_pb2 as term_pb2

from ansys.edb.core.edb_defs import LayoutObjType
from ansys.edb.core.geometry.arc_data import ArcData
from ansys.edb.core.inner import ObjBase, TypeField, conn_obj, messages, parser
from ansys.edb.core.layer.layer import Layer
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.port_post_processing_prop import PortPostProcessingProp
from ansys.edb.core.utility.value import Value


class TerminalType(Enum):
    """Provides an enum representing terminal types."""

    EDGE = term_pb2.EDGE_TERM
    POINT = term_pb2.POINT_TERM
    TERM_INST = term_pb2.TERM_INST_TERM
    PADSTACK_INST = term_pb2.PADSTACK_INST_TERM
    BUNDLE = term_pb2.BUNDLE_TERM
    PIN_GROUP = term_pb2.PIN_GROUP_TERM


class BoundaryType(Enum):
    """Provides an enum representing terminal boundary types."""

    PORT = term_pb2.PORT_BOUNDARY
    PEC = term_pb2.PEC_BOUNDARY
    RLC = term_pb2.RLC_BOUNDARY
    CURRENT_SOURCE = term_pb2.CURRENT_SOURCE
    VOLTAGE_SOURCE = term_pb2.VOLTAGE_SOURCE
    NEXXIM_GROUND = term_pb2.NEXXIM_GROUND
    NEXXIM_PORT = term_pb2.NEXXIM_PORT
    DC_TERMINAL = term_pb2.DC_TERMINAL
    VOLTAGE_PROBE = term_pb2.VOLTAGE_PROBE


class SourceTermToGroundType(Enum):
    """Provides an enum representing source terminal-to-ground types."""

    NO_GROUND = term_pb2.NO_GROUND
    NEGATIVE = term_pb2.NEGATIVE
    POSITIVE = term_pb2.POSITIVE


class HfssPIType(Enum):
    """Provides an enum representing HFSS PI types."""

    DEFAULT = term_pb2.PI_DEFAULT
    COAXIAL_OPEN = term_pb2.PI_COAXIAL_OPEN
    COAXIAL_SHORTENED = term_pb2.PI_COAXIAL_SHORTENED
    GAP = term_pb2.PI_GAP
    LUMPED = term_pb2.PI_LUMPED


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
        return EdgeType(self.__stub.GetType(self.msg))

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
        from ansys.edb.core.primitive import primitive

        return primitive.PadstackInstance(self._params.padstack_instance)

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


class Terminal(conn_obj.ConnObj):
    """Represents a terminal object."""

    __stub = StubAccessor(StubType.terminal)
    type = TypeField(None)
    layout_obj_type = LayoutObjType.TERMINAL

    def cast(self, term_type=None):
        """Cast the terminal object to the correct concrete type, fetching the type if necessary.

        Parameters
        ----------
        term_type : TerminalType

        Returns
        -------
        Terminal
        """
        if self.is_null:
            return

        tt = self.type

        if term_type is not None and tt != term_type:
            return
        elif tt == TerminalType.EDGE:
            return EdgeTerminal(self.msg)
        elif tt == TerminalType.POINT:
            return PointTerminal(self.msg)
        elif tt == TerminalType.TERM_INST:
            return TerminalInstanceTerminal(self.msg)
        elif tt == TerminalType.PADSTACK_INST:
            return PadstackInstanceTerminal(self.msg)
        elif tt == TerminalType.BUNDLE:
            return BundleTerminal(self.msg)
        elif tt == TerminalType.PIN_GROUP:
            return PinGroupTerminal(self.msg)

    @classmethod
    def find(cls, layout, name):
        """Find a terminal by name in a given layout.

        Parameters
        ----------
        layout : :class:`.Layout`
           Layout to search for the terminal.
        name : .str
            Name of the terminal.

        Returns
        -------
        Terminal
        """
        return Terminal(
            cls.__stub.FindByName(messages.term_find_by_name_message(layout, name))
        ).cast(cls.type)

    @property
    def _params(self):
        return self.__stub.GetParams(self.msg)

    @_params.setter
    def _params(self, values):
        self.__stub.SetParams(messages.term_set_params_message(self, **values))

    @property
    def _type(self):
        """:class:`TerminalType`: Terminal type."""
        return TerminalType(self._params.term_type)

    @property
    def bundle_terminal(self):
        """:class:`BundleTerminal`: Bundle terminal that the terminal belongs to, if any."""
        return BundleTerminal(self._params.bundle_term)

    @property
    def reference_terminal(self):
        """:class:`Terminal`: Terminal that the terminal references, if any."""
        return Terminal(self._params.ref_term).cast()

    @reference_terminal.setter
    def reference_terminal(self, value):
        self._params = {"ref_term": value}

    @property
    def reference_layer(self):
        """:class:`.Layer`: Layer that the terminal references, if any, by either layer object or name."""
        return Layer(self._params.ref_layer).cast()

    @reference_layer.setter
    def reference_layer(self, value):
        self._params = {"ref_layer": value}

    @property
    def is_interface_terminal(self):
        """:obj:`bool`: Flag indicating if the terminal is an interface."""
        return self._params.is_interface

    @property
    def is_reference_terminal(self):
        """:obj:`bool`: Flag indicating if the terminal is a reference terminal."""
        return self._params.is_reference

    @property
    def use_reference_from_hierarchy(self):
        """:obj:`bool`: Flag indicating if the terminal can use references from the hierarchy."""
        return self._params.use_ref_from_hierarchy

    @use_reference_from_hierarchy.setter
    def use_reference_from_hierarchy(self, value):
        self._params = {"use_ref_from_hierarchy": value}

    @property
    def is_auto_port(self):
        """:obj:`bool`: Flag indicating if the terminal is an auto port."""
        return self._params.is_auto_port

    @is_auto_port.setter
    def is_auto_port(self, value):
        self._params = {"is_auto_port": value}

    @property
    def is_circuit_port(self):
        """:obj:`bool`: Flag indicating if the terminal is a circuit port."""
        return self._params.is_circuit_port

    @is_circuit_port.setter
    def is_circuit_port(self, value):
        self._params = {"is_circuit_port": value}

    @property
    def name(self):
        """:obj:`str`: Name of the terminal."""
        return self._params.name

    @name.setter
    def name(self, value):
        self._params = {"name": value}

    @property
    def boundary_type(self):
        """:class:`BoundaryType`: Boundary type of the terminal."""
        return BoundaryType(self._params.boundary_type)

    @boundary_type.setter
    def boundary_type(self, value):
        self._params = {"boundary_type": value.value}

    @property
    def impedance(self):
        """:class:`.Value`: Impedance of the terminal."""
        return Value(self._params.impedance)

    @impedance.setter
    def impedance(self, value):
        self._params = {"impedance": value}

    @property
    def source_amplitude(self):
        """:class:`.Value`: Source amplitude of the terminal."""
        return Value(self._params.source_amplitude)

    @source_amplitude.setter
    def source_amplitude(self, value):
        self._params = {"source_amplitude": value}

    @property
    def source_phase(self):
        """:class:`.Value`: Source phase of the terminal."""
        return Value(self._params.source_phase)

    @source_phase.setter
    def source_phase(self, value):
        self._params = {"source_phase": value}

    @property
    def term_to_ground(self):
        """:class:`SourceTermToGroundType`: Source terminal-to-ground type."""
        return SourceTermToGroundType(self._params.term_to_ground)

    @term_to_ground.setter
    def term_to_ground(self, value):
        self._params = {"term_to_ground": value.value}

    @property
    def hfss_pi_type(self):
        """:class:`HfssPIType`: HFSS PI type."""
        return HfssPIType(self._params.hfss_pi_type)

    @hfss_pi_type.setter
    def hfss_pi_type(self, value):
        self._params = {"hfss_pi_type": value.value}

    @property
    def model(self):
        """:obj:`str`: S-parameter model."""
        return self._params.s_param_model

    @model.setter
    def model(self, value):
        self._params = {"s_param_model": value}

    @property
    @parser.to_rlc
    def rlc_boundary_parameters(self):
        """:class:`.Rlc`: RLC boundary parameters."""
        return self._params.rlc

    @rlc_boundary_parameters.setter
    def rlc_boundary_parameters(self, value):
        self._params = {"rlc": value}

    @property
    def port_post_processing_prop(self):
        """:class:`.PortPostProcessingProp`: Port postprocessing properties."""
        msg = self._params.port_post_processing_prop
        return PortPostProcessingProp(
            voltage_magnitude=msg.voltage_magnitude,
            voltage_phase=msg.voltage_phase,
            deembed_length=msg.deembed_length,
            renormalization_impedance=msg.renormalization_impedance,
            do_deembed=msg.do_deembed,
            do_deembed_gap_l=msg.do_deembed_gap_length,
            do_renormalize=msg.do_renormalize,
        )

    @port_post_processing_prop.setter
    def port_post_processing_prop(self, value):
        self._params = {"port_post_processing_prop": value}

    def _product_solvers(self, product_id):
        return self.__stub.GetProductSolvers(
            messages.term_get_product_solver_message(self, product_id)
        )

    def product_solver_option(self, product_id, solver_name):
        """Get the name of the product solver option.

        Parameters
        ----------
        product_id : ProductIdType
            ID of the product.
        solver_name : :obj:`str`
            Name of the solver.

        Returns
        -------
        :obj:`str`
            Name of the product solver option.
        """
        return next(
            solver.option
            for solver in self._product_solvers(product_id)
            if solver.name == solver_name
        )

    def set_product_solver_option(self, product_id, solver_name, option):
        """Set the product solver option.

        Parameters
        ----------
        product_id : ProductIdType
            ID of the product.
        solver_name : obj:`str`
            Name of the solver.
        option : obj:`str`
           Name of the product solver option.
        """
        self.__stub.SetProductSolverOptions(
            messages.term_set_solver_option_message(self, product_id, solver_name, option)
        )

    def product_solver_names(self, product_id):
        """Get the list of solver names.

        Parameters
        ----------
        product_id : ProductIdType
            ID of the product.

        Returns
        -------
        list of str
        """
        return [solver.name for solver in self._product_solvers(product_id)]


class TerminalInstance(conn_obj.ConnObj):
    """Represents a terminal instance."""

    __stub = StubAccessor(StubType.terminal_instance)
    layout_obj_type = LayoutObjType.TERMINAL_INSTANCE

    @classmethod
    def create(cls, layout, cell_instance, name, net_ref):
        """Create a terminal instance.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the terminal instance in.
        cell_instance : :class:`.CellInstance`
            Name of the cell instance to create the terminal instance on.
        name : :obj:`str`
            Name of the terminal instance.
        net_ref : :class:`.Net` or :obj:`str` or None
            Net reference.

        Returns
        -------
        TerminalInstance
        """
        return TerminalInstance(
            cls.__stub.Create(
                messages.term_inst_creation_message(layout, net_ref, cell_instance, name)
            )
        )

    @property
    def owning_cell_instance(self):
        """:class:`.CellInstance`: Cell instance that owns the terminal."""
        from ansys.edb.core.hierarchy import cell_instance

        return cell_instance.CellInstance(self.__stub.GetOwningCellInstance(self.msg))

    @property
    def definition_terminal(self):
        """:class:`Terminal`: Definition terminal, if any."""
        return Terminal(self.__stub.GetDefinitionTerminal(self.msg)).cast()

    @property
    def definition_terminal_name(self):
        """:obj:`str`: Name of the definition terminal."""
        return self.__stub.GetDefinitionTerminalName(self.msg).value


class TerminalInstanceTerminal(Terminal):
    """Represents a terminal instance terminal."""

    __stub = StubAccessor(StubType.terminal_instance_terminal)
    type = TypeField(TerminalType.TERM_INST)

    @classmethod
    def create(cls, layout, term_instance, name, net_ref, is_ref=False):
        """Create a terminal instance terminal.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the terminal instance terminal in.
        term_instance : TerminalInstance
            Terminal instance to create the terminal instance terminal on.
        name : :obj:`str`
            Name of the terminal instance terminal.
        net_ref : :class:`.Net` or :obj:`str` or None
            Net reference.
        is_ref : bool, default: False
            Whether the terminal instance terminal is a reference terminal.

        Returns
        -------
        TerminalInstanceTerminal
        """
        return TerminalInstanceTerminal(
            cls.__stub.Create(
                messages.term_inst_term_creation_message(
                    layout, net_ref, name, term_instance, is_ref
                )
            )
        )

    @property
    def terminal_instance(self):
        """:class:`TerminalInstance`: Terminal instance."""
        return TerminalInstance(self.__stub.GetTerminalInstance(self.msg))

    @terminal_instance.setter
    def terminal_instance(self, value):
        self.__stub.SetTerminalInstance(messages.term_inst_term_set_instance_message(self, value))


class BundleTerminal(Terminal):
    """Represents a bundle terminal object."""

    __stub = StubAccessor(StubType.bundle_terminal)
    type = TypeField(TerminalType.BUNDLE)

    @classmethod
    def create(cls, terminals):
        """Create a bundle terminal.

        Parameters
        ----------
        terminals : list of Terminal

        Returns
        -------
        BundleTerminal
        """
        return BundleTerminal(cls.__stub.Create(messages.edb_obj_collection_message(terminals)))

    @property
    def terminals(self):
        """:obj:`list` of Terminal: All terminals grouped in the terminal."""
        return [Terminal(msg).cast() for msg in self.__stub.GetTerminals(self.msg)]

    def ungroup(self):
        """Delete the grouping."""
        self.__stub.Ungroup(self.msg)
        self.msg = None


class PointTerminal(Terminal):
    """Represents a point terminal object."""

    __stub = StubAccessor(StubType.point_terminal)
    type = TypeField(TerminalType.POINT)

    @classmethod
    def create(cls, layout, net, layer, name, point):
        """Create a point terminal.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the point terminal in.
        net : :class:`.Net` or :obj:`str` or None
            Net.
        layer : :class:`.Layer` or :obj:`str`
            Layer to place the point terminal on.
        name : :obj:`str`
            Name of the point terminal.
        point : :term:`Point2DLike`
            Type of the point terminal.

        Returns
        -------
        PointTerminal
        """
        return PointTerminal(
            cls.__stub.Create(messages.point_term_creation_message(layout, net, layer, name, point))
        )

    @property
    def params(self):
        """:class:`.Layer`, :class:`.PointData`: Layer that the point terminal is placed on and \
        the (x, y) coordinates."""
        res = self.__stub.GetParameters(self.msg)
        point = parser.to_point_data(res.point)
        layer = Layer(res.layer.id).cast()
        return layer, point

    @params.setter
    def params(self, params):
        self.__stub.SetParameters(messages.point_term_set_params_message(self, *params))

    @property
    def layer(self):
        """:class:`.Layer`: Layer that the point terminal is placed on."""
        return self.params[0]

    @layer.setter
    def layer(self, value):
        self.params = (messages.edb_obj_message(value), self.point)

    @property
    def point(self):
        """:class:`.PointData`: Coordinates (x, y) of the point terminal."""
        return self.params[1]

    @point.setter
    def point(self, value):
        self.params = (self.layer, messages.point_message(value))


class PadstackInstanceTerminal(Terminal):
    """Represents a padstack instance terminal."""

    __stub = StubAccessor(StubType.padstack_instance_terminal)
    type = TypeField(TerminalType.PADSTACK_INST)

    @classmethod
    def create(cls, layout, name, padstack_instance, layer, net, is_ref=False):
        """Create a padstack instance terminal.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the padstack instance terminal in.
        name : :obj:`str`
            Name of the padstack instance terminal.
        padstack_instance : :class:`.PadstackInstance`
            Padstack instance.
        layer : :class:`.Layer` or :obj:`str`
            Layer to place the padstack instance terminal on.
        net : :class:`.Net` or :obj:`str` or None
            Net.
        is_ref : :obj:`bool`, default: False
            Whether the padstack instance terminal is a reference terminal.

        Returns
        -------
        PadstackInstanceTerminal
        """
        return PadstackInstanceTerminal(
            cls.__stub.Create(
                messages.padstack_inst_term_creation_message(
                    layout, name, padstack_instance, layer, net, is_ref
                )
            )
        )

    @property
    def params(self):
        """:obj:`list` of :class:`.PadstackInstance` and :class:`.Layer`: Padstack instance and layer."""
        from ansys.edb.core.primitive import primitive

        res = self.__stub.GetParameters(self.msg)
        padstack_instance = primitive.PadstackInstance(res.padstack_instance)
        layer = Layer(res.layer).cast()
        return padstack_instance, layer

    @params.setter
    def params(self, params):
        (padstack_instance, layer) = params
        self.__stub.SetParameters(
            messages.padstack_inst_term_set_params_message(self, padstack_instance, layer)
        )

    @property
    def padstack_instance(self):
        """:class:`.PadstackInstance`: Padstack instance of the terminal."""
        return self.params[0]

    @property
    def layer(self):
        """:class:`.Layer`: Layer the terminal is placed on."""
        return self.params[1]


class PinGroupTerminal(Terminal):
    """Represents a pin group terminal."""

    __stub = StubAccessor(StubType.pin_group_terminal)
    type = TypeField(TerminalType.PIN_GROUP)

    @classmethod
    def create(cls, layout, name, pin_group, net, is_ref=False):
        """Create a pin group terminal.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the pin group terminal in.
        net : :class:`.Net` or :obj:`str` or None
            Net reference.
        name : :obj:`str`
            Name of the pin group terminal.
        pin_group : :class:`.PinGroup`
            Pin group.
        is_ref : :obj:`bool`, default: False
            Whether the pin group terminal is a reference terminal.

        Returns
        -------
        PinGroupTerminal
        """
        return PinGroupTerminal(
            cls.__stub.Create(
                messages.pin_group_term_creation_message(layout, net, name, pin_group, is_ref)
            )
        )

    @property
    def pin_group(self):
        """:class:`.PinGroup`: Pin group of the terminal."""
        from ansys.edb.core.hierarchy import pin_group

        return pin_group.PinGroup(self.__stub.GetPinGroup(self.msg))

    @pin_group.setter
    def pin_group(self, value):
        self.__stub.SetPinGroup(messages.pin_group_term_set_pin_group_message(self, value))

    @property
    def layer(self):
        """:class:`.Layer`: Layer."""
        return Layer(self.__stub.GetLayer(self.msg)).cast()

    @layer.setter
    def layer(self, value):
        self.__stub.SetLayer(messages.pin_group_term_set_layer_message(self, value))


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
        return [Edge(msg).cast() for msg in self.__stub.GetEdges(self.msg)]

    @edges.setter
    def edges(self, edges):
        self.__stub.GetEdges(messages.edge_term_set_edges_message(self, edges))
