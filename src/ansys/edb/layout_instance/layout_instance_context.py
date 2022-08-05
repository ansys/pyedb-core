"""Layout Instance Context."""

from ansys.edb.core import ObjBase, parser
from ansys.edb.core.messages import bool_property_message
import ansys.edb.layout as layout
from ansys.edb.session import LayoutInstanceContextServiceStub, StubAccessor, StubType


class LayoutInstanceContext(ObjBase):
    """Class representing layout instance context object."""

    __stub: LayoutInstanceContextServiceStub = StubAccessor(StubType.layout_instance_context)

    @property
    def layout(self):
        """Get the layout of the layout instance context.

        Returns
        -------
        Layout
        """
        return layout.Layout(self.__stub.GetLayout(self.msg))

    def get_bbox(self, local=False):
        """Get the bounding box of the layout instance context.

        Parameters
        ----------
        local : bool

        Returns
        -------
        ansys.edb.geometry.PolygonData
        """
        return parser.to_polygon_data(self.__stub.GetBBox(bool_property_message(self, local)))

    @property
    def is_top_or_black_box(self):
        """Get flag indicating if this is a top-level or blackbox layout instance context.

        Returns
        -------
        bool
        """
        return self.__stub.IsTopOrBlackBox(self.msg).value

    @property
    def top_or_black_box(self):
        """Get the top-level or blackbox layout instance context.

        Returns
        -------
        LayoutInstanceContext
        """
        return LayoutInstanceContext(self.__stub.GetTopOrBlackBox(self.msg))

    @property
    def placement_elevation(self):
        """Get the placement elevation of this layout instance context.

        Only applies if this layout instance context doesn't have 3D placement.

        Returns
        -------
        float or None
            If this layout instance context has 3d placement is enabled, None is returned because the placement of the
            context is dictated by the underlying 3d transformation. Otherwise, the placement elevation of the layout
            instance context is returned.
        """
        return (
            self.__stub.GetPlacementElevation(self.msg).value if not self.is_3d_placement else None
        )

    @property
    def is_3d_placement(self, local=False):
        """Check if this layout instance context has 3d placement is enabled.

        Parameters
        ----------
        local : bool

        Returns
        -------
        bool
        """
        return self.__stub.Is3DPlacement(bool_property_message(self, local)).value
