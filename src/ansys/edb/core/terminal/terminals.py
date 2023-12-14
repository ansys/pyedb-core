"""Terminals."""

from enum import Enum

import ansys.api.edb.v1.edge_term_pb2 as edge_term_pb2
import ansys.api.edb.v1.term_pb2 as term_pb2

from ansys.edb.core import hierarchy, primitive
from ansys.edb.core.edb_defs import LayoutObjType
from ansys.edb.core.geometry.arc_data import ArcData
from ansys.edb.core.inner.base import ObjBase, TypeField
from ansys.edb.core.inner.conn_obj import ConnObj
from ansys.edb.core.inner.messages import (
    edb_obj_collection_message,
    edge_creation_message,
    edge_term_creation_message,
    edge_term_set_edges_message,
    padstack_inst_term_creation_message,
    padstack_inst_term_set_params_message,
    pin_group_term_creation_message,
    pin_group_term_set_layer_message,
    pin_group_term_set_pin_group_message,
    point_term_creation_message,
    point_term_set_params_message,
    term_find_by_name_message,
    term_get_product_solver_message,
    term_inst_creation_message,
    term_inst_term_creation_message,
    term_inst_term_set_instance_message,
    term_set_params_message,
    term_set_solver_option_message,
)
from ansys.edb.core.inner.parser import to_rlc
from ansys.edb.core.layer.layer import Layer
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.port_post_processing_prop import PortPostProcessingProp
from ansys.edb.core.utility.value import Value


class TerminalType(Enum):
    """Enum class representing terminal types."""

    EDGE = term_pb2.EDGE_TERM
    POINT = term_pb2.POINT_TERM
    TERM_INST = term_pb2.TERM_INST_TERM
    PADSTACK_INST = term_pb2.PADSTACK_INST_TERM
    BUNDLE = term_pb2.BUNDLE_TERM
    PIN_GROUP = term_pb2.PIN_GROUP_TERM


class BoundaryType(Enum):
    """Enum class representing terminal boundary types."""

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
    """Enum class representing source terminal to ground types."""

    NO_GROUND = term_pb2.NO_GROUND
    NEGATIVE = term_pb2.NEGATIVE
    POSITIVE = term_pb2.POSITIVE


class HfssPIType(Enum):
    """Enum class representing HFSS PI types."""

    DEFAULT = term_pb2.PI_DEFAULT
    COAXIAL_OPEN = term_pb2.PI_COAXIAL_OPEN
    COAXIAL_SHORTENED = term_pb2.PI_COAXIAL_SHORTENED
    GAP = term_pb2.PI_GAP
    LUMPED = term_pb2.PI_LUMPED


class EdgeType(Enum):
    """Enum class representing edge types."""

    PRIMITIVE = edge_term_pb2.PRIMITIVE_EDGE
    PADSTACK = edge_term_pb2.PAD_EDGE


class Edge(ObjBase):
    """Class representing an edge."""

    __stub = StubAccessor(StubType.edge)
    type = TypeField(None)

    def cast(self):
        """Cast the base Edge object to correct subclass, if possible.

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
        return cls.__stub.Create(edge_creation_message(cls.type.value, **params))

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
    """Class representing a padstack edge."""

    type = TypeField(EdgeType.PADSTACK)

    @classmethod
    def create(cls, padstack_instance, layer, arc):
        """Create a PadEdge.

        Parameters
        ----------
        padstack_instance : PadstackInstance
        layer : Layer or str
        arc : ArcData

        Returns
        -------
        PadEdge
        """
        return PadEdge(cls._create(padstack_instance=padstack_instance, layer=layer, arc=arc))

    @property
    def padstack_instance(self):
        """Return the padstack instance this edge is on.

        Returns
        -------
        PadstackInstance
        """
        return primitive.PadstackInstance(self._params.padstack_instance)

    @property
    def layer(self):
        """Return the layer this edge is on.

        Returns
        -------
        Layer
        """
        return Layer(self._params.layer.id).cast()

    @property
    def arc(self):
        """Return the arc of this edge.

        Returns
        -------
        ArcData
        """
        return ArcData(self._params.arc)


class PrimitiveEdge(Edge):
    """Class representing a primitive edge."""

    type = TypeField(EdgeType.PRIMITIVE)

    @classmethod
    def create(cls, prim, point):
        """Create a primitive edge.

        Parameters
        ----------
        prim : Primitive
        point : (float, float)

        Returns
        -------
        PrimitiveEdge
        """
        return PrimitiveEdge(cls._create(primitive=prim, point=point))

    @property
    def primitive(self):
        """Return primitive of this terminal.

        Returns
        -------
        Primitive
        """
        return primitive.Primitive(self._params.primitive).cast()

    @property
    def point(self):
        """Return the x, y coordinates of this terminal.

        Returns
        -------
        (Value, Value)
        """
        return self._params.point


class Terminal(ConnObj):
    """Class representing a terminal object."""

    __stub = StubAccessor(StubType.terminal)
    type = TypeField(None)
    layout_obj_type = LayoutObjType.TERMINAL

    def cast(self, term_type=None):
        """Cast the terminal object to correct concrete type. Fetch the type if necessary.

        Parameters
        term_type : TerminalType
        ----------
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
        """Find a terminal by name.

        Parameters
        ----------
        layout : Layout
        name : str

        Returns
        -------
        Terminal
        """
        return Terminal(cls.__stub.FindByName(term_find_by_name_message(layout, name))).cast(
            cls.type
        )

    @property
    def _params(self):
        return self.__stub.GetParams(self.msg)

    @_params.setter
    def _params(self, values):
        self.__stub.SetParams(term_set_params_message(self, **values))

    @property
    def _type(self):
        """Return the terminal type."""
        return TerminalType(self._params.term_type)

    @property
    def bundle_terminal(self):
        """Return a bundle terminal this terminal belongs to, if any.

        Returns
        -------
        BundleTerminal
        """
        return BundleTerminal(self._params.bundle_term)

    @property
    def reference_terminal(self):
        """Return a terminal this terminal references, if any.

        Returns
        -------
        Terminal
        """
        return Terminal(self._params.ref_term).cast()

    @reference_terminal.setter
    def reference_terminal(self, value):
        """Set a terminal this terminal references.

        Parameters
        ----------
        value : Terminal
        """
        self._params = {"ref_term": value}

    @property
    def reference_layer(self):
        """Return a layer this terminal references, if any.

        Returns
        -------
        Layer
        """
        return Layer(self._params.ref_layer).cast()

    @reference_layer.setter
    def reference_layer(self, value):
        """Set a layer this terminal references by Layer object or by layer name.

        Parameters
        ----------
        value : Layer or str
        """
        self._params = {"ref_layer": value}

    @property
    def is_interface_terminal(self):
        """Return whether this terminal is an interface.

        Returns
        -------
        bool
        """
        return self._params.is_interface

    @property
    def is_reference_terminal(self):
        """Return whether this terminal is a reference terminal.

        Returns
        -------
        bool
        """
        return self._params.is_reference

    @property
    def use_reference_from_hierarchy(self):
        """Return whether this terminal can use references from hierarchy.

        Returns
        -------
        bool
        """
        return self._params.use_ref_from_hierarchy

    @use_reference_from_hierarchy.setter
    def use_reference_from_hierarchy(self, value):
        """Set whether this terminal can use references from hierarchy.

        Parameters
        ----------
        value : bool
        """
        self._params = {"use_ref_from_hierarchy": value}

    @property
    def is_auto_port(self):
        """Return whether this terminal is an auto port.

        Returns
        -------
        bool
        """
        return self._params.is_auto_port

    @is_auto_port.setter
    def is_auto_port(self, value):
        """Set whether this terminal is an auto port.

        Parameters
        ----------
        value : bool
        """
        self._params = {"is_auto_port": value}

    @property
    def is_circuit_port(self):
        """Return whether this terminal is a circuit port.

        Returns
        -------
        bool
        """
        return self._params.is_circuit_port

    @is_circuit_port.setter
    def is_circuit_port(self, value):
        """Set whether this terminal is a circuit port.

        Parameters
        ----------
        value : bool
        """
        self._params = {"is_circuit_port": value}

    @property
    def name(self):
        """Return the name of this terminal.

        Returns
        -------
        str
        """
        return self._params.name

    @name.setter
    def name(self, value):
        """Set the name of this terminal.

        Parameters
        ----------
        value : str
        """
        self._params = {"name": value}

    @property
    def boundary_type(self):
        """Return the boundary type of this terminal.

        Returns
        -------
        BoundaryType
        """
        return BoundaryType(self._params.boundary_type)

    @boundary_type.setter
    def boundary_type(self, value):
        """Set the boundary type of this terminal.

        Parameters
        ----------
        value : BoundaryType
        """
        self._params = {"boundary_type": value.value}

    @property
    def impedance(self):
        """Return the impedance of this terminal.

        Returns
        -------
        Value
        """
        return Value(self._params.impedance)

    @impedance.setter
    def impedance(self, value):
        """Set the impedance of this terminal.

        Parameters
        ----------
        value : Value
        """
        self._params = {"impedance": value}

    @property
    def source_amplitude(self):
        """Return the source amplitude of this terminal.

        Returns
        -------
        Value
        """
        return Value(self._params.source_amplitude)

    @source_amplitude.setter
    def source_amplitude(self, value):
        """Set the source amplitude of this terminal.

        Parameters
        ----------
        value : Value
        """
        self._params = {"source_amplitude": value}

    @property
    def source_phase(self):
        """Return the source phase of this terminal.

        Returns
        -------
        Value
        """
        return Value(self._params.source_phase)

    @source_phase.setter
    def source_phase(self, value):
        """Set the source phase of this terminal.

        Parameters
        ----------
        value : Value
        """
        self._params = {"source_phase": value}

    @property
    def term_to_ground(self):
        """Return source term to ground type.

        Returns
        -------
        SourceTermToGroundType
        """
        return SourceTermToGroundType(self._params.term_to_ground)

    @term_to_ground.setter
    def term_to_ground(self, value):
        """Set the source term to ground type.

        Parameters
        ----------
        value : SourceTermToGroundType
        """
        self._params = {"term_to_ground": value.value}

    @property
    def hfss_pi_type(self):
        """Return the HFSS PI type.

        Returns
        -------
        HfssPIType
        """
        return HfssPIType(self._params.hfss_pi_type)

    @hfss_pi_type.setter
    def hfss_pi_type(self, value):
        """Set the HFSS PI type.

        Parameters
        ----------
        value : HfssPIType
        """
        self._params = {"hfss_pi_type": value.value}

    @property
    def model(self):
        """Return the S-parameter model.

        Returns
        -------
        str
        """
        return self._params.s_param_model

    @model.setter
    def model(self, value):
        """Set the S-parameter model.

        Parameters
        ----------
        value : str
        """
        self._params = {"s_param_model": value}

    @property
    @to_rlc
    def rlc_boundary_parameters(self):
        """Return the RLC boundary parameters.

        Returns
        -------
        Rlc
        """
        return self._params.rlc

    @rlc_boundary_parameters.setter
    def rlc_boundary_parameters(self, value):
        """Set the RLC boundary parameters.

        Parameters
        ----------
        value : Rlc
        """
        self._params = {"rlc": value}

    @property
    def port_post_processing_prop(self):
        """Return the port post processing props.

        Returns
        -------
        PortPostProcessingProp
        """
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
        """Set the port post processing props.

        Parameters
        ----------
        value : PortPostProcessingProp
        """
        self._params = {"port_post_processing_prop": value}

    def _product_solvers(self, product_id):
        return self.__stub.GetProductSolvers(term_get_product_solver_message(self, product_id))

    def product_solver_option(self, product_id, solver_name):
        """Return product solver option name.

        Parameters
        ----------
        product_id : ProductIdType
        solver_name : str

        Returns
        -------
        str
        """
        return next(
            solver.option
            for solver in self._product_solvers(product_id)
            if solver.name == solver_name
        )

    def set_product_solver_option(self, product_id, solver_name, option):
        """Set product solver option name.

        Parameters
        ----------
        product_id : ProductIdType
        solver_name : str
        option : str
        """
        self.__stub.SetProductSolverOptions(
            term_set_solver_option_message(self, product_id, solver_name, option)
        )

    def product_solver_names(self, product_id):
        """Return the list of solver names.

        Parameters
        ----------
        product_id : ProductIdType
        """
        return [solver.name for solver in self._product_solvers(product_id)]


class TerminalInstance(ConnObj):
    """Class representing a terminal instance."""

    __stub = StubAccessor(StubType.terminal_instance)
    layout_obj_type = LayoutObjType.TERMINAL_INSTANCE

    @classmethod
    def create(cls, layout, cell_instance, name, net_ref):
        """Create a terminal instance object.

        Parameters
        ----------
        layout : Layout
        cell_instance : CellInstance
        name : str
        net_ref : Net or str or None

        Returns
        -------
        TerminalInstance
        """
        return TerminalInstance(
            cls.__stub.Create(term_inst_creation_message(layout, net_ref, cell_instance, name))
        )

    @property
    def owning_cell_instance(self):
        """Return an cell instance that owns this terminal.

        Returns
        -------
        CellInstance
        """
        return hierarchy.CellInstance(self.__stub.GetOwningCellInstance(self.msg))

    @property
    def definition_terminal(self):
        """Return a definition terminal, if any.

        Returns
        -------
        Terminal
        """
        return Terminal(self.__stub.GetDefinitionTerminal(self.msg)).cast()

    @property
    def definition_terminal_name(self):
        """Return a name of definition terminal.

        Returns
        -------
        str
        """
        return self.__stub.GetDefinitionTerminalName(self.msg).value


class TerminalInstanceTerminal(Terminal):
    """Class representing a terminal instance terminal."""

    __stub = StubAccessor(StubType.terminal_instance_terminal)
    type = TypeField(TerminalType.TERM_INST)

    @classmethod
    def create(cls, layout, term_instance, name, net_ref, is_ref=False):
        """Create a terminal instance terminal.

        Parameters
        ----------
        layout : Layout
        term_instance : TerminalInstance
        name
        net_ref : Net or str or None
        is_ref : bool, optional

        Returns
        -------
        TerminalInstanceTerminal
        """
        return TerminalInstanceTerminal(
            cls.__stub.Create(
                term_inst_term_creation_message(layout, net_ref, name, term_instance, is_ref)
            )
        )

    @property
    def terminal_instance(self):
        """Return the terminal instance.

        Returns
        -------
        TerminalInstance
        """
        return TerminalInstance(self.__stub.GetTerminalInstance(self.msg))

    @terminal_instance.setter
    def terminal_instance(self, value):
        """Set the terminal instance.

        Parameters
        ----------
        value : TerminalInstance
        """
        self.__stub.SetTerminalInstance(term_inst_term_set_instance_message(self, value))


class BundleTerminal(Terminal):
    """Class representing a bundle terminal object."""

    __stub = StubAccessor(StubType.bundle_terminal)
    type = TypeField(TerminalType.BUNDLE)

    @classmethod
    def create(cls, terminals):
        """
        Create a bundle terminal.

        Parameters
        ----------
        terminals : list of Terminal

        Returns
        -------
        BundleTerminal
        """
        return BundleTerminal(cls.__stub.Create(edb_obj_collection_message(terminals)))

    @property
    def terminals(self):
        """Get list of terminals grouped in this terminal.

        Returns
        -------
        list of Terminal
        """
        return [Terminal(msg).cast() for msg in self.__stub.GetTerminals(self.msg)]

    def ungroup(self):
        """Delete this grouping."""
        self.__stub.Ungroup(self.msg)
        self.msg = None


class PointTerminal(Terminal):
    """Class representing a point terminal object."""

    __stub = StubAccessor(StubType.point_terminal)
    type = TypeField(TerminalType.POINT)

    @classmethod
    def create(cls, layout, net, layer, name, point):
        """
        Create a point terminal.

        Parameters
        ----------
        layout : Layout
        net : str or Net or None
        layer : str or Layer
        name : str
        point : PointLike

        Returns
        -------
        PointTerminal
        """
        return PointTerminal(
            cls.__stub.Create(point_term_creation_message(layout, net, layer, name, point))
        )

    @property
    def params(self):
        """Get x, y coordinates and the layer this point terminal is placed on.

        Returns
        -------
        (Layer, (Value, Value))
        """
        res = self.__stub.GetParameters(self.msg)
        point = (
            Value(res.point.x),
            Value(res.point.y),
        )
        layer = Layer(res.layer.id).cast()
        return layer, point

    @property
    def layer(self):
        """Get the layer the point terminal is placed on.

        Returns
        -------
        Layer
        """
        return self.params[0]

    @property
    def point(self):
        """Get the x, y coordinates of the point terminal.

        Returns
        -------
        (Value, Value)
        """
        return self.params[1]

    @params.setter
    def params(self, params):
        """Set x, y coordinates and the layer this point terminal is placed on.

        Parameters
        ----------
        params : tuple[str or Layer, PointData]
        """
        self.__stub.SetParameters(point_term_set_params_message(self, *params))


class PadstackInstanceTerminal(Terminal):
    """Class representing Padstack Instance Terminal."""

    __stub = StubAccessor(StubType.padstack_instance_terminal)
    type = TypeField(TerminalType.PADSTACK_INST)

    @classmethod
    def create(cls, layout, name, padstack_instance, layer, net, is_ref=False):
        """Create a padstack instance terminal.

        Parameters
        ----------
        layout : Layout
        name : str
        padstack_instance : PadstackInstance
        layer : Layer or str
        net : Net or str or None
        is_ref : bool, optional

        Returns
        -------
        PadstackInstanceTerminal
        """
        return PadstackInstanceTerminal(
            cls.__stub.Create(
                padstack_inst_term_creation_message(
                    layout, name, padstack_instance, layer, net, is_ref
                )
            )
        )

    @property
    def params(self):
        """Return padstack instance and layer.

        Returns
        -------
        (PadstackInstance, Layer)
        """
        res = self.__stub.GetParameters(self.msg)
        padstack_instance = primitive.PadstackInstance(res.padstack_instance)
        layer = Layer(res.layer).cast()
        return padstack_instance, layer

    @params.setter
    def params(self, params):
        """Set padstack instance and layer for this terminal.

        Parameters
        ----------
        params : (PadstackInstance, Layer)
        """
        (padstack_instance, layer) = params
        self.__stub.SetParameters(
            padstack_inst_term_set_params_message(self, padstack_instance, layer)
        )

    @property
    def padstack_instance(self):
        """Return the padstack instance of this terminal.

        Returns
        -------
        PadstackInstance
        """
        return self.params[0]

    @property
    def layer(self):
        """Return the layer this terminal is on.

        Returns
        -------
        Layer
        """
        return self.params[1]


class PinGroupTerminal(Terminal):
    """Class representing a pin group terminal."""

    __stub = StubAccessor(StubType.pin_group_terminal)
    type = TypeField(TerminalType.PIN_GROUP)

    @classmethod
    def create(cls, layout, name, pin_group, net_ref, is_ref=False):
        """Create a pin group terminal.

        Parameters
        ----------
        layout : Layout
        net_ref : Net or str or None
        name : str
        pin_group : PinGroup
        is_ref : bool, optional

        Returns
        -------
        PinGroupTerminal
        """
        return PinGroupTerminal(
            cls.__stub.Create(
                pin_group_term_creation_message(layout, net_ref, name, pin_group, is_ref)
            )
        )

    @property
    def pin_group(self):
        """Return the pin group of this terminal.

        Returns
        -------
        PinGroup
        """
        return hierarchy.PinGroup(self.__stub.GetPinGroup(self.msg))

    @pin_group.setter
    def pin_group(self, value):
        """Set the pin group of this terminal.

        Parameters
        ----------
        value : PinGroup
        """
        self.__stub.SetPinGroup(pin_group_term_set_pin_group_message(self, value))

    @property
    def layer(self):
        """Return the layer.

        Returns
        -------
        Layer
        """
        return Layer(self.__stub.GetLayer(self.msg)).cast()

    @layer.setter
    def layer(self, value):
        """Set the layer.

        Parameters
        ----------
        value : Layer
        """
        self.__stub.SetLayer(pin_group_term_set_layer_message(self, value))


class EdgeTerminal(Terminal):
    """Class representing Edge Terminal."""

    __stub = StubAccessor(StubType.edge_terminal)
    type = TypeField(TerminalType.EDGE)

    @classmethod
    def create(cls, layout, name, edges, net_ref=None, is_ref=False):
        """Create an edge terminal.

        Parameters
        ----------
        layout : Layout
        name : str
        edges : list of Edge
        net_ref : Net or str or None
        is_ref : bool, optional

        Returns
        -------
        EdgeTerminal
        """
        return EdgeTerminal(
            cls.__stub.Create(edge_term_creation_message(layout, net_ref, name, edges, is_ref))
        )

    @property
    def edges(self):
        """Return the edges on this terminal.

        Returns
        -------
        list of Edge
        """
        return [Edge(msg).cast() for msg in self.__stub.GetEdges(self.msg)]

    @edges.setter
    def edges(self, edges):
        """Set the edges on this terminal.

        Parameters
        ----------
        edges : list of Edge
        """
        self.__stub.GetEdges(edge_term_set_edges_message(self, edges))
