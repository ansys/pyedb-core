"""Terminals."""

from enum import Enum

import ansys.api.edb.v1.term_pb2 as term_pb2

from ansys.edb.core.edb_defs import LayoutObjType
from ansys.edb.core.inner import TypeField, conn_obj, factory, messages, parser
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
        return factory.create_terminal(self.msg, tt)

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
        return factory.create_terminal(self._params.bundle_term, TerminalType.BUNDLE)

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
