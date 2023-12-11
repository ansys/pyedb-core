"""Netlist Model."""
from ansys.edb.core.hierarchy.model import Model
from ansys.edb.core.inner import messages
from ansys.edb.core.session import NetlistModelServiceStub, StubAccessor, StubType


class NetlistModel(Model):
    """Class representing a Netlist model object."""

    __stub: NetlistModelServiceStub = StubAccessor(StubType.netlist_model)

    @classmethod
    def create(cls, name):
        """Create a new netlist model with a netlist name.

        Parameters
        ----------
        name : str

        Returns
        -------
        NetlistModel
        """
        return cls(cls.__stub.Create(messages.str_message(name)))

    @property
    def netlist(self):
        """:obj:`str`: Netlist name."""
        return self.__stub.GetNetlist(messages.edb_obj_message(self)).value

    @netlist.setter
    def netlist(self, name):
        self.__stub.SetNetlist(messages.string_property_message(self, name))
