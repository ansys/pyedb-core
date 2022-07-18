"""Via Group."""

from ansys.api.edb.v1.via_group_pb2_grpc import ViaGroupServiceStub

from ansys.edb.core.geometry.polygon_data import PolygonData
from ansys.edb.core.interface.grpc import messages
from ansys.edb.core.session import StubAccessor, StubType

from .group import Group


class ViaGroup(Group):
    """Class representing a via group."""

    __stub: ViaGroupServiceStub = StubAccessor(StubType.via_group)

    @classmethod
    def create_with_primitives(cls, layout, primitives, is_persistent):
        """Create a via group with primitives.

        Parameters
        ----------
        layout : Layout
        primitives : list of ConnObjs
        is_persistent : should primitives be persistent

        Returns
        -------
        list of ViaGroup
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
        layout : Layout
        outline : list of Point2D or PolygonData
        conductivity_ratio : float
        layer : str or Layer
        net : str or Net, optional

        Returns
        -------
        ViaGroup
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
        layout : Layout
        name : str

        Returns
        -------
        ViaGroup
        """
        return ViaGroup(cls.__stub.FindByName(messages.object_name_in_layout_message(layout, name)))

    @property
    def outline(self):
        """Get the via group outline.

        Returns
        -------
        list of ConnObjs
        """
        return PolygonData(self.__stub.GetOutline(self.msg))

    @property
    def conductor_percentage(self):
        """Get the conductor percentage of the via group.

        Returns
        -------
        double
        """
        return self.__stub.GetConductorPercentage(self.msg).value

    @property
    def persistent(self):
        """Get if the primitives in the via group are persistent.

        Returns
        -------
        bool
        """
        return self.__stub.IsPersistent(self.msg).value
