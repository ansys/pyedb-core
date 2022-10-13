"""Component Group."""

from enum import Enum

from ansys.api.edb.v1.component_group_pb2_grpc import ComponentGroupServiceStub
import ansys.api.edb.v1.edb_defs_pb2 as edb_defs_pb2

from ansys.edb.core import messages
from ansys.edb.hierarchy.group import Group
from ansys.edb.session import StubAccessor, StubType


class ComponentType(Enum):
    """Enum representing component types.

    - OTHER
    - RESISTOR
    - INDUCTOR
    - CAPACITOR
    - IC
    - IO
    - INVALID
    """

    OTHER = edb_defs_pb2.OTHER
    RESISTOR = edb_defs_pb2.RESISTOR
    INDUCTOR = edb_defs_pb2.INDUCTOR
    CAPACITOR = edb_defs_pb2.CAPACITOR
    IC = edb_defs_pb2.IC
    IO = edb_defs_pb2.IO
    INVALID = edb_defs_pb2.INVALID


class ComponentGroup(Group):
    """Class representing a component group object."""

    __stub: ComponentGroupServiceStub = StubAccessor(StubType.component_group)

    @classmethod
    def create_with_component(cls, layout, name, comp_name):
        """Create a component group with a component.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.layout.Layout>`
            Layout that owns the component group.
        name : str
            Name of the component group to be created.
        comp_name : str
            Name of the :class:`ComponentDef <ansys.edb.definition.ComponentDef>` the component group \
            refers to.

        Returns
        -------
        ComponentGroup
            Newly created component group.
        """
        return ComponentGroup(
            cls.__stub.Create(messages.component_group_create_message(layout, name, comp_name))
        )

    @property
    def num_pins(self):
        """:obj:`int`: Number of pins in the component group.

        Read-Only.
        """
        return self.__stub.GetNumberOfPins(self.msg).value

    @property
    def component_property(self):
        """:obj:`ComponentProperty`: Component property of the component group."""
        return self.__stub.GetComponentProperty(self.msg)

    @component_property.setter
    def component_property(self, value):
        """Set the component property on the component group."""
        self.__stub.SetComponentProperty(messages.point_property_message(self, value))

    @property
    def component_type(self):
        """:obj:`ComponentType`: Component type of the component group."""
        return ComponentType(self.__stub.GetComponentType(self.msg).comp_type)

    @component_type.setter
    def component_type(self, value):
        """Set the component type on the component group."""
        self.__stub.SetComponentType(messages.set_component_group_type_message(self, value))

    @classmethod
    def find(cls, layout, comp_def_name):
        """Find all the components belonging to a specific component definition.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.layout.Layout>`
            Layout to search the component group(s) in.
        comp_def_name : str
            Name of the :class:`ComponentDef <ansys.edb.definition.ComponentDef>`.

        Returns
        -------
        list[ComponentGroup]
            List of component group(s) that are found.
        """
        objs = cls.__stub.FindByDef(
            messages.object_name_in_layout_message(layout, comp_def_name)
        ).items
        return [ComponentGroup(cg) for cg in objs]
