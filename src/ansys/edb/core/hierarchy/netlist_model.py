"""Netlist Model."""
from ansys.edb.core.hierarchy.model import Model
from ansys.edb.core.inner.messages import edb_obj_message, str_message, string_property_message
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
        return cls(cls.__stub.Create(str_message(name)))

    @property
    def netlist(self):
        """:obj:`str`: Netlist name."""
        return self.__stub.GetNetlist(edb_obj_message(self)).value

    @netlist.setter
    def netlist(self, name):
        self.__stub.SetNetlist(string_property_message(self, name))
