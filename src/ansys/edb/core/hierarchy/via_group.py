"""Via group."""

from ansys.api.edb.v1.via_group_pb2_grpc import ViaGroupServiceStub

from ansys.edb.core.hierarchy.group import Group
from ansys.edb.core.inner import messages, parser
from ansys.edb.core.session import StubAccessor, StubType


class ViaGroup(Group):
    """Represents a via group object."""

    __stub: ViaGroupServiceStub = StubAccessor(StubType.via_group)

    @classmethod
    def create_with_primitives(cls, layout, primitives, is_persistent):
        """Create one or more via groups with primitives.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the via groups in.
        primitives : list[:class:`.Primitive`]
            List of primitives to use to create the via groups.
        is_persistent : bool
            Whether to preserve primitives during via group creation. If ``False``
            primitives are deleted during via group creation.

        Returns
        -------
        list[ViaGroup]
            List of newly created via groups.
        """
        via_groups = cls.__stub.CreateWithPrimitives(
            messages.via_group_create_with_primitives_message(layout, primitives, is_persistent)
        ).items
        return [ViaGroup(vg) for vg in via_groups]

    @classmethod
    def create_with_outline(cls, layout, outline, conductivity_ratio, layer, net=None):
        """Create a via group with a polygon outline.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout that owns the via group.
        outline : list[:class:`Point2D <.PointData>`] or \
            list[:class:`.PolygonData`]
            List of primitives to use to create the via group.
        conductivity_ratio : float
        layer : str or :class:`.Layer`
            Placement layer for the via group.
        net : str or :class:`.Net`, default: None
            Net that the via group is to belong to.

        Returns
        -------
        ViaGroup
            Via group created.
        """
        return ViaGroup(
            cls.__stub.CreateWithOutline(
                messages.via_group_create_with_outline_message(
                    layout, outline, conductivity_ratio, layer, net
                )
            )
        )

    @classmethod
    def find(cls, layout, name):
        """Find a via group by name in the given layout.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to search for the via group.
        name : str
            Name of the via group.

        Returns
        -------
        ViaGroup
            Via group that is found, ``None`` otherwise.
        """
        return ViaGroup(cls.__stub.FindByName(messages.object_name_in_layout_message(layout, name)))

    @property
    @parser.to_polygon_data
    def outline(self):
        """:class:`.PolygonData`: Via group outline.

        This property is read-only.
        """
        return self.__stub.GetOutline(self.msg)

    @property
    def conductor_percentage(self):
        """:obj:`float`: Conductor percentage of the via group.

        This property is read-only.
        """
        return self.__stub.GetConductorPercentage(self.msg).value

    @property
    def persistent(self):
        """:obj:`bool`: Flag indicating if the primitives in the via group are persistent.

        This property is read-only.
        """
        return self.__stub.IsPersistent(self.msg).value
