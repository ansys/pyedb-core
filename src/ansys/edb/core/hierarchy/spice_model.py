"""SPICE Model."""
from ansys.edb.core.hierarchy.model import Model
from ansys.edb.core.inner.messages import (
    edb_obj_message,
    spice_model_message,
    spice_model_net_terminal_pin_message,
    string_property_message,
)
from ansys.edb.core.session import SpiceModelServiceStub, StubAccessor, StubType


class SPICEModel(Model):
    """Class representing a SPICE model object."""

    __stub: SpiceModelServiceStub = StubAccessor(StubType.spice_model)

    @classmethod
    def create(cls, name, path, sub_circuit):
        """Create a new SPICE model.

        Parameters
        ----------
        name : str
            SPICE model file name.
        path : str
            SPICE model file path.
        sub_circuit : str
            Sub circuit name of SPICE model.
        """
        return cls(cls.__stub.Create(spice_model_message(name, path, sub_circuit)))

    @property
    def _properties(self):
        return self.__stub.GetProperties(edb_obj_message(self))

    @property
    def model_name(self):
        """:obj:`str`: Name of SPICE model file."""
        return self._properties.name

    @model_name.setter
    def model_name(self, name):
        self.__stub.SetModelName(string_property_message(self, name))

    @property
    def model_path(self):
        """:obj:`str`: File path of SPICE model."""
        return self._properties.path

    @model_path.setter
    def model_path(self, path):
        self.__stub.SetModelPath(string_property_message(self, path))

    @property
    def sub_circuit(self):
        """:obj:`str`: The name of the sub circuit in the SPICE model."""
        return self._properties.sub_ckt

    @sub_circuit.setter
    def sub_circuit(self, name):
        self.__stub.SetSubCkt(string_property_message(self, name))

    def add_terminal(self, terminal, pin):
        """Add a terminal with pin number.

        Parameters
        ----------
        terminal : str
            The terminal name to associate with the pin.
        pin : str
            The pin number.
        """
        self.__stub.AddTerminalPinPair(spice_model_net_terminal_pin_message(self, terminal, pin))

    def remove_terminal(self, terminal):
        """Remove a terminal with pin number.

        Parameters
        ----------
        terminal : str
            The terminal name.
        """
        self.__stub.RemoveTerminalPinPair(string_property_message(self, terminal))
