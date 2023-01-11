"""S-Parameter Model."""
from ansys.edb.core import messages
from ansys.edb.hierarchy.model import Model
from ansys.edb.session import SParameterModelServiceStub, StubAccessor, StubType


class SParameterModel(Model):
    """Class representing a S-Parameter model object."""

    __stub: SParameterModelServiceStub = StubAccessor(StubType.sparameter_model)

    @classmethod
    def create(cls, name, ref_net):
        """Create a new SParameter Model.

        Parameters
        ----------
        name : str
            Name of component model.
        ref_net : str
            Name of reference net.
        """
        return cls(cls.__stub.Create(messages.sparameter_model_message(name, ref_net)))

    @property
    def _properties(self):
        return self.__stub.GetProperties(messages.edb_obj_message(self))

    @property
    def component_model(self):
        """:obj:`str`: Name of component model."""
        return self._properties.name

    @component_model.setter
    def component_model(self, name):
        self.__stub.SetComponentModelName(messages.string_property_message(self, name))

    @property
    def refrence_net(self):
        """:obj:`str`: Name of referencec net."""
        return self._properties.ref_net

    @refrence_net.setter
    def refrence_net(self, name):
        self.__stub.SetReferenceNet(messages.string_property_message(self, name))
