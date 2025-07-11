"""Component pin Definition."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.definition.component_def import ComponentDef

from ansys.api.edb.v1.component_pin_pb2_grpc import ComponentPinServiceStub

from ansys.edb.core.definition import component_def
from ansys.edb.core.inner import ObjBase, messages
from ansys.edb.core.session import StubAccessor, StubType


class ComponentPin(ObjBase):
    """Represents a pin in a :class:`.ComponentDef`."""

    __stub: ComponentPinServiceStub = StubAccessor(StubType.component_pin)

    @classmethod
    def create(cls, comp_def: ComponentDef, name: str) -> ComponentPin:
        """Create a component pin in a given component definition.

        Parameters
        ----------
        comp_def : .ComponentDef
            Component definition to create the component pin in.
        name : str
            Name of the component pin.

        Returns
        -------
        .ComponentPin
        """
        return ComponentPin(cls.__stub.Create(messages.edb_obj_name_message(comp_def, name)))

    @classmethod
    def find(cls, comp_def: ComponentDef, name: str) -> ComponentPin:
        """Find a component pin in a given component definition.

        Parameters
        ----------
        comp_def : .ComponentDef
            Component definition to search for the component pin.
        name : str
            Name of the component pin.

        Returns
        -------
        .ComponentPin
            Component pin found. \
            If a component pin isn't found, the returned component pin is :meth:`null <.is_null>`.
        """
        return ComponentPin(cls.__stub.FindByName(messages.edb_obj_name_message(comp_def, name)))

    @property
    def name(self) -> str:
        """:obj:`str`: Name of the component pin."""
        return self.__stub.GetName(self.msg).value

    @name.setter
    def name(self, value: str):
        self.__stub.SetName(messages.string_property_message(self, value))

    @property
    def number(self) -> int:
        """:obj:`int`: Order number of the component pin inside its component definition.

        This property is read-only.
        """
        return self.__stub.GetNumber(self.msg).value

    @property
    def component_def(self) -> ComponentDef:
        """:class:`.ComponentDef`: Component definition that the component pin belongs to.

        This property is read-only.
        """
        return component_def.ComponentDef(self.__stub.GetComponentDef(self.msg))
