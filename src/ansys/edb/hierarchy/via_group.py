"""Via Group."""

from ansys.api.edb.v1.via_group_pb2_grpc import ViaGroupServiceStub

from ansys.edb.core import messages, parser
from ansys.edb.hierarchy.group import Group
from ansys.edb.session import StubAccessor, StubType


class ViaGroup(Group):
    """Class representing a via group object."""

    __stub: ViaGroupServiceStub = StubAccessor(StubType.via_group)

    @classmethod
    def create_with_primitives(cls, layout, primitives, is_persistent):
        """Create a via group(s) with primitives.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.layout.Layout>`
            Layout that owns the via group.
        primitives : list[:class:`Primitive <ansys.edb.primitive.Primitive>`]
            List of primitives that will be used to create the via groups.
        is_persistent : bool
            Primitives are preserved during via group creation if True, deleted otherwise.

        Returns
        -------
        list[ViaGroup]
            List of newly created via group(s).
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
        layout : :class:`Layout <ansys.edb.layout.Layout>`
            Layout that owns the via group.
        outline : list[:class:`Point2D <ansys.edb.geometry.PointData>`] or \
            list[:class:`PolygonData <ansys.edb.geometry.PolygonData>`]
            List of primitives that will be used to create the via groups.
        conductivity_ratio : float
        layer : str or :class:`Layer <ansys.edb.layer.Layer>`
            Placement layer for the via group.
        net : str or :class:`Net <ansys.edb.net.Net>`, optional
            Net the via group should belong to.

        Returns
        -------
        ViaGroup
            Newly created via group.
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
        layout : :class:`Layout <ansys.edb.layout.Layout>`
            Layout to search the via group in.
        name : str
            Name of the via group.

        Returns
        -------
        ViaGroup
            ViaGroup that is found, None otherwise.
        """
        return ViaGroup(cls.__stub.FindByName(messages.object_name_in_layout_message(layout, name)))

    @property
    @parser.to_polygon_data
    def outline(self):
        """:class:`PolygonData <ansys.edb.geometry.PolygonData>`: Via group outline.

        Read-Only.
        """
        return self.__stub.GetOutline(self.msg)

    @property
    def conductor_percentage(self):
        """:obj:`float`: Conductor percentage of the via group.

        Read-Only.
        """
        return self.__stub.GetConductorPercentage(self.msg).value

    @property
    def persistent(self):
        """:obj:`bool`: Determine whether the primitives in the via group are persistent.

        Read-Only.
        """
        return self.__stub.IsPersistent(self.msg).value
