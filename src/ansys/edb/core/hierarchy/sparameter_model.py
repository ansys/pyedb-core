"""S-parameter model."""
from ansys.edb.core.hierarchy.model import Model
from ansys.edb.core.inner import messages
from ansys.edb.core.session import SParameterModelServiceStub, StubAccessor, StubType


class SParameterModel(Model):
    """Represents an S-parameter model object."""

    __stub: SParameterModelServiceStub = StubAccessor(StubType.sparameter_model)

    @classmethod
    def create(cls, name, ref_net):
        """Create an S-parameter model.

        Parameters
        ----------
        name : str
            Name of the S-parameter model.
        ref_net : str
            Name of the reference net.
        """
        return cls(cls.__stub.Create(messages.sparameter_model_message(name, ref_net)))

    @property
    def _properties(self):
        return self.__stub.GetProperties(messages.edb_obj_message(self))

    @property
    def component_model(self):
        """:obj:`str`: Name of the component model."""
        return self._properties.name

    @component_model.setter
    def component_model(self, name):
        self.__stub.SetComponentModelName(messages.string_property_message(self, name))

    @property
    def reference_net(self):
        """:obj:`str`: Name of the reference net."""
        return self._properties.ref_net

    @reference_net.setter
    def reference_net(self, name):
        self.__stub.SetReferenceNet(messages.string_property_message(self, name))
