"""S-Parameter Model."""
from ansys.edb.core.hierarchy.model import Model
from ansys.edb.core.inner.messages import (
    edb_obj_message,
    sparameter_model_message,
    string_property_message,
)
from ansys.edb.core.session import SParameterModelServiceStub, StubAccessor, StubType


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
        return cls(cls.__stub.Create(sparameter_model_message(name, ref_net)))

    @property
    def _properties(self):
        return self.__stub.GetProperties(edb_obj_message(self))

    @property
    def component_model(self):
        """:obj:`str`: Name of component model."""
        return self._properties.name

    @component_model.setter
    def component_model(self, name):
        self.__stub.SetComponentModelName(string_property_message(self, name))

    @property
    def reference_net(self):
        """:obj:`str`: Name of reference net."""
        return self._properties.ref_net

    @reference_net.setter
    def reference_net(self, name):
        self.__stub.SetReferenceNet(string_property_message(self, name))
