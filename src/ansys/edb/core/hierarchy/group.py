"""Group."""

from ansys.api.edb.v1.group_pb2_grpc import GroupServiceStub

from ansys.edb.core.hierarchy.hierarchy_obj import HierarchyObj
from ansys.edb.core.interface.grpc import messages
from ansys.edb.core.layout.conn_obj import ConnObj
from ansys.edb.core.session import StubAccessor, StubType


class Group(HierarchyObj):
    """Class representing group object."""

    __stub: GroupServiceStub = StubAccessor(StubType.group)

    @classmethod
    def create(cls, layout, name):
        """Create a group.

        Parameters
        ----------
        layout : Layout
        name : str

        Returns
        -------
        Group
        """
        return Group(cls.__stub.Create(messages.object_name_in_layout_message(layout, name)))

    @classmethod
    def find(cls, layout, name):
        """Find a group by name.

        Parameters
        ----------
        layout : Layout
        name : str

        Returns
        -------
        Group
        """
        return Group(cls.__stub.FindByName(messages.object_name_in_layout_message(layout, name)))

    def add_member(self, member):
        """Add an object to the group.

        Parameters
        ----------
        member : ConnObj to be added
        """
        self.__stub.AddMember(messages.group_modify_member_message(self, member))

    def remove_member(self, member):
        """Remove an object from the group.

        Parameters
        ----------
        member : ConnObj to be removed
        """
        self.__stub.RemoveMember(messages.group_modify_member_message(self, member))

    def ungroup(self, recursive):
        """Ungroup the group.

        Parameters
        ----------
        recursive : bool
        """
        self.__stub.Ungroup(messages.bool_property_message(self, recursive))

    @property
    def members(self):
        """Get the list of group members.

        Returns
        -------
        list of ConnObjs
        """
        objs = self.__stub.GetMembers(self.msg).items
        return [ConnObj(co) for co in objs]
