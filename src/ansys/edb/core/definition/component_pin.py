"""Component pin Definition."""
from ansys.api.edb.v1.component_pin_pb2_grpc import ComponentPinServiceStub

from ansys.edb.core.definition import component_def
from ansys.edb.core.inner import ObjBase, messages
from ansys.edb.core.session import StubAccessor, StubType


class ComponentPin(ObjBase):
    """Represents a component pin."""

    __stub: ComponentPinServiceStub = StubAccessor(StubType.component_pin)

    @classmethod
    def create(cls, comp_def, name):
        """Create a component pin in a given component definition.

        Parameters
        ----------
        comp_def : :class:`.ComponentDef`
            Component definition to create the component pin in.
        name : str
            Name of the component pin.

        Returns
        -------
        ComponentPin
            Component pin created.
        """
        return ComponentPin(cls.__stub.Create(messages.edb_obj_name_message(comp_def, name)))

    @classmethod
    def find(cls, comp_def, name):
        """Find a component pin in a given component definition.

        Parameters
        ----------
        comp_def : :class:`.ComponentDef`
            Component definition to search for the component pin.
        name : str
            Name of the component pin.

        Returns
        -------
        ComponentPin
            Component pin found, ``None`` otherwise.
        """
        return ComponentPin(cls.__stub.FindByName(messages.edb_obj_name_message(comp_def, name)))

    @property
    def name(self):
        """:obj:`str`: Name of the component pin."""
        return self.__stub.GetName(self.msg).value

    @name.setter
    def name(self, value):
        self.__stub.SetName(messages.string_property_message(self, value))

    @property
    def number(self):
        """:obj:`int`: Serial number of the component pin inside its component definition.

        This property is read-only.
        """
        return self.__stub.GetNumber(self.msg).value

    @property
    def component_def(self):
        """:class:`.ComponentDef`: Component definition that the component pin belongs to.

        This property is read-only.
        """
        return component_def.ComponentDef(self.__stub.GetComponentDef(self.msg))
