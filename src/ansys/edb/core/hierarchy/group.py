"""Group."""

from ansys.api.edb.v1.group_pb2 import GroupTypeMessage
from ansys.api.edb.v1.group_pb2_grpc import GroupServiceStub

from ansys.edb.core.edb_defs import LayoutObjType
from ansys.edb.core.hierarchy.hierarchy_obj import HierarchyObj
from ansys.edb.core.inner.messages import (
    bool_property_message,
    group_modify_member_message,
    object_name_in_layout_message,
)
from ansys.edb.core.session import StubAccessor, StubType


class Group(HierarchyObj):
    """Class representing a group object."""

    __stub: GroupServiceStub = StubAccessor(StubType.group)
    layout_obj_type = LayoutObjType.GROUP

    def cast(self):
        """Cast the group object to correct concrete type.

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
        layout : :class:`Layout <ansys.edb.core.layout.Layout>`
            Layout that owns the group.
        name : str
            Name of group to be created.

        Returns
        -------
        Group
            Newly created group.
        """
        return Group(cls.__stub.Create(object_name_in_layout_message(layout, name)))

    @classmethod
    def find(cls, layout, name):
        """Find a group by name.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.core.layout.Layout>`
            Layout to search the group in.
        name : str
            Name of the group to be searched.

        Returns
        -------
        Group
            Group that is found, None otherwise.
        """
        return Group(cls.__stub.FindByName(object_name_in_layout_message(layout, name))).cast()

    def add_member(self, member):
        """Add an object to the group.

        Parameters
        ----------
        member : :term:`Connectable`
            Object to be added to the group.
        """
        self.__stub.AddMember(group_modify_member_message(self, member))

    def remove_member(self, member):
        """Remove an object from the group.

        Parameters
        ----------
        member : :term:`Connectable`
            Object to be removed from the group.
        """
        self.__stub.RemoveMember(group_modify_member_message(self, member))

    def ungroup(self, recursive):
        """Dissolves the group.

        Parameters
        ----------
        recursive : bool
            True if all containing groups should also be dissolved, False otherwise.
        """
        self.__stub.Ungroup(bool_property_message(self, recursive))

    @property
    def members(self):
        """:obj:`list` of :term:`Connectables <Connectable>`: List of all the group members.

        Read-Only.
        """
        from ansys.edb.core.inner.factory import create_conn_obj

        objs = self.__stub.GetMembers(self.msg).items
        return [create_conn_obj(co) for co in objs]
