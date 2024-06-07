"""Component group."""

from enum import Enum

from ansys.api.edb.v1.component_group_pb2_grpc import ComponentGroupServiceStub
import ansys.api.edb.v1.edb_defs_pb2 as edb_defs_pb2

from ansys.edb.core.definition import component_property
from ansys.edb.core.hierarchy.group import Group
from ansys.edb.core.inner import messages
from ansys.edb.core.session import StubAccessor, StubType


class ComponentType(Enum):
    """Provides an enum representing component types."""

    OTHER = edb_defs_pb2.OTHER
    RESISTOR = edb_defs_pb2.RESISTOR
    INDUCTOR = edb_defs_pb2.INDUCTOR
    CAPACITOR = edb_defs_pb2.CAPACITOR
    IC = edb_defs_pb2.IC
    IO = edb_defs_pb2.IO
    INVALID = edb_defs_pb2.INVALID


class ComponentGroup(Group):
    """Represents a component group object."""

    __stub: ComponentGroupServiceStub = StubAccessor(StubType.component_group)

    @classmethod
    def create_with_component(cls, layout, name, comp_name):
        """Create a component group with a component.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the component group in.
        name : str
            Name of the component group.
        comp_name : str
            Name of the :class:`.ComponentDef` instance that \
            the component group refers to.

        Returns
        -------
        ComponentGroup
            Component group created.
        """
        return ComponentGroup(
            cls.__stub.Create(messages.component_group_create_message(layout, name, comp_name))
        )

    @property
    def num_pins(self):
        """:obj:`int`: Number of pins in the component group.

        This property is read-only.
        """
        return self.__stub.GetNumberOfPins(self.msg).value

    @property
    def component_property(self):
        """:obj:`ComponentProperty`: Component property of the component group.

        A copy is returned. Use the setter for any modifications to be reflected.
        """
        from ansys.edb.core.definition.ic_component_property import ICComponentProperty
        from ansys.edb.core.definition.io_component_property import IOComponentProperty
        from ansys.edb.core.definition.rlc_component_property import RLCComponentProperty

        comp_prop = component_property.ComponentProperty(self.__stub.GetComponentProperty(self.msg))
        comp_type = self.__stub.GetComponentType(self.msg).comp_type
        if (
            comp_type == edb_defs_pb2.ComponentType.RESISTOR
            or comp_type == edb_defs_pb2.ComponentType.INDUCTOR
            or comp_type == edb_defs_pb2.ComponentType.CAPACITOR
        ):
            return RLCComponentProperty(comp_prop.msg)
        if comp_type == edb_defs_pb2.ComponentType.IO:
            return IOComponentProperty(comp_prop.msg)
        if comp_type == edb_defs_pb2.ComponentType.IC:
            return ICComponentProperty(comp_prop.msg)
        if comp_type == edb_defs_pb2.ComponentType.OTHER:
            return comp_prop
        else:
            return None

    @component_property.setter
    def component_property(self, value):
        """Component property on the component group."""
        self.__stub.SetComponentProperty(messages.pointer_property_message(self, value))

    @property
    def component_type(self):
        """:obj:`ComponentType`: Component type of the component group."""
        return ComponentType(self.__stub.GetComponentType(self.msg).comp_type)

    @component_type.setter
    def component_type(self, value):
        """Component type on the component group."""
        self.__stub.SetComponentType(messages.set_component_group_type_message(self, value))

    @classmethod
    def find_by_def(cls, layout, comp_def_name):
        """Find all components belonging to a given component definition.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to search for component groups.
        comp_def_name : str
            Name of the :class:`.ComponentDef` instance.

        Returns
        -------
        list[ComponentGroup]
            List of component groups that are found.
        """
        objs = cls.__stub.FindByDef(
            messages.object_name_in_layout_message(layout, comp_def_name)
        ).items
        return [ComponentGroup(cg) for cg in objs]
