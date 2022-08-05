"""Component Group."""

from enum import Enum

from ansys.api.edb.v1.component_group_pb2_grpc import ComponentGroupServiceStub
import ansys.api.edb.v1.edb_defs_pb2 as edb_defs_pb2

from ansys.edb.core import messages
from ansys.edb.hierarchy.group import Group
from ansys.edb.session import StubAccessor, StubType


class ComponentType(Enum):
    """Enum representing component types."""

    OTHER = edb_defs_pb2.OTHER
    RESISTOR = edb_defs_pb2.RESISTOR
    INDUCTOR = edb_defs_pb2.INDUCTOR
    CAPACITOR = edb_defs_pb2.CAPACITOR
    IC = edb_defs_pb2.IC
    IO = edb_defs_pb2.IO
    INVALID = edb_defs_pb2.INVALID


class ComponentGroup(Group):
    """Class representing a Component group."""

    __stub: ComponentGroupServiceStub = StubAccessor(StubType.component_group)

    @classmethod
    def create_with_component(cls, layout, name, comp_name):
        """Create a component group with a component.

        Parameters
        ----------
        layout : Layout
        name : str
        comp_name : str

        Returns
        -------
        ComponentGroup
        """
        return ComponentGroup(
            cls.__stub.Create(messages.component_group_create_message(layout, name, comp_name))
        )

    @property
    def num_pins(self):
        """Get the number of pins in the component group.

        Returns
        -------
        int
        """
        return self.__stub.GetNumberOfPins(self.msg).value

    @property
    def component_property(self):
        """Component property of the component group.

        Returns
        -------
        ComponentProperty
        """
        return self.__stub.GetComponentProperty(self.msg)

    @component_property.setter
    def component_property(self, value):
        """Set the component property on the component group.

        Parameters
        ----------
        value : ComponentProperty
        """
        self.__stub.SetComponentProperty(messages.point_property_message(self, value))

    @property
    def component_type(self):
        """Component type of the component group.

        Returns
        -------
        ComponentType
        """
        return ComponentType(self.__stub.GetComponentType(self.msg).comp_type)

    @component_type.setter
    def component_type(self, value):
        """Set the component property on the component group.

        Parameters
        ----------
        value : ComponentType
        """
        self.__stub.SetComponentType(messages.set_component_group_type_message(self, value))

    @classmethod
    def find(cls, layout, comp_def_name):
        """Find all components by the given component definition name.

        Parameters
        ----------
        layout : Layout
        comp_def_name : str

        Returns
        -------
        list of ComponentGroups
        """
        objs = cls.__stub.FindByDef(
            messages.object_name_in_layout_message(layout, comp_def_name)
        ).items
        return [ComponentGroup(cg) for cg in objs]
