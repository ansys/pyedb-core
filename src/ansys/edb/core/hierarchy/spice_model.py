"""SPICE Model."""
from ansys.edb.core.hierarchy.model import Model
from ansys.edb.core.inner import messages
from ansys.edb.core.session import SpiceModelServiceStub, StubAccessor, StubType


class SPICEModel(Model):
    """Represents a SPICE model object."""

    __stub: SpiceModelServiceStub = StubAccessor(StubType.spice_model)

    @classmethod
    def create(cls, name, path, sub_circuit):
        """Create a SPICE model.

        Parameters
        ----------
        name : str
            Name of the SPICE model file.
        path : str
            Path to the SPICE model file.
        sub_circuit : str
            Subcircuit name of the SPICE model.
        """
        return cls(cls.__stub.Create(messages.spice_model_message(name, path, sub_circuit)))

    @property
    def _properties(self):
        return self.__stub.GetProperties(messages.edb_obj_message(self))

    @property
    def model_name(self):
        """:obj:`str`: Name of the SPICE model file."""
        return self._properties.name

    @model_name.setter
    def model_name(self, name):
        self.__stub.SetModelName(messages.string_property_message(self, name))

    @property
    def model_path(self):
        """:obj:`str`: Path to the SPICE model file."""
        return self._properties.path

    @model_path.setter
    def model_path(self, path):
        self.__stub.SetModelPath(messages.string_property_message(self, path))

    @property
    def sub_circuit(self):
        """:obj:`str`: Name of the subcircuit in the SPICE model."""
        return self._properties.sub_ckt

    @sub_circuit.setter
    def sub_circuit(self, name):
        self.__stub.SetSubCkt(messages.string_property_message(self, name))

    def add_terminal(self, terminal, pin):
        """Add a terminal with a pin number.

        Parameters
        ----------
        terminal : str
            Terminal name to associate with the pin.
        pin : str
            Pin number.
        """
        self.__stub.AddTerminalPinPair(
            messages.spice_model_net_terminal_pin_message(self, terminal, pin)
        )

    def remove_terminal(self, terminal):
        """Remove a terminal.

        Parameters
        ----------
        terminal : str
            Terminal name.
        """
        self.__stub.RemoveTerminalPinPair(messages.string_property_message(self, terminal))
