"""Layout Instance Context."""

from ansys.edb.core import parser
from ansys.edb.core.base import ObjBase
from ansys.edb.core.messages import bool_property_message
import ansys.edb.layout as layout
from ansys.edb.session import LayoutInstanceContextServiceStub, StubAccessor, StubType


class LayoutInstanceContext(ObjBase):
    """Class representing layout instance context object."""

    __stub: LayoutInstanceContextServiceStub = StubAccessor(StubType.layout_instance_context)

    @property
    def layout(self):
        """:class:`Layout <ansys.edb.layout.Layout>`: Layout of the context.

        Read-Only.
        """
        return layout.Layout(self.__stub.GetLayout(self.msg))

    @parser.to_polygon_data
    def get_bbox(self, local):
        """Get the bounding box of the context.

        Parameters
        ----------
        local : bool
            If true, return the bounding-box in the local :class:`context <LayoutInstanceContext>`.  Otherwise, \
            return the bounding-box in the global context.

        Returns
        -------
        :class:`PolygonData <ansys.edb.geometry.PolygonData>`
        """
        return self.__stub.GetBBox(bool_property_message(self, local))

    @property
    def is_top_or_black_box(self):
        """:obj:`bool`: Flag indicating if this is a top-level or blackbox context.

        Read-Only.
        """
        return self.__stub.IsTopOrBlackBox(self.msg).value

    @property
    def top_or_black_box(self):
        """:class:`LayoutInstanceContext`: The top-level or blackbox :class:`context <LayoutInstanceContext>`.

        Read-Only.
        """
        return LayoutInstanceContext(self.__stub.GetTopOrBlackBox(self.msg))

    @property
    def placement_elevation(self):
        """:obj:`float`: The placement elevation of the context.

        Only applies if the context doesn't have 3D placement. \
        If the context has 3D placement is enabled, :obj:`None` is returned because the placement of the context is \
        dictated by the underlying 3d transformation. Otherwise, the placement elevation of the context is returned.

        Read-Only.
        """
        return (
            self.__stub.GetPlacementElevation(self.msg).value
            if not self.get_is_3d_placement(False)
            else None
        )

    def get_is_3d_placement(self, local):
        """Check if the context has 3d placement enabled.

        Parameters
        ----------
        local : bool
            If true, check the local :class:`context <LayoutInstanceContext>` only.  If false, check for a 3D \
            Placement anywhere up the hierarchy.

        Returns
        -------
        bool
        """
        return self.__stub.Is3DPlacement(bool_property_message(self, local)).value
