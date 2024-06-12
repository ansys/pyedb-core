"""Group."""

from ansys.api.edb.v1.group_pb2 import GroupTypeMessage
from ansys.api.edb.v1.group_pb2_grpc import GroupServiceStub

from ansys.edb.core.edb_defs import LayoutObjType
from ansys.edb.core.hierarchy.hierarchy_obj import HierarchyObj
from ansys.edb.core.inner import messages
from ansys.edb.core.session import StubAccessor, StubType


class Group(HierarchyObj):
    """Represents a group object."""

    __stub: GroupServiceStub = StubAccessor(StubType.group)
    layout_obj_type = LayoutObjType.GROUP

    def cast(self):
        """Cast the group object to the correct concrete type.

        Returns
        -------
        Group
        """
        from ansys.edb.core.hierarchy.component_group import ComponentGroup
        from ansys.edb.core.hierarchy.structure3d import Structure3D
        from ansys.edb.core.hierarchy.via_group import ViaGroup

        if self.is_null:
            return

        group_type = self.__stub.GetGroupType(self.msg).group_type
        if group_type == GroupTypeMessage.GroupType.GROUP:
            return Group(self.msg)
        elif group_type == GroupTypeMessage.GroupType.COMPONENT:
            return ComponentGroup(self.msg)
        elif group_type == GroupTypeMessage.GroupType.STRUCTURE_3D:
            return Structure3D(self.msg)
        elif group_type == GroupTypeMessage.GroupType.VIA_GROUP:
            return ViaGroup(self.msg)

    @classmethod
    def create(cls, layout, name):
        """Create a group.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the group in.
        name : str
            Name of the group.

        Returns
        -------
        Group
           Group created.
        """
        return Group(cls.__stub.Create(messages.object_name_in_layout_message(layout, name)))

    @classmethod
    def find(cls, layout, name):
        """Find a group by name.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to search for the group.
        name : str
            Name of the group.

        Returns
        -------
        Group
            Group that is found, ``None`` otherwise.
        """
        return Group(
            cls.__stub.FindByName(messages.object_name_in_layout_message(layout, name))
        ).cast()

    def add_member(self, member):
        """Add an object to the group.

        Parameters
        ----------
        member : :term:`Connectable`
            Object to add to the group.
        """
        self.__stub.AddMember(messages.group_modify_member_message(self, member))

    def remove_member(self, member):
        """Remove an object from the group.

        Parameters
        ----------
        member : :term:`Connectable`
            Object to remove from the group.
        """
        self.__stub.RemoveMember(messages.group_modify_member_message(self, member))

    def ungroup(self, recursive):
        """Dissolve the group.

        Parameters
        ----------
        recursive : bool
            Whether all containing groups should also be resolved.
        """
        self.__stub.Ungroup(messages.bool_property_message(self, recursive))

    @property
    def members(self):
        """:obj:`list` of :term:`Connectables <Connectable>`: All group members.

        This property is read-only.
        """
        from ansys.edb.core.inner import factory

        objs = self.__stub.GetMembers(self.msg).items
        return [factory.create_conn_obj(co) for co in objs]
